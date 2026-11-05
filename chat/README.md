# Chat kit — glanceable blocks for T3 Code chat pages

A reply page is one script tag plus a few `<k-*>` tags written as plain lines:

    <script src="https://cdn.jsdelivr.net/gh/punkhop/ai-tools@v1.0.0/chat/kit.js"></script>
    <k-page> …blocks… </k-page>

Render it with T3's `html_preview`, then `html_render`. The kit draws with T3's own theme colors,
so pages follow dark/light and fit 728px desktop and ~360px phone. `kit.js` beside this file is
the same code the script tag loads; the tag is pinned to v1.0.0, so a page never changes under you.

## The five reply shapes — copy one, never compose a new one

Wrap every reply page in `<k-reply s="…">`; it sorts blocks into Head → Show → Links → Status →
Questions and writes the default status bar for `ok` and `needs` (count taken from `k-qs`).

    Start      <k-reply s="work"><k-mission title="Job name">What this thread does, in user terms.</k-mission>
               <k-status s="work">Working · first step⏎No questions yet.</k-status></k-reply>
    Working    <k-reply s="work"><k-head>work Page · what the user gets</k-head><k-status s="work">Working · doing what now⏎No questions.</k-status></k-reply>
    Needs you  <k-reply s="needs"><k-head>needs …</k-head> [Show: k-choose or the thing to review] [k-links] <k-qs>question | my call</k-qs></k-reply>
    Done       <k-reply s="ok" note="path or URL of the session note written THIS turn"><k-head>ok …</k-head> [Show] <k-links>…</k-links></k-reply>
    Waiting    <k-reply s="wait"><k-head>wait …</k-head> <p>why it waits</p> <k-links>…</k-links>
               <k-status s="wait">Waiting on <what> · safe to close⏎Who picks it up.</k-status></k-reply>

`⏎` in this file means a real line break, never the character.

**The green Done bar needs `note="…"`** — the session note written this turn by the `/note`
skill (the Skill tool, never a hand edit). With no `note`, the kit prints "Not finished · no
session note linked" in red instead of green. That is on purpose: green is a claim, and it carries
its proof.

Design rules: the head is plain title text, never a bar · section headings are sentence-case
text, never all-caps eyebrows · lists are one grouped container with hairlines, the note under
the title, never a pill pinned to the far right · no count tiles, no dots, no invented headings ·
Needs you ends on one "Questions" list, no bar or prose prefacing it.

## Endings — every reply closes on exactly one

`ok` Note written (a link to the note file) · nothing left (no subagent, shell or render this chat
started still running) · `needs` Answer questions 1–N · `do` Your turn: the thing to do by hand ·
`work` Working · what now (mid-turn only) · `wait` Waiting on <what> · safe to close.

## Show is ONE block

A screen → `k-pair` (screenshots) · only words → `k-words` · a taste call → `k-choose` · several
screens → `k-flip` · a live page → `k-shot` · no screen → `<p>`.

Never a whole prototype or multi-pane screen in a `k-pair`/`k-choose` — at 728px it is unreadable.
Crop to the one part that matters, and put the full page's link first in `k-links`
(`data-k="open full page"`) and as the reply's first text line. Full pages come from the `/html`
skill.

`k-trail` only beside Show, only when the route changes what the user believes. Chat text under
the page: one line at most. A plain answer with nothing changed: text only, no page.

Status words: `ok` ✓ · `needs` ? · `work` ◐ · `wait` ○ · `bad` ✗. ` ~ ` adds a right-side note.

| Tag | Short form | Use when |
|---|---|---|
| `k-mission` | `<k-mission title="Job name">This thread…</k-mission>` | first reply of a thread started from a brief |
| `k-head` | `Title ~ subtitle`; several `status text ~ note` lines = a grouped list | top of every reply |
| `k-status` | `<k-status s="ok" note="note path">Note written · nothing left` + a real line break + `Safe to close this tab.</k-status>` | LAST block of every reply. Green only for ok, and only with `note=`. needs/work/wait are gray with a colored edge |
| `k-qs` | lines `question \| my call`; `start="20"` numbers from 20 to match the page they came from; a line opening `30. ` keeps that exact number | questions, headed "Questions" |
| `k-choose` | `<k-opt name="A · …" mine>…</k-opt>` | any taste call: draw each option |
| `k-pair` | children: `<img alt>` or `<div cap>` | before and after, side by side |
| `k-words` | lines `where \| was \| now` (empty was = new) | any copy/label change; one column |
| `k-shot` | `src="/abs.png"`, lines `x%,y% note`; `style="--h:380px"` caps height | point at things on a screenshot |
| `k-flip` | several `<img alt>` | a set of screenshots as thumbnails |
| `k-links` | `label="Done"`, `<a href data-k="note" [data-s] [data-kind]>Title</a>`; each row gets a colored kind icon + open arrow, kind read off the href (t3-thread → thread, github pull → PR, gallery.html → gallery, .md → note, .mp4/.mov → video, else page); `data-kind="page\|gallery\|thread\|pr\|task\|note\|video\|link"` overrides (a task link needs `data-kind="task"`) | PR, tasks, pages, threads as a grouped list |
| `k-trail` | `ok step > bad step > final` | only when the route changes what the user believes |
| `k-fold` | `<k-fold title meta>…</k-fold>` | long proof that stays shut |

**Capping a `k-pair` screenshot's height:** set `width:auto; max-width:100%` with the
`max-height`. A height cap on its own keeps the image at full cell width and squashes it.

Every image (shot, pair, flip) opens full screen on click; ←/→ flip through all images on the
page; Esc closes.

Rules: keep a page under 2,000px tall at 728px wide (T3 caps the frame there; the rest scrolls
inside it and gets missed). No outer card or title. Preview every page before sending and look at
the status bar: a link, no stray characters.

## A full example — Needs you

    <script src="https://cdn.jsdelivr.net/gh/punkhop/ai-tools@v1.0.0/chat/kit.js"></script>
    <k-reply s="needs">
    <k-head>needs Recipe app · shopping list, two calls left</k-head>
    <k-pair><img src="/abs/before.png" alt="Before: no way to add a recipe to the list"><img src="/abs/after.png" alt="After: Add to shopping list on the recipe"></k-pair>
    <k-links>
      <a href="file:///abs/shopping-list/index.html" data-k="open full page · 4 states">Shopping list prototype</a>
      <a href="https://github.com/org/repo/pull/44" data-k="draft">Add a recipe to the shopping list</a>
    </k-links>
    <k-qs>
    Merge the same ingredient from two recipes into one line? | Yes
    Tick items off, or swipe them away? | Tick
    </k-qs>
    </k-reply>
