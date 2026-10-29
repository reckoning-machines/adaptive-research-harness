# Adaptive Research Harness

## What this is

An idea I think is right, carried far enough to run.

Coding agents now work inside harnesses. An agent gets a task, a budget, a
test suite and a reviewer, and nothing it writes is merged until the review
passes. In
[An Agentic Coding Proposal: Constitutional Coherence](https://reckoningmachines.substack.com/p/an-agentic-coding-proposal-constitutional)
I argued that the harness is not enough. Tests check behavior, not intent,
so an agent can pass every test while quietly adding a second source of
truth or giving itself decision rights. What a system needs underneath the
harness is a constitution, a statement of what exists, what it means and who
may change it, with the expected change to each declared before any work
begins and measured after.

Investment research has never had either. Researchers are not
pre-registered, their failed ideas are not kept, and nobody can say how many
hypotheses a firm tried before it found the one it now trades. This
repository asks what research would look like under the discipline that
article proposed for code. It contains the constitution that would govern
such a process, the record of how that constitution was written and
reviewed, and a small working prototype that runs one research cycle under
it on synthetic data.

I have put it up for feedback. The questions I most want answered are at
the end.

## The idea

Alpha decays, and so do the methods that find it. A firm needs a
research process that keeps probing its own ideas, retires the bad ones and
records why. In practice the process drifts, and the record of what was
tried lives in people's heads and old notebooks.

Two things change once the researcher is an agent.

**Every test can be registered before it runs.** A human researcher will not
pre-register. An agent has no choice. The harness logs the test, reserves
the budget and only then lets the work proceed. The count of hypotheses
tried becomes a fact in a ledger. That is what makes a multiple-testing
correction or a deflated Sharpe ratio arithmetic rather than a guess, and it
is the single claim this project rests on.

The ledger also records, for every thesis, the condition that would falsify
it before the outcome is known. A quant signal and a fundamental view are
treated the same way, so hit rate and calibration are facts in the record
rather than recollections, and the ideas that were quietly dropped stay on
the record beside the ones that paid.

**A strategy cannot inherit a track record.** A successor strategy starts
with its own record. It cannot borrow a predecessor's history or obtain
capital by being related to it. Agents can propose ideas and run authorized
experiments, but cannot grant themselves money, authority or credibility.

Around those two rules sit the controls a coding harness would recognize.

- **One accountable owner.** A single human, the Principal, sets mandates,
  budgets, limits and the standards results are judged by. Nothing in the
  system changes those without the Principal.
- **Spend is reserved before work.** Every charge is recorded before the
  work runs, so spending can never exceed what was approved.
- **Independent checking.** A separate checker, funded from its own grant
  and written in separate code, replays the committed record and recomputes
  the acceptance criteria from the original inputs. It cannot check work
  from its own lineage. A proposal that fails the check is kept as evidence.
- **Decisions are recorded, then applied.** Proposed, checked, decided,
  applied. Each step leaves a durable entry. Nothing skips a step.
- **Failure is preserved.** Rejected ideas and negative results are kept as
  part of what the firm has learned.

## How it was made

The design was written as documents, tested as documents, and built last.

The Constitution went through twelve revisions. Each one was reviewed by an
independent auditor, and each repair was admitted or rejected in a dated
decision record. Nothing was deleted along the way. Superseded revisions,
rejected proposals and the auditor's findings are all in `docs/`. The
[revision 10 audit](docs/audits/independent_preimplementation_design_audit_20261019.md)
and [PD-010](docs/decisions/principal_decision_010_codex_audit_repairs.md)
show what a review found and what changed.

The code was written last, against the admitted text, and the
[build audit](docs/audits/adversarial_first_cycle_build_audit_20261029.md)
recorded what document review could not catch. That is the article's loop
applied to the harness itself, and the record is there to check whether the
discipline caught anything.

## What exists

The prototype is written in Python with no dependencies beyond the standard
library, and it runs entirely on synthetic data. It implements one bounded
research cycle, from startup through a reservation before any spend, one
researcher forming a hypothesis from synthetic data, two independently written
checkers recomputing the result, and a decision that is recorded before it is
applied.

The example run asks whether larger volatility events in the synthetic data
warrant a narrower selling hypothesis. The run demonstrates the sequence.

1. A first result is registered and costed before it is computed.
2. The researcher finds a limitation in its own result. The two large events
   come from a single shock and are one observation, not two.
3. It changes direction, sets the large-event group aside and tests the rest.
4. The broad claim fails its own threshold.
5. The original claim and the negative result are both preserved. Only the
   narrower question is registered for future testing.
6. The next step is planned and recorded, not executed.

Both checkers verified the contrast. Costs are in simulated units. The run
evidence is retained at
[artifacts/development/adaptation-final/3887aa1acdab4e0cbe39be306f13e183/E01.json](artifacts/development/adaptation-final/3887aa1acdab4e0cbe39be306f13e183/E01.json),
and [BUILD.md](BUILD.md) covers the tests and retained evidence.

Run it from the repository root with Python 3.12.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

The harness is meant to sit under whatever orchestration a team already
uses. LangGraph and MiroFish have been examined as candidates, and the
[feasibility review](docs/audits/feasibility_coherence_public_library_20261029.md)
lists the boundary points any framework would connect through, though none
is attached yet. The first cycle uses an in-house researcher and synthetic
tools so the boundaries are proven before a framework is.

## Open questions

These are the questions I want feedback on.

- **Coverage.** The ledger counts the tests that run through the harness.
  Work done outside it, in a notebook or a spreadsheet, is never counted. If
  that outside work decides which ideas get registered, the ledger
  understates how many were tried, and the multiple-testing correction built
  on it is too small. How much of a firm's research has to run through the
  harness before the count means anything, and how would the firm know?
- **Judgment versus arithmetic.** The checker replays computation. Most of
  what makes research good or bad happens before the computation, in the
  choice of universe, window and definition of an event. The example run shows
  this, when the researcher notices two events are one shock. A checker
  cannot recompute that. What is the harness's answer to judgment errors?
- **Lookahead.** The dominant practical failure in quantitative research is
  a hypothesis formed after seeing the test window. Timestamped registration
  helps only if data vintage is part of the record. Is that enough, and what
  else is needed?

## Where to read

| For | Read |
| --- | --- |
| The design, end to end | [Architecture](architecture.md) |
| The rules themselves | [The Constitution](docs/doctrines/new_speedway_constitution.md), admitted by the [admission record](docs/decisions/cv1_admission_20261019.md). Its own status banner predates admission and is kept so the admitted text stays exact |
| How the rules were reviewed | [Review handoff](docs/audits/cv1_final_handoff_20261019.md), then the [revision 10 audit](docs/audits/independent_preimplementation_design_audit_20261019.md), [PD-010](docs/decisions/principal_decision_010_codex_audit_repairs.md), the [final review](docs/audits/cv1_final_independent_review_20261019.md), the [follow-up](docs/audits/cv1_revision12_bounded_followup_20261019.md) and the [closure review](docs/audits/cv1_revision12_closure_20261019.md) |
| What was built, and its limits | [BUILD.md](BUILD.md), the [first-cycle plan](docs/plans/first_research_cycle_implementation_20261029.md) and the [build audit](docs/audits/adversarial_first_cycle_build_audit_20261029.md) |
| How to run it | [Runbook](runbook.md) |
| The method | [Document-first design plan](docs/plans/document_first_design.md) |
| The original proposal | [Design proposal (.docx)](docs/reference/new_speedway_design_proposal_20261019.docx) and [text transcription](docs/reference/new_speedway_discussion_draft_20261017.md), kept as reference |
| The argument as slides | [Presentations](docs/presentations/README.md) |
| Why some files say "New Speedway" | [Rename record](docs/decisions/project_rename_20261029.md) |
| Everything else | `docs/decisions/`, `docs/audits/` and the [package manifest](docs/package/cv1_review_package_manifest.md) |

## How the documents relate

The Constitution governs. Decision records document what the Principal
approved. Audits are evidence and authorize nothing. Plans propose work.
Reference material preserves the original discussion. This README and the
architecture explain the design without changing its rules.
