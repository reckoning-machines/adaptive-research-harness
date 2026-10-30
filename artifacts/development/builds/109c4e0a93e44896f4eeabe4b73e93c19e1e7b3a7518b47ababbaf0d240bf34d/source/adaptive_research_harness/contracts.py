"""Finite command schemas and Check criterion names, shared as data only."""
from .encoding import fields, require

COMMON = ('authority', 'current_base', 'independence', 'funding', 'closure', 'registration_difference')
CLASS_CRITERIA = {
    'AUTHORIZATION': ('grant_content', 'prior_fence', 'source_declarations', 'tool_permissions'),
    'LIMITS': ('complete_limits', 'composition'),
    'AGENT_DESIGN': ('design_content', 'method_commitment', 'provenance', 'no_inherited_authority'),
    'THEME': ('motivation', 'typed_claims', 'selection'),
    'HYPOTHESIS': ('testability', 'resolution', 'sources', 'disjoint', 'selection', 'methods', 'recomputation', 'restatement'),
    'SUSPEND_POLICY': ('policy', 'scope', 'no_other_mutation'),
}
SCHEMAS = {
 'reserve': ({'grant','amount','purpose'}, {'expiry_ms','expected_sequence'}),
 'attempt': ({'reservation','step','input','dispatch_index','maximum','tier'}, set()),
 'settle': ({'attempt','actual','unit','provenance'}, set()),
 'close': ({'reservation'}, set()), 'fence': ({'grant','reason'}, set()),
 'propose': ({'transition_id','base','class','subject','content','budget','grant','funding_ref','delta'}, {'predecessor_transition'}),
 'check-commit': ({'transition_id','base','grant','attempt','closure','criteria','result','es','constitution','provenance','context'}, set()),
 'decide': ({'transition_id','check','decision','reason'}, set()),
 'policy-decide': ({'transition_id','check'}, set()),
 'apply': ({'transition_id','decision'}, {'bind'}),
 'invalidate-request': ({'bind'}, set()), 'release': ({'bind'}, set()),
 'research-commit': ({'grant','attempt','question','result','closure','claims','kind','snapshot','source_cutoff','parameters','tool','reproducibility','synthetic'}, {'SearchFamily','failure'}),
 'observation-commit': ({'grant','source','revision','form','period','item_id','document','slot'}, {'document_ref','value','items','window','error'}),
 'genesis': ({'constitution_sha256','design','grant'}, set()),
}
READS = {'get','history','state','budget','obligations','inspect-request','clock','profile','closure','dispatch-status'}
STEPS = {'research-counts','replacement-counts','check-transition','verification-candidate'}


def validate(op, payload):
    require(op in SCHEMAS, 'CAPABILITY_UNSUPPORTED', op)
    fields(payload, *SCHEMAS[op])
