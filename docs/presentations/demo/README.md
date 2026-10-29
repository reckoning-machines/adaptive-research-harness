# Research story demo

Status: **PRESENTATION DEMO — NOT THE SYSTEM**

`adaptive-research-harness-research-story.html` is a self-contained research story
in nine scenes for a portfolio manager and a CTO, one visual per scene:
an agent spots selling after volatility spikes, sets up two tests on
existing tools, sees a synthetic pattern and the trade lose after costs,
drops the trade and tests a narrower one on fresh data, proposes a
research method that checks costs first, compares both methods on the
same three tasks, has the change independently checked and funded by
the PM, continues with the narrower trade pending a paper
allocation, and closes on a text-only conclusion. Every human act is
labelled "(human)" in scene copy, diagram labels, Details and the
evidence record, so that routine autonomous research within an
existing grant stays distinct from a person approving new funding or
capital. The underlying objects, evidence record, budget accounting
and approvals are kept behind one "Details" button. It was authorized
as presentation-demo code only. It implements nothing of Adaptive Research Harness,
governs nothing, selects no harness or vendor, and every number in it
is synthetic.

## Open it

Double-click the file, or drag it into any current browser. It needs no
installation, server, network connection or account. The opening
screen states the product and has one Play button, with the Adaptive Research Harness name appearing once the story starts. Play runs the story in
about three minutes. Once started, Pause, Previous and Next sit at the bottom:
Pause holds the current scene for discussion, Previous and Next move
between complete scenes. Autoplay ends on the conclusion and leaves it
on screen, with Replay and Previous available.

- Space pauses and resumes. Arrow keys change scene. The dots at the
  bottom jump to a scene.
- "Details" opens the evidence record, the budget and approvals, and
  the complete research map (methods, hypotheses and strategies with
  their status, lineage and notes) as of the current moment. Escape
  closes it.

To open at a given moment, add `#t=` and a number of seconds to the file
address, for example `adaptive-research-harness-research-story.html#t=40`. Adding
`#play` opens the story already playing from the start.

## Edit it

The file is its own source: embedded CSS, JavaScript and SVG, no build
step. The story is the `SCENES` list near the top of the script, one
entry per scene with its start time, headline, supporting sentence, the
steps that change the underlying state (at offsets from the scene
start) and `settle`, the offset at which the visual has finished
moving. Each scene's drawing is the matching function in `VISUALS`. The
state at any moment is rebuilt by replaying every step up to that
moment, so navigation, autoplay and Details always agree. `T_END` is
the running time. All visible copy is plain ASCII. The chart data is
generated once at load from fixed formulas, so it is the same on every run.

## Historical source

`new_speedway_research_story.html` is retained byte-for-byte at the hash
named in the feasibility audit. It is an archived presentation source, not
the current demo. Its ambiguous synthetic-standing and registration labels
are corrected in the current copy. Neither copy implements the core.
