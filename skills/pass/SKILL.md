---
name: pass
description: Hand this worn-out thread to a fresh Claude that continues the SAME work. Writes a handoff doc, writes a /note, launches a successor thread in this same T3 Code project (same title plus a number) that archives this one. Use when the user says "/pass", "pass this off", or "hand this to a fresh Claude".
disable-model-invocation: false
---

# /pass — hand this thread to a fresh instance, then step aside

Context is full and the thread is getting dull. `/pass` moves the baton: it writes the handoff
doc, writes a session note, and launches a fresh Claude thread **in this same project** already
working on **this exact work**. The successor archives this thread after its first reply.

**`/pass` vs `/handoff`:** `/pass` = same work, this thread is done. `/handoff` = a different
idea goes to its own thread and you keep working here.

**Arguments:** $ARGUMENTS — optional focus. If empty, infer it.

## Non-negotiables

- **One command.** Never ask the user to run `/handoff` first — the doc is built in.
- **No focus question.** Infer from the conversation + git; use `$ARGUMENTS` verbatim if given.
- **Same title, plus a number.** `Team roles` → `Team roles 2`; `Team roles 2` → `Team roles 3`.
  Never a new name. Same project, never a new one.
- **Note before launch.** Launching is the last action; nothing runs after it.
- **Fire-and-forget.** Don't poll, message, or manage the successor.
- **Absolute paths everywhere** — the successor's cwd is its own.

## Steps

### 1. Preflight
```bash
WORKTREE=$(git rev-parse --show-toplevel 2>/dev/null)
BRANCH=$(git branch --show-current 2>/dev/null)
git log --oneline -8 2>/dev/null; git status --short 2>/dev/null | head -20
```
Load the T3 tools (deferred) with ToolSearch:
`select:mcp__t3-code__t3_thread_configuration,mcp__t3-code__t3_thread_launch,mcp__t3-code__t3_thread_read,mcp__t3-code__t3_thread_list`.
Call `t3_thread_configuration {}` — it returns this thread's `threadId` and title; both go in the
kickoff. If the tools don't exist, you're in a plain terminal: see **No T3 Code** below.

### 2. Write the handoff doc
`~/memory/handoffs/YYYY-MM-DD-<slug>.md` (slug = 1-3 plain words, kebabbed; add `-2`/`-3` if
taken today; create the folder if missing). A baton carries the WHOLE state:

```markdown
---
type: handoff
kind: baton
created: YYYY-MM-DD
worktree: [abs path]
branch: [branch]
---

# Baton: [the work in 5-8 words]

## Your first reply
Open with "Continuing <previous thread title>". If Open questions is not empty, re-ask them
first — same numbers, same words. Then state your job in plain English: what the user sees or
does, what happens today, what will be true when you're done. No file names or branch names.

## The job
[2-4 sentences — what this work is and why]

## Done when
[one observable result]

## What's next
1. [the very next action, concrete]
2. [then…]

## What's done
- [committed pieces, PRs]

## Open questions
[the user's unanswered questions, word for word with numbers — or "None"]

## Decisions made
- [decision + the user's reason, so nobody re-asks]

## Leftovers
- [anything noticed but not done — this doc is the record]

## Files changed
- [abs paths]

## How to verify
- [commands / pages that prove it works]

## Gotchas
- [non-obvious traps — or "None"]
```

### 3. Write the kickoff message
A short pointer at the doc, led by the job:
```
Continue this work: <the job in one sentence>. Next: <the very next action>.
You are "<this title> N" — keep that title, never rename it.
Read the full state first: <abs path to handoff doc>
Worktree: <abs path>  Branch: <branch>  Dev server: <running on port X / not running>
Rules from this session: <1-2 corrections the user made, each with its reason>
Predecessor: <this title> (threadId <id>). After your first reply, archive it:
t3_thread_organize {action: "archive", threadId: "<id>"}
(load it first: ToolSearch select:mcp__t3-code__t3_thread_organize).
```

### 4. Write the session note
Run `/note` (or write `~/memory/sessions/YYYY-MM-DD-<topic>.md` directly): what this session
learned, decided, and where it stopped. The handoff is for the next instance; the note is memory.

### 5. Tell the user, one line
"Passing this to **<title> N** in this project — it reads <files-server link to the doc> and
continues on <focus>. Session note saved. It archives this thread after its first reply."
(Link via `~/.claude/bin/files-server url <abs-path>`.)

### 6. Launch — the LAST action
- `t3_thread_launch {title: "<this title> <N>", message: "<kickoff>", workspaceStrategy: …}`
  - in a git worktree/repo: `{type: "existing_worktree", worktreePath: "$WORKTREE", branch: "$BRANCH"}`
  - otherwise: `{type: "root"}`
  - omit `projectId` and `modelSelection` — they inherit this thread's.
- No retry key: on an error or a lost reply, `t3_thread_list` for the title before launching again.
- Confirm with `t3_thread_read {threadId}` that its turn is running. Not running → tell the user
  what you saw; this thread stays.
- Running → stop. Don't archive this thread yourself; the successor does.

## No T3 Code (plain terminal)

Do steps 1-4 the same (skip the T3 tools and the archive line). Then end with a one-line paste
block for a new session, and tell the user: "Run `claude` in a new terminal (or `/clear` here)
and paste this."
```
cd <abs worktree> && claude "Continue this work: <job>. Read <abs path to handoff doc> first."
```
