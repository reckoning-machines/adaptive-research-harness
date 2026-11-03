# Changelog

## Unreleased

### 2026-11-02 — RV-03: declared Checker steps

Fixed an inconsistency where ARH admitted an authorized, declared Checker step for execution but refused its Check commit with `UNFUNDED_CHECK` unless the step was named `check-transition`.

Check validation now resolves the declared step and requires its Checker kind, matching input step, permitted tool and exact declared maximum. Existing role, independence, grant, funding, scope, attempt, receipt and replay restrictions remain in force. The original `check-transition` behavior is preserved; no protocol, schema or public-client change is required.

Regression coverage demonstrates independent 0.25 and 0.50 Checks, invalid-step/maxima/funding/actor refusals, and lost-response recovery across fresh host processes without duplicate Checks or charges. All six targeted regressions, 106 full unit tests and 77 selected native acceptance schedules passed. Existing native coverage limitations remain documented in the [repair and verification record](docs/implementation/rv03_repair_20261102.md).

Repair commit: `301492667eeaaeaf34c93daaad4cef375c2d04fe`. Changed core bytes require an explicitly reviewed dependency pin; old run histories must not be silently migrated. RV-02, the separate public-client convenience-helper limitation, remains open.
