"""Length-framed local IPC, Linux peer credentials and process lifetime locks."""
from __future__ import annotations
import fcntl
import os
import socket
import struct
import sys
import threading
from pathlib import Path
from .encoding import canonical, decode, require, Refusal

class DropReply(Exception):
    """One-shot test fault after durable commit: close without a reply."""


MAX_FRAME=32*1024*1024


def exact_read(sock, size):
    data=bytearray()
    while len(data)<size:
        block=sock.recv(size-len(data))
        if not block:raise EOFError('incomplete frame')
        data.extend(block)
    return bytes(data)


def receive(sock):
    length=struct.unpack('!I',exact_read(sock,4))[0]
    require(0<length<=MAX_FRAME,'FRAME_TOO_LARGE')
    return decode(exact_read(sock,length))


def send(sock,value):
    raw=canonical(value);require(len(raw)<=MAX_FRAME,'FRAME_TOO_LARGE')
    sock.sendall(struct.pack('!I',len(raw))+raw)


def request(path,value):
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
        sock.settimeout(30);sock.connect(str(path));send(sock,value);return receive(sock)


def peer(sock):
    require(sys.platform=='linux' and hasattr(socket,'SO_PEERCRED'),'UNSUPPORTED_HOST')
    pid,uid,gid=struct.unpack('3i',sock.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))
    return {'pid':pid,'uid':uid,'gid':gid}


class LifetimeLock:
    def __init__(self,path):
        self.path=Path(path);self.fd=None
    def __enter__(self):
        self.path.parent.mkdir(parents=True,exist_ok=True)
        self.fd=os.open(self.path,os.O_CREAT|os.O_RDWR|os.O_CLOEXEC,0o600)
        try:fcntl.flock(self.fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            os.close(self.fd);self.fd=None;raise Refusal('INSTANCE_ALREADY_RUNNING')
        return self
    def __exit__(self,*args):
        if self.fd is not None:os.close(self.fd);self.fd=None


def serve(path,handler,allowed_uids):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists():path.unlink() # Must be called only while holding the unit's lifetime lock.
    with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as server:
        server.bind(str(path));os.chmod(path,0o660);server.listen(32)
        def handle_connection(conn):
            with conn:
                conn.settimeout(30)
                try:
                    who=peer(conn);require(who['uid'] in allowed_uids,'UNAUTHENTICATED')
                    result=handler(who,receive(conn));send(conn,result)
                except DropReply:
                    return
                except Refusal as exc:
                    try:send(conn,{'status':'ERROR','reason':exc.code,'detail':exc.detail})
                    except OSError:pass
                except (OSError,ValueError,KeyError,TypeError,EOFError) as exc:
                    try:send(conn,{'status':'ERROR','reason':'OPERATIONAL_ERROR','detail':type(exc).__name__})
                    except OSError:pass
        while True:
            conn,_=server.accept()
            threading.Thread(target=handle_connection,args=(conn,),daemon=True).start()
