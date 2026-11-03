"""What a refusal or an operational error means and what to do about it, the same text the runbook holds."""
from __future__ import annotations

CATALOGUE = {
    'BUDGET_EXCEEDED': ('The grant cannot cover the reservation.', 'Reserve less, close unused reservations, or ask the Principal for a grant.'),
    'CAP_EXCEEDED': ('The lineage cap cannot cover the reservation.', 'Reserve less, close unused reservations, or ask the Principal for a grant.'),
    'GRANT_EXHAUSTED': ('The grant has no spendable budget left.', 'Close unused reservations or ask the Principal for a grant.'),
    'ALLOWANCE_EXCEEDED': ('The attempt\'s maximum exceeds what the reservation still holds.', 'Reserve enough for the tariff before attempting.'),
    'INVALID_ESTIMATE': ('The maximum does not equal the tariff for this input size.', 'Compute it from the profile; the client does this for you.'),
    'TOOL_NOT_PERMITTED': ('The tool is not one the grant permits.', 'Use a tool the grant and the profile declare.'),
    'INVALID_STEP': ('The step is not one the profile declares.', 'Use the declared step.'),
    'CAPABILITY_UNSUPPORTED': ('Parameters or content outside what the profile and the toolkit support.', 'Use the exact declared parameters and supported record kinds.'),
    'INVALID_INPUT': ('The inputs do not match the step\'s declared shapes.', 'Cite the documents and records the step declares, by the same researcher.'),
    'FENCED': ('The Principal stopped new spending under the grant.', 'Nothing to do as a researcher; existing liabilities still settle.'),
    'UNAUTHORIZED': ('This identity cannot do this operation.', 'Run it under the right identity; a researcher cannot check, decide, apply or fence.'),
    'CHECK_NOT_PASS': ('The check did not pass.', 'Read the criteria not met, correct the record, propose again.'),
    'NOT_DECIDED': ('No decision exists to apply.', 'Decide first, then apply.'),
    'STALE_CHECK': ('The check was made against an earlier head.', 'Re-check at the current head, decide, then apply.'),
    'STALE_BASE': ('The proposal names an earlier head.', 'Propose again at the current head.'),
    'NO_CHECK': ('The direction has not been checked.', 'Run the check first.'),
    'PENDING_PREDECESSOR': ('A retry before the earlier attempt was settled.', 'Settle it first, at the receipt or at the maximum.'),
    'WORKER_NOT_QUIESCENT': ('No proof that the earlier work can no longer execute.', 'Prove quiescence through the host control, then retry.'),
    'DUPLICATE_ATTEMPT': ('The same work already has an attempt with this dispatch index.', 'Resume that attempt rather than attempting again.'),
    'GENESIS_SCOPE': ('Startup was already run on this run directory.', 'Reconnect; do not restart.'),
    'INVALID_CLASS': ('A record called itself synthetic while citing historical inputs, or the reverse.', 'Let the client set the class from the cited inputs.'),
    'INVALID_DOCUMENT': ('A document without the provenance or file identity its class requires.', 'Import through the Observer, which supplies them.'),
    'INVALID_CLOSURE': ('The record cites something outside its closure or after it.', 'Cite committed records at or before the closure.'),
    'INCOMPLETE_RESEARCH_RECORD': ('The record lacks a required field.', 'Build the body with the client\'s record_body.'),
    'INVALID_REVISION': ('The record claims to revise something that is not its author\'s research record.', 'Revise only your own research records.'),
    'REQUEST_KEY_CONFLICT': ('A different payload was sent under a key already used.', 'Make a new key for new work; resend the same payload to recover a lost reply.'),
    'NOT_A_CANDIDATE': ('The chosen candidate is not in the live set.', 'Choose from the live set, or name your own question with chosen="own".'),
    'OPERATION_KIND_MISMATCH': ('The operation identity was used for a different kind of work.', 'Give new work a new identity.'),
    'ARTIFACT_CHANGED': ('A file that takes part in execution or recovery changed since the bundle was frozen.', 'Read the old run, or freeze a new run directory.'),
    'ENVIRONMENT_CHANGED': ('The installed Python or a declared package version differs from the one recorded at freeze.', 'Use the recorded environment, or freeze a new run directory.'),
    'ACTOR_MISMATCH': ('The token does not match the identity.', 'Reconnect with the current connection file.'),
    'SOURCE_NOT_ACTIVE': ('No active Observation grant declares this source.', 'Check the source id against the setup.'),
    'RESPONSE_LOST': ('Permission was consumed and no receipt exists anywhere.', 'The liability was kept at the maximum; prove quiescence before any retry.'),
}


def explain(code):
    """(meaning, next action) for a refusal or error code; a generic pair for one the catalogue does not hold."""
    return CATALOGUE.get(code, ('A refusal or error the catalogue does not describe.', 'Read the detail the core gave and the runbook\'s refusals table.'))
