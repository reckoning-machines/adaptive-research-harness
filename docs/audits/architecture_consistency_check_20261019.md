# Author's Consistency Check — `architecture.md`, `README.md` and the Review Package

Status: **AUTHOR'S CHECK — EVIDENCE, NOT DOCTRINE. Not the independent
review. Certifies nothing.** Author: Claude, who also wrote the files
checked. Date: 2026-10-19. Subject: [`architecture.md`](../../architecture.md),
[`README.md`](../../README.md), the
[package manifest](../package/cv1_review_package_manifest.md) and the
§7 addition to the [final handoff](cv1_final_handoff_20261019.md),
against Constitution revision 11 (commit `4407723`).

## 1. Links and anchors

Method: every relative link in `README.md`, `architecture.md` and every
Markdown file under `docs/` was resolved against the package file set;
every `#anchor` was resolved against the target's headings using the
GitHub slug rule (lower case; punctuation other than hyphens and spaces
removed; spaces to hyphens; backticks and emphasis stripped).

```text
links checked: 216
unresolved targets: 0
unresolved anchors: 0
links leaving the package: 0
```

The script is reproduced here so the check can be re-run before the
package is built:

```python
import re, os, glob
files = ["README.md","architecture.md"] + sorted(glob.glob("docs/**/*.md", recursive=True))
pkg = set(files) | {"docs/reference/new_speedway_design_proposal_20261019.docx"}
def slug(h):
    h = re.sub(r"[`*_]", "", h).strip().lower()
    return re.sub(r"[^\w\- ]", "", h).replace(" ", "-")
anchors = {f: {slug(h) for h in re.findall(r"^#{1,6}\s+(.*)$", open(f).read(), flags=re.M)} for f in files}
for f in files:
    for m in re.finditer(r"\]\(([^)\s]+)\)", open(f).read()):
        link = m.group(1)
        if link.startswith(("http://","https://","mailto:")): continue
        path, _, anc = link.partition("#")
        target = os.path.normpath(os.path.join(os.path.dirname(f), path)) if path else f
        assert target in pkg, (f, link)
        if anc and target.endswith(".md"): assert anc in anchors[target], (f, link)
```

## 2. Terminology

Each term `architecture.md` uses is the Constitution's term with the
Constitution's meaning, defined once in the architecture's Terms
section or on first use: Principal, Authorization, Transition, Applied
History, Evidence ledger, Paper Book, Checker, Theme, Hypothesis,
Strategy Version, Agent Design Version, Historical Reconstruction,
Contemporaneous Forward Record, document-phase admission, `FENCE`,
`REDUCE`, `BINDING`. Two simplifications are deliberate and are
flagged for the reviewer: "binding" in §5 compresses the Evidence-side
`BIND` and the Transition-side terminal disposition into one row, and
"functions" in §4 does not restate the three functions' separate
Authorizations. Neither introduces a meaning absent from the text. The
architecture does not use the words "ontology", "ANF", "OSA" or "ΔO/ΔS/ΔA"
and instead says what they mean in the one place it needs them (§1,
why documents first).

## 3. Readiness claims

Sweep of `README.md` and `architecture.md` for "selected", "certified",
"implemented", "proven", "guarantee", "production", "live trading",
"built", "deployed": every hit is either a negation (no runtime
selected; nothing certified; no code), the Constitution's own term
("guarantee tier"), or a statement of design intent ("designed so
that"). One phrasing, "the system is built so that", was changed to
"designed so that" during this check. The architecture claims no
implementation, no selection, no executed genesis, no CPOC witness, no
certification and no edge; §8 says so in those words.

## 4. Reuse table against the Principal's direction

| Direction | Where it holds |
| --- | --- |
| Speedway owns investment semantics, evidence and lineage, evolution policy, budget authority, admission and capital rules | §6 opening paragraph and column 3 of every row |
| Existing engines remain replaceable; no custom swarm framework; no rebuilt commodity infrastructure | §6 opening paragraph; rows 1 and 2 name categories only; row 6 is the one minimal build, with its reason (the Paper Book's admission rules are investment semantics) |
| A runtime checkpoint alone does not establish lawful continuation | §5, the note after the Controls table, and row 2's acceptance criterion |
| Distinguish selected, candidate and deferred; present no candidate as a commitment; name products only with verified capability | Column 5 of every row; no product is named, and §6 says why |

## 5. Package contents

The manifest includes every document `architecture.md` and `README.md`
link to, every decision record with its admission text and amendment
notes, every pre-admission audit and re-audit, the four independent
audits unchanged, both author's checks, both handoffs, the plan and
the reference material including the Principal's design proposal
(`.docx`, with figures) at the Principal's direction. It excludes the
repository's agent router and git metadata and nothing else; no local
runtime data, cache, credential or scratch file exists in the
repository. The four independent audits were not edited in this round
(verified by `git diff` showing no change to them).

## 6. Not checked here

Whether the architecture is persuasive, whether a prospect would
understand it in ten minutes, and whether the design is correct. The
first two are the Principal's judgment; the third is the independent
reviewer's.
