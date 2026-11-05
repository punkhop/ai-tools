<!-- blank template: ONBOARD.md fills this file in, then deletes this line -->
# Your reader — the one file this system is tuned to

Everything else in `~/.claude/skills/html/` is the system. **This file is you.** The method, the blocks and the
stylesheet never need editing to fit a new person; this file does.

Fill it in during onboarding (`ONBOARD.md` walks the conversation). Until it is filled in, the
system runs on the defaults noted under each heading, which are sane but not yours.

---

## 1 · Who reads these pages

> One named person, or one tight audience. Not "stakeholders."

- **Name / role:**
- **What they know cold:**
- **What they never read:** *(code? SQL? JSON? raw logs? name it — the page must not lean on it)*
- **How they read:** *(desk at 1440? phone in bed? both? dark or light?)*
- **What makes them close the tab:**

**Why this matters:** every rule downstream is a rule about this person. "No code as evidence" is
correct for a reader who does not read code and wrong for one who does. Answer honestly, including
"they do read code" — the system bends.

*Default if blank:* a smart non-engineer who owns the product, reads on a phone half the time, and
will not read a paragraph longer than three lines.

---

## 2 · The six kinds of page

These six came out of 330 real pages written for one reader. They are named by **what you have to
DO**, not by what the page is about — which is why there are six and not thirty.

| Kind | You are saying | It opens with |
|---|---|---|
| **Decision** | "Decide this with me." | the choices side by side, and a recommendation already filled in |
| **Mission map** | "Show me this big thing so I don't lose track of it." | the count, then a rail of what is done, doing and next |
| **Findings** | "Go find out and tell me what to do." | the winner, then what is wrong with it |
| **Proof** | "Show me it actually works." | the tally, then a capture beside every claim |
| **Explainer** | "Help me understand how this works." | one metaphor, carried the whole way down |
| **The thing itself** | "Show me the actual screen, not a description of it." | the screen, drawn or framed live |

**These are the ones to start from.** Most pages turn out to be two of them at once, and the rules
for mixing are in `report-method.md` §2.

**Is anything you regularly ask for missing?** If yes, it becomes a seventh kind: name it by what
you have to do, say what it opens with, and add a row. A new kind needs a real ask behind it — not
a topic you happen to care about.

- **Kinds you want to add:**

---

## 3 · Where pages get served

A page has to arrive as a link the reader can click, not a path they have to paste.

- **Where pages are written:**  *(default `~/memory/sessions/YYYY-MM-DD-topic/`)*
- **How they become a URL:**  *(the files server? a local static server? a shared folder?)*
- **The command that prints the URL:**

**Never hand them a bare `file://`.** It is not clickable in most terminals and chat apps, and a
link they cannot click is a page they never read. If the files server is installed, it prints an
http link for any page under `~/memory`:

```bash
~/.claude/bin/files-server url ~/memory/sessions/2026-08-13-topic/page.html
```

If you have nothing yet, the smallest thing that works is a static server over the folder:

```bash
cd ~/memory/sessions && python3 -m http.server 8181
# → http://localhost:8181/2026-08-13-topic/page.html
```

Every page carries its own copy of the stylesheet, so it also renders opened straight from disk.

*Default if blank:* the files server when it exists, else the page's absolute path.

---

## 4 · Screens, and where the drawn ones live

Sooner or later a page will need to show one of your screens — a change you are proposing, a screen
that does not exist yet, an argument about a layout. **It never gets described in a paragraph, and
it never gets a gray placeholder box.** It gets drawn as a real HTML file and framed live on the
page.

**If you have nothing drawn yet, that is the normal case.** The first screen you need becomes the
first file, with its own small stylesheet. `examples/mocks/` shows the shape: three screens and a
kit of about 150 lines carrying a nav, cards, tables, buttons and badges. Keep them in one folder of
their own — the second page that needs the same screen then frames it instead of redrawing it, and
the two can never disagree.

Once you have several, this section names where they are, and one rule turns on: **check that folder
before drawing anything.**

- **Where drawn screens live:**
- **Their index:**

If you already have a component library or Storybook, point at that instead and skip the drawing —
the real component always beats a mock of it.

---

## 5 · Your register — how sentences sound

The system ships with a register measured from 13,002 of one person's own text messages. That
measurement is not portable. **The method is.**

**To measure your own:** take a few hundred of your real messages — chat, email, PR comments. Ask
your Claude to read them and report back: median sentence length, how you open a correction, whether
you hedge, whether you ask or propose, which plain words you use where it would use jargon. That
report becomes this section, and it beats any style guide because it is evidence rather than taste.

Here is the shipped one in full, so you can see what the output of a measurement looks like. Four of
the ten hold for almost any reader and are worth keeping unmeasured; the other six are one person's.

| # | The rule | Keep? |
|---|---|---|
| 1 | One idea per line — the beat is the unit. That reader's median message is six words | measured from them |
| 2 | **Verdict word first, reason second.** "Correction — 3 files, not 5" | **structural — keep** |
| 3 | Answer on their axis before adding anything. Their questions are proposals wanting yes, no, or the correction | measured from them |
| 4 | **Exact nouns, always.** If they could reply "which one?", it is not written yet — and the fix is *more* words, not fewer | **structural — keep** |
| 5 | **Corrections without apology.** Errors are facts | **structural — keep** |
| 6 | Objections, not permission. "I'd ship the pinned version. Any reason not to?" | measured from them |
| 7 | Emphasis is surgical — one bold word. No sprays, no exclamation marks | measured from them |
| 8 | Dry humor unmarked, one per page, only if true | measured from them |
| 9 | **Supply the criterion when asking them to judge**, stacked as separate lines | **structural — keep** |
| 10 | Eloquence when earned, never decoration. Plain fact first, its name second | measured from them |

The four in bold are about being understood, so they survive any reader. The other six are
measurements of one person — their sentence length, their habit of proposing rather than asking,
their one dry aside — and yours will differ.

- **Your measured rules:**

---

## 6 · Locale and house conventions

*Defaults shipped, all easy to flip:*

- US spellings — color, gray, canceled, center
- 12-hour time, `$`
- No emoji anywhere. `✓` and `✗` may carry a verdict; nothing else pictorial
- No exclamation marks, and never the word "successfully"
- Dark mode default, sun/moon toggle top right, choice remembered

- **Yours:**

---

## 7 · The four colors

The stylesheet colors exactly four things, and **a color appearing without its meaning is a bug.**

| Color | Means |
|---|---|
| green | good · done · the pick |
| amber | waiting · caution · their call |
| red | broken · dead · ruled out |
| teal | informational · in flight · magnitude · links |

Everything else is grayscale surface. Changing the hues is one edit at the top of `assets/report.css`
(§1 Tokens) and every page follows. Changing what they *mean* is not recommended — the meanings
are what make a page skimmable at arm's length.

- **Your hues, if different:**
