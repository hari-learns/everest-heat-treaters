#!/usr/bin/env python3
"""Crop the colour-metallography plate into individual tiles.

`micro-colour` is a 3x3 contact sheet of etched-alloy micrographs. Each cell
is a beautiful abstract texture in its own right; used whole the grid just
reads as a figure from a paper. This slices it into nine usable images.

Run after assets.py. Output: assets/img/plate-1.webp ... plate-9.webp
"""
import os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "build_src", "img", "micro-colour.jpg")
OUT = os.path.join(ROOT, "assets", "img")

# The plate has a thin white gutter between cells; inset each crop so no
# white edge bleeds into the tile.
INSET = 0.012
COLS = ROWS = 3
KEEP = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def main():
    if not os.path.exists(SRC):
        raise SystemExit("micro-colour.jpg missing — run fetch_media.py first")
    os.makedirs(OUT, exist_ok=True)
    with Image.open(SRC) as im:
        im = im.convert("RGB")
        W, H = im.size
        cw, ch = W / COLS, H / ROWS
        n = 0
        for r in range(ROWS):
            for c in range(COLS):
                n += 1
                if n not in KEEP:
                    continue
                x0 = int(c * cw + cw * INSET)
                y0 = int(r * ch + ch * INSET)
                x1 = int((c + 1) * cw - cw * INSET)
                y1 = int((r + 1) * ch - ch * INSET)
                tile = im.crop((x0, y0, x1, y1))
                # Etched micrographs are pure high-frequency detail and do not
                # compress like a photograph; they need a tighter cap and a
                # lower quality floor to stay inside budget.
                tile.thumbnail((900, 900), Image.LANCZOS)
                dest = os.path.join(OUT, f"plate-{n}.webp")
                for q in (78, 68, 58, 48, 40):
                    tile.save(dest, "WEBP", quality=q, method=6)
                    if os.path.getsize(dest) <= 150_000:
                        break
                print(f"  plate-{n}  {tile.size[0]}x{tile.size[1]}  "
                      f"{os.path.getsize(dest) // 1024} KB")


if __name__ == "__main__":
    main()
