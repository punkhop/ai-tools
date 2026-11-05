#!/usr/bin/env python3
"""Paste a region of one candidate over an untouched base with a feathered mask.

The no-chaining rule's other half: a local fix on a hard-edged plate (a laptop screen, a sign, a
solid background) is generated, then only THOSE pixels move onto the master; the rest never
re-renders. Never for people or light: in a drawn scene the seam reads instantly (IMAGE-BIBLE.md
Part 5). Rects are (x0, y0, x1, y1) in base pixels; `holes` are rects cut OUT of the mask.

    python3 composite.py base.png candidate.png out.png --rect 0,0,2752,600 --rect 1230,600,1580,810 \
        --hole 600,370,820,600 --feather 24
"""
import argparse


def build_mask(size, rects, holes, feather):
    from PIL import Image, ImageDraw, ImageFilter
    m = Image.new("L", size, 0); d = ImageDraw.Draw(m)
    for r in rects: d.rectangle(r, fill=255)
    for h in holes: d.rectangle(h, fill=0)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m


def composite(base_path, cand_path, out_path, rects, holes=(), feather=24):
    from PIL import Image
    base = Image.open(base_path).convert("RGB"); cand = Image.open(cand_path).convert("RGB")
    if cand.size != base.size: cand = cand.resize(base.size, Image.LANCZOS)
    out = Image.composite(cand, base, build_mask(base.size, rects, holes, feather))
    out.save(out_path); return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Paste regions of a candidate over a base image.")
    ap.add_argument("base"); ap.add_argument("candidate"); ap.add_argument("out")
    ap.add_argument("--rect", action="append", required=True, help="x0,y0,x1,y1 (repeatable)")
    ap.add_argument("--hole", action="append", default=[], help="x0,y0,x1,y1 cut out of the mask (repeatable)")
    ap.add_argument("--feather", type=int, default=24)
    a = ap.parse_args()
    P = lambda s: tuple(int(v) for v in s.split(","))
    composite(a.base, a.candidate, a.out, [P(r) for r in a.rect], [P(h) for h in a.hole], a.feather)
    print("wrote", a.out)
