# Funded Independent Checker Contract

Status: **PROPOSED SPECIFICATION — NO CHECK HAS RUN.**

Owner: CV1 §III.8 and Part V, with Part X where cited. A Checker observes and
reports; it cannot decide, Apply, change a criterion or write population
state. The [A1 supplement](amendments.md) is necessary for this synthetic
arrangement. Separate programs alone do not satisfy the existing provider
supplement. Approval of A1 removes only that supplement within its scope.

## 1. Inputs, execution and records

`check.run(TransitionId, expected_base, checker_grant, reservation_ref)` is a
Checker-client orchestration command. The service authenticates the caller
as the registered Checker, confirms scope and admits its verification attempt
before the Checker program runs. The purpose names the already-proposed
Transition. Every attempt maximum and actual is 0.25 simulated units.
Unsupported content is refused before dispatch where possible; content found
unsupported during computation still costs the declared actual.

Input is immutable proposal content, exact `(E,N,F)` closure and instant,
both parties' registered designs/provenance, all referenced sources/methods,
grant/fence/attempt/binding history, population at N, and the full registration
history needed for restatement checks. The Checker reads committed records
through the service; raw SQL and present-day substitute objects are forbidden.
Unreferenced memory, caller-supplied summaries and expected-result fixtures
cannot substitute for these reads. `F` is N/A only after proving no Execution
Authorization has ever applied. A failed reachable-ledger read interrupts
verification as LEDGER_UNREACHABLE; no usable PASS is emitted.

CHECK-A replays the supplied committed records in order and directly evaluates
each criterion. CHECK-B independently reconstructs subject sets, predecessor
relations and accounting sums, and computes the same criteria. Both parse the
declared narrow scientific templates themselves. They may share transport,
canonical encoding and immutable schema definitions, but **may not import
core admission predicates, researcher calculations, each other's criterion
functions or expected test results**. Review the actual import graph and
installed hashes in acceptance. Common authorship is disclosed; independent
execution/recomputation is not a claim of independent human code authorship.

Output is a Check candidate containing the exact CV1 §III.8 fields:
Transition/class/base; proposer and its authority; Checker/design/grant and
both provenances; CV1/ES-1.0; closure and instant; an observation for every
applicable Part V criterion with MET/NOT MET/NOT DETERMINABLE and exact record
cites; funding attribution; verification attempt and any reproduction records;
PASS/FAIL/STOP and escalation. The service admits the Check only from the
authenticated eligible Checker and validates shape, references and protected
criteria. It cannot replace a judgment by copying its own admission result.

Known failed gates produce NOT MET and, when all criteria are determinable,
FAIL. A missing constitutional identity/meaning/owner/authority produces
NOT DETERMINABLE and STOP with escalation; a Principal-only decision is not
such a gap. Malformed transport, unavailable inputs and content outside the
implemented scientific capability produce an operational refusal/interrupted
verification record, **not a fabricated constitutional STOP or PASS**. The
caller cannot advance on either. Preserve a funded attempt's failure and
settlement even when no complete lawful Check can be produced.

## 2. Common criteria and division of responsibility

For every supported class, evaluate these common items in addition to its
class row below:

1. Exact immutable subject/version and proposal bytes exist at the claimed
   base; the base is current and the criteria are those pinned there.
2. Proposer has the cited class/scope authority. A Principal control act
   cites the Principal directly, has no metered research consumption, and
   records proposer funding N/A. Do not require a fictitious Principal grant.
3. Checker has its own active Checker grant, no Research grant, is not the
   proposer or in its lineage, and is not excluded for this subject. Verify
   separate installed executable/OS identity and A1's synthetic-only scope.
4. Proposer's metered budget is covered by the named open reservation at the
   Check closure, correct purpose/owner, sufficient amount and below fences.
   Show remaining spendable budget for attribution without imposing it as
   a second covered-budget requirement. Checker funding is separate.
5. Every cited artifact, method and evidence member is exact and committed;
   read failures never fall back. All scientific claims cite the appropriate
   closure. Historical/synthetic research carries “authored knowing the
   period” and earns no forward standing.
6. Registrations are not undeclared restatements. Record the concrete
   difference, predecessor where applicable, and same-family relationships.
   A new string ID alone is not a difference. A successor receives no
   inherited grant or performance credit.

The core deterministically enforces caller attribution, immutable identity,
record shape/reference integrity, grant permissions, budgets and ordering,
current-base/Check/decision requirements, P-1, binding/disposition and the
one-time genesis boundary. The independent Checker re-evaluates applicable
deterministic facts and supplies the scientific/content judgments below.
Double validation of a predicate is not duplicate ownership: only the owning
boundary commits the governed fact. A Checker PASS never itself registers it.

## 3. Supported class matrix

| Transition/content | Computation and judgment required | Failure examples; decision route |
| --- | --- | --- |
| Exact Apply-0 bootstrap | No Checker exists. Core verifies empty ledgers and exactly CV1, AD-CK-1.0, AU-CK-A against materialized packet, direct Principal authority and one-time scope | Extra grant, wrong CV1 bytes or nonempty history refuses; no “bootstrap PASS” is fabricated |
| Initial Observation grant | Verify Principal, no research/check/grant rights, complete source meanings/revisions, parser/extraction/print/grace rules, explicit slots, complete-listing contract and synthetic labels. Evaluate completeness of declarations, not existence of an unclaimed SRC-E price | Missing grace, synthetic relabel of SRC-E, implicit network/tool rights or inconsistent enumeration fails; Principal decides after independent Check |
| Initial Research/Checker grants | Resolve all grantees to registered designs at base. Validate class/evidence permissions against CV1, scopes and declarations, finite nonnegative exact budgets, pooled/cap/subgrant relationships, expiry, reservation duration, binding applicability, own named tools/tiers/estimation and uncapped prohibition. Check separate funding, exclusion chains and A1 restriction for Checkers | Missing binding interval, Research rights in Checker grant, permission to grant, extra implicit budget or undeclared provider fails; Principal decides |
| Grant amendment/supersession/revocation | Identify exact predecessor/successor; no inherited extra rights. For Research/Checker revoke or supersession, verify prior Principal FENCE naming predecessor. Re-evaluate complete successor content and own-subject exclusions. Revocation leaves pending settlement liabilities attributable | Missing fence, wrong predecessor or self-check fails. Principal direct authority, proposer budget N/A; CK-B checks anything concerning CK-A/its grant chain |
| Initial limits | Replay current admitted strategies and allocations, confirm both empty, calculate all usages as zero, compare each declared nonnegative limit and enumerate every comparison. No breach may be omitted | Negative limit fails; nonempty composition outside implemented risk capability gets no Check approval. Principal decides |
| Research Agent Design registration (ten startup designs and bounded successors) | Verify immutable instructions/tools/evaluation-input/output contract, RESEARCH class and truthful provider provenance, method commitment bytes/hash, explicit lineage/predecessor, distinct declared question or instruction difference. Registration conveys no permission; every proposed operation must remain behind runtime grants | Absent method, changed bytes under old ID, undeclared restatement, fake provider provenance or request to inherit grant fails. Principal handles initial registrations; P-1 only an eligible no-grant successor |
| Second Checker registration and bounded successors | Same design checks plus CHECKER class, separate implementation description/build hash, no Research permission, contribution method and supported matrix. Inspect independent modules/import inventory under the checking actor's funded verification attempt. Candidate execution waits for its own registration and grant; acceptance then runs it under its own funded attempt | Same proposer lineage, imported researcher outcome/expected approval or missing execution provenance fails. Initial CK-B registration is checked by CK-A. CK-A successor is checked by CK-B, never CK-A |
| Initial Theme and exact bounded Theme content | Verify closure within proposer's scope (Principal direct here), typed claims grounded in exact source documents, explicit assumption/question status, selection uncertainty/decision/experiment/value or UNESTIMATED reason/cost/time/horizon/stopping/origin, and predecessor when applicable | Outside-scope closure, unsupported factual assertion, missing selection field or unmarked restatement fails. Principal decides; no P-1 Theme decision |
| Ordinary synthetic Hypothesis template | Perform the full algorithm below: testability, fixed resolution/extraction, active sources with grace, disjoint formation/resolution, document-member conditions, selection/method completeness, family/restatement and funding | Bad arithmetic, missing grace, overlapping formation/resolution, contradicted restatement or uncovered registration budget fails. P-1 can decide only if all its enumerated conditions hold |

Full grant scope in PD-009 is not a claim that every class has implementation.
Evaluation/standing, Strategy/Allocation/Execution, arbitrary constitutions,
natural-language hypotheses and other source rules have no supported Check
or mutation path in this milestone. No evaluator is silently stubbed to PASS.

Packet-conformance checking is separate from constitutional checking. The
approved fixture client may only submit its exact positive templates and
listed variations. The Checker does **not** add a constitutional rule that
every lawful grant must match a golden JSON file. A legal but unimplemented
request receives CAPABILITY_UNSUPPORTED, no completed approving Check;
it cannot be called constitutionally invalid merely for differing from this
profile. All implementation-capability refusals remain inspectable.

## 4. Scientific judgment within the narrow template

The supported Hypothesis language is the supplied source/date/threshold/ratio
template with explicit fields; arbitrary prose is not interpreted. The
fixed ordinary case is threshold 2, target ratio 2/3, one declared next-day
FIRST_RELEASE member, exact tolerance zero. Mutated invalid fields are
testable failure inputs, never a request to invent a new statistical standard.

The Checker reads the entire formation DOCUMENT and Research Record, validates
unique event IDs and the typed fields, and recomputes n=12, k=8, n_large=2,
k_large=2 using its own algorithm. Compare the result hash and four values
with the submitted Research Record; differing input bytes or counts fail.
The numeric output alone establishes neither an investment edge nor a
probability model. Its justification is that this controlled question is
testable and the selection discloses uncertainty and synthetic limitations.

Resolve the exact source revision under the Observation Authorization active
at base. Recompute extraction and the binary rule `3*k_large >= 2*n_large`;
require n_large>0 for extractability. Check period, print, grace, declared
structural bound and unambiguous enumeration identity. A missing/failing
future item has the declared failure treatment; no later print substitution
is allowed. The future member must not be a formation observation or a member
of any formation resolution set. DOCUMENT members must have the declared
structural bound or a lawful absence witness and remain disjoint under
CV1 §III.2. Synthetic status is retained regardless of either route.

Validate all selection fields and all initial method fields and hashes,
including falsifier, horizon and stopping rule. Check their arithmetic and
declared relation: binary scoring, p=2/3 working predictive model, dependence
clustering, forward-only floor and multiplicity adjustment. This is checking
a declared method's completeness and internal consistency, not executing an
ES-1 evaluation or judging synthetic results economically convincing.

For restatement, compare all earlier registrations in the Theme/family,
including rejected and contradicted history, by the exact tuple (observable,
predicate threshold, ratio, source/field/print, horizon, resolution rule,
falsifier and methods). A changed date or identifier alone is not a scientific
difference. For a bounded successor, require a cited predecessor and explicit
instruction difference; do not reset family history. An unfamiliar scientific
equivalence question is outside capability and gets no approving Check.
The program must not claim that tuple comparison solves arbitrary semantic
equivalence.

## 5. Own-subject routing and failure coverage

CK-A can check startup 1–16 because the proposer is Principal and none is
CK-A's own design/grant chain. Once CK-B exists, it checks CK-A changes;
CK-A checks CK-B changes. Each uses its own reservation and attempt. Before
CK-B's grant applies, an attempted CK-A amendment has no eligible installed
Checker: preserve the refusal and wait; never borrow the genesis waiver.
If both Checker grants are fenced/exhausted/revoked, this profile may be
unable to progress. It retains obligations rather than manufacturing funding
or a third Checker. A future Principal-authorized recovery expansion is a
new scope, not an obligation to make every test fixture live forever.

Add these executable witnesses to R01–R16/B01–B11/T01–T07:

| ID | Stimulus and expected observable result | Prohibited effect |
| --- | --- | --- |
| S01 | Execute startup through 16 using commands; independently inspect sixteen criterion-complete Checks, separate attempts and 4.00 settled CK-A cost | Seeded membership, free Check or second waiver |
| S02 | Supply explicit missing-value null for binding interval, tool tier, source grace or enumeration rule in separate well-formed candidate proposals; computed NOT MET/FAIL where determinable. A missing mandatory wire field instead gets schema refusal, never a Check | Matching a template name supplies missing content |
| S03 | Initial limits zero passes computed empty-composition checks; negative limit is refused at typed ingress with no Check/Apply; explicit missing-value limit in a well-formed candidate receives a computed completeness failure | Fixed “startup always passes” branch or forged Check for a rejected wire request |
| S04 | Missing method/hash, same ID/different content, undeclared duplicate design, inherited grant request; preserve failure per independent criterion | Registration carries runtime authority or ten labels substitute for ten declared designs |
| S05 | Corrupt one formation count/byte, reuse resolution member or remove selection time/origin; recomputation gives failure with exact cites | Expected approved outcome supplied by fixture |
| S06 | Check own grant/design and synthetic program asserting provider diversity; refuse. Route CK-A change to CK-B after grant 14; it independently computes a Check under A1 | Provider-name spoof or role label substitutes for independence |
| S07 | Death during funded Checker computation, after result before Check, after Check before settlement; fresh process inspects actual records and preserves/settles liability | Free rerun, missing negative evidence or Check inferred from receipt alone |
| S08 | Modify installed criterion code after freezing the inventory, or link Checker to core predicate/expected-result code; hash/import validation refuses profile. Send legal but unsupported scientific content; explicit capability refusal | Passing canned checks, silently adding criteria, or mislabelling implementation inability as constitutional STOP |

Run both Checkers against the valid ordinary template and determinable
negative cases. Outputs must agree on criteria, not necessarily byte-identical
explanatory prose or attempt references. Source/build inspection plus
observable mutants is required; a test suite alone cannot prove independence.
