---
name: html
description: "Build an HTML page for the user — a report, brief, plan, decision, mission map, proof, explainer or mockup. Runs the report system: ask what you are presenting, pick blocks by what the content IS, build from the one stylesheet, screenshot before handing it over. Use when the user says \"/html\", \"make me a page\", \"show me this as a page\", \"write it up\", or any output that would otherwise be a wall of markdown."
---

# /html — build the page

**The split is by reader, not by document type.**

| Who reads it | Format |
|---|---|
| **The user** — a brief, plan, decision, status page, digest, findings, proof, mission map, explainer, mockup, anything they open | **an HTML page**, handed over as a link |
| **Only agents** — session notes, agent-to-agent handoffs, skill and rule files, catalogs | markdown |

If the user is going to look at it, it is a page. They do not read markdown for anything
substantial — a status page and a digest are for them, so they are pages. Markdown is what one
Claude leaves for the next one.

**A reply inside a T3 Code thread is not a report page.** It is a chat-kit page — one script tag
plus `<k-*>` blocks in the five fixed reply shapes: `~/.claude/ai-tools/chat/README.md`.
Small things go in chat. Reports, briefs, plans, decisions and anything to read closely get their
own full page, built here.

## First use — is `READER.md` filled in?

`READER.md` is the one file about the person reading these pages. If its first line is still the
`blank template` marker, offer once, in one line, before building: *"Want to spend about twenty
minutes tuning these pages to you first? I'd walk you through the examples and ask a few
questions."* Yes → run `ONBOARD.md`. No → build the page they asked for on the defaults written
under each heading in `READER.md`, and do not offer again this session.

## The canon lives in four files. Read them, don't restate them.

All in `~/.claude/skills/html/`:

| File | What it holds |
|---|---|
| `READER.md` | **who this is for** — their register, their locale, where pages get served, their drawn screens |
| `report-method.md` | the method, the six jobs, the rules, the register, the self-check |
| `BLOCKS.md` | every block: for / holds / never / which kinds it is at home on |
| `assets/report.css` | the one stylesheet. Every block, both modes, the drift knobs |

Read `report-method.md` before writing a line of markup. **This file is a runner, not a second
copy of the rules.** Any rule that needs changing gets changed in `report-method.md`, never here.
Anything about the *person* gets changed in `READER.md`. `CUSTOMIZE.md` maps every knob to its file.

## Run it in this order

### 1 · Say the whole thing out loud first

Plain sentences, the way you would tell the user across a desk. What happened. What it means for
them. What they have to decide. A page that cannot be said out loud becomes an essay, and essays
get rejected. **The speech is the draft — it expands into blocks, never into paragraphs.**

**The title and every heading name the subject.** A page about invoicing has "invoicing" in its
title. Evocative and naming nothing gets rejected.

### 2 · Ask what you are presenting

Name the job by what **the user has to DO**:

- they must answer something → **decision**
- they must not lose track of a big project → **mission map**
- they asked you to go find out → **findings**
- they asked whether it works → **proof**
- they asked how something works → **explainer**
- the subject IS a screen → **the thing itself**

Most pages are two jobs. The dominant job owns the spine; take the union of required blocks, never
the union of spines; the page answers once. Mixing rules are in `report-method.md` §2. A seventh
kind, if the reader added one, is in `READER.md` §2.

### 3 · Shop the shelf

Open `BLOCKS.md`, and open `examples/system.html` if a block is unfamiliar — every block is drawn
live there with its rules beside it. Blocks are tagged by the kind they are at home on — **a
starting shelf, not a fence.** Any block goes on any page when the connector test passes.

**Before drawing anything, say the relationship aloud.** Arrows say "then". A rail says "happened".
Nested boxes say "inside". Stations growing say "becomes". A grid says "and". **If the sentence is a
lie, the shape is wrong.** Peers want "and", so peers want a grid, never arrows.

Then: size means importance · position means order · nesting means containment · color keeps its
four meanings and a color without its meaning is a bug.

### 3b · If a screen appears on the page, use the real one

- **A miniature of a screen** embeds the real page or prototype file in `.r-scale`, live and
  scaled (set `--r-w` and `--r-tall`). Never hand-draw a screen that already exists, and never
  paste a screenshot — both go stale.
- **A thing-itself page** frames the same file full size in `.r-frame`.
- **Nothing drawn yet?** That is the normal case. The screen you need becomes the first file in a
  folder of its own, with its own small stylesheet. `examples/mocks/` is the worked example. Check
  the folder named in `READER.md` §4 first, and say what you found.
- **A real component library or Storybook?** Point at that instead; the real component beats a
  mock of it every time.

### 3c · Measuring behavior across states? Use the matrix

When the subject is "what does each action do in each state", the block is the **state matrix** —
rows are actions, columns are states, every cell a mark plus what happened. The shape of the answer
is the finding: a row green all the way across behaves, one red square in a field of green is the
bug. Never leave a square blank; untested and unchanged are different answers.

### 4 · Build

Unless `READER.md` §3 says otherwise, the page lives in a folder of its own,
`~/memory/sessions/YYYY-MM-DD-topic-slug/<name>.html`, or in the repo's `docs/` folder when it is
about a repo. **Copy the sheet into that folder**, so the page works both served over http and
opened straight from disk:

```bash
D=~/memory/sessions/YYYY-MM-DD-topic-slug
mkdir -p "$D"
cp ~/.claude/skills/html/assets/report.css "$D/"
# only for 8+ row tables:
cp ~/.claude/skills/html/assets/report-table.js "$D/"
```

The head of every page — copy it from any file in `examples/`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Names the subject</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400..700;1,14..32,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="report.css">
</head>
<body>
<div class="r-page">
```

The page skeleton: nav row + toggle · title · dek · the answer · teaching sections whose headings
are sentences · the user's questions at the end of the section that makes them answerable · "Needs
your attention" last, or a recap when nothing is open. The theme toggle goes in the nav row and
its script at the foot:

```html
<div class="r-nav">
  <span class="r-here">Page name</span>
  <span class="r-spacer"></span>
  <button id="theme" class="r-theme" title="Switch theme"></button>
</div>
…
<script src="report-table.js"></script>  <!-- only for 8+ row tables -->
<script>
const b=document.body,t=document.getElementById('theme');
const set=m=>{b.classList.toggle('light',m==='light');t.textContent=m==='light'?'☾':'☀';
try{localStorage.setItem('report-theme',m)}catch(e){}};
let m='dark';try{m=localStorage.getItem('report-theme')||'dark'}catch(e){}
set(m);t.onclick=()=>set(b.classList.contains('light')?'dark':'light');
</script>
```

**Only blocks from the sheet.** A genuinely new block gets built into
`~/.claude/skills/html/assets/report.css` and listed in `BLOCKS.md` the same turn — never inline
on one page. Then copy the updated sheet into the page's folder.

### 5 · Look at it before the user does

Non-negotiable, and the source of every correction that has ever landed on these pages:

1. Screenshot the real render at **1440 and at 390**. Never hand over unseen pixels.
2. Read every arrangement's connector aloud. A shape claiming something the content does not
   support is a defect, not a style choice.
3. Extract the h2s and read them as a paragraph — do they carry the argument alone?
4. Follow-up test on every noun: could the user reply "which one?"
5. Walk the rest of the self-check in `report-method.md` §6.

Screenshot with Playwright, a Chrome DevTools MCP, or headless Chrome, which is fast and needs no
MCP:

```bash
# Mac: Chrome's app path. Linux: whichever of these is installed.
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
[ -x "$CHROME" ] || CHROME=$(command -v google-chrome || command -v chromium || command -v chromium-browser)
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --window-size=1440,1400 \
  --virtual-time-budget=8000 --screenshot=/tmp/page-1440.png "file://$PAGE"
```

Then Read the PNG and look.

**For 390, `--window-size=390` is a trap**: headless lays the page out wider and crops to 390, so
you see a desktop layout with its right side cut off and you go fixing defects that do not exist.
Write a harness — `<iframe src="file://$PAGE" style="width:390px;height:2200px;border:0">` in a
file under `/tmp` — and screenshot THAT at `--window-size=390,2200`. Only then do the sheet's phone
rules fire. Do not pass a fresh `--user-data-dir` per shot; it hangs.

### 6 · Hand it over

If `~/.claude/bin/files-server` exists, give the user the http link it prints:

```bash
~/.claude/bin/files-server url ~/memory/sessions/YYYY-MM-DD-topic-slug/<name>.html
```

Otherwise give the page's absolute path. A **sources line** closes findings, proof and mission
pages only.

**Said "self-contained", or the page is leaving this machine? Write the standalone copy too** —
same turn, no second ask. A page linking the sheet renders as unstyled text once it leaves its
folder, which is exactly what mailing it to someone does. Both files ship, and the inlining
snippet plus its `file://` check are in `report-method.md` §7.

## Standing traps

- **Never `overflow-x:hidden` on `html` or `body`** — it breaks scrolling in Chrome. Containment
  comes from `minmax(0,1fr)` on grids and `.r-tablebox` on wide tables.
- **A recommendation is an opinion and never wears a badge.** It uses `.r-mycall`.
- **Never dim or strike a ruled-out row.** The reader is still comparing against it.
- **A sequence carries no numerals.** Numerals only where something must be cited — proof claims
  and asks.
- **Small multiples and stat rows shrink on a phone, never stack.** Side by side IS the component.
- **Namespace every class `r-`.** A bare modifier name once matched a component and threw a panel
  off the page.
- **After editing `report.css`, reload with the cache bypassed before believing what you see.**
  Chrome can hold the old stylesheet and you will screenshot a fix that did not apply. A `?v=N` on
  the page URL does not help — the stylesheet is a separate request. Reload ignoring the cache, or
  check a computed style before trusting the pixels.

## The page that shows all of it

`examples/system.html` — every block rendered live with what it is for, what it holds and what it
never does. Read it before composing anything unfamiliar.
