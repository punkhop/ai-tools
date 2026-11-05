# The blocks — what exists, what each one claims, where each is at home

The catalog behind `report-method.md`. Every block lives in `report.css` with the same
FOR / HOLDS / NEVER at the source. Read this before composing a page; read the rules in the method
before choosing between two blocks.

**Tags are a starting shelf, not a fence.** A block tagged `decision` is where a decision page
starts, not the only place it may appear. Any block may appear on any page **when the connector
test passes** — a decision block on an explainer is right whenever the reader has a choice to make
there. What is never allowed is a block chosen because it exists.

Kinds: `mission` · `decision` · `thing` (the thing itself) · `findings` · `proof` · `explainer`

Every block on this shelf is drawn live, with its rules beside it, at `examples/system.html`.

---

## 1 · Answer blocks — a page uses exactly one

The first thing under the dek. Every page answers before it teaches; a page uses **one** of these,
never two.

| Block | Class | Claims | FOR | Home on | Anywhere else |
|---|---|---|---|---|---|
| Verdict plate | `.r-verdict` | "this one" | the one conclusion of a page that reached one | findings · decision | any page that reached a single conclusion |
| Decision cards | `.r-cards` | "A or B" | a choice that is the user's, answerable in one word from a phone | decision | ends an explainer that leaves a choice open |
| Miniature of the surface | `.r-scale` | "this is what you are deciding on" | a decision about a screen — put the screen above the cards. Often, not always: a decision with no surface does not get one | decision · findings | any page arguing about a screen |
| Tally | `.r-tally` | "n of n proven" | verdicts counted before any scrolling, so green means skim past | proof | any page that closes a list of checks |
| Stat row | `.r-stats` | "these three numbers" | 2–4 figures sharing one unit, one period, one subject | mission · findings | opens any page whose answer is a number |
| Embedded prototype | `.r-frame` | "here it is" | the real surface, framed live, when the subject IS the surface | thing | any page whose subject is a screen |

**HOLDS and NEVER**

- **Verdict plate** — ribbon word · the name set large · one figure with its unit spelled out · a
  one-line verdict · exactly three reasons · a rail with runner-up and ruled-outs.
  *Never* twice on a page. *Never* the figure wearing the ribbon — the ribbon labels the name.
  *Never* a page that ends open.
- **Decision cards** — 2–4 options at IDENTICAL size: tag, figure, title, two lines, radio
  top-right with the recommendation pre-filled. Two is the best shape.
  *Never* one card smaller than another — that is a thumb on the scale. *Never* more than four —
  that is the table's job.
- **Tally** — the count, then the indexed claim list with its marks.
  *Never* a tally that disagrees with the sections under it.
- **Stat row** — a figure and the consequence line under it. Rules between, no boxes.
  *Never* numbers that disagree in kind — $46/month beside $7,600/year beside 10× is three ideas
  pretending to be a set. *Never* a count with no so-what.
- **Embedded prototype** — one prototype at full stage width in a browser frame, address visible,
  numbered notes under it. *Never* a redescription of what the prototype already shows.

---

## 2 · Argument blocks — the teaching body

| Block | Class | Claims | FOR | Home on | Anywhere else |
|---|---|---|---|---|---|
| State matrix | `.r-table` + `.r-cell` | "for each action, in each state" | every action crossed with every state a thing can be in — the shape of the answer IS the finding | proof · findings | any page measuring behavior across states |
| Comparison table | `.r-table` | "for each: these questions" | one decision across 5+ candidates or 3+ attributes | findings · decision | mission maps listing work by owner |
| Admitted-flaws row | `.r-flaws` | "and here is the catch" | the case against the thing that just won | findings | any page that recommends anything |
| Small multiples | `.r-multi` | "bigger than" | one value among its peers, one shared scale | findings · mission | proof pages sizing what changed |
| Sequence | `.r-seq` | "then" | a path walked ONCE — a flow, a migration, a checkout | explainer · thing | findings explaining how a thing gets built |
| Timeline rail | `.r-rail` | "happened, then" | history and missions — what is done, doing, next, whose move | mission · proof | explainers with a real chronology |
| Points | `.r-points` (a `ul`) | "and" | 2–6 peer facts under a heading sentence, one line each — never order, never nested | findings · mission · explainer | any section whose body is plain facts |
| Evidence pair | `.r-claim` | "and here is the proof" | a claim, its capture, numbered notes on what to look for | proof | findings needing one capture |
| Phone capture | `.r-shot` + `.r-shot-phone` | "on a phone" | a screenshot OF a phone — capped at 340px so it reads as a phone instead of dwarfing the page at its natural ~1100px | proof · findings | any page whose subject is a phone screen |
| Phone screens side by side | `.r-phones` + `.r-scale` | "this one, or this one" | 2–4 versions of one phone screen compared, each a drawn 390px prototype file | decision · thing | findings comparing phone layouts |
| Phones at true size | `.r-phonewall` + `.r-phoneset` (`.r-phoneset-row`, `.r-phoneset-tag`, `.r-scale`, `.r-scale-cap`) | "these, at real size" | comparing phone screens by eye when there are 5+ options or each has two versions — every phone 1:1 at 390px, wrapping 2–3 a row, one a row on a phone. Never shrunk on a desktop. Built 2026-10-02 after `.r-phones` squeezed five into an unreadable row | decision · thing | any mockup round the user compares |
| Tablets in the wall | `.r-phoneset` + `.r-scale.r-scale-tablet` (`--r-w`, `--r-tall` = device points) | "these, on a tablet" | comparing iPad / tablet layouts by eye — each a live prototype file at half size on a desktop, a quarter on a phone, wrapping like the phones. Built 2026-10-03 for the iPad layout page | decision · thing | any tablet mockup round |
| Compare bar | `.r-compare` + `.r-compare-btn` (`.is-on`) + `.r-compare-sep` | "just these two" | a sticky row of option letters: pick two and only those sit side by side; a variant switch (with / without money) flips every set. Pairs with Phones at true size | decision · thing | any wall of options |
| Moving capture | `.r-shot` + `<video controls>` | "watch it happen" | proving MOTION — a still frame of an animation proves the frame, never the animation. Lives inside an evidence pair like any other capture | proof | nowhere a still would do the job |
| Sound capture | `.r-shot.r-shot-sound` + `<audio controls>` | "listen to it" | proving what something SOUNDS like — a crackle, a dropout, a mix — two in `.r-shots` for before / after, the label naming which is which. Inside an evidence pair like any capture. Built 2026-10-06 for a film playback check | proof | any claim about sound |
| Captures in a cell | `.r-table` + `.r-cell` + `.r-cell-shots` (`a.is-fail`) | "and here it is at each width" | a proof matrix whose every square is screenshots: 2–4 small captures under the mark and phrase, each linked to the full image, a failing width edged red. Built 2026-10-21 for the widget-looks proof | proof | any matrix proving a surface at several widths |
| State gallery | `.r-states` (+ `.r-states-phone`) + `.r-shot` + `.r-shot-cap` / `.r-shot-head` | "this surface, in each of its states" | every state of one of our own prototype surfaces two across, caption = state name + its prototype link; also an app screen beside the version copying it. A plate the app never drew holds its real labels in words, never a faked capture. Built 2026-10-12 for the staff booking guide | thing · explainer | proof pages walking states one by one |
| Reference gallery | `.r-shots-wide` + `.r-shot-cap` | "and here is how they did it" | a wall of captures from OTHER products, caption naming the app and the one move worth taking | findings | your own product's screens — that is `.r-claim` or `.r-frame` |
| Capture with a heading | `.r-shot` + `.r-shot-head` (`.r-shot-who`, `.r-shot-when`) | "this is whose screen" | evidence walls where the reader must know who received / owns each capture before reading it — big who, small when above the image | proof · findings | captures whose caption is commentary — that stays `.r-shot-cap` below |
| Width switch | `.r-widths` + `.r-wall` | "right at both widths" | judging one surface at desktop and phone width — the switch drives every frame at once | thing · proof | findings comparing a set of surfaces |
| Screen cards | `.r-screens` + `.r-screen` | "screen by screen" | reviewing a form or flow one screen at a time — question and answers at reading size, all screens comparable | thing · findings | any page reviewing a sequence of surfaces by their copy |
| Test card | `.r-screen` + `.r-screen-qrs` / `.r-screen-qr` + `.r-check` (+ `.r-check-note`) | "do this, expect that, mark it" | a hands-on device checklist the user runs and marks works/broken — numbered steps, optional codes to scan, results feeding the answer bar's copy-back line. Built 2026-10-02 for the mobile check-in test | proof · thing | any checklist the user walks with a device in hand |
| Quote list | `.r-quotes` + `.r-quote` (`.r-quote-who`, `.r-quote-said`, `.r-quote-note`) | "and here is exactly what they said" | verbatim lines from other products or people, each labeled by who said it — the evidence when the argument is about wording. Label beside the quote on a desktop, above it on a phone. Never a paraphrase (that is Points). Built 2026-10-12 for the page-help voice study | findings · decision | any page arguing about copy |
| Picked column | `.r-table` + `.r-col-win` (+ `.r-table-cards.r-table-stack` for long cells on a phone) | "this column" | a comparison table whose candidates are COLUMNS and whose rows are the cases they are tried on — the recommendation tints its whole column, header green. One column only; the others keep full contrast. Built 2026-10-12 | decision | any table comparing candidates side by side across cases |
| Redline | `.r-redline` | "this wording becomes that wording" | a proposed change to a document, in whole sentences: `.r-del`, `.r-add`, `.r-same` lines | decision | any page proposing wording; *never* code or markup |
| Callout | `.r-callout` | "read this differently now" | the one fact that changes how the rest reads | any | max two per page, ever |
| ~~Gutter note~~ | `.r-gutter` | — | **RETIRED 2026-08-13.** Margin notes read as filler. A fact that changes what the reader does goes inline in the sentence it changes; a fact that does not goes nowhere | — | never on a new page |
| Two-column stage | `.r-split` | — | a SPEC beside its specimen — the for/holds/never rails on the system page | system page | nowhere else: a margin note is filler |

**HOLDS and NEVER**

- **State matrix** — rows are actions, columns are states, each cell a mark plus what happened in
  one phrase, plus an optional second line for what the system *claimed* happened. `.r-table-wide`
  past about five columns. A row green all the way across behaves; one red square in a field of
  green is the finding. *Never* a blank square — untested and unchanged are different answers.
  *Never* a cell holding a sentence; that belongs under the grid.
- **Comparison table** — 3–12 banded rows; the winner's whole row tinted with a colored left edge;
  magnitude as a bar inside its own cell. Past ~8 rows it grows search, sortable headers,
  per-column filters and dismissable pills (`report-table.js`). Columns lock their widths — sorting
  moves rows, never columns.
  *Never* dim or strike a ruled-out row. The reader is still comparing against it: full contrast, and a
  chip saying why. *Never* a column repeating one value down every row — that is a grouping in
  disguise.
- **Admitted-flaws row** — exactly three columns, amber rule, short title, two lines each.
  *Never* omitted when a verdict plate exists. *Never* a flaw softened into praise.
- **Small multiples** — 4–10 horizontal rows: name, bar, value. One row lit.
  *Never* stacked on a phone — they SHRINK. Side by side is the component.
- **Sequence** — 3–6 cards, the arrow carries the order so there are no numerals. The stuck step
  tinted amber. Stacks on a phone with the arrow pointing down.
  *Never* things that already happened — that is the timeline. *Never* peers — peers want a grid.
- **Sequence, down** (`.r-seq.r-seq-down`) — the same sequence stacked at every width, for a
  path of 7+ steps whose cards hold full sentences (a build plan's slices). Built 2026-11-05 for the
  tracking-link build plan, where nine steps wrapped into unreadable narrow columns.
- **Timeline rail** — 2–6 milestones: dot, id, headline, status word with its mark, subhead, then
  2–6 sub-items each wearing its own mark and count. The current one carries "we are here".
  *Never* steps someone walks once. *Never* sub-items hiding their counts. Show what is DONE, not
  only what is left.
- **Evidence pair** — four parts, in this order, on a colored left rule:
  1. the numbered **claim** as a heading, in plain words
  2. `.r-claim-saw` — one line of what was actually seen, opening with ✓ or ✗
  3. `.r-claim-walk` — **how you get there**, told as a walk: what you open, what you click, what
     happens. This is the part that gets dropped and must not be — a capture with no walk shows a
     state without saying how anybody reaches it.
  4. the capture, with its caption
  There is no consequence block. A claim that needs a paragraph explaining why it matters was not
  written as a claim.
  *Never* an evidence pile at the end. *Never* code as evidence — behavior is the evidence.
- **Reference gallery** — a grid of plates, each an image over a caption whose first line is the app
  name and whose second is the single move worth taking. Wide enough to read an app's chrome: three
  across on a desktop stage, two on a laptop, one on a phone. Every image wraps in a plain link to
  itself so a click opens it full size, and every image is a LOCAL file — a signed CDN link expires
  and the page silently empties.
  *Never* a caption describing the picture; the caption names what to steal. *Never* below 440px a
  tile — smaller than that a screenshot is texture, not evidence. *Never* for your own product's
  screens: a claim about your own work is `.r-claim`, a live surface is `.r-frame`.
- **Width switch** — a two-button switch, then a wall of framed surfaces that all
  follow it. Each frame is the REAL file in an iframe, so what is judged is the shipping
  artifact rather than a screenshot of it. *Never* three widths — two is a decision, a
  third is a spec sheet. *Never* a switch per frame: the comparison is the page, so the
  page switches. Built 2026-08-20 for the email type audit.
- **Screen cards** — a numbered grid of plates: the number, the question as the user reads it,
  the answer rows, an optional note. `.r-screen-cond` marks a screen only some users see.
  *Never* a miniature of the rendered screen — that is `.r-mini`, and copy you cannot read
  reviews nothing. *Never* for peers: the numbers claim a sequence.
- **Copy specimens** — a numbered list of product copy under review: the number, where the copy
  appears, the specimen drawn at the width and type size it ships at (the surface's own label
  line, then the copy), and its proof (source, a count, a status mark). `--r-spec-w` sets the
  shipping width. Built 2026-10-13 for the help drawer's page cards.
  *Never* a paraphrase of the copy; *never* wider than it ships — a line that wraps in the
  product must wrap here. *Never* unnumbered: the ruling cites the numbers.
- **Callout** — one or two lines, colored by meaning.
  *Never* an alert under every component; that alerts nobody.
- **Gutter note** — retired. Kept defined so older pages still render, never used on a new one.
  The two-column stage survives only for a spec beside its specimen (the for/holds/never rails on
  the system page).

---

## 3 · Drawing blocks — draw the relationship, not a chart

Reach for these when the relationship is the point and a count is not. They are elements the six
kinds build from, **not a kind of page**.

| Block | Class | Claims | Use when |
|---|---|---|---|
| Assembly line | `.r-line` | "becomes" | input is transformed into output. Exactly three stations at EQUAL size, each holding a real miniature of its own contents — a spec listing, chips of what gets stamped on, a wireframe of the product. Add `.r-line-grow` only when the thing itself grows along the line. The recipe-card / kitchen / plate story is the model |
| Nesting doll | `.r-shell` | "inside" | containment, 2–4 shells, the subject innermost and lit. Past four deep, use a tree |
| Split bar | `.r-splitbar` | "plus, equals" | one number cut into its true parts. The honest pie. A slice too narrow for its value hands the value to the legend rather than clipping it |
| Miniature | `.r-mini` · `.r-scale` (`.r-scale-lg` = 0.8 on a desktop, for a 1440 screen whose text must stay readable; drops to .26 on a phone) | "this, small" | **the SUBJECT** at half scale. If it is a screen that already exists as a page or prototype file, embed the REAL file with `.r-scale` — never hand-draw a screen that already exists. If it does not, draw it to that same standard. Never a miniature of our own report blocks: draw the thing being discussed, not the page discussing it |
| Before / after | `.r-minis` | "changed" | two renders at identical size, only the delta colored — red on the broken side, green on the fixed |
| Shelf of peers | `.r-glances` | "and" | equal cards, no arrows, when items have no order |
| Logo test wall | `.r-lockups` + `.r-lockup` (`.r-lockup-wide`, `.r-lockup-art`, `.r-lockup-bg`, `.r-lockup-cap`, `.r-lockup-sizes`, `.r-lockup-true` on any tile that must keep true pixel size) | "this mark on every surface it must survive" | one logo direction drawn on square, circle, photo, ad corner and sign, same tiles in the same order for every direction | thing itself · decision |
| Tree | `.r-tree` | "inside" | a page tree, folder structure or workspace map where the nesting doll runs out — one row per node, databases wear a state mark, children indent under a guide line, an optional bar sizes each node on one scale. Collapse any subtree past ~40 visible rows into one summarizing row. Never arrows between nodes |
| Year strip | `.r-year` | "when" | every message one person gets across 52 weeks, one column a week, colored by kind. Shows the shape of a cadence — bursts, silences, what dominates — without reading a number. Six on a page is the ceiling; past that it is a table |
| Menu specimen | `.r-menus` + `.r-menu-wrap` + `.r-menu` (`.r-menu-trigger`, `.r-menu-row` with `.is-hover` `.is-current` `.is-tint` `.is-dim` `.is-danger`, `.r-menu-check`, `.r-menu-key`, `.r-menu-sep`, `.r-menu-head`, `.r-menu-clip`) | "this is what the menu looks like" | a product menu, dropdown or picker drawn full size with its REAL labels — the trigger showing its value over the open list, each row in its true state. Several side by side in `.r-menus` read as peers ("and"); a pair inside `.r-minis` edges reads as before/after. Never a generic box diagram. Built 2026-10-01 for the menu-system audit |
| Database view miniature | `.r-nv` (+ `.r-nv-pair` for two side by side, `.r-nv-trio` for one layout filled from three records; `.r-nv-h.is-toggle` / `.is-shut` for a toggle heading) | "this is how it looks in the database app" | a database view (a table or board app) or a page of views, drawn as the user will meet it — tab bar, filter line, grouped rows or board columns, select pills — filled with REAL rows. Options compared side by side in `.r-nv-pair`, each captioned with what it is and whether it is built. Never invented rows; boards scroll inside the frame |
| Sidebar specimen | `.r-sides` + `.r-side-wrap` + `.r-side` (`--cols`; `.r-side-head`, `.r-side-row` with `.is-sub` `.is-group` `.is-sel` and `--in`, `.r-side-dot` with `.is-working` `.is-idle` `.is-blocked` `.is-done`, `.r-side-end`) + `.r-side-cap` | "this is what the list looks like, at its real width" | a terminal app's sidebar or list panel — an agents list — drawn in monospace at the panel's true column count, so a label that truncates in the real thing truncates here. Several side by side in `.r-sides` read as peers ("and"). Real names from the real session; never wider than the real panel, because the width is the constraint being argued. `.r-side.r-side-app` (`--w` in px) draws the same rows in the page font for a native Mac app's sidebar; `.r-side-dot.is-ring` is that app's ring mark, drawn still. Row-state modifiers for pages comparing how a row signals state: `.is-tint`, `.is-edge`, `.is-faded`, `.r-side-pill` (`.is-quiet`). Built 2026-10-05 for an agents list options page |

**The real file is the source for any product surface.** Embed it in `.r-scale` (set `--r-w`,
`--r-zoom`, `--r-tall`): it stays live, so restyling the file updates every page carrying it, and a
screenshot cannot go stale because there is no screenshot. Check whether a screen is already drawn
before drawing it — a second proposal for something already drawn is pure waste.

**If you have no prototype kit yet, the first screen you draw starts one.** Give it its own file and
its own small stylesheet, keep it in a folder of its own rather than buried inside the report that
needed it, and every later page frames it instead of redrawing it. `examples/mocks/` is a worked
example: three screens and a small kit carrying a nav, cards, tables, buttons and badges.

Once a kit exists, name it in `READER.md` §4 and check it before drawing anything — a second drawing
of one screen is two drawings that will disagree.

**Never** for all six: gray placeholder blocks tucked beside a text column. A micro-render carries
real content and fills its stage or it does not go on the page.

**Banned outright**: pie · radar · venn · slope · 2×2 quadrant · drop-off funnel ·
ER prongs · gradient nesting boxes · any chart carrying data the reader does not act on.

---

## 4 · Closing blocks — how a page ends

| Block | Class | FOR | Used when |
|---|---|---|---|
| My call | `.r-mycall` | the recommendation, wherever a choice of the user's sits | every page with an opinion |
| Ask, inline | `.r-ask-here` | the question, NUMBERED, at the end of the section that makes it answerable | every question the page raises |
| Needs your attention | `.r-asks` | the same questions INDEXED at the end, so none is missed | any page with 1–6 open questions |
| Answer bar | `.r-answerbar` + `.r-skip` + `.r-edit` | approving a long list — each row can be skipped or edited in place; the pinned foot bar counts changes and builds one line to copy back (copy-paste, never a POST). Never dims a skipped row | any page where the user approves many rows at once |
| The recap | `.r-recap` | one short paragraph closing a page that asks nothing | any page with no open questions |
| Sources line | `.r-recap` + provenance | what was checked, what was not, the date, the links | findings · proof · mission only |

- **My call** — green rules above and below, "My call" green and rolled into the sentence, 21px
  semibold. Identical on every page. *Never* a badge or a pill — pills read as states, and a
  recommendation is an opinion. *Never* body-sized gray text; it has to announce itself.
- **Ask, inline** — every question appears where it becomes answerable: at the end of the section
  that gave the user what they need. Amber panel, its **number in a filled circle**, the question at 19px,
  one line of context, my call under. The number comes from a CSS counter — but the foot index runs
  on a SEPARATE one (`ask` inline, `askindex` at the foot), so the two agree only while every indexed
  row has an inline partner. An index row with no inline ask shifts every number after it, silently.
  Loud on purpose: a question that looks like body text gets read as body text.
- **Needs your attention** — the same questions indexed at the foot, 1–6 numbered rows, so nothing
  is missed on a skim. Amber rule on top; this section is the user's. It **indexes** the inline asks, it
  does not replace them. *Never* questions the page already answered. *Never* a
  row with no inline `.r-ask-here` partner — the two blocks run on different counters, so an
  orphaned index row renumbers the page without any visible error.
  *Never* absent when questions exist. *Never* a literal digit inside `.r-ask-n` — the number
  comes from the CSS counter, and a digit typed in beside it renders as "11", "22". Leave the
  span empty (2026-08-13's finish-lines page shipped with the digits doubled).

---

### Agent output

| Block | Class | Claims | FOR | Home on | Anywhere else |
|---|---|---|---|---|---|
| Tab specimen | `.r-tab` + `.r-tab-bar`, `.r-tab-body`, `.r-tab-head`, `.r-tab-line`, `.r-tab-link`, `.r-tab-draw` | "this is what the tab prints" | a Claude tab drawn at reading size — dark ground in both themes, monospace, title bar with the tab's name and state, the report's lines as they would print, a drawn surface where the report shows one. Built 2026-10-06 for the done-report redesign | decision · thing | any page arguing about what an agent prints |

- **Tab specimen** — the bar names the tab and its state; the body prints the report. *Never* a whole transcript; *never* a sideways scroll; *never* a fifth color.

---

## 5 · Type and furniture

`.r-page` frame · `.r-nav` + `.r-theme` toggle · `.r-title` · `.r-dek` · `.r-h2` (a sentence of the
argument) · `.r-h3` · `.r-body` (capped at `--measure`) · `.r-small` · `.r-label` · `.r-fig` +
`.r-unit` · `.r-chip` (red by default — ruled out; `.r-chip-acc` informational, `.r-chip-green`
already true, `.r-chip-amber` waiting or your call) · `.r-status` + `.r-mark-*` (the seven states, mark AND word, filled = firm,
hollow = pending) · `.r-sec` with its optional colored top rule · bare `code` for a literal — a path,
a field name, a route — which breaks anywhere it has to, so one long path cannot widen the page.

---

## 6 · Adding a block

A genuinely new block gets built INTO `report.css` the same turn — named, commented with its
FOR / HOLDS / NEVER and the word it claims, and added to this file with its tags. Never inline on
one page. If a block looks wrong, fix it in the sheet so every future page improves.

---

## 7 · Film blocks

| Block | Class | Claims | FOR | Home on | Anywhere else |
|---|---|---|---|---|---|
| Storyboard | `.r-board` + `.r-board-shot` (`.r-board-meta`, `.r-board-strip`, `.r-board-frame`, `.is-picked`) + `.r-board-player` (`.r-board-stage`, `.r-board-sub`, `.r-board-track` of `.r-board-seg`) + `.r-board-viewer` | "this shot, then this one" | a film planned shot by shot — every shot in cut order with its timing and the words heard over it, a strip of candidate frames to pick from, and a player running the picks against the sound. Built 2026-10-02 for a commercial | thing · decision | any shot list, animatic or video edit the user reviews |
| Take check | `.r-takes` + `.r-take` (`.r-take-head`, `.r-take-film`, `.r-take-said`, `.r-take-grade` + `.r-take-grade-letter`, `.r-take-facts`, `.r-take-faults` of `.r-take-fault`) + `.r-timebar` (`.r-timebar-lane`, `.r-timebar-label`, `.r-timebar-track`, `.r-timebar-band` with `.is-action` `.is-fault`, `.r-timebar-mark` with `.is-peak`, `.r-timebar-axis`, `.r-timebar-times` of `.r-timebar-jump`) | "this is what was said about this take" | checking a tagger's claims about a video take — the take playing, its time bar under it, and every claim a viewer can verify beside it. Built 2026-10-05 for a commercial tag trial | proof · thing | any page where times on a video have to be checked by eye |

- **Storyboard** — rows in cut order; the meta column carries the shot id, its start time and length, the
  scene, the voiceover line (teal rule), the sound and a note field; the frames wrap into a grid inside
  their row — never a sideways scroll, which hid frames off the right edge (2026-10-03). A pick is a green ring plus a filled "Pick" button; the player's track is cut into
  segments sized by shot length (a split bar — the parts make the whole runtime), green where a shot
  has a pick, teal where the playhead is. Pair with `.r-compare` to flip every row to one room or one
  look, and `.r-answerbar` to copy the picks back.
  *Never* dims an unpicked frame. *Never* reorders shots — the order is the cut. *Never* a frame
  without what varies about it (room, angle, look) under it.
  Every frame carries its permanent number big in the corner (`.r-board-frame-tag`) — the one handle the reviewer
  says out loud ("lock 212"); a locked frame wears `.is-locked` (heavier green ring) and leads its strip.
  The full-screen viewer (`.r-board-viewer-*`, /fit 2026-10-03) shouts only two things over the picture —
  the shot (number + its name) and the frame number — shows the shot's current lock in a corner (hold Space
  to flip to it) and a filmstrip of the set below. Never round numbers, source frames or "new" chips: none of
  them changes "lock this or not". A `?review=527-535` link lines up exactly the frames being asked about.

- **Time bar with named lanes** — `.r-timebar.r-timebar-wide`: the take check's time bar with a wide label column, so each lane can carry a name (a demo's acts, a plan's phases). Lanes top to bottom are the intended order; bands left to right are what actually happened, so changing lanes reads as jumping. Built 2026-10-27 for a demo plan. *Never* more lanes than fit one screen (about 12).

- **Take check** — one row per take: its name as the heading, the video (muted, looping, controls on, loaded
  only when scrolled near) over the time bar, and beside it the grade, the label/value pairs and the faults.
  The time bar is one lane per kind of thing on ONE scale from 0 to the take's length (`--len`): the suggested
  cut is a green band, the action a teal tint with marks at start, peak (the dot) and settle, each fault a red
  band on its own lane. Every band, mark and time chip is a button that seeks the video; a thin line is the
  playhead. The chips under the bar repeat each time in words, because two marks 0.2 s apart cannot be told
  apart on the bar.
  *Never* a time shown that cannot be clicked. *Never* a second scale inside one bar. *Never* a fourth color.
  *Never* a file path as a take's name — "Image 551 — Manager sees the app appear".
