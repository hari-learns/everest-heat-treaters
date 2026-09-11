#!/usr/bin/env python3
"""Builds the brand mark and the favicon from the company's own logo.

    python3 logo.py

The source is the mountain mark on page 2 of the 2025 company profile, lifted
straight out of the PDF at 681x259. It is line art in solid black on white,
so the useful part is its shape: the black becomes alpha and the white is
dropped. That gives a mask rather than a picture, which lets the header tint
the mark with `currentColor` and ride the same heat cycle as the wordmark.

    assets/img/logo-mark.png   alpha-only, tinted in CSS
    favicon.png                orange mark on the site's own ground

Both outputs are committed; the PDF is not needed unless the logo changes.
"""
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
PDF = os.path.expanduser(
    "~/Downloads/EVEREST HEAT TREATERS PROFILE 2025.pdf")

HEAT = (255, 107, 24)      # --heat
GROUND = (8, 12, 20)       # --bg
MARK_W = 340               # ~46px mark at 3x, with headroom
FAV = 180


def source():
    """Page 2 of the profile carries the mark as an embedded raster."""
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdfimages", "-png", "-f", "2", "-l", "2", PDF,
                    os.path.join(tmp, "p")], check=True)
    best = None
    for f in sorted(os.listdir(tmp)):
        im = Image.open(os.path.join(tmp, f)).convert("RGB")
        # the mark is the wide, short one; the other is a slide background
        if im.width > im.height * 1.8:
            best = im
    if best is None:
        raise SystemExit("could not find the mark on page 2 of the profile")
    return best


def to_alpha(im):
    """Black line art on white -> opacity. Darker pixel, more opaque."""
    g = im.convert("L")
    alpha = g.point(lambda v: 255 - v)
    mark = Image.new("RGBA", im.size, (255, 255, 255, 0))
    mark.putalpha(alpha)
    # white stays fully transparent, so crop to what is actually drawn
    box = alpha.point(lambda v: 255 if v > 24 else 0).getbbox()
    if box:
        mark = mark.crop(box)
    h = round(mark.height * MARK_W / mark.width)
    return mark.resize((MARK_W, h), Image.LANCZOS)


def favicon(mark):
    """The mark in brand orange, on the site's ground, square with a radius."""
    pad = round(FAV * 0.12)
    inner = FAV - pad * 2
    scaled = mark.resize((inner, max(1, round(mark.height * inner / mark.width))),
                         Image.LANCZOS)

    ground = Image.new("RGBA", (FAV, FAV), GROUND + (255,))
    radius = round(FAV * 0.22)
    rounded = Image.new("L", (FAV, FAV), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(rounded).rounded_rectangle([0, 0, FAV - 1, FAV - 1],
                                              radius=radius, fill=255)
    ground.putalpha(rounded)

    tint = Image.new("RGBA", scaled.size, HEAT + (255,))
    tint.putalpha(scaled.getchannel("A"))
    ground.alpha_composite(tint, (pad, (FAV - scaled.height) // 2))
    return ground


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    mark = to_alpha(source())
    dest = os.path.join(OUT, "logo-mark.png")
    # alpha-only art quantises hard with no visible loss
    mark.quantize(colors=64, method=Image.FASTOCTREE)\
        .save(dest, "PNG", optimize=True)
    print(f"  assets/img/logo-mark.png  {mark.width}x{mark.height}  "
          f"{os.path.getsize(dest) // 1024} KB")

    fav = os.path.join(ROOT, "favicon.png")
    favicon(mark).save(fav, "PNG", optimize=True)
    print(f"  favicon.png               {FAV}x{FAV}  "
          f"{os.path.getsize(fav) // 1024} KB")
