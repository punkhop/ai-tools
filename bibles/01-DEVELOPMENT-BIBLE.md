---
type: bible
version: 2026.11
description: Universal engineering rules for personal projects — code structure, testing, logging, errors, git, naming
priority: critical
always_load: true
quick_rules:
  - Mature libraries before building from scratch — never hand-roll what a proven library does
  - Simplest complete version first, layer by layer — 200 lines that could be 50 get rewritten as 50
  - Success criteria before code — a check Claude can run, then build until it passes
  - A found bug gets the smallest fix + one real test — never a tooling launch
  - Scope in size, never in time — no duration estimates, ever
  - Files under 200 lines, split at 300, never hit 500
  - No abstractions until 3 uses
  - File headers are business cards (what, where it fits, what it connects to)
  - Structured logging from day one
  - Exhaustive functional tests ship with every feature
  - Tests run the app — a guard that scans source needs the owner's explicit go
  - Scale the fix to the finding — smallest edit first, machinery never by default
  - Dead code is a lie — delete it
  - Errors are written for the human owner, not programmers
status: active
---

# Development Bible

> Universal engineering rules for all of your personal projects.
> Every Claude session MUST read this before writing or modifying code.
> This code is maintained by AI, owned by a human who may or may not read code.

---

## Prime Directive

You (Claude) write the code. The human will rarely if ever debug it. Every decision optimizes for:

- **Immediate comprehension** by any Claude instance opening any file for the first time
- **Zero-maintenance reliability** — things don't break unattended
- **Log trails obvious enough** that a non-coder can paste them and get help
- **Consistency across every project** — the codebase feels like one person wrote it

---

## Scope Check (MANDATORY Before Writing Code)

Before proposing ANY new feature, file, or significant change:

1. **What** — one sentence
2. **Files** — which files touched, with paths
3. **Lines** — approximate lines of new code
4. **Pattern** — which existing file does this follow?
5. **Could it be simpler?** — flat file, bash one-liner, 10 lines instead of 50?

Show the user. Wait for go. **Never estimate duration.** Not hours, not days, not "quick fix." Scope in size (files, lines, patterns), never in time. Claude cannot reliably estimate effort and must not try.

**When the human is not in the loop** — a background worker, an autonomous run — the scope check cannot wait for go, so its default hardens: implementation within established patterns proceeds; anything that would create *machinery* (a guard, scanner, script, dashboard, ratchet, proof harness) defaults to **no**. Ship the product change, name the idea in the handoff.

---

## Build Order

**Mature, established libraries before building from scratch.** For anything real — auth, dates,
image handling, parsing, sync — pick the boring, proven library. The "could I write this in under
50 lines?" test (Dependencies, below) decides only the trivial cases; never hand-roll what a
mature library already does well.

**Simplest complete version first, then layer by layer.** v1 is the simplest version that works
end-to-end. Each layer lands working before the next starts. No speculative flexibility, no
configurability nobody asked for, no abstractions for single-use code. If you wrote 200 lines and
50 would do, rewrite it as 50.

**Success criteria before code.** Before building, state what "working" looks like as a check
Claude can run — a test, a visible behavior in the running app. Then build until it passes.
Declarative beats imperative: Claude loops well against a finish line, badly against a vibe.

**Every changed line traces to the request.** Don't improve adjacent code, comments, or formatting
mid-task. Fix-at-source still applies to real bugs found mid-task — but the fix is scoped to the
bug, not a renovation around it.

## When a Bug Is Found

Build the product, test it, then fix bugs — don't launch a giant effort to fix every tiny thing
each time something turns up.

1. **Smallest fix at the source, this turn.** If the same bug visibly sits in sibling spots, fix
   those in the same commit.
2. **One test that proves it** — a test that runs the app and fails on the old code. Not a guard,
   not a scanner (see Testing, below).
3. **Move on.** A finding never launches tooling, a sweep, a mission, a dashboard, or a new
   machine. Fix the bug, not the class of all imaginable bugs.

---

## The Rules

### Structure & Organization

**Readable in one screen.** Files under 200 lines. Split at 300. Never hit 500. A new Claude session should understand any file without scrolling.

**One file, one job.** Every file does one thing. Its name says what. If you can't describe a file without using "and," split it.

**Same folder skeleton everywhere.** Every project uses the same bones:

```
src/            → always (code lives here)
  lib/          → always (shared modules; server/ for server-only)
  routes/       → if using SvelteKit / Next / similar (pages and API endpoints)
tests/          → always (mirrors src/ structure)
scripts/        → if needed (standalone bash/python)
config/         → if needed (YAML settings)
data/           → if needed (SQLite, local state)
```

Flat until a directory has 7+ files, then subdirectories by domain. Shared code lives in purpose-named directories under `lib/` (`lib/stores/`, `lib/services/`, `lib/types/`). Every file in those directories is named by domain — never grab-bag names like `utils.ts`, `helpers.ts`, or `misc.ts`.

**Files are features.** If it can be a markdown, YAML, or text file instead of code, it should be. Config is YAML. TODOs are markdown. Settings pages only when the user explicitly asks.

**Patterns over invention — for code structure.** When building something new, find the most similar existing thing and copy its skeleton. Clone and adapt, don't invent from scratch. The codebase grows by replication. **Design is unconstrained** — creative UI, consistent bones underneath.

### Naming & Readability

**Name everything like a headline.** `getUserTicketsByEventId()` not `getData()`. `analytics-dashboard.svelte` not `page.svelte`. `FAILED_TO_FETCH_INSIGHTS` not `ERROR_3`. A non-coder scanning file and function names should understand what the system does.

**Code reads like prose.** Every variable name tells you what it holds. Every function name tells you what it does. No single-letter variables. No abbreviations. No cleverness.

```typescript
// No:
const r = d.filter(x => x.s === 'a' && x.t > Date.now() - 86400000);
// Yes:
const oneDayAgo = Date.now() - ONE_DAY_IN_MS;
const activePostsFromLastDay = allPosts.filter(post =>
  post.status === 'active' && post.createdAt > oneDayAgo
);
```

**Magic numbers don't exist.** Every number is a named constant. `MAX_RETRY_ATTEMPTS = 3`, not a bare `3` in a conditional.

**Comments explain why, code explains what.** If code needs a comment to explain what it does, rename the code. Comments exist only for decisions a future Claude session can't infer from the code itself.

### File Headers

Every code file starts with a brief header block — what it does, where it fits, what it connects to:

```typescript
// Fetches Mailchimp campaign data and stores daily metrics in SQLite.
//
// Part of the analytics pipeline. Called by the daily scheduler.
// Depends on: mailchimp-auth.ts for token management, storage.ts for database writes.
```

Three to four lines. A business card, not a novel. A new Claude session reads headers to orient itself without reading logic.

### Quality & Craftsmanship

**Small and correct, not fast and sloppy.** Every feature ships at minimal scope — the simplest version that works. But "small" never means cutting corners on structure. A 30-line feature follows every rule in this bible: naming, headers, tests, logging, error handling. Scope is minimal. Standards are not. v1 does less — it doesn't do it worse.

**No abstractions without three uses.** Don't create a helper for a pattern you've seen once. Write it inline. Extract on the third occurrence.

**No half-finished work in the codebase.** If a feature isn't done, it doesn't exist in the code. No commented-out drafts, no `// TODO: implement`, no empty stubs. Main branch is always a working product.

**Dead code is a lie.** Unused functions, commented-out blocks, stale TODOs — delete them. They mislead future Claude sessions. Git has the history.

**No invented formats.** Use markdown, YAML, JSON, SQL, or bash. Never invent a DSL or custom syntax.

**Fix it now, at its source.** Hit a bug, drift, or stale value mid-task → fix it this turn, at the file that produces it — never a patch at the call site. "Flag it," "file it," "worth fixing later" all mean *lost*; a deferred fix is a bug that now merely *feels* handled, which is how a codebase ends up 70% working and striated with one-offs. Fixing now and fixing at the canonical home are one move, not two. Only honest defer: the correct fix needs a fact you'd otherwise fabricate — name the missing fact, don't invent it.

### Infrastructure & Portability

**Boring infrastructure, beautiful interface.** Databases, file formats, deployment — the most proven, portable, standard options. The UI — premium and modern. SQLite stores the data. The frontend framework of your choice makes it beautiful.

**No lock-in. Ever.** Data in open formats (SQLite, YAML, markdown, JSON). Sync is file-based. If any service disappears tomorrow, migration is manageable, not catastrophic. No proprietary formats, no vendor-specific APIs without a swappable wrapper.

**Security by default.** Prepared statements for every query. Input validation at system boundaries. API keys in environment variables, never in code. Dependencies audited before adding. Good habits now mean ready for the public later.

### Visual State Conventions

**Opacity = state.** Use consistent opacity levels to communicate status across every project:

- 100% — confirmed, active, primary
- 70% — invited, pending, secondary
- 50% — disabled, inactive, muted

**Color carries meaning.** Colors are semantic, not decorative. Green means success/active. Red means destructive/error. Yellow means warning/pending. Follow the project's design system for exact values, but the meaning is universal.

---

## Logging

Structured logging from day one. Not optional. Not "add later." The app should be able to explain itself.

- Every module logs its name: `[watchdog]`, `[scheduler]`, `[storage]`
- Log at boundaries: entry with key params, exit with result summary
- Log errors with full context: what was attempted, what failed, inputs
- Format: `[module] action: detail` — parseable by grep
- Never log secrets, tokens, or full request bodies

```
[scheduler] Starting daily fetch cycle
[content]   Selected 3 items from queue
[api]       Calling external service...
[api]       Got 200 OK, 247 records
[storage]   Wrote 247 rows to insights table
[scheduler] Next run scheduled for 6 hours from now
```

When something breaks, the log shows exactly where the story stopped. No code reading required. If you ask "what happened last night?" the logs tell the full story without calling Claude.

---

## Testing

**Tests are the immune system. Never skip them. Never write smoke-only tests.**

- Tests ship with every feature. No exceptions. No "add later."
- **Exhaustive functional tests.** Given this input, does it produce exactly this output? Given this edge case, does it handle it? Given bad data, does it fail correctly?
- The bar: if Claude changes something and tests still pass, the app still works correctly. If that's not true, there aren't enough tests.
- Tests mirror source structure: `src/lib/watchdog.ts` → `tests/lib/watchdog.test.ts`
- Test behavior, not implementation. Not "does this button have the right class" — does the feature actually work?
- **A test runs the app's code and checks what comes back. A guard reads the repo's own source and polices how it's written** — greps files, walks the tree, asserts about text shapes. Only the first kind counts as a test, and only the first kind is mandatory. **Never write a guard unprompted** — a guard is proposed via scope check and exists only on the owner's explicit go, and only for failures eyes can't see (wrong-mode-only colors, unreachable empty states, unattended money, a test the suite never runs). The measurement behind this, from one real project: 20 unprompted guards, 5,017 lines, zero ever caught anything, 22 commits spent repairing three of them.
- No mocks for things you own — use the real module.
- Tests run with one command from repo root.
- Claude should be able to refactor with confidence because the tests catch any mistake.

---

## Dependencies

**Reviewed like hires.** Every dependency is a person you're trusting with your project's future.

- Before adding: Could I write this in under 50 lines? If yes, write it.
- Check: actively maintained? Bus factor above 1? Smaller alternative?
- Prefer zero-dependency or single-purpose packages over Swiss-army-knife libraries.
- Dead deps are debt. Track what's actually imported.
- When justified, note why in the commit message so future sessions don't re-litigate.

---

## Error Handling

**Errors are written for the human owner, not for programmers.**

- Bad: `SQLITE_CONSTRAINT: UNIQUE constraint failed: posts.snap_id`
- Good: `[mailchimp] This campaign was already imported (duplicate detected) — skipping`

Rules:
- **Let it crash with a clear message.** No silent swallowing.
- **Retry only at system boundaries** — HTTP calls, browser automation, external APIs.
- **Internal code: fail fast, fail loud.** Impossible state? Throw immediately.
- **Every error includes:** module name, what was attempted, what went wrong.
- The user should be able to act on an error message or at least understand it without Googling.

---

## Code Style

### TypeScript
- Strict mode. No `any`. No `@ts-ignore`.
- Functions over classes. Named exports over default exports.
- Functions under 30 lines. Split if longer.
- No barrel files (`index.ts` re-exporting everything).
- All new files TypeScript (`.ts`, `.svelte.ts`), never JavaScript.

### Svelte (if you're using it)
- Svelte 5 runes (`$state`, `$derived`, `$effect`). No legacy stores.
- Components under 150 lines. Split if larger.
- Props interface at top of script block.

### SQL (SQLite)
- WAL mode for personal tools.
- Prepared statements always. Never string-interpolate values.
- One query per function. Function named after what it returns.
- Migrations always additive. Add columns, rename columns, add tables. Never drop tables or delete columns with data. Data is sacred.

### Bash
- `set -euo pipefail` at the top.
- `python3` for JSON construction. Never bash string interpolation for JSON.
- Each check is a function named after what it checks.

---

## Naming Conventions

### File naming (frontend projects)

| Type | Convention | Example |
|------|-----------|---------|
| Components | PascalCase | `EventCard.svelte` (or `.tsx`) |
| Stores | camelCase + `Store` suffix | `analyticsStore.svelte.ts` |
| Services | domain + `.service.ts` | `mailchimp.service.ts` |
| Types | camelCase + `.ts` (in `lib/types/`) | `calendar.ts` |
| Constants | camelCase + `.ts`, values UPPER_SNAKE_CASE | `MAX_RETRY_ATTEMPTS` |
| Validation | domain + `-validation.ts` | `ticket-validation.ts` |
| Tests | same name + `.test.ts` (never `.spec.ts`) | `EventCard.test.ts` |
| Route dirs | kebab-case | `account-settings/` |

### Import ordering

```typescript
// 1. Framework (Svelte/Next/React)
import { onMount } from 'svelte';
import { goto } from '$app/navigation';

// 2. External packages
import { z } from 'zod';

// 3. Lib imports
import { analyticsService } from '$lib/services/analytics.service';
import type { InsightsData } from '$lib/types/analytics';

// 4. Relative imports (same feature)
import MetricsCard from './MetricsCard.svelte';
```

### Store conventions
- One store per feature/domain. Name describes the STATE, not the page.
- Stores don't import from other stores (prevents circular deps).
- Page-specific UI state (sidebar open, active tab) = local `$state()`, not a store.

### Service conventions
- One service per API domain: `mailchimp.service.ts`, `analytics.service.ts`
- All API calls for that domain live in its service.
- Never version in filenames (`mailchimp-v2.service.ts` is wrong — update the original).

---

## Git

- One logical change per commit.
- Message says what and why in one sentence. Not "updated stuff." Not "fixes."
- Never commit to main directly. Always branch.
- Git history reads like a timeline of the project's evolution.

---

## How Claude Works With the Human

**Claude proposes, the human disposes.** New patterns, new files, new dependencies → scope check, wait for approval. Implementation within established patterns → just do it.

**Every session leaves the codebase better documented.** If Claude discovers something undocumented — a quirk, a dependency, a reason — it writes it down. Knowledge accumulates, never evaporates.

**Search memory first.** Before making a judgment call, check memory search (QMD, if installed) and this bible. "Have we solved this before? Is there a rule? Did a previous session leave a note?" Don't reinvent patterns established three sessions ago.

**The codebase has no secrets.** Not API keys — those stay in env vars. But logic, structure, dependencies — nothing hidden or implicit. Every relationship is visible. A new Claude session with zero context can trace any feature from UI to database by following obvious breadcrumbs.

**One-paragraph README per project.** What it does, who it's for, how to run it. Three sentences max. A stranger could understand it.

---

## Anti-Patterns

| Temptation | Why it's wrong | Do this instead |
|-----------|---------------|-----------------|
| Custom DSL/parser | Debug it forever | TypeScript, bash, SQL |
| State machine | Derive state from data | Keep raw, derive everything |
| Abstraction "for later" | Future never comes as planned | Build for today only |
| Config UI for rare settings | Hundreds of lines for biannual changes | YAML is the UI |
| Retry/queue system | `curl --retry 2` is enough | Fail, log, try next cycle |
| Custom sync system | File sync tools exist | Use Syncthing/Dropbox/rsync |
| `utils.ts` / `helpers.ts` / `misc.ts` | Junk drawer names | Name by domain: `dateFormatting.ts`, `currency.ts` |
| Silent `try/catch` | Hides bugs | Crash or log and rethrow |
| Time estimates | Claude can't estimate effort | Scope in size (files/lines) |
| Smoke-only tests | Proves nothing | Exhaustive functional tests |
| Half-built stubs | Misleads future sessions | Ship complete or don't commit |
| Vendor lock-in | Trapped when things change | Open formats, swappable wrappers |
| "Flag it / file it for later" | Deferred = lost = silent rot | Fix at source, same turn |
| Guard that scans source for style | Never catches anything; eats repair commits | Hold style rules by eye + an always-on rule |
| Hand-rolling what a mature library does | Debug it forever, alone | Boring proven library, thin wrapper |
| Machinery in response to a finding | A finding is not a mandate to build | Smallest edit to existing files, same turn |
| A check with no named real failure | Speculative defense = dead weight | Name the failure it would have caught, or skip it |

---

## When In Doubt

Ask: **"What would the bash one-liner version look like?"**

If the one-liner solves 80% of the problem, that's your v1. Build the small, correct version. Every rule followed. Then improve if the user asks for more.
