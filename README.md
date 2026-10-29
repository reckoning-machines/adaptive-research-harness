# Adaptive Research Harness

## What this project is

Here is something we could not do before: run research agents under the same
rules we run coding agents. A coding agent today works inside a harness that
gives it a task, a budget, a test suite and a reviewer before anything is
merged. Adaptive Research Harness does the same for investment research. It
runs research agents under clear mandates, fixed budgets, independent review
before anything is adopted, and a complete record of what was tried, what
worked and what did not.

Strategies lose their edge over time, and so do the research methods that
produced them. The harness keeps every hypothesis, test, approval and
rejection as a permanent record, so a firm can see how its thinking evolved
and why.

The harness is built so that research agents, whether people or software,
can propose ideas and run authorized experiments, but cannot grant themselves
money, authority or credibility. A successor strategy starts with its own
record. It cannot inherit a predecessor's track record or obtain capital
simply by being related to it.

The harness sits underneath the tools a research team already uses. It holds
the budgets, the independent checks and the permanent record, while agent
frameworks supply orchestration and research content on top of it. Two
candidates have been examined so far: LangGraph as an orchestration layer for
the agents, and MiroFish as a producer of scenario research. The
[feasibility review](docs/audits/feasibility_coherence_public_library_20261029.md)
sets out the handful of boundary points any framework would connect through.
The first research cycle uses a simple in-house researcher and two synthetic
tools to prove those boundaries before any framework is attached.

## How it works

- **One accountable owner.** A single human owner, called the Principal, sets
  the mandates, the budgets, the limits and the standards used to judge
  results. Nothing in the system can change those without the Principal.
- **Research within a budget.** Research agents receive a defined allowance
  and spend it on experiments. Every charge is recorded before the work runs,
  so spending can never exceed what was approved.
- **Independent checking.** A separate checker, funded separately and unable
  to review its own work, examines each proposal before it can be adopted.
  A proposal that fails the check is kept as evidence, not deleted.
- **Decisions are recorded, then applied.** A change moves through a fixed
  sequence: proposed, checked, decided, applied. Each step leaves a durable
  entry. Nothing is applied without the steps before it.
- **Failure is preserved.** Rejected ideas, failed tests and negative results
  are retained as part of what the firm has learned.

## Where the project stands

**As of 29 October 2026:** this is a private prototype running entirely on
synthetic data. The governing rulebook, called the Constitution, was reviewed
independently and admitted by the Principal on 19 October 2026 as the design
baseline. A first working research cycle has since been built in Python and
tested on a single machine with simulated tools and simulated costs.

The most recent independent review of the code, the
[first-cycle build audit](docs/audits/adversarial_first_cycle_build_audit_20261029.md),
lists the defects that remain before a fuller runtime validation. The
[build decision addendum](docs/decisions/first_research_cycle_build_approval_addendum_20261029.md)
records what the Principal has authorized.

## What a run looks like

The example cycle asks one question of synthetic data: do larger volatility
events warrant a narrower selling hypothesis? The latest run tells this
story.

1. First result: selling appears in 8 of 12 spike rows, including 2 of 2
   large-event rows.
2. Limitation found: both large-event rows come from a single shock, so they
   are one observation, not independent repetition.
3. The researcher changes direction: it sets the large-event group aside and
   examines the remaining events on their own.
4. Control result: 6 of 10 show selling, below the two-thirds threshold. The
   broad claim does not survive the diagnostic.
5. Decision: the original claim and the negative result are both preserved.
   Only the narrower, still unproven question is registered for future
   testing.
6. Next step: find genuinely independent shocks. That step is planned and
   recorded, not executed.

The run cost 2.00 simulated research units, 0.25 for the registration check
and 4.00 for startup checking. Both independent checker implementations
verified the contrast. Fifty-one unit and component tests and six targeted
integration scenarios passed. The run evidence is retained at
[artifacts/development/adaptation-final/3887aa1acdab4e0cbe39be306f13e183/E01.json](artifacts/development/adaptation-final/3887aa1acdab4e0cbe39be306f13e183/E01.json).

The output states the question, the evidence, the change of direction, the
decision, the cost and the next action. It identifies the control as a
same-cohort synthetic analysis rather than new market evidence.

## Try the example

From the repository root, with standard Python 3.12 and no extra packages:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m acceptance.local --example
```

This creates a disposable database, runs the startup sequence, lets one
research agent form a hypothesis from synthetic data, has an independent
checker review it, and records the result with simulated costs. See
[BUILD.md](BUILD.md) for tests, retained run evidence and known limits.

## Start here

| For | Read |
| --- | --- |
| The investment case, the architecture and the controls | [Architecture](architecture.md) |
| Mandates, budgets, evidence standards and decision rights | [The Constitution](docs/doctrines/new_speedway_constitution.md), admitted by the [admission record](docs/decisions/cv1_admission_20261019.md). Its own status banner predates admission and is kept so the admitted text stays exact |
| What was built and how to run it | [BUILD.md](BUILD.md) and the [first research-cycle plan](docs/plans/first_research_cycle_implementation_20261029.md) |
| The prototype and startup sequence as designed | [Design plan](docs/plans/document_first_design.md), [PD-006](docs/decisions/principal_decision_006_replaceable_tools_and_first_prototype.md) and [PD-009](docs/decisions/principal_decision_009_genesis.md) |
| The original proposal and figures | [Design proposal (.docx)](docs/reference/new_speedway_design_proposal_20261019.docx) and [text transcription](docs/reference/new_speedway_discussion_draft_20261017.md), retained as reference material |
| Presentations for prospects | [Presentations](docs/presentations/README.md) |
| Decision and review history | `docs/decisions/` and `docs/audits/`, including superseded proposals and prior findings |
| Why some files still say "New Speedway" | [Rename record](docs/decisions/project_rename_20261029.md) |
| Package contents | [Manifest](docs/package/cv1_review_package_manifest.md) |

## Reading order for a reviewer

Start with the architecture, then read the Constitution. The
[review handoff](docs/audits/cv1_final_handoff_20261019.md) identifies the
baseline and scope. The [revision 10 audit](docs/audits/independent_preimplementation_design_audit_20261019.md),
[PD-010](docs/decisions/principal_decision_010_codex_audit_repairs.md),
the [final review](docs/audits/cv1_final_independent_review_20261019.md),
the [follow-up](docs/audits/cv1_revision12_bounded_followup_20261019.md) and
the [closure review](docs/audits/cv1_revision12_closure_20261019.md) trace
the findings, approved repairs and remaining work up to admission. The
audits dated 29 October 2026 cover the build.

## How the documents relate

The Constitution governs. Decision records document the Principal's
approvals. Audits provide evidence and authorize nothing. Plans set out
proposed work. Reference material preserves the original discussion. This
README and the architecture explain the design without changing its rules.
