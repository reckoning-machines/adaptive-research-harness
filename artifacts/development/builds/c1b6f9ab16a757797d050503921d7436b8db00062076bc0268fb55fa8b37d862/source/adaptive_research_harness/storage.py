"""SQLite carrier, without a client-visible generic append API."""
from __future__ import annotations
from contextlib import contextmanager
from pathlib import Path
import os
import sqlite3
from .encoding import canonical, decode, digest, raw_digest, require, Refusal


class Store:
    def __init__(self, path: str | Path):
        self.command_context=None
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.db = sqlite3.connect(str(path), isolation_level=None, timeout=5, check_same_thread=False)
        os.chmod(path, 0o600)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("PRAGMA busy_timeout=5000")
        self.db.executescript(Path(__file__).with_name("schema.sql").read_text())
        for pragma, expected in [("journal_mode", "wal"), ("synchronous", 2), ("foreign_keys", 1)]:
            require(self.db.execute("PRAGMA " + pragma).fetchone()[0] == expected,
                    "STORAGE_CONFIGURATION", pragma)
        require(self.db.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()[0]
                == "1", "UNSUPPORTED_SCHEMA")

    def close(self):
        self.db.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield self
            self.db.execute("COMMIT")
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        finally:self.command_context=None

    def events(self, ledger, through=None):
        table = {"E": "evidence", "T": "transitions"}[ledger]
        query = "SELECT * FROM " + table
        args = ()
        if through is not None:
            query += " WHERE seq<=?"
            args = (through,)
        out = []
        for row in self.db.execute(query + " ORDER BY seq", args):
            item = dict(row)
            require(raw_digest(bytes(item["body"])) == item["sha256"], "CORRUPT_LEDGER")
            item["body"] = decode(item["body"])
            if item.get("command") is not None:item["command"]=decode(item["command"])
            out.append(item)
        return out

    def append(self, ledger, kind, actor, body, time_ms=None, transition_id=None):
        require(self.db.in_transaction, "NO_WRITE_TRANSACTION")
        raw = canonical(body)
        context=canonical(self.command_context) if self.command_context else None
        if self.command_context:self.command_context["position"]+=1
        if ledger == "E":
            cur = self.db.execute("INSERT INTO evidence(kind,actor,time_ms,body,sha256,command) VALUES(?,?,?,?,?,?)",
                                  (kind, actor, time_ms, raw, raw_digest(raw),context))
        else:
            require(transition_id is not None, "MISSING_TRANSITION")
            cur = self.db.execute("INSERT INTO transitions(kind,actor,transition_id,time_ms,body,sha256,command) VALUES(?,?,?,?,?,?,?)",
                                  (kind, actor, transition_id, time_ms, raw, raw_digest(raw),context))
        return {"ledger": ledger, "sequence": cur.lastrowid, "sha256": raw_digest(raw)}

    def blob(self, raw):
        key = raw_digest(raw)
        self.db.execute("INSERT OR IGNORE INTO artifacts VALUES(?,?)", (key, raw))
        return key

    def lookup(self, actor, key, request_hash=None):
        row = self.db.execute("SELECT * FROM requests WHERE actor=? AND request_id=?", (actor, key)).fetchone()
        if row is None:
            owned=[]
            for ledger in ('E','T'):
                for event in self.events(ledger):
                    c=event.get('command')
                    if c and c['actor']==actor and c['request_id']==key:owned.append((c['position'],ledger,event))
            if not owned:return None
            owned.sort(key=lambda entry:entry[0]);hashes={x[2]['command']['request_hash'] for x in owned}
            require(len(hashes)==1,'CORRUPT_RECEIPT')
            if request_hash is not None:require(hashes=={request_hash},'REQUEST_KEY_CONFLICT')
            refs=[{'ledger':l,'sequence':e['seq'],'sha256':e['sha256']} for _,l,e in owned]
            refusal=next((e for _,_,e in owned if e['kind']=='REFUSAL'),None)
            return {'status':'REFUSED','reason':refusal['body']['reason'],'detail':refusal['body'].get('detail',''),'refs':refs} if refusal else {'status':'COMMITTED','refs':refs}
        if request_hash is not None:
            require(row["request_hash"] == request_hash, "REQUEST_KEY_CONFLICT")
        result = decode(row["response"])
        for ref in result.get("refs", []):
            table = {"E": "evidence", "T": "transitions"}[ref["ledger"]]
            event = self.db.execute("SELECT sha256 FROM " + table + " WHERE seq=?", (ref["sequence"],)).fetchone()
            require(event is not None and event[0] == ref["sha256"], "CORRUPT_RECEIPT")
        return result

    def begin_command(self,actor,key,request_hash):
        require(self.db.in_transaction,'NO_WRITE_TRANSACTION')
        self.command_context={'actor':actor,'request_id':key,'request_hash':request_hash,'position':0}

    def remember(self, actor, key, request_hash, result):
        require(self.db.in_transaction, "NO_WRITE_TRANSACTION")
        self.db.execute("INSERT INTO requests VALUES(?,?,?,?)", (actor, key, request_hash, canonical(result)))

    def high_water(self):
        return self.db.execute("SELECT MAX(t) FROM (SELECT MAX(time_ms) t FROM evidence UNION ALL SELECT MAX(time_ms) FROM transitions)").fetchone()[0]
