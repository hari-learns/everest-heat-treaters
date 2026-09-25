#!/usr/bin/env python3
"""Generate the Everest Heat Treaters concept site.

A generator only. Every human-readable string lives in content.py.

    python3 build.py

Writes .html into the repo root, which is what GitHub Pages serves.
"""
import hashlib
import html
import json
import os
import re

import content as C
import mark_paths as MARK

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "assets", "img")

try:
    from PIL import Image
except ImportError:
    Image = None


def esc(s):
    return html.escape(str(s), quote=True)


def version(path):
    full = os.path.join(ROOT, path)
    if not os.path.exists(full):
        return "0"
    with open(full, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:12]


CSS_V = version("styles.css")
JS_V = version("script.js")

_dims = {}


def dims(slug):
    if slug in _dims:
        return _dims[slug]
    path = os.path.join(IMG_DIR, slug + ".webp")
    size = None
    if Image and os.path.exists(path):
        try:
            with Image.open(path) as im:
                size = im.size
        except Exception:
            size = None
    _dims[slug] = size
    return size


def has_img(slug):
    return os.path.exists(os.path.join(IMG_DIR, slug + ".webp"))


def img(slug, alt, cls="", eager=False, sizes=""):
    """An <img>, or a heat-gradient block if the asset is missing. A broken
    image icon in the middle of a client pitch is not survivable."""
    if not has_img(slug):
        return (f'<div class="img-fallback {cls}" role="img" '
                f'aria-label="{esc(alt)}"></div>')
    size = dims(slug)
    wh = f' width="{size[0]}" height="{size[1]}"' if size else ""
    loading = "" if eager else ' loading="lazy" decoding="async"'
    sz = f' sizes="{sizes}"' if sizes else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<img src="assets/img/{slug}.webp" alt="{esc(alt)}"'
            f'{cls_attr}{wh}{loading}{sz}>')


def video(slug, caption, cls=""):
    """A phone video from media.py. Nothing downloads until it is played:
    the poster is a small WebP and preload is off."""
    cls_attr = f' class="{cls}"' if cls else ""
    wh = ""
    poster = os.path.join(ROOT, "assets", "video", slug + ".webp")
    if Image and os.path.exists(poster):
        with Image.open(poster) as im:
            wh = f' width="{im.size[0]}" height="{im.size[1]}"'
    return (f'<video{cls_attr} src="assets/video/{slug}.mp4" '
            f'poster="assets/video/{slug}.webp"{wh} preload="none" controls '
            f'playsinline aria-label="{esc(caption)}"></video>')


def tile(entry, i=0, sizes="(max-width:700px) 50vw, 25vw"):
    """One gallery item. Photos open in the lightbox; videos play in place."""
    slug, cap = entry[0], entry[1]
    if len(entry) > 2 and entry[2] == "video":
        return (f'<figure class="shot shot--video" data-reveal style="--i:{i % 6}">'
                f'{video(slug, cap)}'
                f'<figcaption><span class="shot__tag">Video</span>{cap}</figcaption></figure>')
    return (f'<figure class="shot" data-reveal style="--i:{i % 6}">'
            f'<a href="assets/img/{slug}.webp" data-lightbox aria-label="Open: {esc(cap)}">'
            f'{img(slug, cap, sizes=sizes)}</a>'
            f'<figcaption>{cap}</figcaption></figure>')


# --------------------------------------------------------------- chrome ----

def nav(current):
    return "\n        ".join(
        f'<a href="{h}" style="--n:{i}"{" aria-current=\"page\"" if h == current else ""}>{l}</a>'
        for i, (h, l) in enumerate(C.NAV))


def logo():
    """The company's own mark, from the 2025 profile — see logo.py. Carried as
    an alpha mask rather than a picture so it takes the brand colour."""
    return '<span class="logo" aria-hidden="true"><i class="logo__mark"></i></span>'


# The incandescent stops, handed to anything that paints itself from the
# heat scale. Escaped once here rather than per page.
HEAT_STOPS = html.escape(json.dumps(
    [[t, hexv] for t, hexv, _ in C.GLOW_COLOURS],
    separators=(",", ":")), quote=True)


def hero_mark():
    """The company mark, drawn in.

    trace.py lifts the mountain from the profile PDF at full resolution. The
    outlines draw themselves first, peak by peak; then the solid mark fills
    in underneath them and a band of heat travels slowly across it. It is
    the logo itself, and sharp at any size.
    """
    w, h = MARK.VIEW
    lines = "".join(
        f'<path d="{d}" pathLength="1" style="--d:{i * 0.14:.2f}s"/>'
        for i, d in enumerate(MARK.PATHS))
    return f"""<figure class="mark" aria-hidden="true">
  <svg class="mark__svg" viewBox="-12 -12 {w + 24} {h + 24}" focusable="false">
    <defs>
      <linearGradient id="markfill" x1="0" y1="0" x2="1" y2="0.35">
        <stop offset="0" stop-color="#E85F06"/>
        <stop offset=".3" stop-color="#FF8A1F"/>
        <stop offset=".5" stop-color="#FFD26B"/>
        <stop offset=".7" stop-color="#FF8A1F"/>
        <stop offset="1" stop-color="#E85F06"/>
        <animate attributeName="x1" values="-1;0;-1" dur="11s" repeatCount="indefinite"/>
        <animate attributeName="x2" values="0;2;0" dur="11s" repeatCount="indefinite"/>
      </linearGradient>
      <linearGradient id="markline" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#FFD26B"/><stop offset="1" stop-color="#FF7A1A"/>
      </linearGradient>
      <filter id="markglow" x="-10%" y="-20%" width="120%" height="140%">
        <feGaussianBlur stdDeviation="7" result="b"/>
        <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
      </filter>
    </defs>
    <path class="mark__fill" d="{MARK.WHOLE}" fill="url(#markfill)" fill-rule="evenodd" filter="url(#markglow)"/>
    <g class="mark__lines">{lines}</g>
  </svg>
</figure>"""


def header(current):
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr" data-header>
  <div class="hdr__in">
    <a class="brand" href="index.html">
      {logo()}
      <span class="brand__txt">
        <span class="brand__name" data-heat-brand
              data-heat-scale="{HEAT_STOPS}"
              data-heat-lo="{C.BRAND_HEAT_RANGE[0]}"
              data-heat-hi="{C.BRAND_HEAT_RANGE[1]}">{C.NAME}</span>
        <span class="brand__sub">{C.CERT}</span>
      </span>
    </a>
    <nav class="nav" aria-label="Primary">
        {nav(current)}
    </nav>
    <div class="hdr__act">
      <a class="btn btn--sm" href="contact.html"{" aria-current=\"page\"" if current == "contact.html" else ""}>Contact</a>
      <button class="burger" type="button" aria-label="Open menu"
              aria-expanded="false" aria-controls="drawer" data-burger>
        <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"
             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <path d="M3 6h18M3 12h18M3 18h18"/>
        </svg>
      </button>
    </div>
  </div>
</header>
<div class="drawer" id="drawer" data-drawer hidden>
  <button class="drawer__x" type="button" aria-label="Close menu" data-drawer-close>
    <svg viewBox="0 0 24 24" width="26" height="26" fill="none"
         stroke="currentColor" stroke-width="2" stroke-linecap="round">
      <path d="M5 5l14 14M19 5L5 19"/>
    </svg>
  </button>
  <nav class="drawer__nav" aria-label="Mobile">
        {nav(current)}
  </nav>
  <a class="btn btn--block" href="contact.html">Contact</a>
  <div class="drawer__meta">
    <a href="tel:{C.PHONE_LINK}">{C.PHONE}</a>
    <a href="mailto:{C.EMAIL}">{C.EMAIL}</a>
  </div>
</div>'''


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>'
                    for h, l in C.NAV + [C.CONTACT_PAGE])
    procs = "".join(
        f'<li><a href="processes.html#{p["slug"]}">{p["name"]}</a></li>'
        for p in C.PROCESSES[:6])
    addr = "<br>".join(C.ADDRESS_LINES)
    note = (f'<p class="foot__note">{C.FOOTER_NOTE}</p>'
            if C.SHOW_CONCEPT_NOTE else "")
    return f'''
<footer class="foot">
  <div class="wrap foot__in">
    <div class="foot__brand">
      <div class="foot__mark">{logo()}</div>
      <p class="foot__name">{C.NAME}</p>
      <p class="foot__tag">{C.TAGLINE}</p>
      <p class="foot__cert">{C.CERT}</p>
      <p class="foot__gst">GSTIN <span>{C.GSTIN}</span></p>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Works</h2>
      <address>{addr}</address>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Contact</h2>
      {"".join(f'<p>{n}{", " + q if q else ""}<br><span class="foot__role">{r}</span>'
               f'{f"""<br><a href="tel:{tl}">{ph}</a>""" if ph else ""}</p>'
               for n, r, q, ph, tl in C.CONTACTS)}
      <p><a href="tel:{C.PHONE_LINK}">{C.PHONE}</a></p>
      <p><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Processes</h2>
      <ul>{procs}</ul>
    </div>
    <div class="foot__col">
      <h2 class="foot__h">Site</h2>
      <ul>{links}</ul>
    </div>
  </div>
  <div class="wrap foot__base">
    <p>&copy; 2026 {C.NAME}</p>
    {note}
  </div>
</footer>
<a class="wa" href="https://wa.me/{C.WHATSAPP}" target="_blank" rel="noopener"
   aria-label="Message us on WhatsApp">
  <svg viewBox="0 0 24 24" aria-hidden="true" width="24" height="24"><path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.82 9.82 0 0 0 12.04 2Zm0 18.15h-.01a8.2 8.2 0 0 1-4.19-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.18 8.18 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24 2.2 0 4.27.86 5.83 2.42a8.19 8.19 0 0 1 2.41 5.83c0 4.54-3.69 8.23-8.24 8.23Zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.24-.64.8-.78.97-.15.16-.29.18-.53.06-.25-.12-1.05-.39-1.99-1.23-.74-.66-1.23-1.47-1.38-1.72-.14-.25-.01-.38.11-.5.11-.11.25-.29.37-.43.12-.15.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.47c-.17 0-.43.06-.66.31-.22.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>
</a>'''


def clean_urls(doc):
    """Link to /about rather than /about.html, and to / rather than
    /index.html. GitHub Pages serves about.html for /about by itself, so the
    files keep their names and only the links change. A local
    `python3 -m http.server` does not do this; preview with the live site or
    a server that tries .html."""
    doc = re.sub(r'href="index\.html(?=[#"?])', 'href="./', doc)
    return re.sub(r'href="([a-z0-9-]+)\.html(?=[#"?])', r'href="\1', doc)


def page(path, title, description, body, current="", noindex=False):
    # a 404 is never worth indexing, even on a live build
    robots = "noindex, nofollow" if (C.NOINDEX or noindex) else "index, follow"
    doc = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<meta name="robots" content="{robots}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#080C14">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="favicon.png">
<link rel="preload" href="fonts/archivo.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css?v={CSS_V}">
</head>
<body>
{header(current)}
<main id="main">
{body}
</main>
{footer()}
<script src="script.js?v={JS_V}" defer></script>
</body>
</html>'''
    doc = clean_urls(doc)
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path


# -------------------------------------------------------------- helpers ----

def sec_head(eyebrow, title, text="", mid=False):
    t = f'<p class="lede">{text}</p>' if text else ""
    return f'''<div class="sec__head{" sec__head--mid" if mid else ""}" data-reveal>
  <p class="eyebrow">{eyebrow}</p>
  <h2 class="h2">{title}</h2>
  {t}
</div>'''


def cta():
    return f'''
<section class="band">
  <div class="wrap band__in" data-reveal>
    <p class="eyebrow">Contact</p>
    <h2 class="h2">{C.CTA_TITLE}</h2>
    <p class="lede">{C.CTA_TEXT}</p>
    <div class="band__act">
      <a class="btn" href="contact.html#enquire">Contact us</a>
      <a class="btn btn--ghost" href="https://wa.me/{C.WHATSAPP}"
         target="_blank" rel="noopener">WhatsApp {C.PHONE}</a>
    </div>
  </div>
</section>'''


def subhero(eyebrow, title, text, image=None):
    media = (f'<div class="subhero__media">{img(image, "", eager=True, sizes="100vw")}</div>'
             if image else "")
    return f'''
<section class="subhero{"" if image else " subhero--plain"}">
  {media}
  <div class="wrap subhero__in">
    <p class="eyebrow">{eyebrow}</p>
    <h1 class="h1">{title}</h1>
    <p class="lede">{text}</p>
  </div>
</section>'''


def people():
    """The managing director, then the metallurgist, as one block."""
    return "".join(
        f'<div class="person"><p class="person__name">{n}</p>'
        f'{f"<p class=person__quals>{q}</p>" if q else ""}'
        f'<p class="person__role">{r}</p>'
        f'{f"""<p class="person__tel"><a class="link" href="tel:{tl}">{ph}</a></p>""" if ph else ""}</div>'
        for n, r, q, ph, tl in C.CONTACTS)


def process_line(p, i=0):
    """One process on the homepage: its photograph and its name, pointing into
    the processes page. The write-up lives there and only there."""
    return f'''<a class="ptile" href="processes.html#{p["slug"]}" data-reveal style="--i:{i % 4}">
  {img(p["image"], "", sizes="(max-width:640px) 50vw, 25vw")}
  <h3 class="ptile__name">{p["name"]}</h3>
</a>'''


def process_section(p, i=0):
    """A process in full, on the processes page."""
    prose = "".join(f"<p>{x}</p>" for x in p["body"])
    pts = "".join(f"<li>{x}</li>" for x in p["points"])
    suits = "".join(f'<span class="chip">{x}</span>' for x in p["suits"])
    return f'''<article class="proc{" proc--flip" if i % 2 else ""}" id="{p["slug"]}">
  <figure class="proc__fig" data-reveal>{img(p["image"], p["name"], sizes="(max-width:900px) 100vw, 42vw")}</figure>
  <div class="proc__text" data-reveal>
    <h2 class="h2">{p["name"]}</h2>
    <p class="lede">{p["short"]}</p>
    <dl class="proc__spec">
      <div><dt>Result</dt><dd>{p["result"]}</dd></div>
    </dl>
    <div class="prose">{prose}</div>
    <div class="proc__how">
      <h3 class="proc__how-h">How we do it</h3>
      <p>{p["example"]}</p>
    </div>
    <ul class="ticks">{pts}</ul>
    <div class="chips">{suits}</div>
  </div>
</article>'''


def enquiry_form():
    opts = "".join(f'<option>{p["name"]}</option>' for p in C.PROCESSES)
    return f'''<form class="form" data-enquiry data-wa="{C.WHATSAPP}"
      data-endpoint="{esc(C.FORM_ENDPOINT)}" id="enquire" novalidate>
  <div class="form__row">
    <label><span class="form__lbl">Your name <i class="req">required</i></span><input type="text" name="name" required autocomplete="name"></label>
    <label><span class="form__lbl">Company</span><input type="text" name="company" autocomplete="organization"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Phone <i class="req">required</i></span><input type="tel" name="phone" required autocomplete="tel"></label>
    <label><span class="form__lbl">Email</span><input type="email" name="email" autocomplete="email"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Material grade</span><input type="text" name="grade" placeholder="EN31, SAE 8620&hellip;"></label>
    <label><span class="form__lbl">Treatment</span><select name="process">
      <option>General</option>{opts}</select></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Weight</span><input type="text" name="weight" placeholder="e.g. 400 kg"></label>
    <label><span class="form__lbl">Size</span><input type="text" name="size" placeholder="e.g. 60 dia &times; 450 mm"></label>
  </div>
  <div class="form__row">
    <label><span class="form__lbl">Hardness required</span><input type="text" name="hardness" placeholder="e.g. 58&ndash;62 HRC"></label>
    <label class="file"><span class="form__lbl">Drawing <i class="opt">PDF, image or DWG</i></span><input type="file" name="drawing"
      accept=".pdf,.png,.jpg,.jpeg,.webp,.dwg,.dxf"></label>
  </div>
  <label><span class="form__lbl">Part description or problem</span><textarea name="message" rows="4"
    placeholder="What the part does, what it runs against, how it is failing&hellip;"></textarea></label>
  <button class="btn btn--block" type="submit">Send enquiry</button>
  <p class="form__note">Name and phone are all we need. Everything else is optional. {C.RFQ_FIELDS_NOTE}</p>
</form>'''


# ---------------------------------------------------------------- pages ----

def build_home():
    stats = "".join(
        f'<div class="stat" data-reveal style="--i:{i}">'
        f'<b><span data-count="{v}">{v}</span><i class="stat__u">{u}</i></b>'
        f'<span class="stat__l">{l}</span></div>'
        for i, (v, u, l) in enumerate(C.STATS))

    by_slug = {p["slug"]: p for p in C.PROCESSES}
    procs = "".join(process_line(by_slug[slug], i)
                    for i, slug in enumerate(C.PROCESSES_HOME_ORDER))

    tests = "".join(
        f'<blockquote class="quote" data-reveal style="--i:{i}">'
        f'<p>{t["text"]}</p><cite>{t["name"]}<span>{t["meta"]}</span></cite></blockquote>'
        for i, t in enumerate(C.TESTIMONIALS))

    custs = "".join(
        f'<li class="cust" data-reveal style="--i:{i}">'
        f'<span class="cust__plate"><img class="cust__logo" src="assets/logos/{logo_file}" alt="{esc(html.unescape(n))} logo" loading="lazy"></span>'
        f'<span class="cust__name">{n}</span></li>'
        for i, (n, logo_file) in enumerate(C.CUSTOMERS))

    by_slug = {e[0]: e for e in C.GALLERY}
    gallery = "".join(tile(by_slug[s], i) for i, s in enumerate(C.GALLERY_HOME))

    plates = "".join(
        f'<figure class="plate" data-reveal style="--i:{i}">'
        f'{img(slug, f"{name} micrograph", sizes="(max-width:800px) 50vw, 25vw")}'
        f'<figcaption><b>{name}</b><span>{note}</span></figcaption></figure>'
        for i, (slug, name, note) in enumerate(C.MICROSTRUCTURES))

    body = f'''
<section class="hero hero--chart hero--mark">
  <div class="hero__glow" aria-hidden="true"></div>
  <div class="wrap hero__in">
   <div class="hero__copy">
    <p class="hero__eyebrow">{C.HERO_EYEBROW}</p>
    <h1 class="hero__title" data-heat-scale="{HEAT_STOPS}"
        data-heat-lo="{C.HERO_HEAT_RANGE[0]}" data-heat-hi="{C.HERO_HEAT_RANGE[1]}">{C.HERO_TITLE}</h1>
    <p class="hero__text">{C.HERO_TEXT}</p>
    <div class="hero__act">
      <a class="btn" href="contact.html#enquire">Contact us</a>
      <a class="btn btn--ghost" href="processes.html">See the processes</a>
    </div>
   </div>
   {hero_mark()}
  </div>
</section>

<section class="stats-band">
  <div class="wrap stats">{stats}</div>
</section>


<section class="sec">
  <div class="wrap">
    {sec_head("What we do", C.H_PROCESSES, C.PROCESSES_HOME_INTRO)}
    <div class="ptiles">{procs}</div>
    <div class="sec__more" data-reveal>
      <a class="btn btn--ghost" href="processes.html">How we run each process</a>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Proof", C.H_PROOF, C.QUALITY_HOME_INTRO, mid=True)}
    <ul class="qstrip">{"".join(
      f'<li class="qstrip__item" data-reveal style="--i:{n}"><b>{t}</b><span>{d}</span></li>'
      for n, (t, d) in enumerate(C.QUALITY_HOME))}</ul>
    <div class="sec__more" data-reveal>
      <a class="btn btn--ghost" href="quality.html">How we test every batch</a>
    </div>
  </div>
</section>

<section class="sec sec--plates">
  <div class="wrap">
    {sec_head("Microstructure", C.H_MICRO, C.H_MICRO_TEXT, mid=True)}
    <div class="plates">{plates}</div>
  </div>
</section>

<section class="sec sec--plates">
  <div class="wrap">
    {sec_head("Gallery", C.GALLERY_TITLE, C.GALLERY_INTRO, mid=True)}
    <div class="shots shots--home">{gallery}</div>
    <div class="sec__more" data-reveal>
      <a class="btn btn--ghost" href="gallery.html">See the full gallery</a>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("Customers", C.H_CUSTOMERS, C.CUSTOMERS_INTRO, mid=True)}
    <ul class="custs">{custs}</ul>
    {f"""<div class="quotes" data-quotes>
      <div class="quotes__track">{tests}</div>
      <div class="quotes__dots" role="tablist" aria-label="Customer reviews">{
        "".join(f'<button type="button" role="tab" data-quote-dot="{i}"'
                f' aria-label="Review {i + 1}"></button>'
                for i in range(len(C.TESTIMONIALS)))}</div>
    </div>""" if C.TESTIMONIALS and C.SHOW_TESTIMONIALS else ''}
  </div>
</section>

{cta()}'''
    return page("index.html", C.TAB_NAME,
                C.DESCRIPTION, body, "index.html")


def build_processes():
    jump = "".join(f'<a class="chip chip--link" href="#{p["slug"]}">{p["name"]}</a>'
                   for p in C.PROCESSES)
    secs = "".join(process_section(p, i) for i, p in enumerate(C.PROCESSES))
    body = f'''
{subhero("Processes", C.H_PROCESSES_PAGE, C.PROCESSES_INTRO,
         "g-pit-furnaces")}
<nav class="wrap jump" aria-label="Processes on this page">{jump}</nav>
<section class="sec sec--tight"><div class="wrap procs">{secs}</div></section>
{cta()}'''
    return page("processes.html", f"{C.TAB_NAME} — Heat treatment processes",
                C.PROCESSES_INTRO, body, "processes.html")


def build_materials():
    rows = "".join(
        f'<tr data-grade="{esc(html.unescape(g))}" tabindex="0" role="button"'
        f' aria-label="Enquire about {esc(html.unescape(g))}">'
        f'<th scope="row">{g}</th><td>{fam}</td><td>{proc}</td>'
        f'<td class="mono">{res}</td><td class="mat__note">{note}</td></tr>'
        for g, fam, proc, res, note in C.MATERIALS)
    body = f'''
{subhero("Materials", "Grade reference", C.MATERIALS_INTRO)}
<section class="sec sec--tight">
  <div class="wrap">
    <div class="mat__tools" data-reveal>
      <label class="search">
        <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor"
             stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>
        <input type="search" placeholder="Filter by grade, family or process&hellip;"
               data-mat-search aria-label="Filter the materials table">
      </label>
      <p class="mat__count" data-mat-count aria-live="polite"></p>
    </div>
    <div class="tablewrap" data-reveal>
      <table class="mat" data-endpoint="{esc(C.FORM_ENDPOINT)}" data-wa="{C.WHATSAPP}">
        <thead><tr>
          <th scope="col">Grade</th><th scope="col">Family</th>
          <th scope="col">Usual process</th><th scope="col">Typical result</th>
          <th scope="col">Notes</th>
        </tr></thead>
        <tbody data-mat-body>{rows}</tbody>
      </table>
    </div>
    <p class="mat__empty" data-mat-empty hidden>
      No grade matches that. Send it to us anyway &mdash;
      <a href="contact.html#enquire">we will specify it</a>.
    </p>
  </div>
</section>
{cta()}'''
    return page("materials.html", f"{C.TAB_NAME} — Material grade reference",
                C.MATERIALS_INTRO, body, "materials.html")


def build_quality():
    tiles = "".join(
        f'<article class="qsec{" qsec--flip" if i % 2 else ""}">'
        f'<figure class="qsec__fig" data-reveal>{img(q["image"], q["name"], sizes="(max-width:860px) 100vw, 55vw")}</figure>'
        f'<div class="qsec__text" data-reveal><h2 class="h2">{q["name"]}</h2><p class="lede">{q["text"]}</p></div></article>'
        for i, q in enumerate(C.QUALITY))
    pts = "".join(
        f'<div class="feat" data-reveal style="--i:{i}"><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(C.QUALITY_POINTS))
    body = f'''
{subhero("Quality", C.H_QUALITY, C.QUALITY_INTRO,
         "g-lab")}
<section class="sec"><div class="wrap qsecs">{tiles}</div></section>
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("The system", C.H_QUALITY_SYSTEM, mid=True)}
    <div class="feats">{pts}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--narrow">
    {sec_head("Policy", C.POLICY_TITLE, C.POLICY_INTRO, mid=True)}
    <ul class="policy" data-reveal>
      {"".join(f"<li>{t}</li>" for t in C.POLICY_POINTS)}
    </ul>
  </div>
</section>
{cta()}'''
    return page("quality.html", f"{C.TAB_NAME} — Quality & testing",
                C.QUALITY_INTRO, body, "quality.html")


def slugify(name):
    return "".join(c if c.isalnum() else "-"
                   for c in html.unescape(name).lower()).strip("-").replace("--", "-").replace("--", "-")


def build_industries():
    blocks = []
    for i, d in enumerate(C.INDUSTRIES):
        prose = "".join(f"<p>{x}</p>" for x in d["body"])
        chips = "".join(f'<span class="chip">{x}</span>' for x in d["points"])
        blocks.append(f'''<article class="sector{" sector--flip" if i % 2 else ""}" id="{slugify(d["name"])}">
  <div class="sector__fig" data-reveal>{img(d["image"], d["alt"], sizes="(max-width:800px) 100vw, 50vw")}</div>
  <div class="sector__text" data-reveal>
    <h2 class="h2">{d["name"]}</h2>
    <div class="prose">{prose}</div>
    <div class="chips">{chips}</div>
  </div>
</article>''')
    body = f'''
{subhero("Industries", C.H_INDUSTRIES, C.INDUSTRIES_INTRO, "g-dispatch")}
<section class="sec"><div class="wrap sectors">{"".join(blocks)}</div>
  <div class="wrap more" data-reveal>
    <p class="more__h">{C.INDUSTRIES_MORE_TITLE}</p>
    <p class="more__list">{" <span aria-hidden=\"true\">&middot;</span> ".join(C.INDUSTRIES_MORE)}</p>
  </div>
</section>
{cta()}'''
    return page("industries.html", f"{C.TAB_NAME} — Industries served",
                C.INDUSTRIES_INTRO, body, "industries.html")


def build_about():
    prose = "".join(f"<p>{x}</p>" for x in C.ABOUT_BODY)
    body = f'''
{subhero("About", C.ABOUT_TITLE, "", C.ABOUT_IMAGE)}
<section class="sec">
  <div class="wrap split">
    <div class="split__text"><div class="prose prose--lg" data-reveal>{prose}</div></div>
    <aside class="card-person" data-reveal>
      <p class="eyebrow">Who you will deal with</p>
      {people()}
      <hr>
      <p><a class="link" href="tel:{C.PHONE_LINK}">{C.PHONE}</a></p>
      <p><a class="link" href="mailto:{C.EMAIL}">{C.EMAIL}</a></p>
      <a class="btn btn--block" href="contact.html#enquire">Talk to us</a>
    </aside>
  </div>
</section>
<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("The team", C.TEAM_TITLE, C.TEAM_INTRO, mid=True)}
    <figure class="teamshot" data-reveal>{img(C.TEAM_IMAGE[0], C.TEAM_IMAGE[1], sizes="(max-width:1100px) 100vw, 1100px")}</figure>
    <ul class="team">{"".join(
        f'<li class="member" data-reveal style="--i:{i}"><b>{n}</b><span>{r}</span></li>'
        for i, (n, r) in enumerate(C.TEAM))}</ul>
  </div>
</section>

<section class="sec">
  <div class="wrap wrap--narrow">
    {sec_head("The plant", C.PLANT_TITLE, C.PLANT_INTRO, mid=True)}
    <div class="tablewrap" data-reveal>
      <table class="plant">
        <thead><tr><th scope="col">Equipment</th><th scope="col">Size</th><th scope="col">Used for</th></tr></thead>
        <tbody>{"".join(
          f'<tr><th scope="row">{n}</th><td class="mono">{sz}</td><td>{u}</td></tr>'
          for n, sz, u in C.PLANT)}</tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec sec--alt" id="safety">
  <div class="wrap split split--media">
    <figure class="safety__fig" data-reveal>{img(C.SAFETY_IMAGE[0], C.SAFETY_IMAGE[1], sizes="(max-width:900px) 100vw, 40vw")}</figure>
    <div class="split__text">
      {sec_head("Safety", C.SAFETY_TITLE, C.SAFETY_INTRO)}
      <div class="feats feats--2 feats--flat">{"".join(
        f'<div class="feat" data-reveal style="--i:{i}"><h3>{t}</h3><p>{d}</p></div>'
        for i, (t, d) in enumerate(C.SAFETY_POINTS))}</div>
    </div>
  </div>
</section>

<section class="sec" id="visits">
  <div class="wrap">
    {sec_head("Industrial visits", C.VISITS_TITLE, C.VISITS_BODY, mid=True)}
    <div class="shots shots--visits">{"".join(tile(v, i, "(max-width:700px) 100vw, 33vw") for i, v in enumerate(C.VISITS))}{tile((C.VISITS_VIDEO, "Industrial visit", "video"), 3)}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap">
    {sec_head("How we work", C.H_ABOUT_PILLARS, mid=True)}
    <div class="holds">{"".join(
      f'<div class="hold" data-reveal style="--i:{i}"><h3>{t}</h3><p>{d}</p></div>'
      for i, (t, d) in enumerate(C.ABOUT_PILLARS))}</div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap wrap--narrow">
    {sec_head("Certification", C.CERTS_TITLE, C.CERTS_INTRO, mid=True)}
    <div class="certs">
      {"".join(
        f'<figure class="cert" data-reveal style="--i:{i}">'
        f'<a class="cert__sheet" href="assets/img/{slug}.webp" target="_blank" '
        f'rel="noopener" aria-label="Open the {esc(name)} certificate full size">'
        f'{img(slug, alt, sizes="(max-width:700px) 90vw, 40vw")}</a>'
        f'<figcaption><b>{name}</b><span>{note}</span></figcaption></figure>'
        for i, (slug, name, note, alt) in enumerate(C.CERTIFICATES))}
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    {sec_head("Where we are going", C.H_VISION, mid=True)}
    <div class="aims">
      <div class="aim" data-reveal style="--i:0">
        <p class="aim__k">{C.VISION_TITLE}</p>
        {"".join(f"<p>{t}</p>" for t in C.VISION_BODY)}
      </div>
      <div class="aim" data-reveal style="--i:1">
        <p class="aim__k">{C.MISSION_TITLE}</p>
        {"".join(f"<p>{t}</p>" for t in C.MISSION_BODY)}
      </div>
    </div>
    <div class="promise" data-reveal>
      <p class="aim__k">{C.PROMISE_TITLE}</p>
      <p class="promise__lead">{C.PROMISE_BODY[0]}</p>
      <p class="promise__sub">{C.PROMISE_BODY[1]}</p>
    </div>
  </div>
</section>
{cta()}'''
    return page("about.html", f"{C.TAB_NAME} — About",
                "A metallurgist-run commercial heat treatment shop in Chennai.",
                body, "about.html")


def build_gallery():
    lead, rest = C.GALLERY[0], C.GALLERY[1:]
    body = f'''
<section class="gal-lead">
  <div class="wrap gal-lead__in">
    <figure class="gal-lead__fig shot">
      <a href="assets/img/{lead[0]}.webp" data-lightbox aria-label="Open: {esc(lead[1])}">
        {img(lead[0], lead[1], eager=True, sizes="(max-width:900px) 100vw, 60vw")}
      </a>
      <figcaption>{lead[1]}</figcaption>
    </figure>
    <div class="gal-lead__text">
      <p class="eyebrow">Gallery</p>
      <h1 class="h1">{C.GALLERY_TITLE}</h1>
      <p class="lede">{C.GALLERY_INTRO}</p>
      <p class="gal-lead__count">{sum(1 for e in C.GALLERY if len(e) < 3)} photographs &middot; {sum(1 for e in C.GALLERY if len(e) > 2)} videos</p>
    </div>
  </div>
</section>
<section class="sec sec--tight">
  <div class="wrap">
    <div class="masonry">{"".join(tile(e, i, "(max-width:600px) 50vw, (max-width:1000px) 33vw, 25vw") for i, e in enumerate(rest))}</div>
  </div>
</section>
{cta()}'''
    return page("gallery.html", f"{C.TAB_NAME} — Gallery", C.GALLERY_INTRO,
                body, "gallery.html")


def build_contact():
    faq = "".join(
        f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>'
        for q, a in C.FAQ)
    addr = "<br>".join(C.ADDRESS_LINES)
    hours = "".join(f"<dt>{d}</dt><dd>{h}</dd>" for d, h in C.HOURS)
    map_src = ("https://www.google.com/maps?q="
               + C.MAP_QUERY.replace(" ", "+").replace(",", "%2C") + "&output=embed")
    body = f'''
{subhero("Contact", "Contact", C.CONTACT_INTRO)}

<section class="sec sec--tight">
  <div class="wrap split split--wide">
    <div class="split__text">
      {sec_head("Enquiry", "Tell us about the part")}
      {enquiry_form()}
    </div>
    <aside class="cinfo" data-reveal>
      <h2 class="h3">{C.NAME}</h2>
      <p class="cinfo__cert">{C.CERT}</p>
      <div class="cinfo__people">
        <p class="eyebrow">Who you will deal with</p>
        {people()}
      </div>
      <address>{addr}</address>
      <dl class="cinfo__list">
        <dt>Phone</dt><dd><a href="tel:{C.PHONE_LINK}">{C.PHONE}</a></dd>
        <dt>Email</dt><dd><a href="mailto:{C.EMAIL}">{C.EMAIL}</a></dd>
        <dt>GSTIN</dt><dd class="mono">{C.GSTIN}</dd>
      </dl>
      <h3 class="h4">Opening hours</h3>
      <dl class="cinfo__list">{hours}</dl>
    </aside>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap">
    <div class="map" data-reveal>
      <iframe src="{map_src}" title="Map of {esc(C.MAP_QUERY)}"
              loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    </div>
  </div>
</section>

<section class="sec sec--alt">
  <div class="wrap wrap--narrow">
    {sec_head("Questions", "Before you ask", mid=True)}
    <div class="faqs" data-reveal>{faq}</div>
  </div>
</section>'''
    return page("contact.html", f"{C.TAB_NAME} — Contact",
                C.CONTACT_INTRO, body, "contact.html")


def build_404():
    body = '''
<section class="nf">
  <div class="wrap nf__in">
    <p class="eyebrow">404</p>
    <h1 class="h1">This one got quenched.</h1>
    <p class="lede">The page is not here. The furnaces still are.</p>
    <div class="hero__act">
      <a class="btn" href="index.html">Back to the start</a>
      <a class="btn btn--ghost" href="processes.html">See the processes</a>
    </div>
  </div>
</section>'''
    return page("404.html", f"{C.TAB_NAME} — Page not found",
                "That page could not be found.", body, noindex=True)


def main():
    made = [build_home(), build_processes()]
    made += [build_materials(), build_quality(), build_industries(),
             build_about(), build_gallery(), build_contact(), build_404()]

    missing = sorted({s for s in _dims if _dims[s] is None})
    print(f"built {len(made)} pages")
    for p in made:
        print(f"  {p}")
    if missing:
        print(f"\n  ! {len(missing)} image(s) missing, using fallback blocks:")
        print("    " + ", ".join(missing))
    if C.NOINDEX:
        print("\n  noindex is ON (concept build)")


if __name__ == "__main__":
    main()
