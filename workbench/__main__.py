"""python3 -m workbench [--port 8765] [--demo]

Serves the local research workbench on 127.0.0.1. With --demo, runs the
headless demonstration (three cohorts, an interrupted run resumed, a
read-only inspection) and prints what happened.
"""
import argparse
import signal
import sys


def main():
    p=argparse.ArgumentParser(prog='workbench');p.add_argument('--port',type=int,default=8765);p.add_argument('--demo',action='store_true')
    args=p.parse_args()
    if args.demo:
        from .demo import run_demo
        return run_demo()
    from .api import serve
    bench,server=serve(args.port)
    print(f'Adaptive Research Harness workbench: http://127.0.0.1:{args.port}/  (loopback only; Ctrl-C closes live runs)',flush=True)
    import threading
    def stop(*_):
        # shutdown() must run off the serving thread, or it waits on itself.
        print('closing live runs',flush=True);threading.Thread(target=server.shutdown,daemon=True).start()
    signal.signal(signal.SIGINT,stop);signal.signal(signal.SIGTERM,stop)
    try:server.serve_forever()
    finally:bench.close_all();server.server_close()
    return 0

if __name__=='__main__':raise SystemExit(main())
