---
name: prototype
description: Make a clickable HTML prototype of an app, page, screen or tool, so the person can judge it by clicking instead of reading code. Use when someone asks for a prototype, a mockup, a wireframe, "sketch this", "draw this", "what would X look like", "make me a prototype of", or types /prototype <thing>.
---

# /prototype — a clickable sketch before the real build

The person you are helping judges by clicking, not by reading code. A prototype is how they see
an idea before anything real gets built: one HTML page they can open on their laptop or phone,
tap through, and react to. Cheap to make, cheap to throw away, cheap to change.

## 1 · Understand the ask (one round, at most)

- Clear enough to draw? Just build. Most asks are.
- Genuinely ambiguous? Ask at most 2-3 quick questions, each with your own guess, then wait once:
  - Who uses it? (just them, their team, the public)
  - The one main job — what does someone open it to do?
  - Phone first or desktop first?
- Never ask about tech, frameworks or file formats. Those are your call.

## 2 · Build it in one folder

```
~/memory/prototypes/YYYY-MM-DD-<short-name>/index.html   (plus any images or extra pages)
```

- Today's date, a short lowercase name (`2026-03-14-plant-tracker`). Create the folder if missing.
- Plain HTML, CSS and JavaScript. No build step, no npm, no server needed: it works by
  double-clicking `index.html`. Inline the CSS and JS unless the file gets unwieldy.
- No outside libraries unless one saves real work (a chart, a map); then load a pinned version
  from a CDN and make sure the page still makes sense if it fails to load.
- **Light and dark aware**: colors as CSS variables, a `@media (prefers-color-scheme: dark)` block
  that swaps them.
- **Phone-width friendly**: at 390px wide nothing runs off the screen. Rows wrap or stack, tab rows
  scroll sideways, grid and flex children get `min-width: 0` so one long line can't widen the page.

## 3 · Real states, not gray boxes

A prototype is judged by using it, so it has to behave like the thing.

- **Realistic sample content**: believable names, numbers, dates and text — never "Lorem ipsum",
  "Item 1", "John Doe". Include a long name and a big number to show what breaks.
- **Every button does something**: navigates, opens a panel or dialog, adds, deletes, saves.
  Persist changes in `localStorage` so a refresh keeps them, with a quiet "Reset demo" somewhere.
- **The states that matter**: empty (first time, nothing yet), loading, error (it failed — what now?),
  full (lots of data). Draw the ones this thing would really hit, not all of them by rote.
- **A small state switcher** only when a state can't be reached by clicking (e.g. the error state).
  Keep it out of the way — a little floating control in a corner.

## 4 · Design rules for anything you draw

- **Copy what people already know.** A calendar works like Google Calendar, a chat like iMessage,
  a list like the Notes or Reminders app, settings like the phone's Settings. Never invent a new
  gesture or layout when a familiar one fits.
- **Headings in sentence case** ("Your plants", not "Your Plants"), set apart by size and weight.
- **No small all-caps, letter-spaced labels** anywhere — not as section titles, not above headlines,
  not as tags. No `text-transform: uppercase` with `letter-spacing` on small text.
- **No placeholder text in inputs.** A label above the box says what it is; the box stays empty.
  The one exception is a box with no label at all, like a search field.
- **No helper text or subtitles** under headings, cards or settings. Write a better heading instead.
  Only add a line when it prevents a real mistake (e.g. "This deletes all 40 photos").
- **Words the user would say**, not developer words. Buttons say what they do ("Save plant", not
  "Submit").
- One accent color, plenty of space, readable text sizes (16px body on phones). Plain beats clever.

## 5 · Check it before showing it

Never send a link you haven't looked at.

- If a headless browser exists (`chromium`, `chromium-browser`, `google-chrome`, or Chrome on a Mac at
  `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`), take two screenshots:

  ```bash
  B=$(command -v chromium || command -v chromium-browser || command -v google-chrome)
  P=~/memory/prototypes/<folder>
  "$B" --headless --hide-scrollbars --screenshot="$P/check-desktop.png" --window-size=1280,860 "file://$P/index.html"
  "$B" --headless --hide-scrollbars --screenshot="$P/check-phone.png"   --window-size=390,844  "file://$P/index.html"
  ```

- Open both images and actually look: anything cut off or overlapping on the phone, unreadable in
  dark mode, empty where it shouldn't be, a broken image? Fix it and re-shoot.
- If a browser automation tool is available, also click through the main path once and check
  `document.documentElement.scrollWidth` equals the window width at 390px.
- No browser at all? Re-read the page for the phone and dark-mode rules above and say it's unchecked.

## 6 · Show it as a link

- **The link**: if `~/.claude/bin/files-server` exists, run `~/.claude/bin/files-server url <abs-path>`
  for an http link that also opens on their phone. Otherwise give the full file path.
- **Inside T3 Code** (the `mcp__t3-code__html_render` tool exists — fetch it with ToolSearch): reply
  with a small chat page — the link first, then the phone screenshot (or a cropped part of the
  desktop one), then the questions. If a chat-kit guide is installed, build the page from it.
  Never paste a whole multi-screen prototype as one giant image.
- **Anywhere else**, a short reply in plain words:
  1. What it is, in one line ("A plant tracker: your plants, when each needs water, a log of waterings.")
  2. The link.
  3. 1-3 questions where you need their call, numbered, each with your recommendation
     ("1. Water reminders as a list or a calendar? I'd go list — faster to scan.").
- No code, no file listings, no tech talk in the reply.

## 7 · Iterate

- Their feedback edits the **same folder**, in place. Re-check (step 5) after every round.
- Keep earlier versions only when they want to compare: copy to `v1/`, `v2/` inside the folder and
  show them side by side — the `/html` skill's compare view if it's installed, otherwise a simple
  flip page (`compare.html` with a toggle between the two in an iframe).
- Keep going until they say it feels right. Small fixes don't need questions; just make them.

## 8 · When they're happy

Offer to turn it into the real app. That is normal Claude Code building work, not part of this
skill: pick a proper stack, build it with tests, and use the prototype as the spec. If the
Development Bible is installed at `~/.claude/ai-tools/bibles/01-DEVELOPMENT-BIBLE.md`, read it first
and follow it. The prototype folder stays as the record of what was agreed.
