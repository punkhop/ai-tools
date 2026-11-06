---
name: status
description: Catch the person up on any project they are working on — what it is, where it stands, what changed lately, what is unfinished and what is theirs to decide — in plain words, no code. Reads the project's own history and the memory folder's notes, never just this chat. Use when someone types /status, /status <project>, or asks "where are we", "catch me up", "what's the status of", "where did we leave off".
---

# /status — catch me up on a project

The person builds things with Claude and does not read code. They come back to a project after a
day, a week, a month, and need the hospital shift handoff: what this is, how far it got, what
moved, what is stuck, what is on them. This skill reads the project and says that, plainly.

Never answer from this chat's memory alone. The point is that the chat's picture is stale; the
project's files and notes are the truth.

## 1 · Which project

- `/status <name>` → find it. Try, in order: a folder by that name under the current folder, under
  `~` (one or two levels: `~/<name>`, `~/*/<name>`, `~/dev/<name>`, `~/projects/<name>`,
  `~/Documents/<name>`), then a match among session-note `project:` fields in
  `~/memory/sessions/`. Several matches → ask which, once, listing them.
- `/status` alone → the current folder. If it is the home folder or holds no project (no git, no
  code, no notes naming it), ask which project, offering the 3 most recent `project:` names from
  `~/memory/sessions/` if that folder exists.

## 2 · Read — every source that exists, quietly

Run what applies; skip what doesn't exist without mentioning it. Pipe long output to a file and
read only what matters.

```bash
P=<the project folder>
cd "$P" || exit
# What it is
ls; head -40 README* 2>/dev/null; head -30 CLAUDE.md 2>/dev/null
cat package.json 2>/dev/null | head -20      # or pyproject.toml, Cargo.toml, … whatever is there
# What changed and what is unsaved
git log --since='30 days ago' --date=relative --pretty='%ad · %s' 2>/dev/null | head -25
git log -1 --date=relative --pretty='last change %ad' 2>/dev/null
git status --short 2>/dev/null | head -20
git branch --sort=-committerdate 2>/dev/null | head -5
git rev-list --left-right --count @{u}...HEAD 2>/dev/null   # behind / ahead of the online copy
git remote -v 2>/dev/null | head -1
```

- **The memory folder** (only if `~/memory/sessions` exists): the newest notes about this project.
  Match on the `project:` front-matter line or the folder name in the file name:
  `grep -l "project: <name>" ~/memory/sessions/*.md ~/memory/sessions/*/SESSION-NOTE.md 2>/dev/null`,
  newest 3-5 by date. Read their decisions and leftovers first. Also any brief in
  `~/memory/handoffs/` naming the project, and any `/spec` files in `~/memory/specs/` for it.
- **Memory search** (only if the `qmd` tools exist): one search for the project name, to catch
  notes that named it in other words.
- **Online** (only if `gh` is installed and signed in, and the remote is GitHub):
  `gh pr list --limit 10` and `gh issue list --limit 10`, so open work counts.
- **Unfinished work in the code**: `git grep -n -E "TODO|FIXME" | head -15` — read them, keep only
  the ones that describe something a user would notice.
- **Does it still run?** Only if it is quick and harmless: the project's own test command (from
  `package.json`, a Makefile, the README). Never start a server, deploy or install anything for a
  status check. Skip when there are no tests.

## 3 · Decide what is true

- **Built vs designed vs idea.** Built = code that runs, saved in the project. A prototype, a spec
  or a plan is designed, not built. Say which, flat. "Have we built anything?" always gets a
  straight answer in the first lines.
- **Unsaved work** (uncommitted changes, commits not yet online) is a fact worth saying: work that
  only lives on this computer can be lost. Offer to save it.
- **Failure is a fact**: tests failing, a note that says something broke, work abandoned halfway.
  Say what, no apology, no drama.
- **Time words, not dates**: "last touched 3 weeks ago", not a timestamp.

## 4 · The reply

Follow the installed reply format (`~/.claude/ai-tools/rules/reply-format.md` if it is there).
The handoff shape, nothing else:

1. **Head** — `Project · where it is in a few words`, then the state: `✓ Done` if nothing is
   open, `? Needs you` if something is theirs to decide, `○ Waiting` if it waits on something
   outside.
2. **What it is** — one sentence, in the user's words: what the thing does and for whom.
3. **Where it stands** — up to 5 one-line bullets with a symbol each: ✓ works · ◐ half done ·
   ○ not started · ✗ broken. The first says built / designed / idea.
4. **Lately** — up to 5 bullets of what changed, newest first, described as what a user would
   see ("the shopping list now merges duplicates"), never commit messages pasted raw.
5. **Unfinished** — what is left, from the notes' leftovers, unsaved work, open PRs and TODOs.
   Skip the section if nothing is.
6. **Links** — the project folder, the newest notes, any open PR by its title, any prototype or
   page. Each a word carrying its link: `~/.claude/bin/files-server url <abs-path>` when that file
   exists (it opens on their phone too), otherwise the full path.
7. **Next** — one line: what you would do next and who does it. Then, only if something is
   theirs to decide, numbered questions, each with **My call**, last.

No code, no file listings, no commit hashes, no branch names, no counts that change nothing.

### Where it shows

- **T3 Code with the Chat pages piece** (`mcp__t3-code__html_render` exists and
  `~/.claude/ai-tools/chat/README.md` is there): read that guide and draw the reply as one chat
  page — `k-head` with the head line, a `<p>` for what it is, a grouped `k-head` list for where it
  stands, `k-links`, then `k-qs` if there are questions. A status check writes no note, so never
  the green `ok` bar: end on `needs` when there are questions, otherwise
  `<k-status s="do">Your turn · the next step in a few words</k-status>`. Preview, then render.
- **A big project with Report pages installed** (`~/.claude/skills/html/SKILL.md` exists) and more
  than fits in a short reply (several parts, a long history): make the full status page with
  `/html`, give its link first, and keep the chat reply to the head line and the questions.
- **Anywhere else** (terminal, the Claude desktop app's Code tab): plain markdown in the shape
  above.

## 5 · After the reply

- Offer the obvious next step in one line: save unsaved work, pick up the top leftover, or answer
  the questions. Do it only when they say so.
- Don't write a session note just for a status check; a status changes nothing.
