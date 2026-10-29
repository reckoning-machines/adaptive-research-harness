"""Fresh independent record/accounting reader; no core model or predicates imported."""
from adaptive_research_harness.client import Client
from adaptive_research_harness.encoding import digest,units,canonical


def read(client=None):
    client=client or Client('/run/adaptive-research-harness/core/commands.sock','Principal')
    records={}
    for ledger in ('E','T'):
        records[ledger]=[];after=0;through=None
        while True:
            p={'ledger':ledger,'after':after,'limit':1000}
            if through is not None:p['through']=through
            page=client.query('history',p);records[ledger]+=page['records'];after=page['next_after'];through=page['through']
            if after>=through or not page['records']:break
    es,ts=records['E'],records['T']
    for rows in (es,ts):
        assert [x['seq'] for x in rows]==list(range(1,len(rows)+1))
        assert all(digest(x['body'])==x['sha256'] for x in rows)
    applied=[x for x in ts if x['kind']=='APPLIED'];assert [x['body']['n'] for x in applied]==list(range(len(applied)))
    assert len({x['transition_id'] for x in applied})==len(applied)
    bindings={x['seq']:x for x in es if x['kind']=='BIND'}
    consumed=[x['body']['bind'] for x in applied if x['body'].get('bind')]
    invalidated=[x['body']['bind'] for x in ts if x['kind']=='BINDING_INVALIDATED']
    assert not set(consumed)&set(invalidated)
    assert len(consumed)==len(set(consumed)) and len(invalidated)==len(set(invalidated))
    settled={}
    for x in es:
        if x['kind']=='SETTLEMENT':
            aid=x['body']['attempt'];assert aid not in settled;settled[aid]=x
    totals={};pending=[]
    for x in es:
        if x['kind']!='ATTEMPT':continue
        b=x['body'];value=units(settled[x['seq']]['body']['actual']) if x['seq'] in settled else units(b['maximum'])
        totals[b['grant']]=totals.get(b['grant'],0)+value
        if x['seq'] not in settled:pending.append(x['seq'])
    for grant,value in totals.items():assert units(client.query('budget',{'grant':grant})['committed'])==value
    states={k:'CONSUMED' if k in consumed else 'PENDING_RELEASE' if k in invalidated else 'FROZEN' for k in bindings}
    for x in es:
        if x['kind']=='RELEASE':
            assert x['body']['bind'] in invalidated;states[x['body']['bind']]='RELEASED'
    return {'status':'RECONSTRUCTED','N':len(applied)-1,'E':len(es),'pending_attempts':pending,
      'binding_states':{str(k):v for k,v in states.items()},'committed_hundredths':totals,
      'preserved_refusals':sum(x['kind']=='REFUSAL' for x in es+ts),'synthetic_forward_standing':0,
      'next_operation':'Settle retained pending liabilities through original grantee/Principal; otherwise inspect current authority and exact closure before any new work.'}

if __name__=='__main__':print(canonical(read()).decode())
