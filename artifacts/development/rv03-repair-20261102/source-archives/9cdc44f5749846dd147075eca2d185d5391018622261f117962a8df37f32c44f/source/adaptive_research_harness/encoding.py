"""Strict, shared byte/quantity contract; contains no admission predicates."""
from __future__ import annotations
import hashlib
import json
import re
from datetime import datetime, timezone


class Refusal(ValueError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (": " + detail if detail else ""))
        self.code, self.detail = code, detail


def require(condition: bool, code: str, detail: str = "") -> None:
    if not condition:
        raise Refusal(code, detail)


def _validate(value):
    if value is None or type(value) in (bool, int):
        return
    if isinstance(value, str):
        value.encode("utf-8", "strict")
    elif isinstance(value, list):
        for item in value:
            _validate(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            require(isinstance(key, str) and key.isascii(), "INVALID_FIELD_NAME")
            _validate(item)
    else:
        raise Refusal("INVALID_JSON_TYPE", type(value).__name__)


def canonical(value) -> bytes:
    try:
        _validate(value)
        return json.dumps(value, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (UnicodeError, RecursionError) as exc:
        raise Refusal("INVALID_ENCODING") from exc


def _pairs(items):
    out = {}
    for key, value in items:
        require(key not in out, "DUPLICATE_FIELD", key)
        out[key] = value
    return out


def _integer(text):
    require(text != "-0", "NONCANONICAL_NUMBER")
    return int(text)


def _no_float(text):
    raise Refusal("INVALID_JSON_NUMBER", text)


def decode(raw: bytes | str):
    try:
        text = raw.decode("utf-8", "strict") if isinstance(raw, bytes) else raw
        value = json.loads(text, object_pairs_hook=_pairs, parse_int=_integer,
                           parse_float=_no_float, parse_constant=_no_float)
        _validate(value)
        return value
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise Refusal("INVALID_JSON") from exc


def digest(value) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def raw_digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def units(text: str) -> int:
    require(isinstance(text, str) and re.fullmatch(r"(?:0|[1-9][0-9]*)\.[0-9]{2}", text)
            is not None, "INVALID_UNITS")
    whole, fraction = text.split(".")
    return int(whole) * 100 + int(fraction)


def amount(value: int) -> str:
    require(type(value) is int and value >= 0, "INVALID_UNITS")
    return f"{value // 100}.{value % 100:02d}"


def instant(text: str) -> int:
    require(isinstance(text, str) and re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", text) is not None,
        "INVALID_TIME")
    try:
        value = datetime.strptime(text, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
        return int(value.timestamp()) * 1000 + value.microsecond // 1000
    except ValueError as exc:
        raise Refusal("INVALID_TIME") from exc


def time_text(value: int) -> str:
    seconds, ms = divmod(value, 1000)
    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%S") + f".{ms:03d}Z"


def fields(value: dict, required: set[str], optional: set[str] = frozenset()):
    require(isinstance(value, dict), "INVALID_OBJECT")
    require(required <= value.keys(), "MISSING_FIELD", ",".join(sorted(required-value.keys())))
    require(value.keys() <= required | optional, "UNKNOWN_FIELD",
            ",".join(sorted(value.keys() - required - optional)))


def reference(ledger: str, sequence: int, content: dict):
    return {"ledger": ledger, "sequence": sequence, "sha256": digest(content)}
