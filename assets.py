#!/usr/bin/env python3
"""build_src/img/*.jpg  ->  assets/img/*.webp

The Commons downloads are 0.5-5 MB each. Shipped as-is they would make the
pitch feel slow on a phone, which is the one impression we cannot afford.
This caps the long edge and re-encodes to WebP.

Only the output is committed; build_src/ is git-ignored and fully
reproducible from fetch_media.py.

    python3 assets.py            # skip anything already converted
    python3 assets.py --force
"""
import os
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "build_src", "img")
OUT = os.path.join(ROOT, "assets", "img")
FORCE = "--force" in sys.argv

# Sources that exist only to be processed into something else.
# micro-colour is a 3x3 contact sheet sliced by tiles.py; shipping the
# whole plate would be a 1 MB asset nothing ever references.
EXCLUDE = {"micro-colour"}

# Outputs that are generated rather than converted, so there is no file in
# build_src/ to match them against. Without this they get pruned as stale.
GENERATED = {"billet-heat"}

MAX_EDGE = 1900          # plenty for a full-bleed image on a 2x display
WIDE = {"micro-colour", "molten-pour", "furnace-castings", "forge", "molten-ladle"}
WIDE_EDGE = 2400         # full-bleed banners get a little more room

# Dense foliage and market-stall textures do not compress like a calm lake
# does, so a single fixed quality gives wildly uneven file sizes. Budget the
# output instead and let each image find the quality it needs.
BUDGET = 260_000
WIDE_BUDGET = 420_000
QUALITY_STEPS = (82, 76, 70, 64, 58)


def convert(name):
    src = os.path.join(SRC, name)
    stem = os.path.splitext(name)[0]
    dest = os.path.join(OUT, stem + ".webp")

    if os.path.exists(dest) and not FORCE \
            and os.path.getmtime(dest) >= os.path.getmtime(src):
        return None

    wide = stem in WIDE
    cap = WIDE_EDGE if wide else MAX_EDGE
    budget = WIDE_BUDGET if wide else BUDGET

    with Image.open(src) as im:
        # Phone photos carry EXIF rotation that Pillow ignores unless asked.
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        if max(im.size) > cap:
            im.thumbnail((cap, cap), Image.LANCZOS)

        for quality in QUALITY_STEPS:
            im.save(dest, "WEBP", quality=quality, method=6)
            if os.path.getsize(dest) <= budget:
                break
        else:
            # Still over budget at the lowest acceptable quality: the image is
            # genuinely too detailed, so trade pixels rather than more artefacts.
            im.thumbnail((int(cap * 0.75), int(cap * 0.75)), Image.LANCZOS)
            im.save(dest, "WEBP", quality=QUALITY_STEPS[-1], method=6)
            quality = QUALITY_STEPS[-1]

    return os.path.getsize(src), os.path.getsize(dest), im.size, quality


def main():
    if not os.path.isdir(SRC):
        sys.exit("no build_src/img — run: python3 fetch_media.py")
    os.makedirs(OUT, exist_ok=True)

    names = sorted(f for f in os.listdir(SRC)
                   if f.lower().endswith((".jpg", ".jpeg", ".png"))
                   and os.path.splitext(f)[0] not in EXCLUDE)
    before = after = 0
    done = skipped = 0
    bad = []

    for name in names:
        try:
            result = convert(name)
        except Exception as exc:
            bad.append((name, str(exc)[:60]))
            continue
        if result is None:
            skipped += 1
            continue
        s, d, size, q = result
        before += s
        after += d
        done += 1
        print(f"  {os.path.splitext(name)[0]:<16} "
              f"{s // 1024:>5} KB -> {d // 1024:>4} KB  "
              f"{size[0]}x{size[1]}  q{q}")

    # Stale outputs left behind when a slug is renamed or dropped upstream.
    stems = {os.path.splitext(n)[0] for n in names}
    for f in sorted(os.listdir(OUT)):
        stem = os.path.splitext(f)[0]
        if stem.startswith("plate-"):      # derived by tiles.py, no source file
            continue
        if stem in GENERATED:              # rendered by hero.py, no source file
            continue
        if f.endswith(".webp") and stem not in stems:
            os.remove(os.path.join(OUT, f))
            print(f"  removed stale {f}")

    print(f"\n  converted {done}, skipped {skipped}")
    if done:
        print(f"  {before / 1e6:.1f} MB -> {after / 1e6:.1f} MB "
              f"({after / before * 100:.0f}%)")
    if bad:
        print("\n  FAILED:")
        for name, err in bad:
            print(f"    {name}: {err}")
        print("  re-run: python3 fetch_media.py --force")


if __name__ == "__main__":
    main()
