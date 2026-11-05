# Image bible

The rules behind every `/image` project. Distilled from many rounds of real work across very
different kinds of images: illustrated scenes, photoreal editorial pictures, embroidered patch
art and app icons.

Part 1 is law for every project, whatever the style. Part 2 is the round protocol `/image` runs.
Parts 3 and 4 are how the models actually behave, learned the hard way. Part 5 is the
reference-image (img2img) rulebook.

---

## Part 1 · Universal principles (every project, every style)

1. **Decide where the eye lands first.** Every image has exactly one focal point; everything
   else supports it. How you get there depends on the kind of image (a spotlight in a stage
   scene, the cut-out silhouette of a patch, shallow depth of field in a photo, negative space in
   an icon). The universal part is the decision, not the technique.

2. **Emulate, never invent.** Every project starts by collecting the real thing it should feel
   like (real product photos, real vintage objects, a named photographer's work), then isolating
   single clean specimens as references ("donors"). Style described only in words produces "AI
   that looks like AI."

3. **Match the style to the subject.** Pick the style that tells THIS story best; don't default
   to the last project's look. Different styles per subject within one project can be a feature.

4. **Specific beats generic.** "A chipped enamel mug with a faded logo and a coffee ring," never
   "a mug." Real years, real object features, real named details. When output is off-model, the
   fix is a real photo plus a named feature list, never more adjectives.

5. **Concept before pixels.** The image exists to say something: a story, a moment, a joke. An
   image with no concept is decoration. Write the concept (and ALL copy) in text and get it
   approved before any generation runs. Words are free; images are round-trips.

6. **Lock the series with a repeated anchor.** Some anchor repeats word for word in every prompt
   of a series: a KEEP EXACTLY block, a photographer/camera/film sentence, a donor image.
   Identical anchors are what make N images read as one set.

7. **Judge at the size it will actually be seen at.** Every image ships into a surface (a card, a
   row, a hero slot, an icon well) and that surface is usually far smaller than 1024 pixels.
   Downscale every candidate to its real display width and judge only the small one. A candidate
   that reads at full size and turns to mush at card size has failed, however good the big
   version is.

   **This bites the type as hard as the picture.** Copy set in a thin strip of small capitals is
   beautiful at full size and a grey smear at card size. The rule that fixes it: the title's
   capitals stand at least a twelfth of the image's SHORT side (height on a tall poster, width on
   a wide cover) inside a solid full-width band, everything else at half that. Stating it against
   height alone shrinks the type to nothing on every 16:9 cover. An image whose words cannot be
   read at its display size has failed even when the artwork survives.

8. **Never let the model render text or UI.** It misspells, mangles spacing, invents fonts.
   Generate with a placeholder (TV static for screens, nothing for copy) and composite the real
   thing afterwards. Exception: when text IS the art (a patch, a badge), Claude writes it, the
   user approves it, and it goes into the prompt as exact locked copy.

## Part 2 · The iteration protocol

Projects run without this protocol have taken 13 to 22 rounds. With it, most converge in about 4.

0. **Collect real references first.** Subject photos plus form references; isolate single clean
   specimens as donors (Part 1, rule 2).
1. **Approve all words before any pixels.** Concepts and copy written in the reference's own
   voice; the user approves them in text.
2. **Style round before content rounds.** Test whole styles first (clean vector, ligne claire,
   risograph, anime, paper cut-out, graphic novel…) and commit to one before iterating any
   subject.
3. **One variable per round.** Composition → shape → text content → placement → colour. A round
   that changes two things wastes itself.
4. **Winners become donors.** Every polish round uses a picked output as the reference image; the
   style stays locked while the one variable moves.
5. **The user picks from a gallery.** Batch 6 to 20 per round, variants side by side,
   click to pick. Show everything: surprise winners come from prompts you'd have dismissed.
6. **Versioned filenames, never overwrite.** Keep the rejects; save the exact prompt that
   produced each keeper.
7. **Verify with your own eyes before reporting.** Models drop about 1 instruction in 5.
   Spot-check every batch: composition honoured, text correct, subject on-model.

## Part 3 · Series consistency

- **CHANGE/KEEP prompts.** Editing a reference: a numbered CHANGE list by region, then the KEEP
  EXACTLY anchor list. Without anchors the whole composition drifts.
- **Lean prompts when a reference is attached.** Don't re-describe what the reference shows:
  "the person from the reference image," not 50 words. Measured: about 40% shorter, more
  consistent.
- **Variant from the winner.** Need a sibling (a light version of a dark one, a second angle)?
  Make the main version first, then use IT as the reference and ask for "exact same composition
  and positions." Paired states change together (a dark scene gets a dark screen).
- **Edit the master, re-derive the rest.** The same fix applied separately to two files makes
  them diverge.
- **One style donor per request.** Several references average into mush.

## Part 4 · Mechanics and post-processing

- **A donor pins COMPOSITION hardest, so attach one only when the round varies rendering.**
  Varying rendering (style, colour, depth, 3D, material)? Attach a donor: it holds the
  composition still while the treatment moves, and one donor will happily give 20 distinct
  treatments. Varying composition (pose, angle, scale, crop, orientation)? Attach nothing and
  generate from text. A pose instruction against a donor comes back as the same picture with the
  instruction ignored, five times in a row (measured on an app-icon project: the round that
  varied pose off a donor produced near-identical frames; the next round dropped the donor and
  every pose landed). The trade is real: dropping the donor also drops the craft it carried, so
  get the shape from text first, then re-attach a donor to put the style back.
- **Micro-nudges don't happen.** "Move it slightly" returns a photocopy. Remove the element
  (check the clean result), then add it back at the described position: two generations.
- **Never name a letterform; describe its path.** Asking for "a capital M" makes the model fetch
  a typeset M and place it beside the subject. Describing the route ("climbs to a high point,
  drops to a low point, climbs to a second matching high point") plus "no lettering or alphabet
  character anywhere in this image" produces the letter as a drawn object, first try.
- **Unreadable type is fixed physically, never by asking for readability.** "Make the title
  legible" changes nothing; a style that implies small or low-contrast lettering beats a stated
  type rule every time. What works is measurable: the title's capitals at a named fraction of
  the image's short side (a tenth to a sixth), inside a solid full-width band, in a flat colour.
  Three failures from one round, all with perfectly correct copy: chrome lettering on a peach sky
  (invisible at thumbnail), Swiss minimalism taken literally until the poster was a rectangle
  with a smudge, and cut-paper letters that came out small and fussy.
- **A stated line count stops repetition only when each line also gets a POSITION.** "Exactly
  four lines, each appearing once" still repeats; "line 1 across the top third, line 2 beneath
  it, line 3 in the lower band" does not.
- **Naming a historical period for the lettering imports that period's spelling.** "Vienna 1901"
  returned QVEEN and OPERA HOVSE through two explicit bans; the Roman V is part of the style
  being asked for. Name the period for the ornament and palette; specify the lettering
  separately, in modern spelling.
- **The word "reversed" makes the model mirror the line.** Say "knocked out of a solid band"
  when you mean light type on dark.
- **Transparency: never ask the model.** It paints a literal checkerboard. Generate on solid
  #FFFFFF, then cut it out with `backgroundremover` for a clean alpha channel.
- **Negative constraints must be explicit and physical:** "the trailer stays upside down; do not
  right it," "exactly ONE bolt." Vague style words drift.
- **4K finals; Pillow (PIL) for cleanup** (palette snapping, masking), not prompts. `vtracer` for
  SVG, after re-saving the image as plain RGB.

## Part 5 · Reference images (img2img)

- **ONE style donor per request.** Several refs average into mush.
- On OpenAI, a prompt with refs goes through a different call (`images.edit`) on the edit model;
  `generate.py` picks both automatically. Everything below still applies.
- **Lean prompts with a ref attached.** Don't re-describe what the image shows.
- **CHANGE/KEEP structure when editing.** Without KEEP anchors the composition drifts.
- **No micro-nudges.** Remove the element (check the clean result), then re-add it positioned.
- **Edit the master, re-derive siblings;** ask for "exact same composition and positions" for
  pairs.
- **Adding a new element to a scene = re-roll the original prompt, never edit it in.** Paste-and-
  blend edits, two-step restyles and repainting a 3D blockout all failed (floating, ghosted
  props, then flat over-lit clay); a fresh draw of the keeper's own prompt with the element
  written in held up. Watch for: a reference image that contains a similar prop gets it copied in
  its own spot, and a word the base prompt already uses ("back wall") for another place.
- **Never chain edits. Every image stays ONE generation from its sharp master.** Each edit
  re-renders the whole frame and softens it; four edits deep the lines go wavy and the light
  muddles. Measured with a sharpness score (Laplacian variance): about 15% lost over four chained
  edits, recovered by regenerating from the master with the whole accumulated CHANGE list in one
  prompt. So the change list is the record: a new tweak means re-running the full list from the
  master, not editing the last output, and rolling several so the user can pick.
- **Don't composite regions of a drawn scene.** The seam reads instantly. `composite.py` is only
  for hard-edged plates (a laptop screen, a sign, a solid background), never for people or light.
- **Edits are full-frame, not masked.** Masked inpainting looks pasted on. An edit is always the
  whole source as the reference with a strong KEEP lock, then a colour match back to the original
  in Pillow if brightness or colour drifted.
- **Realistic faces: describe the photo, never ban the look.** The wording that read least
  plastic described a candid, unedited phone or camera photo of real people (skin texture, uneven
  light, ordinary faces) with no ban list. Never write the words plastic, airbrushed, AI or CGI
  in a prompt; naming the look pulls it in. An "open the eyes" fix opens squinting eyes too, so
  add "keep shut eyes shut". Colour drifted up to 12% on edits: match mean and spread back to the
  original. This is the best wording found, not a solved problem.
- **Sharpness on an edit** (Laplacian variance, master = 556): quality `high` 463 to 495, `max`
  509, rendering at 3840 wide then Lanczos down to the master's size 520. Always pass the exact
  `size`; `auto` picks its own canvas and resamples, a second softening. An unsharp mask inflates
  the score (825) by inventing edges; never ship one. **`quality: "max"` + 3840 wide + Lanczos down
  to the master's size made an edit sharpness-neutral (594 → 585 to 606).** That is the recipe for
  any edit on a keeper: max, 3840, downsample, one generation from the keeper.
- **Explore cheap, finalize big.** Every exploration round runs `--draft` (1K, quality medium).
  Only the pick goes to max: `generate.py --final "<round>/<name>"` redraws that exact draft at
  full size with a change-nothing prompt. Never roll a batch at max to explore.
- **A cleanup edit brightens, sharpens and writes words unless told not to.** Measured on a dark
  office photo: mean brightness 16.5 → 35.6; a soft crowd came back sharp; a mug grew a slogan.
  End every cleanup edit with a lock: "exactly as dark as the attached photograph, no fill,
  nothing lifted; whatever is out of focus stays exactly that soft; add no new words anywhere."
  That held 16.5 → 19.1. Measure brightness before and after. Never ask for "unreadable"
  lettering: say what each thing on the wall IS, or attach a set-dressing sheet as the second
  image so the wall is the same wall in every shot.
- **A real place is described from its photos, never from memory.** List what the room actually
  holds and name what the model keeps inventing ("no gold-framed mirrors, no big bright
  fixtures"). Crop the room refs below anything you don't want copied; otherwise the model adds
  the same mirrors and chandeliers to every wall.
- **A low camera needs the shot described, not the height.** Asked for a floor-level lens with a
  table in the scene, the model parks the lens on the tabletop anyway. Lead the prompt with the
  vantage, keep any table out from between the lens and the face, and describe what a low angle
  shows: the underside of the chin, the ceiling behind the head, chair legs blurred in the
  foreground.
- **Negative constraints physical and explicit** ("exactly ONE bolt", "stays upside down").
- **Transparency:** solid #FFFFFF background + `backgroundremover`, never ask the model.
