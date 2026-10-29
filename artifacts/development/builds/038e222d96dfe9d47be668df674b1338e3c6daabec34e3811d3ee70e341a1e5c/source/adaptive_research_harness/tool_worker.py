"""A/B worker with no ledger socket or credentials; fixed root-managed entrypoint."""
from pathlib import Path
import threading
import time
from .encoding import decode, digest, require, Refusal
from .clock import durable_write
from .host import generation
from .transport import LifetimeLock, serve


def run_worker(tool_id, socket_path, state_dir, profile, *, serve_function=serve, generation_provider=generation):
    from . import tools_a, tools_b
    calculate={'SYN-A-1':tools_a.calculate,'SYN-B-1':tools_b.calculate}[tool_id]
    state=Path(state_dir);state.mkdir(parents=True,exist_ok=True,mode=0o700)
    lock=threading.Lock();gen=generation_provider()
    def handle(who,b):
        require(who['uid']==20000,'UNAUTHORIZED')
        if b['op']=='describe':return {'tool_id':tool_id,'generation':gen}
        require(b['op'] in ('run','lookup') and b['claim']['tool_id']==tool_id,'INVALID_TOOL_REQUEST')
        claim=b['claim'];key=digest([claim['inventory_sha256'],claim['core'],claim['attempt']])
        marker=state/(key+'.claim');result=state/(key+'.receipt')
        # Receipt files are atomically replaced. Lookup must not wait behind a
        # paused calculation: absence means uncertainty, never non-dispatch.
        if b['op']=='lookup':return {'receipt':decode(result.read_bytes()) if result.exists() else None}
        with lock:
            if result.exists():return decode(result.read_bytes())
            require(claim['worker']==gen,'WORKER_GENERATION_CHANGED')
            require(not marker.exists(),'UNCERTAIN_OLD_DISPATCH')
            durable_write(marker,claim)
            fault=b.get('fault') or {}
            if fault.get('kind')=='PAUSE_AT_BOUNDARY' and fault.get('point')!='after_tool_execution':
                # Root fixture releases this barrier or terminates the whole unit.
                barrier=state/(key+'.release')
                durable_write(state/(key+'.paused'),{'generation':gen,'claim':claim})
                while not barrier.exists():time.sleep(.05)
            actual=b['maximum'];value=None;error=None
            try:
                if fault.get('kind')=='AFTER_START_FAILURE':raise Refusal('AFTER_START_FAILURE')
                value=calculate(b['document'])
                if fault.get('case')=='T03':value=dict(value,approval='ADMITTED',grant='FORGED-NO-AUTHORITY')
            except Refusal as exc:error=exc.code
            if fault.get('kind')=='OVERRUN_601':
                require(fault.get('case')=='R09','INVALID_FAULT');actual='601.00'
            receipt={'attempt':claim['attempt'],'input_hash':claim['input_hash'],'tool_id':tool_id,
                     'actual':actual,'synthetic':True,'result':value,'error':error,'generation':gen}
            durable_write(result,receipt)
            if fault.get('kind')=='PAUSE_AT_BOUNDARY' and fault.get('point')=='after_tool_execution':
                durable_write(state/(key+'.paused'),{'point':'after_tool_execution','generation':gen,'claim':claim})
                while not (state/(key+'.release')).exists():time.sleep(.05)
            if fault.get('kind')=='DROP_TOOL_RESPONSE':raise ConnectionError('injected loss after receipt')
            return receipt
    with LifetimeLock(state/'worker.lock'):serve_function(socket_path,handle,{20000})
