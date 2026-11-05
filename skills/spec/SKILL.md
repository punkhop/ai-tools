---
name: spec
description: Design interview + specification. Research the domain, interview the user about the desired user experience, and produce a structured Design Spec markdown file. Use when the user wants to specify a new feature, page, or app before building. First step of the spec → logic → design pipeline.
disable-model-invocation: false
---

# /spec — Design Spec Interview

Run a guided interview to produce a structured Design Spec for a new feature. The spec is the input to `/logic` (next) and eventually `/design` (the prototyping step).

The point: stop letting Claude jump straight to code. Build a spec first, get the user-experience decisions on paper, then implement.

## Process

### Phase 0: Research the domain

Before asking the user anything, take 60 seconds to understand the domain.

If the feature is "user auth," look at how other apps in the user's stack handle auth. If it's a dashboard, look at similar dashboards in major products. WebSearch is fine. So is reading documentation for the libraries the user already has installed.

Output a 3-bullet summary: "Domain has these conventions: A, B, C." Don't go deeper than that yet.

### Phase 1: The Interview

Use `AskUserQuestion` to ask one focused question at a time. Build options dynamically based on previous answers.

**Question 1: Problem statement**
"What problem does this feature solve, in one sentence?"
Options: build 2-3 from your domain research; leave Other for custom.

**Question 2: Primary user**
"Who is the primary user, and what state are they in when they reach this feature?"
Build options from the answer to Q1.

**Question 3: Core experience**
"In one sentence, what does the user *feel* when this works perfectly?"
This is the emotional core — surface it.

**Question 4: Inputs and outputs**
"What does the user bring in, what do they take away?"
Build concrete options based on the feature type.

**Question 5: States**
"What states can this feature be in? Empty, loading, populated, error, partial?"
Get every state on paper — most bugs hide in the unloved states.

**Question 6 (if applicable): Mobile behavior**
"How does this work on a phone? Same as desktop? Subset? Different flow?"

**Question 7: Inspiration**
"What apps or features do this well? What do you want to steal from?"

Stop asking when you have enough to write the spec. Usually 5-7 questions.

### Phase 2: Write the spec

Save to `~/memory/specs/YYYY-MM-DD-<feature-slug>.md` (create `specs/` if it doesn't exist).

```markdown
---
type: spec
created: YYYY-MM-DD
feature: <slug>
status: drafted
---

# Design Spec: <Feature Name>

## Problem statement
[One sentence from Q1]

## Primary user + state
[From Q2]

## Core experience
[The one-sentence feel from Q3]

## Information hierarchy
[Top-to-bottom or visual priority — what does the user see first, second, third?]

## User actions
[What the user can do, ordered by frequency or importance]

## States
- **Empty**: [what shows]
- **Loading**: [what shows]
- **Populated**: [what shows]
- **Error**: [what shows]
- **Edge case A**: [what shows]

## Mobile behavior
[Same / different / subset, with specifics]

## Inspiration / pattern references
- [App or feature] — [what to steal]

## Open questions for /logic
- [Anything you couldn't resolve in the interview]
```

### Phase 3: Hand off to /logic

Tell the user: "Spec is at `~/memory/specs/YYYY-MM-DD-<slug>.md`. Next step: run `/logic` to resolve the non-visual decisions (state shape, data flow, edge cases). Then `/design` to prototype."

## Rules

- **One question at a time.** Don't batch — each answer informs the next question.
- **Plain English.** Don't ask "what's the data model" — ask "what does the user bring in, what do they take away."
- **Don't write code.** The spec is the artifact. Code comes in `/design`.
- **Don't skip Phase 0.** Five minutes of domain research saves an hour of arguing about details.

## When to Use

- New feature or page you're about to build
- Existing feature that's gotten messy and needs a redesign
- When the user says "I want to make X but I'm not sure how" — start here, not at the code

## When NOT to Use

- Bug fixes — overkill
- Tiny changes to existing patterns — just do them
- When the spec already exists — read it, don't redo it
