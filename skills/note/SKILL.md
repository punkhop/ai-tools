---
name: note
description: Write a dated markdown session note to ~/memory/sessions/. Use at the end of every discussion, before /clear, or whenever something worth remembering happened.
disable-model-invocation: false
---

# /note — the session note

Write one note for this session to `~/memory/sessions/`. Don't ask the user what to write — zoom
out and write it. Run `/note` LAST, after every other change in the turn, so the note describes the
finished state.

## Where it goes

- A note alone: `~/memory/sessions/YYYY-MM-DD-<topic>.md`
- A session that also made files (HTML pages, screenshots, proof): a folder
  `~/memory/sessions/YYYY-MM-DD-<topic>/` with `SESSION-NOTE.md` inside, next to those files.

`<topic>` is plain kebab-case words — `postgres-row-locks`, not `session-1`. If this session already
wrote a note today, **rewrite that same file whole** — never append bullets to it, never make a
second file for the same session.

## Front-matter (mandatory)

Auto-detect every field; never ask.

```yaml
---
created: 2026-10-21
type: session
project: dashboard        # git remote repo name, else basename of cwd, else "personal"
tags: [auth, postgres]    # 2-5 lowercase keywords — they make the note findable later
---
```

## Sections

1. **PURPOSE** — what this session was about, one sentence.
2. **DECISIONS** — what was decided and why. "Chose X over Y because Z." Decisions, not diffs.
3. **DISCOVERIES** — gotchas, constraints, things learned. Exact file paths, function names,
   error messages, numbers.
4. **WHAT GOT DONE** — concrete deliverables: files, features, fixes, links to any pages made.
5. **LEFTOVERS** — only if something is genuinely unfinished: one line each, specific enough that
   a fresh Claude can pick it up cold. If you use a task tracker, file them there first and link
   them here instead. A to-do that lives only in a note tends to get lost.

Write it as a narrative, not a changelog. Skip empty sections.

**Searchability matters.** QMD indexes these notes. "Fixed SIGHUP in session-save.sh worker" is
findable next month; "fixed a bug" is not.

## Last step — print the stamp

Finish by printing the save time and the clickable link (served by the files-server):

```bash
NOTE=~/memory/sessions/<the file>
echo "Note written $(date -r "$NOTE" +%H:%M) → $(~/.claude/bin/files-server url "$NOTE")"
```

End your reply with that line as a link: `[Note written 14:02](http://…)`. The time proves the note
was the last thing written; if it's earlier than the turn's last change, rewrite the note.

If the files-server isn't installed, print the absolute path instead.

## When not to use

Trivial sessions where nothing was decided or made — the transcript auto-export already covers
those.
