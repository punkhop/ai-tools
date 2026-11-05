---
name: design
description: Build working prototypes from a /spec + /logic pair. Generate 3-5 parallel design variants, let the user pick a winner, then evolve from the chosen direction. Use after /spec and /logic. Outputs working code, not mockups.
disable-model-invocation: false
---

# /design — Parallel Design Exploration

Take a Design Spec + DECISIONS file and produce 3-5 working prototypes in parallel. The user picks a winner; you evolve from there.

The point: design by comparison, not by argument. Three variants in front of you decide what looks right faster than a paragraph describing one.

## Prerequisites

- A spec exists at `~/memory/specs/<slug>.md` (output of `/spec`)
- A decisions file exists at `~/memory/specs/<slug>-decisions.md` (output of `/logic`)

If either is missing, tell the user: "I need a spec + decisions first. Run `/spec` then `/logic`, then come back."

## Process

### Phase 1: Read inputs

Read the spec and the decisions file. Internalize:
- The problem + primary user (spec)
- The information hierarchy (spec)
- Every constraint from decisions

The constraints are non-negotiable — every variant must satisfy all of them. Variation happens in the visual + interaction layer, not in the behavior.

### Phase 2: Pick 3-5 design directions

Each direction should be visually distinct enough that a user could pick a winner without overthinking. Examples of directions:

- **Density**: dense table vs roomy cards
- **Navigation**: tabs vs sidebar vs single-page scroll
- **Density of motion**: still vs subtle vs prominent animation
- **Visual register**: editorial / structured / playful

State the directions to the user before generating:
"I'll generate 4 variants: [Direction A], [B], [C], [D]. Each will satisfy all constraints. Generate?"

Wait for go.

### Phase 3: Generate in parallel

Set up a working showcase directory inside the project's own folder:
```
<project>/showcase/<feature-slug>/
  ├── variant-a/
  ├── variant-b/
  ├── variant-c/
  └── variant-d/
```

Each variant is a working implementation in the user's stack (SvelteKit, Next, plain HTML+CSS+JS, whatever's local). Not a mockup — runnable code.

Generate them in parallel via the Agent tool, one agent per variant. Brief each agent with:
- The full spec + decisions
- Which direction they're embodying
- Where to write output
- A reminder that all constraints from decisions are mandatory
- The writing rules below, word for word — an agent that never saw them will break them

### Writing rules for every variant

These hold in every variant, whatever the direction:

- **Sentence-case headings** — "Account settings", not "Account Settings".
- **No eyebrow labels** — no small all-caps, letter-spaced caption over a heading or a group of controls. Set headings apart by weight and size instead.
- **No placeholder text in inputs** — a label above the box says what it is; the box ships empty. The only exception is a box with no visible label, like a search field.
- **No helper text under headings** — no subtitle or descriptive line restating the heading. If a heading needs explaining, write a better heading.

### Phase 4: Show the user

Once all variants are in, surface them:
- Each variant gets a link the user can click. If `~/.claude/bin/files-server` is installed, use `~/.claude/bin/files-server url <abs-path>` for an `http://` link; otherwise a `file://` markdown link to its directory
- A one-line caption per variant ("Variant A: dense table, no animation, focus on scannability")
- Don't pick a favorite yet — let the user look

### Phase 5: Pick winner + evolve

Ask the user which variant lands closest. Then:
- Read the winner's code
- Ask 1-2 questions about what to change ("keep the table density but use the sidebar nav from variant C")
- Generate a v2 of the winner with those changes

Repeat the evolution loop until the user says it's done.

### Phase 6: Promote

When the user is happy:
- Move the final variant into the actual codebase (out of `showcase/`)
- Delete the other variants
- Tell the user: "Final design is at [path]. Specs and decisions are still at [paths] for reference."

## Rules

- **Variants must be visually distinct.** Two near-identical variants waste time. If you can't articulate the difference in one sentence, you don't have two variants.
- **All constraints from /logic are mandatory.** No exceptions in any variant. Variation is in the visual + interaction layer only.
- **Working code, not mockups.** The user runs each variant in a real browser to compare. Static images don't capture interaction.
- **Don't argue for a favorite.** Until the user picks, you're neutral. State the tradeoffs each variant makes; let them decide.
- **Every link is clickable** so the user can open each variant directly without copying paths.

## When to Use

- After `/spec` and `/logic` are done, for a fresh feature
- When an existing feature needs a redesign and you want to compare alternatives
- When the user says "I don't know what it should look like" — generate variants and let them react

## When NOT to Use

- When the spec doesn't exist — run `/spec` first
- For a tiny isolated component (Button, Input) — overkill
- When the user has a clear visual reference already — just build that
