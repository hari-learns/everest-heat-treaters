#!/usr/bin/env python3
"""Pulls the plant photographs and the two certificates out of the profile.

    python3 plant.py

Everything here comes from the client's own "Everest Heat Treaters Profile
2025" PDF, so it is their kit rather than stock or another company's.

Two different extractions, because the two things need different treatment:

  * the equipment photographs are embedded rasters, so pdfimages gives them
    at their true resolution. They are small — 150 to 275 px — which is why
    they are only ever used at tile size.
  * the certificates are a full page of layout, so the page is rendered at
    200 dpi and each sheet cut out of it by comparing every row against the
    page background sampled from the gutter between them. That avoids the
    caption band underneath, which a plain whiteness test kept swallowing.

Outputs land in assets/img/ as WebP and are committed; the PDF is only needed
if the source ever changes.
"""
import os
import subprocess
import tempfile

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")
PDF = os.path.expanduser("~/Downloads/EVEREST HEAT TREATERS PROFILE 2025.pdf")

# pdfimages emits these in page order across pages 8-10; the index is stable
# for this document. Anything not listed is a logo or a decoration.
KIT = {
    "k-007": ("kit-bogie-furnace", "Work at temperature in the bogie hearth furnace"),
    "k-008": ("kit-pit-carburising", "Sealed pit furnace for gas carburising"),
    "k-009": ("kit-pit-tempering", "Pit furnace on the tempering line"),
    "k-003": ("kit-rockwell", "Rockwell hardness tester"),
    "k-004": ("kit-brinell", "Brinell hardness tester"),
    "k-005": ("kit-optical", "Optical Brinell-cum-Rockwell tester"),
    "k-006": ("kit-portable", "Portable hardness tester for large work"),
    "k-002": ("kit-crane", "Two-tonne overhead crane"),
    "k-000": ("kit-generator", "Standby generation, 24x7"),
    "k-010": ("kit-cutoff", "Abrasive cut-off saw for test pieces"),
    "k-011": ("kit-mounting", "Mounting press for microsections"),
    "k-012": ("kit-polisher", "Twin-disc grinder and polisher"),
    "k-013": ("kit-microscope", "Metallurgical microscope, up to 500x"),
}

CERT_BANDS = [((100, 796), "cert-gst"), ((1136, 1840), "cert-iso")]
CERT_GUTTER_X = 960          # a column of pure page background at every row
BUDGET = 190_000


def save(im, stem, budget=BUDGET):
    dest = os.path.join(OUT, stem + ".webp")
    for q in (88, 82, 76, 70, 64):
        im.save(dest, "WEBP", quality=q, method=6)
        if os.path.getsize(dest) <= budget:
            break
    return dest, os.path.getsize(dest)


def equipment():
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdfimages", "-png", "-f", "8", "-l", "10", PDF,
                    os.path.join(tmp, "k")], check=True)
    done = 0
    for key, (stem, _) in KIT.items():
        src = os.path.join(tmp, key + ".png")
        if not os.path.exists(src):
            print(f"  MISSING {key} -> {stem}")
            continue
        im = Image.open(src).convert("RGB")
        # upscale a little so a 250px photo is not mushy on a 2x tile
        if im.width < 640:
            im = im.resize((640, round(im.height * 640 / im.width)), Image.LANCZOS)
        _, size = save(im, stem)
        print(f"  {stem:22} {im.size[0]}x{im.size[1]}  {size // 1024} KB")
        done += 1
    return done


def certificates():
    tmp = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-png", "-r", "200", "-f", "11", "-l", "11",
                    PDF, os.path.join(tmp, "page")], check=True)
    page = [f for f in os.listdir(tmp) if f.endswith(".png")][0]
    im = Image.open(os.path.join(tmp, page)).convert("RGB")
    W, H = im.size
    px = im.load()

    def differs(c, b):
        return abs(c[0] - b[0]) + abs(c[1] - b[1]) + abs(c[2] - b[2]) > 26

    done = 0
    for (x0, x1), stem in CERT_BANDS:
        rows = []
        for y in range(H):
            bg = px[CERT_GUTTER_X, y]
            rows.append(sum(1 for x in range(x0, x1, 3) if differs(px[x, y], bg)))
        need = ((x1 - x0) // 3) * 0.55
        ys = [y for y, v in enumerate(rows) if v >= need]
        if not ys:
            print(f"  MISSING {stem}")
            continue
        # the longest unbroken stretch is the sheet; the caption below is short
        best = (0, 0)
        run = prev = ys[0]
        for y in ys[1:]:
            if y - prev > 6:
                if prev - run > best[1] - best[0]:
                    best = (run, prev)
                run = y
            prev = y
        if prev - run > best[1] - best[0]:
            best = (run, prev)
        crop = im.crop((x0, best[0], x1, best[1] + 1))
        _, size = save(crop, stem, budget=260_000)
        print(f"  {stem:22} {crop.size[0]}x{crop.size[1]}  {size // 1024} KB")
        done += 1
    return done


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("equipment")
    n1 = equipment()
    print("certificates")
    n2 = certificates()
    print(f"\n{n1} photographs, {n2} certificates")
