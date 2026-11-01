# Adoption Review - What ARH Adds, What It Costs to Adopt, and the Next Test

Status: **AUDIT EVIDENCE - REVIEW OF THE PROTOTYPE AS A TOOL FOR ANOTHER TEAM, WITH RECOMMENDATIONS. AUTHORIZES NOTHING.**

Date: 2026-11-01. Reviewer: Claude (Fable 5.1), recording and checking an
external reader's review of the public documents against the repository at
`3736a8b`. The external review is quoted where its claims are checked. Its
recommendations are kept, and each is tied to the code or document that
would have to change.

## 1. Disposition

**A credible prototype of one thing: keeping spending, evidence and
acceptance consistent while the agents change. Its usefulness to another
team is not yet demonstrated, and the cost of adopting it is the main
risk.** The four properties the review names as the contribution are each
enforced in the core, not only described. The overlap with agent
frameworks is real and the README now says what ARH adds beyond it. The
adaptive claim rests on a workflow that responds to evidence, not yet on
history improving an autonomous researcher's choices. The next piece of
work should be a practical test on an existing workflow, measured.

## 2. The four properties, checked against the code

| Review claim | Where it is enforced | Where it is exercised |
| --- | --- | --- |
| Completed work does not become accepted research by itself | `rules.do_apply` requires a `DECISION` of `ADMITTED` citing a `PASS` check at the current base, and `do_policy_decide` and `do_decide` refuse without one (`rules.py`, `CHECK_NOT_PASS`, `NOT_DECIDED`) | Headline example: an overstated count fails its check and `policy-decide` is refused. Local documents: a forged conclusion fails on `motivation` and cannot be decided (`tests/integration/test_local_documents.py`) |
| An interrupted attempt keeps its cost and its unresolved status | Pending attempts count at their maximum in every total (`model.View.reservation`); a second `tool-run` never re-permits (`dispatch.run`); replacement needs settlement plus a quiescence proof and, for a provider that can outlive its caller, a recorded disposition (`dispatch.ensure_retry`) | Headline example demonstrations 8 to 13; `tests/component/test_experiment.py::CallerExecutedTools`; path E of the runbook across a host restart |
| Rejected work stays useful history | Ledger tables refuse update and delete by trigger (`schema.sql`); refusals are appended as events (`engine._commit`); a `REJECTED` decision is a record, and design revisions name their predecessor and keep both (`rules.do_research_commit`, `revises`) | Local documents: a revised design concluded NOT_MET, a rejected direction, both still listed (`workbench/local_session.derive`) |
| Researchers and evaluators change while the acceptance rules stay | The experiment profile moves the experiment's shape out of enforcement code (`experiment.py`); the client registers a researcher and an evaluator through tokens and grants, not code changes; criteria names are fixed in `contracts.CLASS_CRITERIA` | The headline experiment and the local-documents experiment were added with no change to `actors.py`, the Checkers or the acceptance cases; 77 acceptance cases and the original example still pass |

The review's point that "agents need memory, checks and permissions" is
not a distinction holds. LangGraph supplies persistence and interrupts,
and the adapter uses them. The OpenAI Agents SDK supplies guardrails and
human approval. ARH's difference is where the check happens: at a commit
boundary that the researcher's process cannot write to, with a refusal
that is itself a record. The README's section on where ARH sits now says
this in the review's own four points.

## 3. The cost of adopting it, inventoried

What a new team must supply today, from `examples/langgraph_headlines/make_setup.py`
and `experiments/local_documents/make_setup.py`:

| Artifact | Size in the examples | What a new user has to understand |
| --- | --- | --- |
| `setup.json` | Three grants of about twenty fields each, limits, a theme, clock, constitution digest | Grant classes, scopes, budgets, forbidden subjects, source declarations with twelve required fields |
| `designs_and_methods.json` | Two designs, two tools, two or three methods, a hypothesis template, a formation document, each with content hashes | Design lineage, provenance under the A1 exception, method commitments, template fields the Checker compares |
| `experiment.json` | Steps, tools, tariffs, sources, genesis pair | Steps and tariffs, tool execution kinds, validators |
| Identities | Tokens for Principal, Observation function, researcher, Checker | Which process runs under which token |
| Startup | Genesis plus five or sixteen checked control transitions | That startup must run once, and what `GENESIS_SCOPE` means |

Both setup generators are about two hundred lines, and they are the only
way the three files have been produced. The host runs from the checkout
because `build_support/freeze.py` verifies the approved specification
manifest and walks repository directories. A retained run opens read-only
after any change to a file in its inventory, and the inventory covers
`tests/`, `workbench/`, `acceptance/`, `isolation/`, `experiments/`,
`build_support/` and `BUILD.md` as well as the core package. A new user
editing a test or a document therefore loses live reopen of every earlier
run. These two facts are what make the prototype feel like a reference
implementation rather than a tool.

## 4. Recommendations

Each is tied to a place in the repository. None is authorized by this
review. R2 and R3 touch build identity and need a Principal decision; the
rest are routine development.

| | Recommendation | Where | Why it closes a gap |
| --- | --- | --- | --- |
| R1 | A setup generator with defaults. One command takes a question, a source kind (text documents, tables or a synthetic cohort), one tool and a budget, and writes the three files with sensible grants, limits, methods, provenance and a theme. Factor it from the two `make_setup.py` scripts into `arh_client` | `client/arh_client/`, new module; the two `make_setup.py` files become callers of it | A new user connects one experiment without reading the Constitution. The generated files stay inspectable and the core keeps refusing what they do not declare |
| R2 | An installable host. Package `adaptive_research_harness` and `build_support` with the specification manifest and the files it covers, so `python -m adaptive_research_harness.local_host` runs from any environment | `build_support/freeze.py` (manifest and directory walk), a root `pyproject.toml` | Removes the checkout dependency the runbook has to explain. The manifest check is traceability of the build, so changing how it is satisfied is a decision for the Principal, not a code change to make quietly |
| R3 | Narrow what makes a run reopen live. Keep the full inventory as the build identity, but decide live eligibility on the core package, the experiment directory and the bundle, with the rest recorded as metadata | `workbench/session.inventory_matches`, `build_support/freeze.py` | Editing a test or a document stops turning earlier runs read-only. Because `BUILD.md` states that identical source yields one identity, the Principal should decide what identity covers |
| R4 | A quickstart for one existing script. Wrap a user's Python callable as a caller-executed tool with a generic design, through R1, so an existing research script runs as an attempt with its inputs, variants, refusals and acceptance recorded | `client/arh_client/`, building on `examples/langgraph_headlines/provider.py` and `experiments/local_documents/researcher.py` | This is the review's "connect one existing experiment with little additional work", and it is the strongest near-term case |
| R5 | Make the candidate rule read history. Today `CANDIDATE_RULE` in `experiments/local_documents/researcher.py` depends only on the current conclusion. Have it exclude candidates already rejected under the same direction, prefer documents not yet examined, and record which earlier records changed the set. Add a test where different history yields a different candidate set | `experiments/local_documents/researcher.py`, `evaluator.py` to recheck the derivation, `tests/integration/test_local_documents.py` | This is the smallest demonstration that accumulated research changes what is tried next, which the adaptive claim currently lacks |
| R6 | The practical test. Put one existing research workflow through ARH and show one concrete benefit: an unchecked revision refused, an interrupted paid call recovered, or a previous failure changing the next experiment. Record the integration effort in lines of code and hours | A new `examples/` directory and a report under `docs/implementation/` | The headline example already recovers an interrupted call and the local-documents path already turns a failure into candidates. What is missing is an existing workflow, a real provider under the decisions D-14 and the provider caps, and a measured cost of integration |

## 5. What should not change

The commit boundary, the refusal records, the separation of researcher
and Checker identities, the replacement rule for uncertain attempts, and
the document class. The review values these and the acceptance suite
exercises them. Adoption work should sit around them.

`dO/dS/dA` of this review: **`0/0/0`**. It adds evidence and
recommendations only.
