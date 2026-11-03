"""Derive the research sequence, next permitted step and controls from ledger records.

Pure functions over evidence (E) and transition (T) records. They hold no
authority: the core re-checks permission and state when a step executes.
"""
from pathlib import Path
import sqlite3
from adaptive_research_harness.encoding import decode, raw_digest, require

RESEARCHER='AD-R1.0'
STAGES=['question','experiment','result','diagnostic','revised_question','control','check','admission']


def ref(e,ledger='E'):return {'ledger':ledger,'sequence':e['seq'],'sha256':e['sha256']}


def load_readonly(db_path):
    """Read a retained ledger without a core. Verifies every body hash. Writes nothing."""
    con=sqlite3.connect(f'file:{Path(db_path).resolve()}?mode=ro',uri=True);con.row_factory=sqlite3.Row
    out={}
    try:
        for ledger,table in (('E','evidence'),('T','transitions')):
            rows=[]
            for row in con.execute('SELECT * FROM '+table+' ORDER BY seq'):
                item=dict(row);require(raw_digest(bytes(item['body']))==item['sha256'],'CORRUPT_LEDGER')
                item['body']=decode(item['body'])
                if item.get('command') is not None:item['command']=decode(item['command'])
                rows.append(item)
            out[ledger]=rows
        claims=[{'attempt':r['attempt_seq'],'claim':decode(r['body']),'receipt':decode(r['receipt']) if r['receipt'] else None} for r in con.execute('SELECT * FROM dispatch_claims ORDER BY attempt_seq')]
    finally:con.close()
    return out['E'],out['T'],claims


def derive(es,ts,actor=RESEARCHER):
    """Locate the researcher's records for one cycle. Returns None for absent pieces."""
    ei={e['seq']:e for e in es}
    def result_of(e):return e['body'].get('result') or {}
    plain=[e for e in es if e['kind']=='RESEARCH_RECORD' and e['actor']==actor and not e['body'].get('failure') and e['body'].get('kind')=='plain']
    original=next((e for e in plain if 'n' in result_of(e) and 'adaptation' not in result_of(e)),None)
    selection=control=proposal=check=failed_check=decision=applied=None
    if original:
        selection=next((e for e in es if e['kind']=='RESEARCH_RECORD' and e['actor']==actor and e['body'].get('kind')=='SELECTION'
                        and (result_of(e).get('adaptation') or {}).get('prior_research',{}).get('sequence')==original['seq']),None)
    if selection:
        control=next((e for e in plain if (result_of(e).get('adaptation') or {}).get('selection_ref',{}).get('sequence')==selection['seq']),None)
    if control:
        proposal=next((e for e in ts if e['kind']=='PROPOSED' and e['actor']==actor and
                       ((e['body'].get('content') or {}).get('selection_basis') or {}).get('origin',{}).get('research_record',{}).get('sequence')==control['seq']),None)
    if proposal:
        tid=proposal['transition_id']
        checks=[e for e in ts if e['kind']=='CHECK' and e['transition_id']==tid]
        check=next((e for e in checks if e['body']['result']=='PASS'),None)
        failed_check=next((e for e in checks if e['body']['result']!='PASS'),None)
        decision=next((e for e in ts if e['kind']=='DECISION' and e['transition_id']==tid and e['body']['decision']=='ADMITTED'),None)
        applied=next((e for e in ts if e['kind']=='APPLIED' and e['transition_id']==tid),None)
    settled={e['body']['attempt'] for e in es if e['kind']=='SETTLEMENT'}
    pending=[e for e in es if e['kind']=='ATTEMPT' and e['actor']==actor and e['seq'] not in settled]
    funding=None;funding_open=False
    if proposal:
        funding=ei.get(proposal['body'].get('funding_ref'))
        if funding and funding['kind']=='RESERVATION':
            funding_open=not any(e['kind']=='CLOSED' and e['body']['reservation']==funding['seq'] for e in es)
    first_attempt=None
    if original:
        first_attempt=ei.get(original['body'].get('attempt'))
    return dict(original=original,first_attempt=first_attempt,selection=selection,control=control,proposal=proposal,check=check,
                failed_check=failed_check,decision=decision,applied=applied,pending=pending,funding=funding,funding_open=funding_open)


def next_step(d,cohort=None,claims=None):
    """The one operation the researcher program or Principal would perform next.

    A convenience for the page. The core enforces permission and state when it runs.
    """
    if d['pending']:
        a=d['pending'][0];seq=a['seq']
        has_receipt=any(c['attempt']==seq and c['receipt'] is not None for c in (claims or []))
        if has_receipt:return {'op':'complete-research','actor':'r01','payload':{'attempt':seq},'label':'Record the completed tool result and settle its charge','why':'An attempt was dispatched and has a receipt, but no research record or settlement yet.'}
        return {'op':'settle-pending','actor':'r01','payload':{'attempt':seq},'label':'Settle the interrupted attempt at its reserved maximum','why':'An attempt is pending without a usable receipt. Its liability is settled before any new work.'}
    if not d['original']:
        return {'op':'research','actor':'r01','payload':{'tool':'SYN-A-1','cohort':None if cohort=='original' else cohort},'label':'Run the first experiment (tool A counts selling after spikes)','why':'No research record exists for this run yet.'}
    if not d['selection']:
        return {'op':'choose-next-experiment','actor':'r01','payload':{'research_ref':ref(d['original'])},'label':'Apply the diagnostic and choose the next experiment','why':'The first result exists and has not been examined.'}
    if not d['control']:
        choice=((d['selection']['body'].get('result') or {}).get('adaptation') or {}).get('id')
        text={'complement-control':'Run the control: non-large rows only, tool B','independent-reproduction':'Reproduce the counts with tool B (independent calculation, same rows)'}.get(choice,'Run the selected next experiment')
        return {'op':'run-next-experiment','actor':'r01','payload':{'selection_ref':ref(d['selection'])},'label':text,'why':'The researcher selected an experiment that has not run.'}
    if not d['proposal']:
        return {'op':'propose-hypothesis','actor':'r01','payload':{'research_ref':ref(d['control'])},'label':'Propose registration of the narrowed hypothesis and reserve its funding','why':'The control result exists and nothing has been proposed from it.'}
    tid=d['proposal']['transition_id']
    if d['failed_check'] and not d['check']:
        return None
    if not d['check']:
        return {'op':'check','actor':'ck1','payload':{'transition_id':tid},'label':'Independent Check by Checker A (separate code, separate grant)','why':'A proposal awaits its Check.'}
    if not d['decision']:
        return {'op':'policy-decide','actor':'Principal','payload':{'transition_id':tid,'check':d['check']['seq']},'label':'P-1 policy decision on the passed Check','why':'The Check passed and no decision is recorded.'}
    if not d['applied']:
        return {'op':'apply','actor':'Principal','payload':{'transition_id':tid,'decision':d['decision']['seq']},'label':'Apply the admitted registration','why':'The decision is recorded and not yet applied.'}
    if d['funding_open'] and d['funding']:
        return {'op':'close-reservation','actor':'r01','payload':{'reservation':d['funding']['seq']},'label':'Close the consumed funding reservation','why':'The registration is applied; its reservation is still open.'}
    return None


def stages(d,es,ts):
    """Eight stage cards. Each carries plain text and the record it rests on."""
    out=[]
    def card(key,title,text=None,record=None,ledger='E',extra=None):
        item={'key':key,'title':title,'done':record is not None,'text':text,'ref':ref(record,ledger) if record else None,'kind':record['kind'] if record else None}
        if extra:item.update(extra)
        out.append(item)
    o=d['original'];r=(o or {}).get('body',{}).get('result',{}) if o else {}
    card('question','Question',o['body']['question'] if o else 'Do large synthetic volatility events warrant a narrower selling hypothesis?',o)
    a=d['first_attempt']
    card('experiment','Experiment',f"Tool {a['body']['input']['tool_id']} on the declared cohort, reserved before dispatch (maximum {a['body']['maximum']} units)" if a else None,a)
    card('result','Result',f"{r.get('k')} of {r.get('n')} spike rows show selling; {r.get('k_large')} of {r.get('n_large')} large-event rows" if o else None,o)
    s=d['selection'];ad=((s or {}).get('body',{}).get('result',{}) or {}).get('adaptation',{}) if s else {}
    card('diagnostic','Diagnostic',ad.get('reason') if s else None,s,extra={'initial_failure':ad.get('initial_failure'),'chosen':ad.get('chosen_subset')} if s else None)
    card('revised_question','Revised question',ad.get('question') if s else None,s)
    c=d['control'];ca=((c or {}).get('body',{}).get('result',{}) or {}).get('adaptation',{}) if c else {}
    control_text=None;nature=None
    if c:
        if ca.get('id')=='complement-control':
            control_text=f"{ca.get('comparison_k')} of {ca.get('comparison_n')} non-large rows show selling; {'meets' if ca.get('passes') else 'falls below'} the two-thirds diagnostic"
            nature='Descriptive diagnostic on the same synthetic rows. The two-thirds rule is the researcher\'s criterion, not a statistical test.'
        else:
            control_text='Tool B reproduced the counts from the same rows' if ca.get('passes') else 'Tool B did not reproduce the counts'
            nature='Independent calculation, not independent evidence. No new observation was obtained.'
    card('control','Control result',control_text,c,extra={'nature':nature,'research_failure':ca.get('research_failure'),'next_action':ca.get('next_action'),'passes':ca.get('passes'),'analysis':ca.get('id')} if c else None)
    ck=d['check'] or d['failed_check']
    card('check','Independent Check',(f"{ck['body']['result']} by {ck['actor']}: {sum(1 for x in ck['body']['criteria'].values() if x['status']=='MET')} of {len(ck['body']['criteria'])} criteria met") if ck else None,ck,'T')
    ap=d['applied'];dec=d['decision']
    text=None
    if ap:text=f"Registered at N={ap['body']['n']} by {dec['body']['decider'] if dec else '?'}. This admits a registration for future testing, not scientific support."
    elif dec:text='Decided, not yet applied'
    card('admission','Admission',text,ap or dec,'T')
    return out


def controls(es,ts,budgets=None):
    """Reservations, attempts, settlements, refusals and obligations from records."""
    settled={e['body']['attempt']:e for e in es if e['kind']=='SETTLEMENT'}
    closed={e['body']['reservation'] for e in es if e['kind']=='CLOSED'}
    rows=[]
    for e in es:
        b=e['body']
        if e['kind']=='RESERVATION':rows.append({'seq':e['seq'],'kind':'RESERVATION','actor':e['actor'],'grant':b['grant'],'amount':b['amount'],'purpose':b['purpose'],'closed':e['seq'] in closed})
        elif e['kind']=='ATTEMPT':
            s=settled.get(e['seq']);rows.append({'seq':e['seq'],'kind':'ATTEMPT','actor':e['actor'],'grant':b['grant'],'reservation':b['reservation'],'step':b['step'],'tool':b['input']['tool_id'],'maximum':b['maximum'],'settled':s['body']['actual'] if s else None,'provenance':(s['body']['provenance']['kind'] if s else None)})
        elif e['kind']=='SETTLEMENT':rows.append({'seq':e['seq'],'kind':'SETTLEMENT','actor':e['actor'],'grant':b['grant'],'attempt':b['attempt'],'actual':b['actual'],'provenance':b['provenance']['kind']})
        elif e['kind'] in ('CLOSED','BIND','RELEASE','FENCE'):rows.append({'seq':e['seq'],'kind':e['kind'],'actor':e['actor'],'body':b})
    refusals=[{'ledger':'E','seq':e['seq'],'actor':e['actor'],'op':e['body'].get('op'),'reason':e['body'].get('reason'),'detail':e['body'].get('detail')} for e in es if e['kind']=='REFUSAL']
    refusals+=[{'ledger':'T','seq':e['seq'],'actor':e['actor'],'op':e['body'].get('op'),'reason':e['body'].get('reason'),'detail':e['body'].get('detail'),'transition_id':e['transition_id']} for e in ts if e['kind']=='REFUSAL']
    pending=[e['seq'] for e in es if e['kind']=='ATTEMPT' and e['seq'] not in settled]
    spent={}
    for e in es:
        if e['kind']=='SETTLEMENT':spent[e['body']['grant']]=spent.get(e['body']['grant'],0)+int(round(float(e['body']['actual'])*100))
    return {'rows':rows,'refusals':refusals,'pending_attempts':pending,'settled_hundredths_by_grant':spent,'budgets':budgets}


def observations(es,d=None):
    """Every DOCUMENT observation on the ledger, with its declared variant, if any, and whether this run's research used it."""
    used=set()
    if d and d.get('original'):used={r['sequence'] for r in d['original']['body']['closure']['refs'] if r['ledger']=='E'}
    out=[]
    for e in es:
        if e['kind']!='OBSERVATION' or e['body'].get('form')!='DOCUMENT':continue
        doc=e['body']['document'];v=doc.get('variant')
        from adaptive_research_harness.encoding import digest
        out.append({'seq':e['seq'],'sha256':e['sha256'],'item_id':doc['item_id'],'content_sha256':digest(doc),'rows':len(doc['rows']),
                    'variant':v['name'] if v else None,'of_content_sha256':v['of_content_sha256'] if v else None,'edits':v['edits'] if v else None,'standing':v['standing'] if v else 'Admitted formation cohort',
                    'used_by_research':e['seq'] in used})
    return out
