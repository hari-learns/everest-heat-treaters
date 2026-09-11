#!/usr/bin/env python3
"""Traces the logo bitmap into vector outlines.

    python3 trace.py > mark_paths.py

The mark arrives from the PDF as line art, which is fine for a favicon and
useless for anything that wants to move. This walks the alpha channel with
marching squares, joins the segments into closed rings and simplifies them
with Ramer-Douglas-Peucker, so the hero can draw the mountain as strokes and
run heat through it instead of tinting a rectangle.

No tracing tool is installed on this machine and none is needed: the source is
two-tone line art, which is the easy case.
"""
import sys

from PIL import Image

SRC = "assets/img/logo-mark.png"
LEVEL = 0.5          # alpha midpoint
EPS = 0.55           # RDP tolerance, in source pixels
MIN_RING = 26        # drop specks
VIEW_W = 340         # the viewBox the paths are written against


def grid(path):
    # the mark ships quantised to a palette, so ask for RGBA explicitly
    im = Image.open(path).convert("RGBA")
    a = im.getchannel("A")
    w, h = a.size
    px = list(a.getdata())
    return w, h, [[px[y * w + x] / 255.0 for x in range(w)] for y in range(h)]


def segments(w, h, g):
    """Marching squares, with linear interpolation along each edge."""
    def ix(a, b, xa, xb):
        # where between two samples the contour crosses
        if abs(b - a) < 1e-9:
            return xa
        return xa + (xb - xa) * (LEVEL - a) / (b - a)

    out = []
    for y in range(h - 1):
        for x in range(w - 1):
            tl, tr = g[y][x], g[y][x + 1]
            bl, br = g[y + 1][x], g[y + 1][x + 1]
            case = ((tl > LEVEL) << 3) | ((tr > LEVEL) << 2) | \
                   ((br > LEVEL) << 1) | (bl > LEVEL)
            if case in (0, 15):
                continue
            top = (ix(tl, tr, x, x + 1), y)
            bot = (ix(bl, br, x, x + 1), y + 1)
            lef = (x, ix(tl, bl, y, y + 1))
            rig = (x + 1, ix(tr, br, y, y + 1))
            pairs = {
                1: [(lef, bot)], 2: [(bot, rig)], 3: [(lef, rig)],
                4: [(top, rig)], 5: [(lef, top), (bot, rig)],
                6: [(top, bot)], 7: [(lef, top)], 8: [(lef, top)],
                9: [(top, bot)], 10: [(lef, bot), (top, rig)],
                11: [(top, rig)], 12: [(lef, rig)], 13: [(bot, rig)],
                14: [(lef, bot)],
            }[case]
            out.extend(pairs)
    return out


def rings(segs):
    """Join segments end to end into closed loops.

    Marching squares emits each edge crossing independently and in no order,
    so the join has to work from both ends of a segment and consume each one
    exactly once. An earlier version looked segments up with list.index, which
    matches the first identical segment rather than the one being followed —
    that shattered every contour into slivers.
    """
    def key(p):
        return (round(p[0], 3), round(p[1], 3))

    ends = {}
    for i, (a, b) in enumerate(segs):
        ends.setdefault(key(a), []).append((i, 0))
        ends.setdefault(key(b), []).append((i, 1))

    used = [False] * len(segs)
    loops = []
    for i0 in range(len(segs)):
        if used[i0]:
            continue
        used[i0] = True
        a, b = segs[i0]
        loop = [a, b]
        cur = b
        while True:
            nxt = None
            for j, which in ends.get(key(cur), []):
                if used[j]:
                    continue
                pa, pb = segs[j]
                # follow whichever end of j touches where we are
                nxt = (j, pb if which == 0 else pa)
                break
            if nxt is None:
                break
            used[nxt[0]] = True
            loop.append(nxt[1])
            cur = nxt[1]
            if key(cur) == key(a):
                break
        if len(loop) >= MIN_RING:
            loops.append(loop)
    return loops


def rdp(pts, eps):
    if len(pts) < 3:
        return pts
    ax, ay = pts[0]
    bx, by = pts[-1]
    dx, dy = bx - ax, by - ay
    n = (dx * dx + dy * dy) ** 0.5 or 1e-9
    worst, at = 0.0, 0
    for i in range(1, len(pts) - 1):
        px, py = pts[i]
        d = abs(dy * px - dx * py + bx * ay - by * ax) / n
        if d > worst:
            worst, at = d, i
    if worst <= eps:
        return [pts[0], pts[-1]]
    return rdp(pts[:at + 1], eps)[:-1] + rdp(pts[at:], eps)


def main():
    w, h, g = grid(SRC)
    loops = rings(segments(w, h, g))
    scale = VIEW_W / w
    paths = []
    for loop in loops:
        pts = rdp(loop, EPS)
        if len(pts) < 4:
            continue
        d = "M" + " L".join(f"{x * scale:.1f},{y * scale:.1f}" for x, y in pts) + "Z"
        paths.append(d)
    paths.sort(key=len, reverse=True)

    sys.setrecursionlimit(10000)
    print('"""Vector outlines of the company mark, produced by trace.py.')
    print()
    print("Do not hand-edit: re-run `python3 trace.py > mark_paths.py` instead.")
    print('"""')
    print(f"VIEW = ({VIEW_W}, {round(h * scale)})")
    print("PATHS = [")
    for d in paths:
        print(f'    "{d}",')
    print("]")
    total = sum(len(d) for d in paths)
    print(f"# {len(paths)} rings, {total} chars", file=sys.stderr)


if __name__ == "__main__":
    sys.setrecursionlimit(20000)
    main()
