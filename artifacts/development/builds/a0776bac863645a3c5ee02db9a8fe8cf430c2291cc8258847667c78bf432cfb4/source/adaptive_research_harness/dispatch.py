"""Attempt-backed handoff. Receipts suppress duplication, never authorize work."""
from pathlib import Path
from .encoding import canonical, decode, digest, require, Refusal, units
from .transport import request
from .host import generation, verify_quiescence


class Dispatcher:
    def __init__(self, engine, tool_sockets, supervisor_directory, *, generation_value=None, quiescence_verifier=verify_quiescence):
        self.engine=engine;self.tool_sockets=tool_sockets;self.supervisor_directory=Path(supervisor_directory)
        self.generation=generation_value or generation();engine.generation=self.generation
        self.verify_quiescence=quiescence_verifier

    def caller_executed(self, tool_id): return self.engine.profile.experiment.caller_executed(tool_id)

    def work_key(self, attempt):
        b=attempt['body'];i=b['input'];step=self.engine.profile.experiment.step(b['step'])
        return digest({'actor':attempt['actor'], 'step':'research' if step and step['kind']=='research' else b['step'],
                       'inputs':i['input_refs'],'question':i['parameters'].get('transition_id')})

    def ensure_retry(self, view, actor, body):
        candidate={'actor':actor,'body':body}
        for seq,a in view.attempts.items():
            if self.work_key(a)!=self.work_key(candidate):continue
            claim=self.engine.store.db.execute('SELECT * FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            settled=view.settlements.get(seq)
            if settled is not None and claim is not None and claim['receipt'] is not None:continue
            require(settled is not None,'PENDING_PREDECESSOR')
            tool=a['body']['input']['tool_id']
            if self.caller_executed(tool):
                # The core handed nothing to a worker. Without a claim nothing was
                # ever permitted to run. With one, the caller that consumed it must
                # be gone, and a provider that can outlive its caller must have a
                # recorded disposition showing the earlier work can no longer
                # execute: completion or cancellation. Provider deduplication
                # recovers the original claim under its own identity and never
                # authorizes a new one. Settlement at the maximum is accounting
                # and establishes none of these.
                if claim is None:continue
                old=decode(claim['body']);receipt=self.supervisor_directory/(digest(old['worker'])+'.json')
                proof=self.verify_quiescence(receipt,self.engine.profile.inventory_hash,None,old['worker'])
                if self.engine.profile.experiment.may_outlive_caller(tool):
                    disposition=(proof.get('provider_dispositions') or {}).get(str(seq))
                    require(isinstance(disposition,dict) and disposition.get('state') in ('COMPLETED','CANCELLED')
                            and disposition.get('claim_input_hash')==old['input_hash'],'WORKER_NOT_QUIESCENT','provider disposition for attempt %d not recorded'%seq)
                continue
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
        if self.caller_executed(tool):worker=peer_generation
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
            doc=None;inputs=None
            if not self.caller_executed(tool):
                inputs=[{'kind':x['kind'],'seq':x['seq'],'sha256':x['sha256'],'actor':x['actor'],'body':x['body']} for x in (v.exact(ref) for ref in a['body']['input']['input_refs'])]
                first=next((x for x in inputs if x['kind']=='OBSERVATION'),None);doc=first['body']['document'] if first else None
            fault=e.store.db.execute('SELECT body FROM faults WHERE target=? AND consumed=0',(str(seq),)).fetchone()
            fault=decode(fault['body']) if fault else None
            if fault:e.store.db.execute('UPDATE faults SET consumed=1 WHERE target=?',(str(seq),))
        e.fault_hook('after_dispatch_claim_commit')
        if self.caller_executed(tool):return {'status':'PERMISSION_CONSUMED','claim':claim}
        try:
            receipt=request(self.tool_sockets[tool],{'op':'run','claim':claim,'document':doc,'inputs':inputs,
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

    def finish(self, actor, seq, receipt):
        """Register the receipt of a caller-executed attempt once. A different receipt for the same claim is refused."""
        e=self.engine;exp=e.profile.experiment
        with e.lock,e.store.transaction():
            a=e.view().attempts.get(seq);require(a is not None and a['actor']==actor,'UNAUTHORIZED')
            tool=a['body']['input']['tool_id'];require(self.caller_executed(tool),'UNAUTHORIZED')
            step=exp.step(a['body']['step'])
            require(isinstance(receipt,dict) and receipt.get('attempt')==seq and receipt.get('input_hash')==a['body']['input_hash']
                    and receipt.get('tool_id')==tool and receipt.get('synthetic') is True and isinstance(receipt.get('actual'),str),'INVALID_TOOL_RECEIPT')
            if step['kind']=='check':require(receipt['actual']==step['maximum'],'INVALID_TOOL_RECEIPT')
            else:units(receipt['actual'])
            row=e.store.db.execute('SELECT receipt FROM dispatch_claims WHERE attempt_seq=?',(seq,)).fetchone()
            require(row is not None,'NO_DISPATCH_CLAIM')
            if row['receipt'] is not None:require(decode(row['receipt'])==receipt,'RECEIPT_CONFLICT')
            else:e.store.db.execute('UPDATE dispatch_claims SET receipt=? WHERE attempt_seq=?',(canonical(receipt),seq))
        return {'status':'RECEIPT','receipt':receipt}
