# HTML pages for the user — one method, one sheet, a shelf of blocks

Every big document Claude gives the user — to review, decide from, or learn from — is one of these
pages. The goal: richer communication bandwidth. The richer the communication, the more aligned
you are, and the more efficient and creative the work gets. A page that makes the user reread, or
reply "which one?", spends that bandwidth instead of building it.

**Who your reader is lives in `READER.md`.** Read it first. Every rule below is a rule about that
person, and a few of them flip when the person changes.

## How this works, start to finish

1. **Say the whole thing out loud first** — the speech, in plain sentences, across a desk.
2. **Ask what you are presenting.** Is this a decision? A mission? Findings? Proof? Teaching? The
   thing itself? Name the job by what the user has to DO. Most pages are two jobs at once.
3. **Shop the shelf** — `BLOCKS.md`. Blocks are tagged by the
   kind they are at home on, and any block may go on any page **when the connector test passes**.
4. **Build only from `report.css`.** Three lines at the top of the page, no libraries, no build step.
5. **Screenshot it, look at it, walk the self-check**, then hand over the link (§7).

---

## 1 · The method — write the speech first

**Before any HTML: say the whole thing in a few plain sentences.** What happened. What it means for
the user. What they need to decide. A page that can't be said out loud first becomes an essay — and
essays are what get rejected.

**The speech is the draft, never the render.** It expands into blocks — drawn rules, cards, chips,
hero numbers — not into paragraphs. Rendering the speech as prose is a wall of text that does
nothing with HTML; the whole point is to show things using the visual components and typography
sizing. Short doesn't mean two paragraphs; it means few blocks, each carrying one point. **A
finished page has no prose block over ~3 lines** — anything longer is a block that hasn't been
drawn yet.

1. **The headline reads like a book title, and it names the subject.** Short, plain, one thought,
   no quotation marks, at most one dash — but the actual thing has to be in it. A page about the
   HTML reports says "HTML report" in the title; a page about the task system names the task
   system. "Rebuilding how you get told things" fails exactly this: evocative, and it names
   nothing. The test: the user wrote the underlying idea six months ago and remembers none of it;
   the title alone tells them what the page is about. Never a tease, never a quoted phrase up
   front, never clause chained to clause. **The same applies to every h2** — "The whole thing runs
   on one file now" fails it; "Every report page runs on one stylesheet now" passes.
2. **The line under the title describes the page in a handful of words, with no data.** "Five payout
   providers, compared." The data arrives where it lives, in blocks.
3. **When the page opens a subject the user hasn't held for months, introduce it cold.** Never "the
   test / the plan / the question" before saying what it is — *"You checked what? Which test?"* is
   an instant rejection.
4. **Every h2 is a sentence of the speech.** Extract the headings and read them as a paragraph
   before handing over: 15 seconds of headings and 6 minutes of full reading must reach the same
   conclusion.
5. **Evidence sits against the sentence it proves.** Never a separate evidence pile to join back up.
6. **Answer first, teach inside, the user's calls at the end of the section that makes them
   answerable, one recap last.** Both, not either: the question appears inline where they can
   answer it, AND the "Needs your attention" section at the foot indexes every one so a skim misses
   none. A page whose questions live only at the bottom makes them scroll back to answer.
   **One numbered list, one order.** Number every question once, in page order; the inline ask shows
   its number, the recap lists the same numbers in the same order with the same words, and the chat
   reply copies the recap. Never a verdict rail or recap that reorders them — a reply in recap order
   against inline asks in reading order is crossed wires.

On "advertising copy": this means the directness — benefit first, plain claim, no build-up — not
the selling tone. **State it like an ad, prove it like a report.**

---

## 2 · What am I presenting? — the six jobs

**Name the dominant job by what the user has to DO**, not by how much of the page each job fills.
If they must answer something, it is a decision however long the teaching runs. If they only have
to understand, it is an explainer however many numbers appear.

| Job | The ask, in the user's words | Answers first with | Required blocks |
|---|---|---|---|
| **Mission map** | "Bird's-eye view of this huge project so I don't lose track" | stat row or tally | timeline rail · status marks · asks |
| **Decision** | "Decide this with me" | decision cards | my call · asks |
| **The thing itself** | "Show me the actual screen, not a description of it" | embedded prototype | numbered notes · asks |
| **Findings** | "Go find out and tell me what to do" | verdict plate | admitted-flaws row · my call · asks |
| **Proof** | "Show me it actually works" | tally | evidence pairs · what this does not cover |
| **Explainer** | "Help me understand how this works" | callout, or the first stage of the metaphor | a carried sequence or drawing · recap |

Six is the whole list to start from. A seventh gets added only when the reader regularly asks for
something none of the six covers — named by what they have to do, with its own answer-first block
(`READER.md` §2). **Drawings are not a seventh job** — the assembly line, nesting doll, split
bar, miniature and before/after are elements the six build from, the same way a table is.

**The explainer is the craft job.** Give it the most drafting care: one metaphor mapping 1:1 to real
parts (recipe card → kitchen → plate is the standard), every new term getting a household name with
the real name beside it, once, where it lands.

### Mixing two jobs — three rules, in order

1. **The dominant job owns the spine** — the answer slot and the section order.
2. **Take the union of required blocks, never the union of spines.** The secondary job's
   answer-first block drops. A page answers once.
3. **The page never switches format halfway down.**

*Worked — a page that is both an explainer and a decision:* the user has to answer, so it is a
decision. The cards go near the top with the recommendation pre-filled, the teaching earns them
underneath, my call sits at the end of the section that makes it answerable, and "Needs your
attention" closes it — the explainer's recap drops. Flip it so the choice is already made and
exactly one thing changes: the cards move down, lose their radio, and become the illustration of a
decision taken.

---

## 3 · Picking a block — form follows function

Three completely different things that have nothing to do with each other, laid out in a sequence
line only because the one-two-three boxes with arrows exist, is exactly what not to do. The form
follows the function for all displays on all pages.

**Having a block is never a reason to use it.**

### The connector test — say it out loud before you draw

Every arrangement makes a claim about how its items relate. Read the claim aloud. **If the sentence
is a lie, the shape is wrong.**

| Drew | Claims | Read aloud |
|---|---|---|
| cards with arrows | order | "A **then** B **then** C" |
| a rail with dots | happened, at times | "A **happened**, then B" |
| nested boxes | containment | "B is **inside** A" |
| three stations growing | transformation | "A **becomes** B" |
| a bar cut into slices | parts of a whole | "A **plus** B **equals** the total" |
| bars on one scale | magnitude | "A is **bigger than** B" |
| a grid of equal cards | peers, no order | "A **and** B" |
| a table | the same questions of each | "for each: price, size, verdict" |

Peers want "and", so peers want a grid — never arrows.

### The four drawing laws

- **Size means importance.** A bigger block claims it matters more. If it doesn't, shrink it.
- **Position means order.** Left to right, top to bottom, is a sequence claim. Don't make it idly.
- **Nesting means containment.** A box inside a box says the inner thing belongs to the outer one.
- **Color keeps its four meanings, always** — green good/done/the pick · amber
  waiting/caution/your call · red broken/dead/ruled out · teal informational, in flight, magnitude,
  links. Everything else is grayscale surface. **A color appearing without its meaning is a bug.**

### The fact test — does it change a decision?

Before a fact, figure, chart or section earns its place: **does the user make a different decision
because it's here, given what this page is for?** Stat cards used just because they exist, facts
shown because they are known, two charts because charts are available — all fail it.

- **Never draw what seven words can say.** A chart illustrating a concept rather than carrying data
  the user acts on is decoration.
- **The history of an idea is one line, not a section.** "It's called X, named by Y" — then move.
- **Numbers shown side by side share one axis** — same unit, same period, same subject. If they
  don't compare, they don't sit together.
- **No needless precision.** A third number that changes no decision comes off.
- **The cup test** — every block has a shape and a capacity. Text overflowing its cup means the
  wrong block, not a shorter label.

---

## 4 · The stack

Three lines at the top of every page. No libraries, no build step, renders years from now.

```html
<link rel="stylesheet" href="report.css">
<script src="report-table.js"></script>   <!-- only for 8+ row tables -->
<!-- theme toggle script at the foot — copy it from ~/.claude/skills/html/SKILL.md step 4 -->
```

**The sheet sits next to the page.** Every page lives in a folder of its own, and `/html` copies
`~/.claude/skills/html/assets/report.css` (and `report-table.js` when a table needs it) into that
folder. So the link is just `report.css`, and the page renders the same served over http or opened
straight from disk. **Relative, never absolute — and that goes for every internal link on the page
too.** An absolute path only resolves while a server is up; open the file from disk and the page
renders unstyled with every link dead. A page copied before the sheet changed keeps its old copy;
copy the sheet over it again to bring it up to date.

- **`assets/report.css`** — the whole system: four semantic hues in light and dark, the type
  scale, the spacing scale, every block with its FOR / HOLDS / NEVER at the source. The **drift
  knobs** are named at the top: `--stage`, `--measure`, `--r-plate`, `--r-chip`, `--sec-gap`.
  Change one and every page linking the sheet follows.
- **`assets/report-table.js`** — search, sortable headers, per-column filters, dismissable
  pills, clear-all, phone card mode. It reads the table already in the page, so the data lives in
  the markup and the page still reads with the script missing. Columns lock their widths on load:
  **sorting moves rows, never columns.**
- **`BLOCKS.md`** — the tagged catalog. Read it before composing.

`report.css` is the only stylesheet a page links.

**Every page is built only from blocks in the sheet.** A genuinely new block gets built INTO
`report.css` and listed in `BLOCKS.md` the same turn — declared and reusable, never inline as a
one-off. If a block looks wrong, fix it in the sheet so every future page improves.

### Standing craft rules

- **Hierarchy by size, weight and color only.** Never underline, box, or capitalize something into
  importance. No all-caps letter-spaced labels anywhere. No eyebrow labels — roll the word into the
  title. Headings are sentence case.
- **A recommendation is an opinion and never wears a badge** — recommendations are not badges, they
  are your opinion. It uses `.r-mycall`.
- **A ruled-out row is never dimmed or struck through.** The reader is still comparing against it.
- **A sequence carries no numerals.** Numerals only where something must be cited by number — proof
  claims and asks. Off section headings.
- **Status is dots on pages, glyphs in chat.** On a page: the mark AND the word, filled = firm
  state, hollow = fading or pending. In chat: the status glyphs in `~/.claude/ai-tools/rules/reply-format.md`.
- **Containment is a rule.** Every grid uses `minmax(0,1fr)`; wide tables scroll inside `.r-tablebox`,
  never the page; on a phone a comparison table becomes one card per row wearing its column names.
  **Never `overflow-x:hidden` on `html` or `body`** — it breaks scrolling in Chrome.
- **Prose runs the stage.** No measure cap: a paragraph is as wide as the page, because a narrow
  column leaves a ragged half-empty right side that reads as a mistake. **No margin notes** — a
  fact that changes what the user does goes inline in the sentence it changes; a fact that does
  not goes nowhere.
- **Blocks size to their content**, never stretch to fill the stage.
- **State fills are solid, not borders.** Bolder reads faster.
- **Verdict bars are rare** — one or two per page. An alert under every component is annoying.
- **Light and dark are both first-class**, sun/moon toggle top-right, dark default, choice
  remembered.
- **US conventions**: 12-hour time, $, American spellings — center not centre, catalog not
  catalogue, canceled not cancelled, gray not grey, color not colour. No emoji. ✓ and ✗ may carry a verdict;
  nothing else pictorial. No exclamation marks. Never the word "successfully".

---

## 5 · The register

### The seven laws — what earns a sentence

These came from a blind bake-off: eleven writers wrote the same page, and the arm following an
older register section lost every duel to the same model writing with no rules at all. The laws
below are the diagnosis of why.

1. **Say it. Never set it up.** At the end of every sentence the user must know more than at the
   start. "One real fix, one silent failure caught" teaches nothing — don't set the reader up and
   lead them with clickbaity lines; just say what happened. A sentence whose only job is to make
   them read the next one is deleted, not rewritten. Counting — "three changes landed", "five
   product rules that don't exist yet" — is the same failure wearing a number, and it is the
   version most likely to survive a self-check, because it is short and exact. **The test: if the
   line still works with the number swapped for any other number, it is carrying nothing.** It is
   "ten recipes you won't believe": what are they? It tells the reader nothing.
2. **Name it in the user's words, before you use it.** If it says "the controller", the reader is
   already confused: what controller? Is that the router? Use the names they use.
3. **Establish the thing before the event.** What it is, where it runs, what it does for the user —
   then what happened to it. Never open mid-event at a timestamp with an unnamed subject.
4. **Situation, action, consequence**, in that order, in plain verbs: "whenever you uploaded
   anything it was stalling the whole network, because this." **One list per sentence, and the verb
   stays near its subject.** Two stacked lists force a reparse — *"what publishing, canceling,
   moving and announcing a whole series currently do to a postponed, canceled or draft date"* is
   four items, then three, with the verb twelve words from its subject. Split it into two short
   sentences, or move one list into the bullets below.
5. **Length follows importance. Symmetry is a defect.** Blocks all the exact same length mean the
   writer is filling a shape instead of saying a thing. Bullets are the default; a paragraph earns
   itself.
6. **Only numbers the user would act on. No clock times in prose.** Drop ranges, addresses and
   identifiers they will never type. Dates and times go in a list at the foot of the page.
   **Never a relative date.** "Last week", "this morning", "today", "yesterday" — the page may be
   opened in two months, and the sentence goes quietly wrong without anyone touching it. Absolute
   dates only, with the year, and only where the date carries weight.
7. **Never dramatize.** No emergency, no silent failure, no "what nearly went wrong", no story arc.
   A real risk is a fact plus its cost, which lands harder than the drama anyway.

### The register

1. **Verdict word first, reason second.** "Correction — 3 files, not 5."
2. **Exact nouns, always.** If the user could reply "which one?", it isn't written yet — and the
   fix is more words, not fewer.
3. **Corrections without apology.** Errors are facts.
4. **Emphasis is surgical** — one bold word. No sprays, no emoji, no exclamation marks.
5. **Dry humor unmarked, one per page, only if true.**
6. **Supply the criterion when asking the user to judge**, stacked as separate lines.
7. **Eloquence when earned, never decoration.** Plain fact first, its name second: "More choices,
   slower decision. It's called Hick's law" — never the name leading.

---

## 6 · Before handing over — the self-check

Walk this on the real render. Redesigns die on execution, not intent.

1. **Screenshot the page and look at it** — containment, typography, alignment. Never hand over
   unseen pixels. Check 390 and 1440.
2. **Read every arrangement's connector aloud.** Arrows say "then", a rail says "happened", a grid
   says "and". A shape claiming something the content doesn't support is a defect, not a style
   choice.
3. **Read the title and the line under it cold, as a stranger.** Two tests:
   - **No context.** Someone who knows nothing opens the page — do they know what they are about to
     read? *"Nobody has ruled on any of these. Whatever the code does today is the rule."* Read
     with no context, there is no idea what is coming: nobody has ruled on any of what? That could
     be about absolutely anything.
   - **Two weeks later.** Does it still mean something when the user opens it cold in a fortnight?
   The title names the subject in plain product words. **Never open it with jargon**, and never with
   a coined compound — starting with a jargon word and a hyphen ("Run-wide …") reads as weird.
4. **Extract the h2s and read them as a paragraph** — do they carry the argument alone?
5. **Does the page break any rule it states?**
6. **Every claim has its proof beside it.** "You haven't backed up what you're saying" is an instant
   rejection.
7. **Follow-up test on every noun** — could the user reply "which one?" or "what is that?"
8. **Search what is already written down for every question before you ask it.** A findings page
   asks the user for facts; the project's notes, docs or task tracker often already hold them,
   written by an earlier session. Search for the page's nouns BEFORE drafting: it saves asking the
   user something they already decided, and it catches work marked closed that is not settled.
9. One dry aside max · no enthusiasm · no process narration · counts carry their consequence.

---

## 7 · Delivery

Write the page to `~/memory/sessions/YYYY-MM-DD-topic-slug/<name>.html`, or the repo's `docs/`
folder when it is about a repo, with the sheet copied beside it (§4). Hand it over as a link: if
`~/.claude/bin/files-server` exists, `~/.claude/bin/files-server url <absolute path>` prints an
http link that opens anywhere; otherwise give the page's absolute path. A **sources line** — what was checked, what was not, the date, the links — closes
findings, proof and mission pages only; decisions, explainers and mockups end where the format
says.

### Self-contained — say it once, get a standalone file

**When the user says "self-contained", or the page is for anyone else, `/html` also writes a
standalone copy in the same folder — no extra ask, no second turn.** The normal page links the
sheet sitting beside it; a linked page mailed to someone else, without that file, renders as
unstyled text. Both files ship: the linked page stays live, `<topic>-standalone.html`
beside it is the one that travels.

```python
from pathlib import Path
src = Path('<topic>.html')
css = Path.home() / '.claude/skills/html/assets/report.css'
link = '<link rel="stylesheet" href="report.css">'
Path('<topic>-standalone.html').write_text(src.read_text().replace(link, '<style>\n'+css.read_text()+'\n</style>'))
```

Verify it by copying the standalone somewhere the relative link cannot reach and screenshotting it
over `file://` — that is the only check that proves it travels. The Google font link stays external
and falls back to the system font offline; layout and color hold, so leave it. **Editing the linked
page later does not regenerate the standalone — rebuild it in the same turn.**

**The split between a page and markdown is by reader, not by document type.** Anything the user
opens is a page: brief, plan, decision, status page, digest, findings, proof, mission map,
explainer, mockup. Markdown is only for what agents read — session notes, agent-to-agent handoffs,
skill and rule files. A status page and a digest are for the user, so both are pages. Small things
in a T3 Code thread go in chat as a chat-kit page, documented at
`~/.claude/ai-tools/chat/README.md`; in a plain terminal they stay ordinary chat text.
