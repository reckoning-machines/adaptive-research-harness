"""Linux generation/quiescence evidence; never grants a governed role."""
from pathlib import Path
import os
import stat
from .encoding import decode, require, Refusal, raw_digest


def generation(pid=None):
    pid=pid or os.getpid()
    try:
        text=Path(f'/proc/{pid}/stat').read_text();rest=text[text.rindex(')')+2:].split()
        group=Path(f'/proc/{pid}/cgroup').read_text().strip()
        return {'pid':pid,'start_ticks':int(rest[19]),'boot_id':Path('/proc/sys/kernel/random/boot_id').read_text().strip(),'cgroup':group}
    except (OSError,ValueError,IndexError) as exc:raise Refusal('GENERATION_UNAVAILABLE') from exc


def still_alive(old):
    try:os.kill(old['pid'],0)
    except ProcessLookupError:return False
    except OSError as exc:raise Refusal('WORKER_NOT_QUIESCENT','Cannot inspect original process') from exc
    try:return generation(old['pid'])==old
    except Refusal as exc:raise Refusal('WORKER_NOT_QUIESCENT','Original generation is unreadable') from exc


def verify_quiescence(path, inventory_hash, old_core, old_worker):
    """Trusted root supervisor evidence plus current absence checks, not a caller Boolean."""
    path=Path(path);require(path.is_file(),'WORKER_NOT_QUIESCENT')
    st=path.stat();require(st.st_uid==0 and not st.st_mode&(stat.S_IWGRP|stat.S_IWOTH),'UNTRUSTED_QUIESCENCE')
    b=decode(path.read_bytes())
    require(b.get('inventory_sha256')==inventory_hash and b.get('kind')=='HOST_QUIESCENCE', 'WORKER_NOT_QUIESCENT')
    require(old_core in b.get('terminated_generations',[]) and
            (old_worker is None or old_worker in b['terminated_generations']), 'WORKER_NOT_QUIESCENT')
    require(not still_alive(old_core) and (old_worker is None or not still_alive(old_worker)), 'WORKER_NOT_QUIESCENT')
    require(b.get('activation_jobs_cancelled') is True and b.get('old_channels_closed') is True,'WORKER_NOT_QUIESCENT')
    required={'harness-core.service','harness-tool-a.service','harness-tool-b.service'}
    require(required <= set(b.get('stopped_units', [])), 'WORKER_NOT_QUIESCENT')
    require(bool(b.get('closed_channels')) and bool(b.get('empty_cgroups')), 'WORKER_NOT_QUIESCENT')
    # A stopped unit path may now contain its replacement generation. The root
    # receipt witnesses emptiness before restart; all recorded old descendants
    # must remain dead. Current emptiness would reject legitimate replacements.
    for old in b['terminated_generations']:
        require(not still_alive(old), 'WORKER_NOT_QUIESCENT')
    for group in b['empty_cgroups']:
        p=Path(group)
        require(p.is_relative_to('/sys/fs/cgroup') and 'harness-' in p.name, 'INVALID_CGROUP')
    return b
