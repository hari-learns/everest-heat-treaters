#!/usr/bin/env python3
"""Converts the client's own photographs and videos into web assets.

    python3 media.py [source-folder]

The source is the folder the client supplied (~/Desktop/eht by default):
phone photographs of the works and four short phone videos. File names are
the captions, so the mapping below keeps each slug next to the words it
will be shown with; content.py only refers to the slugs.

    photos  -> assets/img/<slug>.webp          (long edge 1600, ~q78)
    videos  -> assets/video/<slug>.mp4 + .webp poster (H.264, faststart)

Outputs are committed. The source folder is only needed if a file changes.
"""
import os
import subprocess
import sys

from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "assets", "img")
VID = os.path.join(ROOT, "assets", "video")
SRC = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/Desktop/eht")

# source file -> slug. The captions live in content.py (GALLERY).
PHOTOS = {
    "normalising.jpeg": "g-normalising",
    "iv2.webp": "g-charge-lift",
    "bogie_furnace.jpeg": "g-bogie-furnace",
    "pittypefurnace.jpeg": "g-pit-furnaces",
    "pittypefurnacef5.jpeg": "g-pit-furnace-f5",
    "tempering_furnace2.jpeg": "g-tempering-furnace",
    "WhatsApp Image 2026-09-22 at 15.04.50 (5).jpeg": "g-quench-tanks",
    "WhatsApp Image 2026-09-22 at 15.04.50 (2).jpeg": "g-rockwell-floor",
    "WhatsApp Image 2026-09-22 at 15.04.50 (12).jpeg": "g-shop-floor",
    "lab.jpeg": "g-lab",
    "lab2.jpeg": "g-lab-2",
    "inspection_area.jpeg": "g-inspection-area",
    "inspection.jpeg": "g-inspection",
    "process_area.jpeg": "g-process-area",
    "receiving_area.jpeg": "g-receiving-area",
    "rec_area.jpeg": "g-receiving-2",
    "rec_area1.jpeg": "g-receiving-3",
    "dispatch.jpeg": "g-dispatch",
    "dispatch1.jpeg": "g-dispatch-2",
    "bolts.jpeg": "g-bolts",
    "board.jpeg": "g-board",
    "daily_prod_plan.jpeg": "g-prod-plan",
    "safety.jpeg": "g-safety",
    "office.jpeg": "g-office",
    "business_meeting.jpeg": "g-meeting",
    "team.jpeg": "g-team",
    "team2.jpeg": "g-team-2",
    "iv1.jpeg": "g-iv-group",
    "iv2.jpeg": "g-iv-group-2",
    "iv1.webp": "g-iv-furnace",
    "iv3.webp": "g-iv-pit",
    "ivexplaining.jpeg": "g-iv-explaining",
}

VIDEOS = {
    "hardening_oil_quench.mp4": "v-oil-quench",
    "oil_agitations.mp4": "v-oil-agitation",
    "oil and water.mp4": "v-quench-tanks",
    "IVvideo.mp4": "v-industrial-visit",
}

LONG_EDGE = 1600
BUDGET = 260_000


def save_webp(im, dest, budget=BUDGET):
    for q in (80, 74, 68, 62):
        im.save(dest, "WEBP", quality=q, method=6)
        if os.path.getsize(dest) <= budget:
            break
    return os.path.getsize(dest)


def photos():
    for name, slug in PHOTOS.items():
        src = os.path.join(SRC, name)
        if not os.path.exists(src):
            print(f"  MISSING {name}")
            continue
        # phone photos carry their rotation in EXIF; bake it in
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        im.thumbnail((LONG_EDGE, LONG_EDGE), Image.LANCZOS)
        size = save_webp(im, os.path.join(IMG, slug + ".webp"))
        print(f"  {slug:22} {im.size[0]}x{im.size[1]}  {size // 1024} KB")


def videos():
    for name, slug in VIDEOS.items():
        src = os.path.join(SRC, name)
        if not os.path.exists(src):
            print(f"  MISSING {name}")
            continue
        dest = os.path.join(VID, slug + ".mp4")
        # 720 on the long edge is plenty for a gallery tile or a lightbox on
        # a phone; the originals run to 17 MB for a minute and a half
        subprocess.run([
            "ffmpeg", "-v", "error", "-y", "-i", src,
            "-vf", "scale='if(gt(iw,ih),min(960,iw),-2)':'if(gt(iw,ih),-2,min(960,ih))'",
            "-c:v", "libx264", "-preset", "slow", "-crf", "28",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            "-c:a", "aac", "-b:a", "64k", dest], check=True)
        poster = os.path.join(VID, slug + ".jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", dest,
                        "-frames:v", "1", poster], check=True)
        im = Image.open(poster).convert("RGB")
        save_webp(im, os.path.join(VID, slug + ".webp"), budget=120_000)
        os.remove(poster)
        print(f"  {slug:22} {im.size[0]}x{im.size[1]}  "
              f"{os.path.getsize(dest) // 1024} KB")


if __name__ == "__main__":
    os.makedirs(IMG, exist_ok=True)
    os.makedirs(VID, exist_ok=True)
    print("photos")
    photos()
    print("videos")
    videos()
