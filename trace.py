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

LEVEL = 0.5          # alpha midpoint
UPSCALE = 2          # trace the PDF original at twice its size: the
                     # interpolated edge is far smoother than the pixels
EPS = 0.9            # RDP tolerance, in upscaled pixels
MIN_RING = 7         # low, so the pine trees survive
MIN_BLOB = 40        # upscaled pixels; drops specks, keeps the trees
VIEW_W = 680         # the viewBox the paths are written against


def grid():
    """The mark straight from the company profile, black on white, at full
    resolution and upscaled, rather than the 340px header copy."""
    from logo import source
    im = source().convert("L")
    im = im.resize((im.width * UPSCALE, im.height * UPSCALE), Image.LANCZOS)
    # dark is ink: invert so the mark is the foreground
    a = im.point(lambda v: 255 - v)
    box = a.point(lambda v: 255 if v > 60 else 0).getbbox()
    a = a.crop((box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2))
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


def components(w, h, g):
    """Split the foreground into separate blobs.

    The mark is not one shape: the crevasse slivers inside the peaks, each
    pine tree and the lower sweep are all detached. Tracing the whole grid at
    once let the walk hop between them wherever two contours passed close, and
    everything but the outer boundary was swallowed. Labelling first keeps
    them apart, and each blob is then traced on a grid of its own.
    """
    seen = [[False] * w for _ in range(h)]
    blobs = []
    for sy in range(h):
        for sx in range(w):
            if seen[sy][sx] or g[sy][sx] <= LEVEL:
                continue
            stack = [(sx, sy)]
            seen[sy][sx] = True
            cells = []
            while stack:
                x, y = stack.pop()
                cells.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1),
                               (1, 1), (1, -1), (-1, 1), (-1, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] \
                            and g[ny][nx] > LEVEL:
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if len(cells) >= MIN_BLOB:
                blobs.append(cells)
    return blobs


def rdp_closed(ring, eps):
    """Simplify a closed ring.

    Plain RDP cannot do this: on a loop the first and last point coincide, so
    the baseline it measures against has zero length, every distance comes out
    as zero and it hands back two points. Split the ring at the point furthest
    from its start, simplify the two open chains, then rejoin.
    """
    pts = ring[:-1] if len(ring) > 1 and ring[0] == ring[-1] else ring[:]
    if len(pts) < 4:
        return pts
    ax, ay = pts[0]
    far, at = -1.0, 0
    for i, (x, y) in enumerate(pts):
        d = (x - ax) ** 2 + (y - ay) ** 2
        if d > far:
            far, at = d, i
    first = rdp(pts[:at + 1], eps)
    second = rdp(pts[at:] + [pts[0]], eps)
    return first[:-1] + second[:-1]


def main():
    w, h, g = grid()
    scale = VIEW_W / w
    paths = []
    for cells in components(w, h, g):
        xs = [c[0] for c in cells]
        ys = [c[1] for c in cells]
        # a 1px margin so the blob never touches the edge of its own grid
        x0, x1 = min(xs) - 1, max(xs) + 2
        y0, y1 = min(ys) - 1, max(ys) + 2
        bw, bh = x1 - x0, y1 - y0
        sub = [[0.0] * bw for _ in range(bh)]
        for x, y in cells:
            sub[y - y0][x - x0] = 1.0
        for loop in rings(segments(bw, bh, sub)):
            pts = rdp_closed(loop, EPS)
            if len(pts) < 4:
                continue
            d = "M" + " L".join(
                f"{(x + x0) * scale:.1f},{(y + y0) * scale:.1f}"
                for x, y in pts) + "Z"
            paths.append(d)
    paths.sort(key=len, reverse=True)
    # all rings as one path too: filled even-odd, the holes (the crevasses
    # in the peaks) come out as holes
    whole = "".join(paths)

    print('"""Vector outlines of the company mark, produced by trace.py.')
    print()
    print("Do not hand-edit: re-run `python3 trace.py > mark_paths.py` instead.")
    print('"""')
    print(f"VIEW = ({VIEW_W}, {round(h * scale)})")
    print("PATHS = [")
    for d in paths:
        print(f'    "{d}",')
    print("]")
    print(f'WHOLE = "{whole}"')
    print(f"# {len(paths)} rings, {sum(len(d) for d in paths)} chars",
          file=sys.stderr)


if __name__ == "__main__":
    sys.setrecursionlimit(20000)
    main()
