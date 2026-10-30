"""Loopback HTTP API and page server for the workbench. Standard library only.

Binds to 127.0.0.1. Every read is a core query or a verified read-only ledger
load. Every write is one existing actor operation or Principal command,
performed by the session; the core enforces permission and state.
"""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import json
import threading
import traceback
from adaptive_research_harness.encoding import decode, Refusal
from . import session as sessions

HERE=Path(__file__).resolve().parent


class Workbench:
    def __init__(self):self.live={};self.starting={};self.lock=threading.RLock()
    def cohorts(self):
        catalog=decode((sessions.ROOT/'workbench/cohorts.json').read_bytes())['cohorts']
        out=[]
        for name in sorted(catalog,key=lambda n:(n!='original',n)):
            c=catalog[name]
            rows=c['content']['rows'];spikes=[r for r in rows if r['spike']];large=[r for r in spikes if r['size_units']>=2]
            out.append({'name':name,'description':c['description'],'differs_from_formation':c['differs_from_formation'],'expected_path':c['expected_path'],
                        'rows':len(rows),'spike_rows':len(spikes),'large_rows':len(large),'large_shocks':sorted({r['shock_id'] for r in large}),
                        'selling_rows':sum(r['selling'] for r in spikes),'non_large_selling':sum(r['selling'] for r in spikes if r['size_units']<2),'non_large_rows':sum(1 for r in spikes if r['size_units']<2)})
        return out
    def start(self,cohort):
        import time,uuid
        name=time.strftime('%Y%m%d-%H%M%S')+'-'+cohort+'-'+uuid.uuid4().hex[:6]
        with self.lock:self.starting[name]={'status':'starting','cohort':cohort}
        def work():
            try:
                s=sessions.Session.create(cohort,name)
                with self.lock:self.live[name]=s;self.starting.pop(name,None)
            except Exception as exc:
                with self.lock:self.starting[name]={'status':'failed','cohort':cohort,'error':str(exc),'trace':traceback.format_exc()}
        threading.Thread(target=work,daemon=True).start();return {'run':name,'status':'starting'}
    def get(self,name):
        with self.lock:
            if name in self.live:return self.live[name]
            if name in self.starting:return None
        raise KeyError(name)
    def open(self,name):
        with self.lock:
            if name in self.live:return self.live[name]
            path=sessions.RUNS/name
            if not (path/'workbench.json').is_file():raise KeyError(name)
            r=sessions.open_run(path);self.live[name]=r;return r
    def close(self,name):
        with self.lock:r=self.live.pop(name,None)
        if r is not None:r.close()
        return {'run':name,'status':'closed'}
    def close_all(self):
        with self.lock:items=list(self.live.items());self.live.clear()
        for name,r in items:
            try:r.close()
            except Exception:pass
    def runs(self):
        with self.lock:live=dict(self.live);starting=dict(self.starting)
        out=sessions.list_runs(live)
        known={x['run'] for x in out}
        for name,st in starting.items():
            if name not in known:out.append({'run':name,'cohort':st['cohort'],'status':st['status'],'error':st.get('error'),'open':False,'progress':None})
            else:
                for x in out:
                    if x['run']==name:x['status']=st['status'];x['error']=st.get('error')
        return out


def make_handler(bench):
    class Handler(BaseHTTPRequestHandler):
        server_version='ARHWorkbench/0.1'
        def log_message(self,*a):pass
        def send_json(self,code,value):
            body=json.dumps(value,indent=None,sort_keys=True).encode()
            self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def body_json(self):
            n=int(self.headers.get('Content-Length') or 0)
            return json.loads(self.rfile.read(n) or b'{}') if n else {}
        def route(self,method):
            path=self.path.split('?')[0].rstrip('/') or '/';parts=path.split('/')[1:]
            if method=='GET' and path=='/':
                html=(HERE/'index.html').read_bytes()
                self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(html)));self.end_headers();self.wfile.write(html);return
            if parts[:1]!=['api']:return self.send_json(404,{'error':'NOT_FOUND'})
            parts=parts[1:]
            if parts==['cohorts'] and method=='GET':return self.send_json(200,{'cohorts':bench.cohorts()})
            if parts==['runs'] and method=='GET':return self.send_json(200,{'runs':bench.runs()})
            if parts==['runs'] and method=='POST':
                b=self.body_json();return self.send_json(202,bench.start(b.get('cohort','original')))
            if len(parts)>=2 and parts[0]=='runs':
                name=parts[1];rest=parts[2:]
                if rest==['open'] and method=='POST':r=bench.open(name);return self.send_json(200,r.view())
                if rest==['close'] and method=='POST':return self.send_json(200,bench.close(name))
                r=bench.get(name)
                if r is None:
                    st=bench.starting.get(name,{});return self.send_json(200,{'run':name,'status':st.get('status','starting'),'cohort':st.get('cohort'),'error':st.get('error'),'mode':None})
                if rest==[] and method=='GET':return self.send_json(200,r.view())
                if rest==['step'] and method=='POST':
                    b=self.body_json();return self.send_json(200,r.step(b.get('op')))
                if rest==['reader'] and method=='GET':return self.send_json(200,r.reader())
                if len(rest)==2 and rest[0]=='records' and method=='GET':
                    es,ts=r.records();return self.send_json(200,{'ledger':rest[1],'records':es if rest[1]=='E' else ts})
                if len(rest)==3 and rest[0]=='record' and method=='GET':return self.send_json(200,r.record(rest[1],int(rest[2])))
            return self.send_json(404,{'error':'NOT_FOUND'})
        def handle_any(self,method):
            try:self.route(method)
            except Refusal as exc:self.send_json(409,{'error':exc.code,'detail':exc.detail})
            except KeyError as exc:self.send_json(404,{'error':'NO_SUCH_RUN','detail':str(exc)})
            except (ValueError,AssertionError) as exc:self.send_json(400,{'error':type(exc).__name__,'detail':str(exc)})
            except Exception as exc:self.send_json(500,{'error':type(exc).__name__,'detail':str(exc),'trace':traceback.format_exc()})
        def do_GET(self):self.handle_any('GET')
        def do_POST(self):self.handle_any('POST')
    return Handler


def serve(port=8765,host='127.0.0.1'):
    assert host in ('127.0.0.1','localhost','::1'),'loopback only'
    bench=Workbench();server=ThreadingHTTPServer((host,port),make_handler(bench));server.daemon_threads=True
    return bench,server
