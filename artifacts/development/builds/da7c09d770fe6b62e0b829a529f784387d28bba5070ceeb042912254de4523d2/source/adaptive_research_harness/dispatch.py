"""Attempt-backed handoff. Receipts suppress duplication, never authorize work."""
from pathlib import Path
from .encoding import canonical, decode, digest, require, Refusal
from .transport import request
from .host import generation, verify_quiescence


class Dispatcher:
    def __init__(self, engine, tool_sockets, supervisor_directory, *, generation_value=None, quiescence_verifier=verify_quiescence):
        self.engine=engine;self.tool_sockets=tool_sockets;self.supervisor_directory=Path(supervisor_directory)
        self.generation=generation_value or generation();engine.generation=self.generation
        self.verify_quiescence=quiescence_verifier

    def work_key(self, attempt):
        b=attempt['body'];i=b['input']
        return digest({'actor':attempt['actor'], 'step':'research' if b['step'] in ('research-counts','replacement-counts') else b['step'],
                       'inputs':i['input_refs'],'question':i['parameters'].get('transition_id')})

    def ensure_retry(self, view, actor, body):
        candidate={'actor':actor,'body':body}
        for seq,a in view.attempts.items():
            if self.work_key(a)!=self.work_key(candidate):continue
            claim=self.engine.store.db.execute('SELECT * FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            settled=view.settlements.get(seq)
            if settled is not None and claim is not None and claim['receipt'] is not None:continue
            require(settled is not None,'PENDING_PREDECESSOR')
            old=decode(claim['body']) if claim else {'core':a['body']['admission_generation'],'worker':None}
            receipt=self.supervisor_directory/(digest(old['core'])+'.json')
            self.verify_quiescence(receipt,self.engine.profile.inventory_hash,old['core'],old.get('worker'))

    def run(self, actor, seq, peer_generation):
        e=self.engine
        # Inspect the fixed worker before taking the ledger write lock. The
        # admission/claim checks below are repeated under serialization.
        with e.lock:
            a=e.view().attempts.get(seq);require(a is not None and a['actor']==actor,'UNAUTHORIZED')
            old=e.store.db.execute('SELECT * FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            if old:return {'status':'RECEIPT','receipt':decode(old['receipt'])} if old['receipt'] else {'status':'IN_PROGRESS_OR_UNCERTAIN'}
            require(a['body'].get('admission_generation')==self.generation,'UNCERTAIN_OLD_ATTEMPT')
            tool=a['body']['input']['tool_id']
        if tool.startswith('CHECK'):worker=peer_generation
        else:
            desc=request(self.tool_sockets[tool],{'op':'describe'})
            require(desc['tool_id']==tool,'TOOL_VERSION_MISMATCH');worker=desc['generation']
        with e.lock,e.store.transaction():
            v=e.view();a=v.attempts.get(seq);require(a is not None and a['actor']==actor,'UNAUTHORIZED')
            old=e.store.db.execute('SELECT * FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            if old:return {'status':'RECEIPT','receipt':decode(old['receipt'])} if old['receipt'] else {'status':'IN_PROGRESS_OR_UNCERTAIN'}
            require(a['body'].get('admission_generation')==self.generation,'UNCERTAIN_OLD_ATTEMPT')
            claim={'attempt':seq,'input_hash':a['body']['input_hash'],'core':self.generation,'worker':worker,
                   'tool_id':tool,'inventory_sha256':e.profile.inventory_hash}
            e.store.db.execute('INSERT INTO dispatch_claims(attempt_seq,body) VALUES(?,?)',(seq,canonical(claim)))
            doc=None
            if not tool.startswith('CHECK'):doc=v.exact(a['body']['input']['input_refs'][0])['body']['document']
            fault=e.store.db.execute('SELECT body FROM faults WHERE target=? AND consumed=0',(str(seq),)).fetchone()
            fault=decode(fault['body']) if fault else None
            if fault:e.store.db.execute('UPDATE faults SET consumed=1 WHERE target=?',(str(seq),))
        e.fault_hook('after_dispatch_claim_commit')
        if tool.startswith('CHECK'):return {'status':'PERMISSION_CONSUMED','claim':claim}
        try:
            receipt=request(self.tool_sockets[tool],{'op':'run','claim':claim,'document':doc,
                             'maximum':a['body']['maximum'],'fault':fault})
            require(receipt['attempt']==seq and receipt['input_hash']==a['body']['input_hash'],'INVALID_TOOL_RECEIPT')
        except (OSError,EOFError,KeyError) as exc:
            return {'status':'UNKNOWN','reason':type(exc).__name__}
        with e.lock, e.store.transaction():
            e.store.db.execute('UPDATE dispatch_claims SET receipt=? WHERE attempt_seq=? AND receipt IS NULL',
                               (canonical(receipt),seq))
        return {'status':'RECEIPT','receipt':receipt}

    def receipt(self,actor,seq):
        e=self.engine
        with e.lock:
            a=e.view().attempts.get(seq);require(a is not None and actor in ('Principal',a['actor']),'UNAUTHORIZED')
            row=e.store.db.execute('SELECT * FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            if row is None:return {'receipt':None,'status':'RECEIPT_OR_UNKNOWN'}
            if row['receipt']:return {'receipt':decode(row['receipt']),'status':'RECEIPT_OR_UNKNOWN'}
            claim=decode(row['body'])
        receipt=None
        if claim['tool_id'] in self.tool_sockets:
            try:receipt=request(self.tool_sockets[claim['tool_id']],{'op':'lookup','claim':claim}).get('receipt')
            except (OSError,EOFError):pass
        if receipt is not None:
            require(receipt.get('attempt')==seq and receipt.get('input_hash')==claim['input_hash'],'INVALID_TOOL_RECEIPT')
            with e.lock,e.store.transaction():
                e.store.db.execute('UPDATE dispatch_claims SET receipt=? WHERE attempt_seq=? AND receipt IS NULL',(canonical(receipt),seq))
                receipt=decode(e.store.db.execute('SELECT receipt FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()['receipt'])
        return {'receipt':receipt,'status':'RECEIPT_OR_UNKNOWN'}

    def finish_check(self, actor, seq, receipt):
        e=self.engine
        with e.lock,e.store.transaction():
            a=e.view().attempts.get(seq);require(a is not None and a['actor']==actor and a['body']['input']['tool_id'].startswith('CHECK'),'UNAUTHORIZED')
            require(receipt['attempt']==seq and receipt['input_hash']==a['body']['input_hash'] and receipt['actual']=='0.25' and receipt['synthetic'] is True,'INVALID_TOOL_RECEIPT')
            row=e.store.db.execute('SELECT receipt FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            require(row is not None,'NO_DISPATCH_CLAIM')
            if row['receipt'] is not None:require(decode(row['receipt'])==receipt,'RECEIPT_CONFLICT')
            else:e.store.db.execute('UPDATE dispatch_claims SET receipt=? WHERE attempt_seq=?',(canonical(receipt),seq))
        return {'status':'RECEIPT','receipt':receipt}
