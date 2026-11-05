# Every knob, and which file to turn it in

Nothing here needs turning to start using the system. This is the map for when something bothers
you — and something will, which is the point.

All paths below are inside `~/.claude/skills/html/`.

**The rule of thumb:** anything about the *person* goes in `READER.md`. Anything about the
*method* goes in `report-method.md`. Anything about the *look* goes in `assets/report.css`. Never
in a single page — a one-off `<style>` tag is how a design system dies.

---

## The person

| Knob | Where | Notes |
|---|---|---|
| Who reads these pages | `READER.md` §1 | the answer that bends the most rules. "I do read code" changes what counts as evidence |
| A seventh kind of page | `READER.md` §2, then the table in `report-method.md` §2 | the six stay; add one when something you regularly ask for is not covered |
| How pages get served | `READER.md` §3 | must end in a clickable link |
| Where your drawn screens live | `READER.md` §4 | blank is normal — the first screen a page needs becomes the first file |
| Your writing register | `READER.md` §5 | measure it from real messages rather than guessing |
| Spellings, time format, currency, emoji | `READER.md` §6 | ships US, 12-hour, `$`, no emoji |

---

## The look

All in `assets/report.css`. Change a value there and every page built from then on follows — that
is the whole reason there is one sheet. Each page carries a copy of the sheet in its own folder, so
an older page picks up the change when you copy the sheet over its copy again.

| Knob | Where in the file | Ships as |
|---|---|---|
| The four colors | §1 Tokens — `--green` `--amber` `--red` `--acc`, plus their `-t` tints, in both the dark block and the `body.light` block | Keep the four *meanings* even if you change the hues. A color without its meaning is a bug |
| Dark or light by default | §1 Tokens — the `body{}` block is the default, `body.light{}` is under the toggle. Swap the values to flip | dark |
| Page width | `--stage` | 1680px |
| Prose width | `--measure` | `none` — prose runs the full stage. Set a `ch` value if a narrow column suits your reader better |
| Corner radius | `--r-plate` (cards), `--r-chip` (chips, buttons, inputs) | 8px / 4px |
| Spacing | `--sec-gap` `--comp-gap` `--peer-gap` | 68 / 28 / 56px. **Four steps and nothing invents a fifth.** A block never carries its own section-sized margin — spacing belongs to the container. That rule exists because a block that added its own produced a 190px hole |
| Typeface | the `font-family` on `body`, and the Google Fonts link in each page's head | Inter |

---

## The method

In `report-method.md`. These are rules with reasons; change them, but write down the reason you
changed them next to the change.

| Knob | Where |
|---|---|
| The kinds of page and their required blocks | §2 |
| The connector test and the four drawing laws | §3 — **load-bearing, changing these breaks the system** |
| The fact test | §3 |
| Craft rules: no eyebrow labels, no badges on recommendations, never dim a ruled-out row, verdict bars are rare | §4 |
| The self-check before serving | §6 |
| Whether findings and proof pages carry a sources line | §7 |

---

## The blocks

In `BLOCKS.md` and `assets/report.css` together — always both, never one.

**Adding a block.** Build it into `report.css` with a comment above it naming what it is FOR, what
it HOLDS, what it must NEVER hold, and the one word it claims ("then", "inside", "and", "becomes").
Then add a row to `BLOCKS.md` with the same information and the kinds of page it is at home on.
Namespace the class `r-` — a bare modifier name once matched a component and threw a panel off the
page.

**Changing a block.** Fix it in the sheet, not on the page that revealed the problem. Every future
page then improves for free, and every past page improves the next time it is opened.

**Retiring a block.** Leave the CSS in place so old pages still render, strike the row in
`BLOCKS.md`, and say why. The gutter note is the worked example: retired because margin notes read
as filler, still defined, never used on a new page.

---

## What not to change

- **Do not add a second stylesheet.** One sheet is the entire mechanism.
- **Do not put a `<style>` block on a page.** If a page needs something the sheet lacks, the sheet
  lacks it.
- **Do not set `overflow-x:hidden` on `html` or `body`.** It kills scrolling in Chrome. Containment
  comes from `minmax(0,1fr)` on grids and `.r-tablebox` on wide tables.
- **Do not skip the screenshot.** Every rule in this system exists because somebody skipped it.

---

## A note on the comments in `report.css`

The stylesheet carries its own documentation: every block has FOR / HOLDS / NEVER written above it,
and many cite the date they were added or ruled. The dates were left in — a rule with a date on it
is easier to overturn honestly than an anonymous one.
