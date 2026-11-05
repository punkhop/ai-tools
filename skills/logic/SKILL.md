---
name: logic
description: Resolve non-visual design decisions from a /spec output. For each open question, research evidence-based options, present them, capture the user's decision, and document each as an enforceable constraint. Second step of the spec → logic → design pipeline.
disable-model-invocation: false
---

# /logic — Resolve Behavioral Decisions

Takes a Design Spec from `/spec` and resolves every non-visual decision it raised. Outputs a DECISIONS.md file with each decision recorded as an enforceable constraint that `/design` later builds against.

The point: separate behavioral choices ("when the user clicks X, what happens?") from visual choices ("what does it look like?"). Resolve behavior first, then design pretty around it.

## Process

### Phase 0: Read the spec

```bash
ls ~/memory/specs/*.md | head
```

Ask the user which spec to work from if it's ambiguous. Read the chosen spec's "Open questions" section + any other behavioral ambiguities in the spec.

### Phase 1: Build the question list

For each open question, expand it into:
- **What's actually being decided** — make the ambiguity concrete
- **2-3 evidence-based options** — research how other apps in the domain handle it (WebSearch is fine; so is reading library docs)
- **Tradeoffs** — what each option gains and loses

If the spec has 5 open questions, you'll end up with 5-10 decisions to make (some questions branch).

### Phase 2: Interview

Use `AskUserQuestion`. One decision at a time. For each:

- **Question label**: short, like "Empty state"
- **2-3 options** with brief tradeoffs in the description
- Let the user pick "Other" for custom

Example:

```
Q: Empty state — what do new users see before they've added any data?
Options:
  - Onboarding card with a sample button (low friction; can feel patronizing)
  - Plain empty state with one "Add your first X" CTA (clean; less guidance)
  - Pre-seeded demo data the user can edit (most engaging; risks confusion about what's real)
```

### Phase 3: Write DECISIONS.md

Save to `~/memory/specs/YYYY-MM-DD-<slug>-decisions.md` (same slug as the spec).

```markdown
---
type: decisions
created: YYYY-MM-DD
feature: <slug>
spec: ~/memory/specs/YYYY-MM-DD-<slug>.md
status: resolved
---

# Behavioral Decisions: <Feature Name>

## Decision 1: <topic>
**Decided:** [chosen option]
**Why:** [reasoning the user gave or you inferred]
**Constraint for /design:** [the rule this implies — must be testable]

## Decision 2: <topic>
**Decided:** ...
**Why:** ...
**Constraint for /design:** ...

[... etc.]

## Out of scope
- [things explicitly excluded]
```

The **Constraint** line is the load-bearing part. It should be specific enough that a reviewer could check whether the design satisfies it. "Don't show the empty state with no CTA" is a constraint. "Make it user-friendly" is not.

### Phase 4: Hand off to /design

Tell the user: "Decisions at `~/memory/specs/YYYY-MM-DD-<slug>-decisions.md`. Run `/design` next to prototype against these constraints."

## Rules

- **Don't decide for the user.** Present options + tradeoffs, let them pick. The whole point of this step is *their* decisions, not yours.
- **Constraints, not preferences.** Every decision ends in a testable rule. "Use blue buttons" is too soft; "Primary CTA uses brand color, secondary CTA is outlined" is enforceable.
- **Research before asking.** Don't present made-up options. Look at how similar apps solve the same problem.
- **One decision at a time.** Don't batch — earlier decisions narrow later options.

## When to Use

- After running `/spec`, before running `/design`
- Anytime a spec is too vague to build from
- When you catch yourself making behavioral decisions in code without writing them down

## When NOT to Use

- Pure visual decisions (color, typography, layout) — those are `/design`
- When decisions are already locked — read the DECISIONS.md, don't redo it
