#!/usr/bin/env python3
"""Image-generation starter. new_project.py copies it into a project as tools/generate.py; edit
the PROMPTS list (and the defaults below if needed), nothing else.

Follows IMAGE-BIBLE.md (beside SKILL.md): named rounds, never overwrite, a manifest for the
gallery, optional reference images (ONE style donor per request), threaded batch with
rate-limit retry, every paid call logged with its cost.

Two services behind one prompt list. A prompt's "model" picks which:
  (left out)         → the default: Gemini if you have a Gemini key, else OpenAI
  "gemini"           → MODELS["gemini"]
  "openai"           → MODELS["openai"] normally, MODELS["openai_edit"] when the prompt has refs
  any full model id  → used as is (gemini-* goes to Google, gpt-image-* / chatgpt-image-* to OpenAI)
Keys come from the environment (OPENAI_API_KEY, GEMINI_API_KEY) or ~/.claude/ai-tools/keys.env.
This script never prints a key.

Usage:
  python3 generate.py --check                       # which keys and packages are present
  python3 generate.py --round "01 style matrix" --draft   # explore cheap: Gemini 1K, OpenAI medium
  python3 generate.py --round "01 style matrix"     # run every prompt into rounds/01 style matrix/
  python3 generate.py --round "02 colder palette" hero-a  # run one prompt by name
  python3 generate.py --manifest-only               # rebuild the gallery's manifest
  python3 generate.py --costs                       # dollars per model and the total
  python3 generate.py --final "01 style matrix/hero-a-v1" # redraw one picked draft at full size
  python3 generate.py --models                      # list the image models your keys can reach

Cost rule: every paid call appends one line to tools/usage.log; tools/prices.json holds each
vendor's price sheet (URL + date checked). A model missing from it prints as UNPRICED.
"""

import argparse
import base64
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

# --- Models — the one place model ids live. One edit here upgrades everything. ---------------
MODELS = {
    "gemini": "gemini-3-pro-image",             # Google's image model
    "openai": "gpt-image-2.6-flare",            # OpenAI: fast, high-quality generation
    "openai_edit": "gpt-image-2.6-sunburst",    # OpenAI: precise editing, used when refs are attached
}

# --- Defaults (a prompt can override aspect / size / quality / model) ------------------------
ASPECT = "16:9"     # "1:1", "2:3", "3:2", "4:5", "5:4", "9:16", "16:9", "21:9"
SIZE = "2K"         # Gemini: "1K", "2K"; "4K" for finals only
QUALITY = "high"    # OpenAI: "low", "medium", "high"; "max" for finals only
WORKERS = 3

HERE = Path(__file__).resolve().parent   # <project>/tools: this script, gallery.html, manifest
ROOT = HERE.parent                       # <project>: refs/, rounds/, picks/, finals/
OUT = ROOT / "rounds"     # one folder per round, NAMED for its one variable
REFS = ROOT / "refs"      # refs/style/ form references · refs/donors/ · refs/subject/
FINALS = ROOT / "finals"  # full-size redraws of picks, one generation from their draft
USAGE = HERE / "usage.log"     # one line per paid call; only ever appended
PRICES = HERE / "prices.json"  # dollars per 1M tokens, copied from each vendor's price page

KEYS_FILE = Path.home() / ".claude" / "ai-tools" / "keys.env"
KEY_HELP = {
    "OPENAI_API_KEY": "OpenAI key: platform.openai.com → API keys → Create new secret key",
    "GEMINI_API_KEY": "Gemini key: aistudio.google.com → Get API key → Create API key",
}
PACKAGES = {"PIL": "pillow", "openai": "openai", "google.genai": "google-genai"}

try:
    from PIL import Image
except ImportError:
    Image = None

# --- Prompts — a list of dicts, never inline strings -------------------------------------------
# name:  versioned output name (the round folder keeps generations apart)
# label: what the gallery shows; the text before " · " is the idea the card is grouped under
# refs:  image paths attached after the prompt. ONE style donor max; subject photos may follow.
#        Leave empty for text-to-image.
# aspect / size / model / quality: OPTIONAL per-prompt overrides of the defaults above.
#        A deliberately mixed set (tall posters, wide banners, square thumbs) is one round, not
#        three, so the comparison is real. Same for services: duplicate an entry with
#        "model": "openai" and a -oai name suffix to see both answer the same prompt.
#        size is "2K" for Gemini, pixels ("1536x1024") for OpenAI; leave it off and the aspect
#        decides.
# Prompt shape: CHANGE/KEEP when editing a ref; lean when a ref is attached. See IMAGE-BIBLE.md.
PROMPTS = [
    {
        "name": "example-a-v1",
        "label": "Example A",
        "refs": [],  # e.g. [REFS / "donors" / "donor-1.png"]
        "prompt": """...""",
    },
]

# OpenAI takes pixel sizes, not ratios: map the aspect onto its shapes.
OPENAI_SIZES = {"1:1": "1024x1024", "4:5": "1024x1536", "2:3": "1024x1536",
                "9:16": "1024x1536", "5:4": "1536x1024", "3:2": "1536x1024",
                "16:9": "1536x1024", "21:9": "1536x1024"}
GEMINI_ASPECTS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]

# The change-nothing prompt for a final. A cleanup edit brightens, sharpens and writes words
# unless told not to (IMAGE-BIBLE.md Part 5), so the lock rides along every time.
FINAL_PROMPT = (
    "Redraw this exact image at full resolution. Change nothing: same people, same faces, same "
    "expressions, same hands, same pose, same framing, same light, same colours. Exactly as dark as the "
    "attached image, no fill, nothing lifted; whatever is out of focus stays exactly that soft; "
    "add no new words anywhere.")


# --- Keys ----------------------------------------------------------------------------------------
def load_keys() -> None:
    """Fill OPENAI_API_KEY / GEMINI_API_KEY from keys.env when the environment lacks them."""
    if not KEYS_FILE.exists():
        return
    for line in KEYS_FILE.read_text().splitlines():
        line = line.strip()
        if line.startswith("export "):
            line = line[len("export "):]
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip().strip('"').strip("'")
        if k in KEY_HELP and v and not os.environ.get(k):
            os.environ[k] = v


load_keys()


def has_key(name: str) -> bool:
    return bool(os.environ.get(name))


def key_for(model: str) -> str:
    return "GEMINI_API_KEY" if model.startswith("gemini") else "OPENAI_API_KEY"


def missing_key_exit(names) -> None:
    print("A key is missing, so nothing was generated.")
    for n in sorted(set(names)):
        print(f"  {KEY_HELP[n]}")
    print("Save it with:  python3 ~/.claude/skills/image/scripts/save_key.py " + " / ".join(sorted(set(names))))
    sys.exit(2)


def need_package(module: str) -> None:
    try:
        __import__(module)
    except ImportError:
        pip = PACKAGES.get(module, module)
        print(f"The Python package '{pip}' is not installed.\n"
              f"  Install it:  python3 -m pip install --user {pip}\n"
              f"  (If pip says 'externally-managed-environment', use the venv described in SKILL.md.)")
        sys.exit(3)


# --- Costs ---------------------------------------------------------------------------------------
_usage_lock = threading.Lock()


def log_usage(name, model, size, in_text, in_image, out_text, out_image):
    """stamp, name, model, size, words in, pictures in, text/thinking out, picture out (tokens)."""
    line = "\t".join(str(x) for x in (datetime.now().isoformat(timespec="seconds"), name, model, size,
                                      in_text, in_image, out_text, out_image))
    with _usage_lock, open(USAGE, "a") as f:
        f.write(line + "\n")


def print_costs() -> None:
    prices = json.loads(PRICES.read_text()) if PRICES.exists() else {}
    rows = {}
    for line in USAGE.read_text().splitlines() if USAGE.exists() else []:
        f = line.split("\t")
        if len(f) < 8:
            continue
        model, toks = f[2], [int(x or 0) for x in f[4:8]]
        p = prices.get(model)
        key = model if p else model + " UNPRICED"
        cost = sum(t * p[k] for t, k in zip(toks, ("in_text", "in_image", "out_text", "out_image"))) / 1e6 if p else 0
        r = rows.setdefault(key, [0, 0.0]); r[0] += 1; r[1] += cost
    for k, (n, c) in sorted(rows.items()):
        print(f"{k:32s} {n:4d} calls  ${c:.2f}")
    print(f"{'total':32s} {sum(r[0] for r in rows.values()):4d} calls  ${sum(r[1] for r in rows.values()):.2f}")


# --- Clients -------------------------------------------------------------------------------------
_clients = {}
_clients_lock = threading.Lock()  # workers race to build the client; the loser's copy got
                                  # garbage-collected mid-request ("client has been closed")


def _gemini():
    with _clients_lock:
        if "gemini" not in _clients:
            from google import genai
            _clients["gemini"] = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _clients["gemini"]


def _openai():
    with _clients_lock:
        if "openai" not in _clients:
            from openai import OpenAI
            _clients["openai"] = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    return _clients["openai"]


def default_engine() -> str:
    if has_key("GEMINI_API_KEY"):
        return "gemini"
    return "openai" if has_key("OPENAI_API_KEY") else "gemini"


def resolve_model(item: dict) -> str:
    model = item.get("model") or default_engine()
    if model == "openai":  # shorthand: the edit model earns its keep only with refs
        return MODELS["openai_edit"] if item.get("refs") else MODELS["openai"]
    if model == "gemini":
        return MODELS["gemini"]
    return model


# --- Runners -------------------------------------------------------------------------------------
def _run_gemini(item: dict, model: str, aspect: str, out_path: Path) -> bool:
    from google.genai import types
    contents = [item["prompt"]] + [Image.open(p) for p in item.get("refs", [])]
    response = _gemini().models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(aspect_ratio=aspect, image_size=item.get("size", SIZE)),
        ),
    )
    u = response.usage_metadata
    mod = {d.modality.name: d.token_count for d in (u.prompt_tokens_details or [])}
    out = {d.modality.name: d.token_count for d in (u.candidates_tokens_details or [])}
    log_usage(item["name"], model, item.get("size", SIZE), mod.get("TEXT", 0), mod.get("IMAGE", 0),
              out.get("TEXT", 0) + (u.thoughts_token_count or 0), out.get("IMAGE", 0))
    for part in response.parts or []:
        if part.inline_data:
            part.as_image().save(out_path)  # genai.Image: .save works, .size doesn't
            return True
    return False


def _run_openai(item: dict, model: str, aspect: str, out_path: Path) -> bool:
    # size: pixels per prompt ("1536x1024"), or the aspect map decides.
    size = item.get("size") if "x" in str(item.get("size", "")) else OPENAI_SIZES.get(aspect, "auto")
    kwargs = dict(model=model, prompt=item["prompt"], size=size,
                  quality=item.get("quality", QUALITY), n=1)
    refs = item.get("refs", [])
    if refs:  # img2img: OpenAI edits, not generations
        handles = [open(p, "rb") for p in refs]
        try:
            response = _openai().images.edit(image=handles, **kwargs)
        finally:
            for h in handles:
                h.close()
    else:
        response = _openai().images.generate(**kwargs)
    u = response.usage
    det = getattr(u, "input_tokens_details", None)
    log_usage(item["name"], model, size, getattr(det, "text_tokens", u.input_tokens) if det else u.input_tokens,
              getattr(det, "image_tokens", 0) if det else 0, 0, u.output_tokens)
    b64 = response.data[0].b64_json
    if not b64:
        return False
    out_path.write_bytes(base64.b64decode(b64))
    return True


def run(item: dict, model: str, aspect: str, out_path: Path) -> bool:
    """One call with retries; prints one plain line per outcome."""
    runner = _run_gemini if model.startswith("gemini") else _run_openai
    for attempt in range(3):
        try:
            if runner(item, model, aspect, out_path):
                print(f"  ok {out_path.relative_to(ROOT)}  [{model} {aspect}]")
                return True
            print(f"  NO IMAGE {item['name']} (the model answered without a picture; try again or reword)")
            return False
        except Exception as e:
            msg = str(e)
            if "must be verified" in msg:
                print(f"  NOT VERIFIED {item['name']}: {model} needs your OpenAI organization verified "
                      "(platform.openai.com → Settings → Organization → General → Verify Organization; "
                      "can take 15 minutes to apply)")
                return False
            if "credit" in msg.lower() or "insufficient_quota" in msg or "billing" in msg.lower():
                print(f"  NO CREDITS {item['name']}: add credit or billing on the provider's account. {msg[:120]}")
                return False
            if "api key" in msg.lower() or "401" in msg or "unauthorized" in msg.lower():
                print(f"  KEY REJECTED {item['name']}: the {key_for(model)} was refused; make a new one. "
                      f"{KEY_HELP[key_for(model)]}")
                return False
            if "model_not_found" in msg or "404" in msg or "does not exist" in msg or "is not found" in msg:
                print(f"  MODEL GONE {item['name']}: {model} is retired or not open to this key. Run "
                      "generate.py --models, put the newest image model in MODELS at the top of "
                      "generate.py, add its price to prices.json, then run again.")
                return False
            if "429" in msg or "quota" in msg.lower() or "rate limit" in msg.lower() or "rate_limit" in msg:
                wait = 30 * (attempt + 1)
                print(f"  rate-limited {item['name']}, waiting {wait}s")
                time.sleep(wait)
            else:
                print(f"  ERROR {item['name']}: {msg[:300]}")
                return False
    return False


def generate_one(round_dir: Path, item: dict) -> bool:
    return run(item, resolve_model(item), item.get("aspect", ASPECT), round_dir / f"{item['name']}.png")


def nearest_aspect(w: int, h: int) -> str:
    def ratio(a):
        x, y = a.split(":")
        return int(x) / int(y)
    return min(GEMINI_ASPECTS, key=lambda a: abs(ratio(a) - w / h))


def finalize(spec: str) -> None:
    """One generation from the picked draft, at full size. Writes finals/<name>.png: the master;
    derive web sizes from it. OpenAI's edit model at quality max when you have an OpenAI key,
    else Gemini at 4K."""
    src = OUT / f"{spec}.png"
    if not src.exists():
        print(f"  not found: rounds/{spec}.png")
        return
    w, h = Image.open(src).size
    FINALS.mkdir(exist_ok=True)
    item = {"name": f"{src.stem}-final", "prompt": FINAL_PROMPT, "refs": [src]}
    if has_key("OPENAI_API_KEY"):
        # 3840 on the long edge, capped at the pixel budget the edit model accepts
        # (3840x2144 passes, 3840x2720 is refused "exceeds the current pixel budget").
        k = min(3840 / max(w, h), (3840 * 2144 / (w * h)) ** 0.5)
        item.update(size=f"{int(w * k / 16) * 16}x{int(h * k / 16) * 16}", quality="max")
        run(item, MODELS["openai_edit"], "", FINALS / f"{src.stem}.png")
    else:
        item.update(size="4K")
        run(item, MODELS["gemini"], nearest_aspect(w, h), FINALS / f"{src.stem}.png")


# --- Manifest ------------------------------------------------------------------------------------
def pngs(folder: Path, deep: bool = False) -> list:
    """PNGs in a folder, minus the `._name.png` companions macOS writes beside files on network
    and external drives; read as images they take a number and break the gallery."""
    if not folder.exists():
        return []
    found = folder.rglob("*.png") if deep else folder.glob("*.png")
    return sorted(p for p in found if not p.name.startswith("._"))


def write_review_jpgs() -> None:
    """A 1600px JPEG beside every PNG. The gallery loads these (~300KB) instead of the 5MB master,
    which keeps it fast. The PNG stays the master."""
    for png in pngs(OUT, True) + pngs(REFS, True) + pngs(FINALS):
        jpg = png.with_suffix(".review.jpg")
        if jpg.exists() and jpg.stat().st_mtime > png.stat().st_mtime:
            continue
        im = Image.open(png).convert("RGB"); im.thumbnail((1600, 1600))
        im.save(jpg, "JPEG", quality=84, optimize=True)


def rebuild_manifest() -> None:
    write_review_jpgs()
    # The prompt list is the record: carry its labels and ratios into the gallery so a card says
    # what it IS, not just which file it is.
    meta_by_name = {p["name"]: {
        "label": p.get("label", p["name"]),
        "sub": p.get("sub", ""),
        "aspect": p.get("aspect", ASPECT),
        "model": resolve_model(p),
    } for p in PROMPTS}
    entries = []
    for round_dir in sorted(p for p in OUT.iterdir() if p.is_dir()) if OUT.exists() else []:
        for png in pngs(round_dir):
            meta = meta_by_name.get(png.stem, {})
            model = meta.get("model", "")
            entries.append({
                "round": round_dir.name,
                "src": os.path.relpath(png, HERE),   # gallery.html sits beside the manifest
                "file": png.stem,
                "label": meta.get("label", png.stem),
                # When a round mixes services, which engine drew it IS the variable.
                "sub": meta.get("sub") or " · ".join(x for x in (round_dir.name, model) if x),
                "aspect": meta.get("aspect", ASPECT),
                "model": model,
            })
    for png in pngs(FINALS):  # full-size redraws, last in the nav
        meta = meta_by_name.get(png.stem, {})
        entries.append({"round": "finals", "src": os.path.relpath(png, HERE), "file": png.stem,
                        "label": meta.get("label", png.stem) + " · final", "sub": "final",
                        "aspect": meta.get("aspect", ASPECT), "model": ""})
    number(entries)
    data = json.dumps(entries, indent=1)
    (HERE / "manifest.json").write_text(data)
    # Same data as a script, so gallery.html also works opened straight from disk (file://),
    # where browsers refuse to fetch manifest.json.
    (HERE / "manifest.js").write_text("window.MANIFEST = " + data + ";\n")
    print(f"manifest: {len(entries)} images")


def number(entries: list) -> None:
    """Every image gets a plain number, project-wide, the first time the manifest sees it, and
    keeps it for good (numbers.json is the record; never reused, never renumbered). Notes go by
    number ("7 warmer, 19 tighter") and the gallery shows it big. A final keeps its draft's number."""
    path = HERE / "numbers.json"
    nums = json.loads(path.read_text()) if path.exists() else {}
    by_file = {}
    for e in entries:
        if e["round"] == "finals":
            continue
        key = f'{e["round"]}/{e["file"]}'
        if key not in nums:
            nums[key] = max(nums.values(), default=0) + 1
        e["n"] = by_file[e["file"]] = nums[key]
    for e in entries:
        if e["round"] == "finals" and e["file"] in by_file:
            e["n"] = by_file[e["file"]]
    path.write_text(json.dumps(nums, indent=1))


# --- Checks --------------------------------------------------------------------------------------
def check() -> None:
    for name in KEY_HELP:
        print(f"{name}: {'found' if has_key(name) else 'missing'}")
    for module, pip in PACKAGES.items():
        try:
            __import__(module)
            ok = "installed"
        except ImportError:
            ok = "missing"
        print(f"{pip}: {ok}")
    print(f"default engine: {default_engine()} ({MODELS[default_engine()]})")


def list_models() -> None:
    if has_key("GEMINI_API_KEY"):
        need_package("google.genai")
        print("Gemini:", ", ".join(sorted(m.name.split("/")[-1] for m in _gemini().models.list()
                                           if "image" in m.name)))
    if has_key("OPENAI_API_KEY"):
        need_package("openai")
        print("OpenAI:", ", ".join(sorted(m.id for m in _openai().models.list() if "image" in m.id)))
    if not (has_key("GEMINI_API_KEY") or has_key("OPENAI_API_KEY")):
        missing_key_exit(KEY_HELP)


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate a round of images, rebuild the gallery, print costs.")
    ap.add_argument("--round", default="01 first pass",
                    help='named round folder under rounds/, e.g. "03 clay plus swatch sheet"')
    ap.add_argument("--manifest-only", action="store_true", help="rebuild the gallery's manifest only")
    ap.add_argument("--draft", action="store_true", help="explore cheap: Gemini 1K, OpenAI quality medium")
    ap.add_argument("--costs", action="store_true", help="print dollars per model and the total")
    ap.add_argument("--final", nargs="+", metavar="ROUND/NAME", help="redraw picked drafts at full size into finals/")
    ap.add_argument("--check", action="store_true", help="say which keys and packages are present")
    ap.add_argument("--models", action="store_true", help="list the image models your keys can reach")
    ap.add_argument("names", nargs="*", help="run only these prompt names")
    args = ap.parse_args()

    if args.check:
        return check()
    if args.costs:
        return print_costs()
    if args.models:
        return list_models()
    need_package("PIL")

    if args.final:
        if not (has_key("OPENAI_API_KEY") or has_key("GEMINI_API_KEY")):
            missing_key_exit(KEY_HELP)
        need_package("openai" if has_key("OPENAI_API_KEY") else "google.genai")
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            list(pool.map(finalize, args.final))
        rebuild_manifest()
        return print_costs()

    global SIZE, QUALITY
    if args.draft:
        SIZE, QUALITY = "1K", "medium"

    if not args.manifest_only:
        selected = [p for p in PROMPTS if not args.names or p["name"] in args.names]
        models = sorted({resolve_model(p) for p in selected})
        missing = [key_for(m) for m in models if not has_key(key_for(m))]
        if missing:
            missing_key_exit(missing)
        for m in models:
            need_package("google.genai" if m.startswith("gemini") else "openai")
        round_dir = OUT / args.round
        round_dir.mkdir(parents=True, exist_ok=True)
        print(f"{' + '.join(models)} · {ASPECT} · {len(selected)} prompts → {round_dir}")
        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            list(pool.map(lambda item: generate_one(round_dir, item), selected))

    rebuild_manifest()
    print_costs()


if __name__ == "__main__":
    main()
