---
name: image
description: Run an AI image-generation project the reliable way. Gemini or OpenAI image models behind one prompt list, the same project folder every time (references, rounds named for their one variable, picks, finals), a click-to-pick gallery with numbered images, a side-by-side compare and flip view, reference-image (img2img) rules, full-size finals, and the exact cost of every call. Use when the user says "/image", "generate images", "make me an image / logo / icon / poster / illustration", "img2img", or starts any project that produces AI images.
---

# /image: image-generation projects

The user is usually not a coder. Talk in plain words, never paste code or JSON at them, and do
every technical step yourself. Name images by their number only ("7 and 19 are the strongest"),
never by file name or model name.

## 0. Load the rules first

Read `IMAGE-BIBLE.md` (beside this file) before anything else.
- **Part 1 is law** for every project: one place for the eye, copy real references, specific
  beats generic, concept and copy approved before pixels, a locked series anchor, never let the
  model render text, judge at the size it ships.
- **Part 2** is the round protocol this skill runs.
- **Parts 3 to 5** are how the models really behave; read Part 5 before any reference-image round.

Below, `SKILL_DIR` means this skill's folder (normally `~/.claude/skills/image`) and `PY` means
`~/.claude/ai-tools/venv/bin/python` if that file exists, else `python3`.

## 1. First run: folder, keys, packages

Check all three at the start of every project; each takes one command once it is set.

**Projects folder.** `PY SKILL_DIR/scripts/new_project.py --where`. If it says `not set`, ask the
user which folder their image projects should live in, suggesting `~/memory/images`, then save
the answer with `PY SKILL_DIR/scripts/new_project.py --set-folder "<their answer>"` (this writes
`~/.claude/ai-tools/image.json`; later runs read it and don't ask again).

**Keys.** `PY SKILL_DIR/scripts/generate-template.py --check` says which keys and packages are
present (it never prints a key). Keys come from the `OPENAI_API_KEY` / `GEMINI_API_KEY`
environment variables, or from `~/.claude/ai-tools/keys.env` (readable only by the user). One
service is enough; use whichever they have. If they have neither, ask which they'd like and tell
them plainly how to get one:
- OpenAI: platform.openai.com → API keys → Create new secret key (needs billing set up).
- Gemini: aistudio.google.com → Get API key → Create API key.

Then collect it without it ever landing in the chat:
- **In T3 Code** (the `mcp__t3-code__request_secret` tool exists; load it with ToolSearch): call
  it with `delivery: "file"` and a clear label ("OpenAI API key"). The user pastes into a private
  box. Save it with `PY SKILL_DIR/scripts/save_key.py OPENAI_API_KEY --from-file <file>`. Never
  read, print or `cat` that file.
- **Anywhere else:** ask the user to open a separate terminal window and run
  `python3 ~/.claude/skills/image/scripts/save_key.py OPENAI_API_KEY` (or `GEMINI_API_KEY`), then
  paste the key there when asked; the paste stays hidden.
- Never ask them to paste a key into this chat: chats are saved. Never echo a key, put it in a
  command line, or write it anywhere except through `save_key.py`.

**Python packages.** Always `pillow`; plus `google-genai` for Gemini and/or `openai` for OpenAI.
Optional: `vtracer` (SVG tracing in finals) and `backgroundremover` (transparent backgrounds; a
large download). Install with `python3 -m pip install --user pillow openai` (only the services
they use). If pip refuses with "externally-managed-environment" (PEP 668: most Linux
distributions and Homebrew Python on Mac do this), make a private environment once and use it
for every script from then on:

```bash
python3 -m venv ~/.claude/ai-tools/venv
~/.claude/ai-tools/venv/bin/python -m pip install pillow openai google-genai
```

## 2. Models and money

**Two services, one prompt list.** The model ids live in one constant, `MODELS`, at the top of
`generate.py`; one edit upgrades everything.
- **Gemini:** `gemini-3-pro-image` through the `google-genai` SDK (never the old
  `google-generativeai`).
- **OpenAI:** `gpt-image-2.6-flare` for fast, high-quality generation; `gpt-image-2.6-sunburst`
  for precise editing (used automatically when a prompt carries reference images).

A prompt with no `model` uses Gemini if there's a Gemini key, else OpenAI. `"model": "openai"` or
`"model": "gemini"` picks a service; a full model id is used as is. **To compare services,
duplicate a prompt with a `-oai` name suffix and `"model": "openai"`**: one round, one gallery,
the service as the labelled variable.

Which one when (a starting bet, not a ruling):
- **Gemini:** anything needing 4K, and faithful derivations (a twin that must not move). On a
  remaster with the source as the only reference, Gemini returned a near pixel-copy: it honours
  "keep" and does no cleanup.
- **OpenAI:** dense correct text inside the image, keeping a subject from reference photos,
  edits that must leave the rest of the frame untouched, and remaster/cleanup of an existing
  image (the edit model actually redraws it: faces defined, signage legible, composition held).

Differences that bite: OpenAI takes pixel sizes, not ratios. The script maps the aspect to
`1024x1024` / `1536x1024` / `1024x1536`, but any `WxH` in multiples of 16 up to 3840 on the long
edge works: pass `"size": "2752x1536"` per prompt to match a source image exactly. OpenAI has
`quality` (low / medium / high / max) where Gemini has 1K / 2K / 4K, and does reference images
through a different call (`images.edit`, already wired).

If a run prints NOT VERIFIED, the OpenAI account must verify its organization (platform.openai.com
→ Settings → Organization → General → Verify Organization; photo ID, up to 15 minutes to take
effect). Until it clears, `gpt-image-2` is a working fallback: set it in `MODELS`.

**Before a new project, check for newer models:** `PY tools/generate.py --models` lists the image
models the user's keys can reach. If a newer one than `MODELS` exists, say so and use it; never
silently stay stale.

**Every paid call's cost is known to the cent, never estimated from memory.** Three parts, all
built into `generate.py`:
1. **Every call is logged** as it happens to `tools/usage.log`: model id as the API reports it,
   input tokens split into words and pictures, output tokens, a time stamp.
2. **One price table**, `tools/prices.json`, copied from each vendor's own price page with the
   page's URL and the date checked (never from this file, never from recall). The starter table
   carries OpenAI's image prices read 2026-11-04 and no Gemini row. Before the first round of a
   new project, open the price page for each service in use (OpenAI:
   developers.openai.com/api/docs/pricing; Gemini: ai.google.dev/gemini-api/docs/pricing),
   update or add the rows (dollars per million tokens: `in_text`, `in_image`, `out_text`,
   `out_image`), and update the date in `_sources`. Re-read the page whenever a model id changes.
3. **One command prints dollars per model and the total:** `generate.py --costs`, and every run
   ends with it. That total goes in every round report ("this round: 12 images, 1 dollar 60").

A model with no price in the table prints as UNPRICED; report it that way, never guess.

Rough feel, for planning only: Gemini about 13 cents an image at 1K/2K and 24 cents at 4K;
OpenAI bills image output by the token, so `quality` is the cost dial (a low-quality square is
well under a cent, high quality near 12 cents). Iterate cheap; full size is for finals only.

## 3. Project folder: same layout every time

`PY SKILL_DIR/scripts/new_project.py "<project name>"` makes (or reuses) the project inside the
saved projects folder and prints its path. Add `--compare` for big same-composition images (see
section 4). It copies the starter kit into `tools/` and never overwrites anything.

```
<YYYY-MM> <project name>/
  refs/style/     form references: the real thing it should FEEL like
  refs/donors/    single clean specimens cropped from style refs (crop_donors.py)
  refs/subject/   photos of the real subject
  rounds/01 <what this round asked>/   every generation, versioned names, never overwritten
  rounds/02 <what this round asked>/   one folder per round, named for its ONE variable
                  ("02 colder palette", "05 clay plus swatch sheet"), never a bare number
  picks/          the winners, copied out of their rounds: what the next round starts from
  finals/         full-size masters, plus flat and SVG versions when needed
  tools/          generate.py, gallery.html, manifest, prices, usage log: nothing the user opens
                  except the gallery
```

Every folder the user opens is a noun they would say; everything a script writes sits under
`tools/` or is one of those nouns. The round folder's name is the round's one variable, so the
tree reads as the project's own history without opening a file.

## 4. The starter kit: copy, don't rewrite

Templates live in this skill's `scripts/`; extend them here, not per project.

- `generate-template.py` → `tools/generate.py`. `MODELS` constant, prompts as a list of dicts,
  optional refs per prompt (ONE style donor max), threaded batch, rate-limit retry, named round
  folders (`--round "02 colder palette"`), manifest rebuild, cost log. Edit only `PROMPTS`.
- `gallery-template.html` → `tools/gallery.html`. Its one job: pick winners from a round, judging
  each image big and at the size it ships. Left nav (title, view switch, rounds → ideas with pick
  counts, Picked only, Copy picks); grid grouped by idea; click an image for a full-size viewer
  (Fit / Actual pixels, ← →, Space picks, Esc); the ✓ on a card picks. Edit ONLY the `CONFIG`
  block: `title`, and `surface` when the image ships into a known surface (a phone lock screen,
  a card, a hero slot); the page then adds a view drawing every candidate inside that surface
  (`?view=surface`). Grouping comes from the label: the text before " · " is the idea.
  **Every image has a plain number.** `generate.py` gives each new image the next number,
  project-wide, in `tools/numbers.json`, never reused or renumbered; a final keeps its draft's
  number. The gallery shows it big on each card and in the viewer, ← → walk in number order,
  typing a number jumps to it, and Copy picks gives "7 — label" lines the user can paste back to
  you. Numbers live in the page, never drawn onto the image.
- `gallery-compare-template.html` → `tools/gallery.html` **instead of the grid whenever the
  candidates are big same-composition images** (hero art, remasters, light/dark twins). One big
  image with Flip (hold Space or press the image to see the reference in the same spot), or two
  panes side by side; ← → step through candidates. Set `TITLE`, `SUBJECTS` and `STAGES` at the
  top of its script: one rail entry per subject, each with a fixed reference and a pattern that
  claims its candidates by name; one pick per subject; a last catch-all subject swallows
  experiments. The grid is for small objects; hero images need to be seen big and compared.
- `composite.py`: paste one region of a candidate over the untouched master with a feathered
  mask. Only for hard-edged plates (a laptop screen, a sign, a solid background), never for
  people or light.
- `crop_donors.py`: cut single specimens out of group reference photos into `refs/donors/`.
- `finalize.py`: full-size master → flat version → SVG (`vtracer`).

Both galleries read the manifest `generate.py` writes (`manifest.json`, plus `manifest.js` so the
page also works opened straight from disk). Picks are remembered by the browser, per gallery.

## 5. The loop (bible Part 2, in practice)

1. **Collect** references with the user: subject photos and form references. Crop donors.
2. **Words first.** Concepts and ALL copy written in the reference's own voice, approved by the
   user in text before any generation runs.
3. **Round 1: matrix.** Styles × concepts with `--draft`. Rebuild the manifest, give the gallery
   link, the user picks styles.
4. **Rounds 2+: converge.** One variable per round; winners become the next round's donors.
   Batch 6 to 20; show everything.
5. **Finalize.** `generate.py --final "<round>/<name>"` for each pick (one generation from the
   draft, at full size). Then Pillow cleanup if needed (palette snap, colour match), and
   `finalize.py flat` / `trace` when a flat or SVG version is needed. Composite real text and UI
   afterwards.
6. **Verify with your own eyes before reporting.** Models drop about 1 instruction in 5. Look at
   every batch: composition honoured, text exact, subject on-model. Also look at every candidate
   downscaled to the smallest width it ships at.

## 6. Showing the user

- After every round: the manifest is rebuilt by the run; give the gallery as a link. If
  `~/.claude/bin/files-server` exists, get an http link with
  `~/.claude/bin/files-server url <absolute path to tools/gallery.html>`; otherwise give the
  absolute file path (it opens in any browser).
- Each round report says: what changed (the ONE variable), how many images, the gallery link,
  the cost of the round and the project so far, and what you need picked.
- When the user picks, copy those images into `picks/`.
- Save the exact prompt that produced every keeper: the `PROMPTS` list in `generate.py` IS the
  record; never delete a prompt that made a keeper.

## 7. Reference-image (img2img) quick rules

Full list: IMAGE-BIBLE.md Parts 3 to 5. The ones that bite most often:

- ONE style donor per request; several average into mush.
- Lean prompts with a ref attached; don't re-describe what the image shows.
- CHANGE/KEEP structure when editing; without KEEP anchors the composition drifts.
- Attach a donor when the round varies rendering; attach nothing when it varies composition.
- No micro-nudges: remove the element (check the clean result), then re-add it positioned.
- Adding a new element = re-roll the keeper's original prompt with it written in, never edit it in.
- Never chain edits: every image stays one generation from its sharp master; a new tweak re-runs
  the whole change list from the master.
- Edits are full-frame (whole source as the reference, strong KEEP lock), never masked; colour
  match back to the original in Pillow if it drifted.
- Explore with `--draft`; only picks go to `--final`. Never roll a batch at max to explore.
- End every cleanup edit with the lock: "exactly as dark as the attached photograph, no fill,
  nothing lifted; whatever is out of focus stays exactly that soft; add no new words anywhere."
- Negative constraints physical and explicit ("exactly ONE bolt", "stays upside down").
- Transparency: solid #FFFFFF background + `backgroundremover`, never ask the model.
