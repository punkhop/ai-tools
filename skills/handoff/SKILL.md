---
name: handoff
description: Throw a tangent into its own fresh T3 Code thread. Writes a handoff doc, launches a new thread (short name) already working on it, and you keep working here. Use ONLY when the user says "/handoff". NEVER suggest it.
disable-model-invocation: false
---

# /handoff — throw a tangent into its own thread

**Never suggest this skill.** Only run it when the user types "/handoff". Never say "this is
getting long" — the user decides.

The user is mid-thread on one thing and has a *different* idea to chase without losing their
place. `/handoff <idea>` writes a short handoff doc, launches a fresh top-level T3 Code thread
already working on it, and **this thread keeps going**.

**`/handoff` vs `/pass`:** `/handoff` = a different idea, you keep working here. `/pass` = the
same work moves to a fresh thread because this one is spent.

**Arguments:** $ARGUMENTS — the tangent. If empty, infer the latest divergent idea.

## Non-negotiables

- **You keep working.** The new thread runs in the background. Report one line, then resume.
- **A visible thread, not a subagent.** Use `t3_thread_launch`, never the `Agent` tool.
- **Fire-and-forget.** Don't track, poll, or message the new thread.
- **Short name.** Title is lowercase, 1-3 plain words (`sms retry`, `dark embed`). The doc
  filename kebabs the same words.
- **No focus question.** Infer it; don't interrupt the user.
- **Absolute paths everywhere** — the new thread's cwd is its own.

## Steps

### 1. Preflight
```bash
WORKTREE=$(git rev-parse --show-toplevel 2>/dev/null)
BRANCH=$(git branch --show-current 2>/dev/null)
```
Load the T3 tools (deferred) with ToolSearch:
`select:mcp__t3-code__t3_thread_launch,mcp__t3-code__t3_thread_list,mcp__t3-code__t3_project_list`.
If they don't exist, you're in a plain terminal: see **No T3 Code** below.

### 2. Write the handoff doc
`~/memory/handoffs/YYYY-MM-DD-<slug>.md` (slug = the title kebabbed; add `-2`/`-3` if taken
today; create the folder if missing). Lean — the idea and a starting point, not a project dump:

```markdown
---
type: handoff
kind: tangent
created: YYYY-MM-DD
from_worktree: [abs path, or "none"]
from_branch: [branch]
---

# Tangent: [the idea in 5-8 words]

## Your first reply
Before any work, state your job in plain English: what the user sees or does, what happens
today, what will be true when you're done.

## The idea
[2-4 sentences — what to investigate or build, and why]

## Done when
[one observable result]

## Where it came from
[1-2 sentences of context from the parent thread]

## Where to start
- [first concrete move — a file, a repo, a question]
- [needs its own branch? make one yourself]

## How to end
- Run `/note`. List anything left undone under a "Leftovers" heading in this doc.

## Gotchas
- [non-obvious traps — or "None"]
```

### 3. Launch the thread
- `t3_thread_launch {title: "<1-3 words>", message: "<kickoff>", workspaceStrategy: {type: "root"}}`
- Kickoff message:
  ```
  Your job: <the idea in one sentence>.
  Read the brief first: <abs path to handoff doc>
  You run on your own; nobody is tracking you. If it needs its own branch or worktree, make one.
  First reply, before any work: state your job in plain English.
  ```
- Omitted `projectId` = this project; omitted `modelSelection` = this thread's model. If the idea
  clearly belongs to another repo, find its project with `t3_project_list` and pass that
  `projectId`.
- Want it isolated from this checkout? Use `{type: "worktree", baseRef: "main", branch: "<new-branch>"}`
  instead of `root`.
- No retry key: on an error or a lost reply, `t3_thread_list` for the title before launching again.

### 4. Report one line, then resume
"Threw `<idea>` to its own thread **<title>** — it's reading <files-server link to the doc>.
Back to what we were doing." (Link via `~/.claude/bin/files-server url <abs-path>`.)

Then go straight back to the original work. Don't end, don't manage the new thread.

## No T3 Code (plain terminal)

Write the doc (step 2) the same way, then give the user a one-line paste for a second terminal
and keep working here:
```
cd <abs worktree> && claude "Your job: <idea>. Read <abs path to handoff doc> first."
```
