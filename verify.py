#!/usr/bin/env python3
"""Checks that must pass before this goes in front of anyone.

Static only — no browser needed. Run after every build.

    python3 verify.py
"""
import ast
import os
import re
import sys
from html.parser import HTMLParser

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
problems = []


def fail(msg):
    problems.append(msg)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.assets, self.imgs = [], [], []
        self.h1 = 0
        self.title = self.desc = self.robots = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag == "img":
            self.imgs.append((a.get("src", ""), a.get("alt")))
            if a.get("src"):
                self.assets.append(a["src"])
        elif tag in ("link", "script") and (a.get("href") or a.get("src")):
            self.assets.append(a.get("href") or a.get("src"))
        elif tag == "h1":
            self.h1 += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            if a.get("name") == "description":
                self.desc = a.get("content", "")
            elif a.get("name") == "robots":
                self.robots = a.get("content", "")

    def handle_data(self, d):
        if self._in_title:
            self.title += d

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False


def check_pages():
    pages = sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))
    if not pages:
        fail("no HTML built — run: python3 build.py")
        return
    titles, descs = {}, {}
    for name in pages:
        p = Page()
        p.feed(open(os.path.join(ROOT, name), encoding="utf-8").read())
        if p.h1 != 1:
            fail(f"{name}: {p.h1} <h1> elements (want exactly 1)")
        if not p.desc:
            fail(f"{name}: no meta description")
        if C.NOINDEX and "noindex" not in p.robots:
            fail(f"{name}: NOINDEX on but robots={p.robots!r}")
        # 404 opts out on purpose, even on a live build
        if not C.NOINDEX and "noindex" in p.robots and name != "404.html":
            fail(f"{name}: NOINDEX off but page still says noindex")
        titles.setdefault(p.title.strip(), []).append(name)
        descs.setdefault(p.desc.strip(), []).append(name)
        for src, alt in p.imgs:
            if alt is None:
                fail(f"{name}: <img> without alt: {src}")
        for ref in set(p.assets):
            if ref.startswith(("http", "//", "data:")):
                continue
            if not os.path.exists(os.path.join(ROOT, ref.split("?")[0])):
                fail(f"{name}: missing asset {ref}")
        for href in set(p.links):
            if href.startswith(("http", "mailto:", "tel:", "#", "//")):
                continue
            target = href.split("#")[0]
            if target and not os.path.exists(os.path.join(ROOT, target)):
                fail(f"{name}: broken link -> {href}")
    for t, names in titles.items():
        if len(names) > 1:
            fail(f"duplicate <title> {t!r} on {names}")
    for _, names in descs.items():
        if len(names) > 1:
            fail(f"duplicate meta description on {names}")
    print(f"  {len(pages)} pages checked")


def check_contrast():
    """WCAG AA on the pairs that carry real text."""
    css = open(os.path.join(ROOT, "styles.css")).read()
    root = re.search(r":root\{([^}]*)\}", css)
    t = dict(re.findall(r"--([\w-]+):(#[0-9A-Fa-f]{6})", root.group(1)))

    def lum(h):
        h = h.lstrip("#")
        ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        ch = [v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4 for v in ch]
        return .2126 * ch[0] + .7152 * ch[1] + .0722 * ch[2]

    def ratio(a, b):
        la, lb = lum(a), lum(b)
        return (max(la, lb) + .05) / (min(la, lb) + .05)

    pairs = [("ink", "bg", "body text"),
             ("muted", "bg", "secondary text"),
             ("faint", "bg", "captions"),
             ("heat-2", "bg", "eyebrow / accent text"),
             ("on-heat", "heat", "button label"),
             ("ink", "surface", "text on cards"),
             ("muted", "surface", "secondary on cards")]
    for a, b, what in pairs:
        if a not in t or b not in t:
            fail(f"contrast check: token --{a} or --{b} missing")
            continue
        r = ratio(t[a], t[b])
        # captions are large-ish/uppercase mono; hold them to the AA large bar
        floor = 3.0 if a == "faint" else 4.5
        if r < floor:
            fail(f"{what} (--{a} on --{b}) is {r:.2f}:1, below {floor}:1")
    print("  contrast AA passes")


def check_single_source():
    """build.py must stay a generator — no client-visible copy in it."""
    src = open(os.path.join(ROOT, "build.py")).read()
    doc = ast.get_docstring(ast.parse(src))
    if doc:
        src = src.replace(doc, "")
    for label, value in [("phone", C.PHONE), ("email", C.EMAIL),
                         ("company name", C.NAME), ("GSTIN", C.GSTIN),
                         ("contact name", C.CONTACT_NAME),
                         ("address", C.ADDRESS_LINES[0])]:
        if value in src:
            fail(f"{label} {value!r} is hard-coded in build.py — belongs in content.py")
    print("  build.py holds no content")


def check_temperature_data():
    """The scale is the centrepiece; bad data would be visible and wrong."""
    for name, table in [("TEMPER_COLOURS", C.TEMPER_COLOURS),
                        ("GLOW_COLOURS", C.GLOW_COLOURS)]:
        temps = [t for t, _, _ in table]
        if temps != sorted(temps):
            fail(f"{name} is not in ascending temperature order")
        for t, hexv, label in table:
            if not re.fullmatch(r"#[0-9A-Fa-f]{6}", hexv):
                fail(f"{name}: {label} has a malformed colour {hexv!r}")
            if not (C.TEMP_MIN <= t <= C.TEMP_MAX):
                fail(f"{name}: {t}degC is outside the scale range")

    # bands must tile the whole range with no gap and no overlap
    bands = sorted(C.TEMP_BANDS, key=lambda b: b[0])
    if bands[0][0] > C.TEMP_MIN:
        fail(f"TEMP_BANDS starts at {bands[0][0]}, leaving {C.TEMP_MIN} uncovered")
    if bands[-1][1] <= C.TEMP_MAX:
        fail(f"TEMP_BANDS ends at {bands[-1][1]}, leaving {C.TEMP_MAX} uncovered")
    for i in range(len(bands) - 1):
        if bands[i][1] != bands[i + 1][0]:
            fail(f"TEMP_BANDS gap/overlap between {bands[i][1]} and {bands[i + 1][0]}")
    print(f"  temperature scale: {len(bands)} bands cover "
          f"{C.TEMP_MIN}-{C.TEMP_MAX}degC continuously")


def check_heat_text_contrast():
    """The hero word and the header brand paint themselves from the glow scale.
    Nothing in the stylesheet pins those colours, so the only thing keeping
    them readable is where each range starts. A floor set too low makes the
    company name fade into the header for part of every cycle."""
    def lin(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4

    def lum(c):
        return 0.2126 * lin(c[0]) + 0.7152 * lin(c[1]) + 0.0722 * lin(c[2])

    def ratio(a, b):
        la, lb = lum(a), lum(b)
        hi, lo = max(la, lb), min(la, lb)
        return (hi + 0.05) / (lo + 0.05)

    def hx(h):
        h = h.lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def sample(t):
        stops = [(k, hx(v)) for k, v, _ in C.GLOW_COLOURS]
        if t <= stops[0][0]:
            return stops[0][1]
        if t >= stops[-1][0]:
            return stops[-1][1]
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                f = (t - t0) / (t1 - t0)
                return tuple(round(a + (b - a) * f) for a, b in zip(c0, c1))
        return stops[-1][1]

    GROUND = (8, 12, 20)           # --bg, behind both the hero and the header
    # 3:1 for the headline (large text); 4.5:1 for the brand, which drops to
    # 16px on a phone and stops counting as large text there.
    for label, rng, need in [("hero word", C.HERO_HEAT_RANGE, 3.0),
                             ("header brand", C.BRAND_HEAT_RANGE, 4.5)]:
        worst = min(ratio(sample(t), GROUND)
                    for t in range(rng[0], rng[1] + 1, 5))
        if worst < need:
            fail(f"{label}: {rng[0]}-{rng[1]}degC drops to {worst:.2f}:1 "
                 f"against the ground, needs {need}:1 — raise the lower bound")
    print("  heat-driven text stays legible across its whole cycle")


def check_media():
    referenced = ({C.HERO_IMAGE, C.ABOUT_IMAGE}
                  | {p["image"] for p in C.PROCESSES}
                  | {q["image"] for q in C.QUALITY}
                  | {f"plate-{n}" for n in range(1, 7)})
    missing = [s for s in referenced
               if not os.path.exists(os.path.join(ROOT, "assets", "img", s + ".webp"))]
    if missing:
        fail(f"referenced image(s) not built: {sorted(missing)} "
             "— run: python3 fetch_media.py && python3 assets.py && python3 tiles.py")
    else:
        print("  every referenced image exists")

    img_dir = os.path.join(ROOT, "assets", "img")
    big = [(f, os.path.getsize(os.path.join(img_dir, f)) // 1024)
           for f in os.listdir(img_dir)
           if os.path.getsize(os.path.join(img_dir, f)) > 450_000]
    if big:
        fail(f"oversized images (>450 KB): {big} — re-run assets.py")


if __name__ == "__main__":
    print("verifying build\n")
    check_pages()
    check_contrast()
    check_single_source()
    check_temperature_data()
    check_heat_text_contrast()
    check_media()
    print()
    if problems:
        print(f"{len(problems)} PROBLEM(S):")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("all checks passed")
    if C.NOINDEX:
        print("\nnote: pages are noindex (concept build)")
    if C.SHOW_CONCEPT_NOTE:
        print("note: the 'figures are illustrative' banner is ON")
