"""Exact runtime scope; all cases require separate artifact/run approval."""
CASES={}
for prefix, labels in {
'R':['unauthorized','concurrent-budget','settlement-retry','revoked-settlement','invalid-settlement','tool-failure','uncertain-dispatch','fenced-retry','overrun','close-pending','stale-check','independence','synthetic-standing','bad-registration','historical-read','genesis-reuse'],
'B':['bind-restart','fence-after-bind','revoke-after-bind','strict-interval','terminal-race','atomic-refusal','release-restart','terminal-duplicates','old-binding','ledger-outage','expiry-frozen','policy-suspension'],
'C':['writer-lock','command-dedup','dispatch-dedup','worker-quiescence','prospective-reference','clock-outage','researcher-attribution'],
'S':['startup','missing-grant-fields','limits','design-defects','scientific-defects','checker-routing','checker-death','artifact-integrity'],
'T':['replacement','tool-permission','forged-output','swap-pending','undeclared-tool','host-isolation','peer-impersonation']}.items():
    CASES.update({f'{prefix}{i:02d}':label for i,label in enumerate(labels,1)})
DEATH_POINTS=['before_reserve_commit','after_reserve_commit','before_attempt_commit','after_attempt_commit',
 'after_dispatch_claim_commit','tool_before_execution','tool_after_execution_before_reply','after_research-commit_commit',
 'after_settle_commit','checker_during_computation','checker_after_result','after_check-commit_commit',
 'after_decide_commit','after_bind_commit','before_apply_commit','after_invalidate-request_commit','after_apply_commit',
 'principal_control_continuation','clock_unavailable','all_components_restart']
CASES['E01']='first-working-research-cycle'
