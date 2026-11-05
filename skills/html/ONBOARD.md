# ONBOARD — the first conversation, for Claude to run

**You are Claude. The `/html` skill is installed at `~/.claude/skills/html/` and `READER.md` is
still the blank template. Read this file before you build anything, and run the conversation below
before you start obeying the system.**

This system was built for one person over two days of hard rulings. It works. It is also tuned to
a reader who is not the person in front of you now. Your job in this first session is to **present
it, get their reaction, and reshape it to them** — not to start obeying it as shipped.

Budget about twenty minutes. The output is a filled-in `READER.md` and a first real page.

---

## Step 0 · Read, then look

In this order, all in `~/.claude/skills/html/`, before you say anything:

1. `SKILL.md` — the steps, in order
2. `report-method.md` — the method and the rules
3. `BLOCKS.md` — the shelf
4. `CUSTOMIZE.md` — which knobs exist

Then **open the examples and look at them yourself** — screenshot them the way `SKILL.md` step 5
does. They link the stylesheet relatively, so they render served or opened from disk. To give the
user a link: `~/.claude/bin/files-server url ~/.claude/skills/html/examples/system.html` if the
files server is installed; otherwise serve the folder:

```bash
cd ~/.claude/skills/html && python3 -m http.server 8181
# → http://localhost:8181/examples/system.html
```

Start with `examples/system.html`. Every block in the system is drawn there with its rules beside
it. You cannot present a visual system you have not looked at.

---

## Step 1 · Present it — six beats, out loud, no files

Tell them, in your own words, in about this order. Keep it short; the examples do the arguing.

1. **What it is.** A method for turning anything long into a page they open in a browser instead
   of a wall of text in a chat window. One stylesheet, no build step, no libraries.
2. **The core move.** Say the thing out loud in plain sentences first. That speech becomes *blocks*
   — cards, rules, numbers, drawings — never paragraphs. If a page has a paragraph longer than
   three lines, a block has not been drawn yet.
3. **The one rule that carries the rest — form follows function.** Every arrangement makes a claim.
   Arrows say "then". A rail says "happened". Nested boxes say "inside". A grid says "and". Say the
   claim out loud, and if the sentence is a lie, the shape is wrong. Having a block is never a
   reason to use it.
4. **Six kinds of page**, named by what the reader has to DO: decide, don't lose track, go find
   out, show me it works, help me understand, show me the actual screen.
5. **Questions are loud and in two places** — inline at the end of the section that makes them
   answerable, and indexed again at the foot so a skim misses none.
6. **You look at it before they do.** Screenshot the real render at desktop and phone width and
   actually look at the image. Every rule in this system exists because a page was rejected.

**Then send them the link to `examples/system.html` and stop talking.** Let them scroll. Their
first reaction to the real thing is worth more than anything else you will learn today.

---

## Step 2 · Say what is load-bearing and what is taste

Be straight about this — it is what makes the system theirs rather than borrowed.

**Load-bearing.** Change these and the system stops working:

- Say it out loud first; the speech becomes blocks, not prose
- Form follows function, and the connector test
- Size means importance · position means order · nesting means containment · color keeps its
  meanings
- One stylesheet; a new block is built into the sheet, never inline on one page
- The answer comes before the teaching, and a page answers once
- Look at the real render at both widths before serving

**Taste, and up for debate.** Every one of these is a default with a reason, not a law:

- Dark by default
- The four colors and the seven status words
- No emoji, no exclamation marks, US spellings, 12-hour time
- The measured register — genuinely one person's, and not portable
- Whether the six kinds of page need a seventh

Ask directly: **"Anything in the load-bearing list you disagree with?"** If they do, hear them out
before defending it. The list earned its place empirically, so you should be able to say which
failure produced each rule — but a rule that survives contact with a new reader is stronger than
one you defended by citing its author.

---

## Step 3 · The questions

Ask these in batches of two or three, not as a form. Every one has a default, so "just use the
defaults" is a complete answer and you should offer that up front.

**About them**

1. Who reads these pages — just you, or a team? What do you know cold, and what do you never read?
   *(This is the big one. "I don't read code" and "I do read code" produce different pages.)*
2. Desk, phone, or both? Dark or light?
3. What makes you close a tab?

**About the work**

4. Walk them through the six kinds — one sentence each, from `READER.md` §2 — and ask whether
   anything they regularly want is missing. *(These six are the starting set and they stay. The
   question is additions, not deletions: a seventh kind is a legitimate answer, and it needs a real
   recurring ask behind it plus its own answer-first block.)*
5. Do you have a component library, Storybook, or any screens already drawn? *(Most people do not,
   and that is fine. It means the first screen a page needs gets drawn as a real file in a folder of
   its own, and every later page frames it. Show them `examples/mocks/`.)*

**About delivery**

6. Where should pages get written, and how do you want to open them? A local server, a shared
   drive, a static host? *(Whatever it is, it has to end in a clickable link. A path they have to
   paste is a page they never read.)*

**About the sound**

7. Do you want your register measured? If they have a few hundred messages to you somewhere — chat,
   email, PR comments — offer to read them and report back what you find: sentence length, how they
   correct someone, whether they hedge, which plain words they use where you would use jargon. The
   shipped register is one person's and should not be inherited.

---

## Step 4 · Apply the answers

Fill in `READER.md` from what they said, and delete its first line (the `blank template` marker)
so `/html` stops offering this conversation. That file is the only place their answers live —
leave `report-method.md`, `BLOCKS.md` and `assets/report.css` alone unless they asked for a rule
change.

Then, only if they asked for it:

| They said | You edit |
|---|---|
| "Add a seventh kind of page" | the table in `READER.md` §2, then `report-method.md` §2 and `SKILL.md` step 2 |
| "Light by default" | `assets/report.css` §1 Tokens — swap which block is the default and which is under the toggle |
| "Different colors" | `assets/report.css` §1 Tokens, the four hue variables. Keep the four meanings |
| "I do read code" | `BLOCKS.md` §2, the evidence-pair NEVER line, which currently bans code as evidence |
| "Drop a rule" | the rule in `report-method.md`, and note in `READER.md` that it was dropped and why |

**Record every change you make with the reason they gave.** In six months the reason is worth more
than the change.

---

## Step 5 · Nothing to install

The skill is already in place at `~/.claude/skills/html/`, with the examples in `examples/` beside
it. Every page gets its own copy of `assets/report.css` in its folder (`SKILL.md` step 4), so pages
render served or opened from disk and never depend on a folder that might move.

---

## Step 6 · Build one real page today

**Do not end this session with the system installed and unused.** Ask for one real thing they were
going to have you write up anyway, and make it a page. Walk every step aloud so they see the method
work: the speech, the job, the blocks you picked and the ones you rejected, the screenshot you
looked at, the link.

Then ask the only question that matters: **what would you change?** Change it, in the sheet, that
same session. A system that improves the day it lands is a system they will keep.
