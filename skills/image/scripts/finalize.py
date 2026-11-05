#!/usr/bin/env python3
"""Finals kit: full-size master → flat version → traced SVG.

Step 0 is `generate.py --final "<round>/<name>"`, which writes the full-size master to finals/.
Then, for artwork that needs a flat or vector version (a logo, a patch, an icon):

  python3 finalize.py flat  hero-a-v3   # flat vector-style art from finals/hero-a-v3.png
  python3 finalize.py trace hero-a-v3   # SVG from finals/hero-a-v3-flat.png (needs: pip install vtracer)

Uses whichever service you have a key for, through generate.py beside this file.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate as g  # noqa: E402  (loads keys, models, runners and cost logging)

FLAT_PROMPT = """IMAGE 1 is the final approved design. Redraw this EXACT design as FLAT 2D
vector-style artwork: identical composition, silhouette, shapes, lettering, and colours, but
solid flat colour fills with clean smooth outlines. NO texture, NO shadows, NO 3D relief. The
silhouette stays as a flat shape on a pure white background. Same text, exactly as in the image,
nothing more."""


def flat(name: str) -> None:
    src = g.FINALS / f"{name}.png"
    if not src.exists():
        sys.exit(f"missing finals/{src.name}: run generate.py --final first")
    w, h = g.Image.open(src).size
    item = {"name": f"{name}-flat", "prompt": FLAT_PROMPT, "refs": [src]}
    out = g.FINALS / f"{name}-flat.png"
    if g.has_key("OPENAI_API_KEY"):
        g.need_package("openai")
        k = min(3840 / max(w, h), (3840 * 2144 / (w * h)) ** 0.5)
        item.update(size=f"{int(w * k / 16) * 16}x{int(h * k / 16) * 16}", quality="high")
        g.run(item, g.MODELS["openai_edit"], "", out)
    elif g.has_key("GEMINI_API_KEY"):
        g.need_package("google.genai")
        item.update(size="4K")
        g.run(item, g.MODELS["gemini"], g.nearest_aspect(w, h), out)
    else:
        g.missing_key_exit(g.KEY_HELP)
    g.print_costs()


def trace(name: str) -> None:
    try:
        import vtracer
    except ImportError:
        sys.exit("The Python package 'vtracer' is not installed: python3 -m pip install --user vtracer")
    src = g.FINALS / f"{name}-flat.png"
    if not src.exists():
        sys.exit(f"missing finals/{src.name}: run `finalize.py flat {name}` first")
    rgb = g.FINALS / f"{name}-flat-rgb.png"   # vtracer chokes on some PNG modes; re-save as plain RGB first
    g.Image.open(src).convert("RGB").save(rgb)
    dst = g.FINALS / f"{name}.svg"
    vtracer.convert_image_to_svg_py(
        str(rgb), str(dst),
        colormode="color", mode="spline",
        filter_speckle=8, color_precision=7,
        corner_threshold=60, length_threshold=4.0,
    )
    rgb.unlink()
    print(f"saved finals/{dst.name} ({dst.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("flat", "trace") or sys.argv[2] in ("-h", "--help"):
        sys.exit(__doc__)
    g.need_package("PIL")
    (flat if sys.argv[1] == "flat" else trace)(sys.argv[2])
