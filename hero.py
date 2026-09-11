#!/usr/bin/env python3
"""Renders the hero image instead of sourcing a photograph.

    python3 hero.py

A billet at heat, running the full working range from cold steel on the left
to white heat on the right. The colour ramp is sampled from the same
TEMPER_COLOURS / GLOW_COLOURS tables that drive the temperature scale on the
homepage, so the picture and the interactive control are the same palette
rather than two things that happen to both be orange.

Composition is built around the copy: the left third stays dark so the
headline sits on near-black, and the heat and bloom gather to the right where
the image is uncovered.

Output goes straight to assets/img/ as WebP, sized and budgeted to match what
assets.py produces for the other wide images. Nothing here needs the network,
so the asset is fully reproducible from this file.
"""
import math
import os
import random

from PIL import Image, ImageChops, ImageDraw, ImageFilter

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "assets", "img")

NAME = "billet-heat"
W, H = 2400, 1500
BUDGET = 420_000           # the wide-image budget assets.py works to
QUALITY_STEPS = (86, 82, 76, 70, 64, 58)

random.seed(20260911)      # a fixed seed keeps rebuilds byte-identical


# ----------------------------------------------------------- colour ramp ---

def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _sample(table, t):
    """Interpolate a [(temp, hex, name)] table at t."""
    stops = [(k, _hex(v)) for k, v, _ in table]
    if t <= stops[0][0]:
        return stops[0][1]
    if t >= stops[-1][0]:
        return stops[-1][1]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t0 <= t <= t1:
            f = (t - t0) / (t1 - t0)
            return tuple(round(a + (b - a) * f) for a, b in zip(c0, c1))
    return stops[-1][1]


GLOW_FROM = C.GLOW_COLOURS[0][0]      # first visible red
OXIDE_TO = C.TEMPER_COLOURS[-1][0]    # last oxide colour


def colour_at(t):
    """The site's own rule: oxide film below, incandescence above, blended."""
    ox = _sample(C.TEMPER_COLOURS, t)
    gl = _sample(C.GLOW_COLOURS, t)
    if t <= OXIDE_TO:
        return ox
    if t >= GLOW_FROM:
        return gl
    f = (t - OXIDE_TO) / (GLOW_FROM - OXIDE_TO)
    return tuple(round(a + (b - a) * f) for a, b in zip(ox, gl))


def heat_at(t):
    """0 while the steel is dark, 1 at white heat. Drives bloom and sparks."""
    if t <= GLOW_FROM:
        return 0.0
    return min(1.0, (t - GLOW_FROM) / (C.TEMP_MAX - GLOW_FROM))


# --------------------------------------------------------------- helpers ---

def vgrad(size, top, bottom):
    """A vertical gradient, built one pixel wide and stretched."""
    strip = Image.new("RGB", (1, 256))
    px = strip.load()
    for y in range(256):
        f = y / 255
        px[0, y] = tuple(round(a + (b - a) * f) for a, b in zip(top, bottom))
    return strip.resize(size, Image.BILINEAR)


def noise(size, blur=0):
    """Cheap grain — random bytes are far faster than a Python pixel loop."""
    w, h = size
    n = Image.frombytes("L", (w, h), os.urandom(w * h))
    if blur:
        n = n.filter(ImageFilter.GaussianBlur(blur))
    return n


def temp_for_x(x):
    """Map image x to a temperature, biased so the hot range gets the room."""
    f = x / (W - 1)
    return C.TEMP_MIN + (C.TEMP_MAX - C.TEMP_MIN) * (f ** 1.35)


# ----------------------------------------------------------------- build ---

def build():
    # 1. the room: a cold near-black, very slightly warmer along the bottom
    base = vgrad((W, H), (10, 13, 20), (4, 5, 9))

    # 2. the billet. Colour runs along x; form shading runs down y.
    bar_top, bar_h = int(H * 0.300), int(H * 0.125)
    bar_x0, bar_x1 = int(W * 0.055), W + bar_h   # runs off the right edge

    ramp = Image.new("RGB", (W, 1))
    rpx = ramp.load()
    for x in range(W):
        t = temp_for_x(x)
        c = colour_at(t)
        # brightness climbs only as the steel starts to glow, so the cold end
        # sits back in the dark where the headline needs it
        lum = 0.12 + 0.88 * (heat_at(t) ** 0.75)
        rpx[x, 0] = tuple(max(0, min(255, round(v * lum))) for v in c)
    ramp = ramp.resize((W, bar_h), Image.BILINEAR)

    # cylindrical shading: dark at the top edge, a specular line a third down,
    # falling to a warm underside
    form = Image.new("L", (1, bar_h))
    fpx = form.load()
    for y in range(bar_h):
        f = y / (bar_h - 1)
        spec = math.exp(-((f - 0.34) ** 2) / 0.020)     # the highlight
        body = 0.42 + 0.46 * math.sin(math.pi * min(1.0, f * 1.06))
        fpx[0, y] = max(0, min(255, round((body + spec * 0.55) * 235)))
    form = form.resize((W, bar_h), Image.BILINEAR)

    billet = Image.new("RGB", (W, H), (0, 0, 0))
    lit = ImageChops.multiply(ramp, Image.merge("RGB", (form, form, form)))
    billet.paste(lit, (0, bar_top))

    # rounded ends, and the bar only exists between x0 and x1
    shape = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shape).rounded_rectangle(
        [bar_x0, bar_top, bar_x1, bar_top + bar_h],
        radius=bar_h // 2, fill=255)
    shape = shape.filter(ImageFilter.GaussianBlur(2.2))
    billet = ImageChops.multiply(billet, Image.merge("RGB", (shape,) * 3))

    # 3. bloom. Two passes: a tight halo and a wide atmospheric one, both
    #    weighted by how hot that part of the bar actually is.
    heat_mask = Image.new("L", (W, 1))
    hpx = heat_mask.load()
    for x in range(W):
        hpx[x, 0] = round(255 * heat_at(temp_for_x(x)) ** 1.6)
    heat_mask = heat_mask.resize((W, H), Image.BILINEAR)

    hot = ImageChops.multiply(billet, Image.merge("RGB", (heat_mask,) * 3))
    tight = hot.filter(ImageFilter.GaussianBlur(26))
    wide = hot.filter(ImageFilter.GaussianBlur(130))

    out = ImageChops.add(base, wide.point(lambda v: int(v * 0.42)))
    out = ImageChops.add(out, tight.point(lambda v: int(v * 0.26)))
    # and now the billet itself, sharp, on top of the light it is throwing
    out = ImageChops.add(out, ImageChops.multiply(
        billet, Image.merge("RGB", (shape,) * 3)))

    # 4. the floor: a soft reflection, fading as it falls away from the bar
    refl = hot.transpose(Image.FLIP_TOP_BOTTOM)
    refl = ImageChops.offset(refl, 0, (bar_top + bar_h) * 2 - H + 26)
    refl = refl.filter(ImageFilter.GaussianBlur(26))
    fade = Image.new("L", (1, H))
    fpx2 = fade.load()
    floor0 = bar_top + bar_h
    for y in range(H):
        if y <= floor0:
            fpx2[0, y] = 0
        else:
            f = (y - floor0) / max(1, H - floor0)
            fpx2[0, y] = round(255 * max(0.0, (1 - f) ** 2.4) * 0.38)
    fade = fade.resize((W, H), Image.BILINEAR)
    out = ImageChops.add(out, ImageChops.multiply(
        refl, Image.merge("RGB", (fade,) * 3)))

    # 5. sparks, thrown from the hot end only
    sparks = Image.new("RGB", (W, H), (0, 0, 0))
    sd = ImageDraw.Draw(sparks)
    for _ in range(230):
        x = int(W * (0.30 + 0.70 * random.random() ** 0.7))
        h = heat_at(temp_for_x(x))
        if random.random() > h * 0.95:
            continue
        y = bar_top + bar_h * 0.5 + random.gauss(0, bar_h * 1.5)
        if not (0 < y < H):
            continue
        r = random.uniform(1.2, 3.4)
        c = colour_at(min(C.TEMP_MAX, temp_for_x(x) + 140))
        sd.ellipse([x - r, y - r, x + r, y + r], fill=c)
    sparks = sparks.filter(ImageFilter.GaussianBlur(1.4))
    out = ImageChops.add(out, sparks.point(lambda v: int(v * 0.9)))

    # 6. Exposure. The hero puts filter:brightness(.62) over the image and
    #    then a dark gradient on top of that, both sized for a photograph.
    #    Pre-compensate here rather than weakening the CSS the rest of the
    #    design depends on.
    out = out.point(lambda v: min(255, int(v * 1.55)))

    # 7. grain, so the gradients never band on a large display
    g = noise((W // 3, H // 3), blur=0.6).resize((W, H), Image.BILINEAR)
    g = g.point(lambda v: 128 + (v - 128) // 9)
    out = ImageChops.overlay(out, Image.merge("RGB", (g,) * 3))

    return out


def save(im):
    os.makedirs(OUT, exist_ok=True)
    dest = os.path.join(OUT, NAME + ".webp")
    for q in QUALITY_STEPS:
        im.save(dest, "WEBP", quality=q, method=6)
        if os.path.getsize(dest) <= BUDGET:
            return dest, q, os.path.getsize(dest)
    return dest, QUALITY_STEPS[-1], os.path.getsize(dest)


if __name__ == "__main__":
    dest, q, size = save(build())
    print(f"{os.path.relpath(dest, ROOT)}  {W}x{H}  q{q}  {size // 1024} KB")
