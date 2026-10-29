"""Private CLI. All mutations use peer-authenticated IPC; no direct database flag."""
import argparse
import os
from pathlib import Path
from .encoding import canonical, decode, Refusal, require


def main():
    parser=argparse.ArgumentParser(prog='adaptive-research-harness')
    sub=parser.add_subparsers(dest='mode',required=True)
    cli=sub.add_parser('command');cli.add_argument('operation');cli.add_argument('--request',type=Path)
    cli.add_argument('--socket',default='/run/adaptive-research-harness/core/commands.sock');cli.add_argument('--actor',required=True);cli.add_argument('--request-id')
    for name in ('serve','clock-service','tool-service','actor-service'):
        p=sub.add_parser(name);p.add_argument('--bundle',required=True);p.add_argument('--root',required=True)
        p.add_argument('--run-approval',default=None,help=argparse.SUPPRESS);p.add_argument('--socket',required=True);p.add_argument('--state',required=True)
        if name=='serve':
            p.add_argument('--clock-socket',required=True);p.add_argument('--tool-a-socket',required=True);p.add_argument('--tool-b-socket',required=True)
            p.add_argument('--supervisor-receipts',required=True)
        if name=='tool-service':p.add_argument('--tool',choices=['SYN-A-1','SYN-B-1'],required=True)
        if name=='actor-service':p.add_argument('--actor',required=True);p.add_argument('--core-socket',required=True)
    args=parser.parse_args()
    try:
        if args.mode=='command':
            from .client import Client
            result=Client(args.socket,args.actor).call(args.operation,decode(args.request.read_bytes()) if args.request else {},args.request_id)
            print(canonical(result).decode());return 0 if result.get('status') not in ('ERROR','REFUSED') else 2
        if args.mode=='serve':
            from .service import run_core
            run_core(args)
        elif args.mode=='clock-service':
            from .service import run_clock
            run_clock(args)
        elif args.mode=='actor-service':
            from .service import run_agent
            run_agent(args)
        else:
            from .profile import Profile
            from .tool_worker import run_worker
            profile=Profile(args.bundle);profile.approve_run(args.run_approval,args.root)
            require(os.getuid()=={'SYN-A-1':20101,'SYN-B-1':20102}[args.tool],'WRONG_TOOL_UID')
            run_worker(args.tool,args.socket,args.state,profile)
        return 0
    except (Refusal,OSError) as exc:
        print(canonical({'status':'ERROR','reason':getattr(exc,'code',type(exc).__name__),'detail':str(exc)}).decode());return 2


if __name__=='__main__':raise SystemExit(main())
