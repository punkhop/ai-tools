#!/usr/bin/env python3
"""Crop single specimens out of group reference photos → refs/donors/, plus a contact sheet.

Each donor is one real example whose exact style gets copied through a reference image
(IMAGE-BIBLE.md Part 1, rule 2). Put the source photos in refs/style/, list the crops below,
run it, then look at refs/donors/_contact-sheet.png to check every crop.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent   # <project>; this script sits in <project>/tools
STYLE = ROOT / "refs" / "style"
OUT = ROOT / "refs" / "donors"

# (source file in refs/style/, crop box in original pixels (x0, y0, x1, y1), donor name)
CROPS = [
    # ("shelf-of-badges.jpg", (2015, 94, 2533, 510), "round-badge-red"),
]

if __name__ == "__main__":
    from PIL import Image, ImageDraw
    if not CROPS:
        raise SystemExit("CROPS is empty: list (source file, crop box, donor name) entries first.")
    OUT.mkdir(parents=True, exist_ok=True)
    thumbs = []
    for src, box, name in CROPS:
        img = Image.open(STYLE / src).convert("RGB").crop(box)
        img.save(OUT / f"{name}.png")
        t = img.copy()
        t.thumbnail((300, 300))
        thumbs.append((name, t))
        print(f"{name}: {img.size}")

    # contact sheet for checking every crop by eye
    cols, cell = 5, 310
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 20)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, t) in enumerate(thumbs):
        x, y = (i % cols) * cell, (i // cols) * (cell + 20)
        sheet.paste(t, (x + (cell - t.width) // 2, y + (cell - t.height) // 2))
        d.text((x + 8, y + cell - 2), name, fill="black")
    sheet.save(OUT / "_contact-sheet.png")
    print(f"contact sheet: {OUT / '_contact-sheet.png'}")
