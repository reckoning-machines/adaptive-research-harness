"""The host's wire contract, reimplemented without importing the core.

Strict canonical JSON (no floats, sorted keys, UTF-8), exact decimal unit
strings with two places, millisecond instants, and length-framed messages
over a Unix socket. Equal bytes to the core's encoding module by construction.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
import re
import socket
import struct

MAX_FRAME = 32 * 1024 * 1024


class HarnessError(Exception):
    """An operational failure: transport, host or a malformed request. Never a governed refusal."""
    def __init__(self, code: str, detail: str = ''):
        super().__init__(code + (': ' + detail if detail else ''))
        self.code, self.detail = code, detail


Refusal = HarnessError  # internal alias


def require(condition, code, detail=''):
    if not condition: raise HarnessError(code, detail)


def _validate(value):
    if value is None or type(value) in (bool, int): return
    if isinstance(value, str): value.encode('utf-8', 'strict')
    elif isinstance(value, list):
        for item in value: _validate(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str) and key.isascii(), 'INVALID_FIELD_NAME'); _validate(item)
    else: raise Refusal('INVALID_JSON_TYPE', type(value).__name__)


def canonical(value) -> bytes:
    _validate(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def _pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, 'DUPLICATE_FIELD', key); out[key] = value
    return out


def _no_float(text): raise Refusal('INVALID_JSON_NUMBER', text)


def decode(raw):
    try:
        text = raw.decode('utf-8', 'strict') if isinstance(raw, bytes) else raw
        value = json.loads(text, object_pairs_hook=_pairs, parse_float=_no_float, parse_constant=_no_float)
        _validate(value); return value
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Refusal('INVALID_JSON') from exc


def digest(value) -> str: return hashlib.sha256(canonical(value)).hexdigest()
def raw_digest(raw: bytes) -> str: return hashlib.sha256(raw).hexdigest()


def units(text: str) -> int:
    require(isinstance(text, str) and re.fullmatch(r'(?:0|[1-9][0-9]*)\.[0-9]{2}', text) is not None, 'INVALID_UNITS')
    whole, fraction = text.split('.'); return int(whole) * 100 + int(fraction)


def amount(value: int) -> str:
    require(type(value) is int and value >= 0, 'INVALID_UNITS'); return f'{value // 100}.{value % 100:02d}'


def instant(text: str) -> int:
    require(isinstance(text, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z', text) is not None, 'INVALID_TIME')
    value = datetime.strptime(text, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)
    return int(value.timestamp()) * 1000 + value.microsecond // 1000


def time_text(value: int) -> str:
    seconds, ms = divmod(value, 1000)
    return datetime.fromtimestamp(seconds, timezone.utc).strftime('%Y-%m-%dT%H:%M:%S') + f'.{ms:03d}Z'


def _exact_read(sock, size):
    data = bytearray()
    while len(data) < size:
        block = sock.recv(size - len(data))
        if not block: raise EOFError('incomplete frame')
        data.extend(block)
    return bytes(data)


def request(path, value, timeout=30):
    raw = canonical(value); require(len(raw) <= MAX_FRAME, 'FRAME_TOO_LARGE')
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout); sock.connect(str(path)); sock.sendall(struct.pack('!I', len(raw)) + raw)
        length = struct.unpack('!I', _exact_read(sock, 4))[0]; require(0 < length <= MAX_FRAME, 'FRAME_TOO_LARGE')
        return decode(_exact_read(sock, length))
