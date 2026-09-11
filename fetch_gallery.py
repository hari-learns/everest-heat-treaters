#!/usr/bin/env python3
"""Pulls the company's own gallery photographs into build_src/img/.

    python3 fetch_gallery.py && python3 assets.py

These are the client's pictures of their own plant and their own treated
components, published on amtheat.com. They beat stock photography for a shop
like this because the machines in them are the machines the copy describes.

They come off that site small — the plant shots are 396x264 and the component
shots 500x280 — so they are used at tile size in the gallery and never
full-bleed. Ask the client for the originals before launch and re-run this.

Only the converted WebP in assets/img/ is committed; build_src/ is ignored.
"""
import os
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "build_src", "img")
BASE = "https://amtheat.com/galleryimages/"

# (remote file, local name, what it shows)
SHOTS = [
    ("1782390069135bc113253b37e5d148200c41fcd5b5.png", "amt-furnace-line",
     "The continuous mesh belt furnace line"),
    ("17823900694de4163dcb613c4e6eea8c814e377469.png", "amt-pit-bays",
     "Pit furnace bays on the shop floor"),
    ("1782390069a5befc8ea7a58d18d6d9a8bbd863bbe4.png", "amt-loading",
     "Loading a gear ring into a pit furnace"),
    ("178239007049020bb9d46344ad81a46ab8590af53c.png", "amt-optical",
     "Optical hardness testers in the laboratory"),
    ("17823900709d2804bd82686438919edef77a4626d4.png", "amt-lab-press",
     "Mounting press and sample preparation"),
    ("1782390070f5220c88e9b113e314ffaeec6af3d5c9.png", "amt-draw-hot",
     "Work drawn from the furnace at temperature"),
    ("1782390111032b2cc936860b03048302d991c3498f.jpg", "amt-part-1",
     "Treated components"),
    ("1782390111156005c5baf40ff51a327f1c34f2975b.jpg", "amt-part-2",
     "Treated components"),
    ("178239011118e2999891374a475d0687ca9f989d83.jpg", "amt-part-3",
     "Treated components"),
    ("1782390111799bad5a3b514f096e69bbc4a7896cd9.jpg", "amt-part-4",
     "Treated components"),
    ("1782390111d0096ec6c83575373e3a21d129ff8fef.jpg", "amt-part-5",
     "Treated components"),
    ("1782390111f3ccdd27d2000e3f9255a7e3e2c48800.jpg", "amt-part-6",
     "Treated components"),
]


def main():
    os.makedirs(DEST, exist_ok=True)
    got = skipped = failed = 0
    for remote, name, _ in SHOTS:
        ext = os.path.splitext(remote)[1]
        out = os.path.join(DEST, name + ext)
        if os.path.exists(out):
            skipped += 1
            continue
        try:
            req = urllib.request.Request(
                BASE + remote, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r, \
                    open(out, "wb") as f:
                f.write(r.read())
            got += 1
            print(f"  {name}{ext}")
        except Exception as e:          # a flaky fetch must never break a build
            failed += 1
            print(f"  FAILED {name}: {e}")
    print(f"\n{got} fetched, {skipped} already present, {failed} failed")


if __name__ == "__main__":
    main()
