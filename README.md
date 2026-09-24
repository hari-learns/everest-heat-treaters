# Everest Heat Treaters — concept site

A demo website for a commercial heat treatment company in Chennai, built from
their business card. Dark navy from their logo, incandescent orange from the
thing they actually sell.

**Live:** https://hari-learns.github.io/everest-heat-treaters-concept/

---

## ⚠️ What is real and what is not

**Real** — taken from the business card, safe to keep:

| | |
|---|---|
| Company | Everest Heat Treaters |
| Person | S. Aravindth, B.E., M.E. — Metallurgist |
| Phone | +91 63795 47322 |
| Email | sathyaaravindth03@gmail.com · everest_heattreaters@yahoo.co.in |
| Address | S. No. 315/1, Meppur Road, Malayambakkam, Nazarathpettai, Chennai 600123 |
| GSTIN | 33ANNPS4415M1ZK |
| Certification | ISO 9001:2015 (BSI) |

**Invented — must be confirmed or replaced before this goes live:**

- The four figures in the stats band (max temperature, hardness, furnace
  uniformity, reporting rate)
- The equipment implied by the process pages — which of the eight processes
  they actually run in-house, and which they sub-contract
- The two testimonials, both labelled "Sample testimonial"
- Turnaround times in the FAQ
- The material grade table is standard industry data, but the grades *they*
  routinely handle should be confirmed

Pages are `noindex` and a disclosure line sits in the footer. Both are
controlled by flags at the top of `content.py`.

---

## The temperature scale

The centrepiece on the homepage, and the reason this site is not like other
heat-treatment sites. Drag it and the steel bar takes the real colour of steel
at that temperature, with the process that happens there.

It is not decorative. Below about 400 °C steel does not glow — what you see is
the interference colour of the oxide film, which is how toolmakers have judged
tempering by eye for two centuries. Above roughly 480 °C the metal is
incandescent and the colour is blackbody radiation. The widget crosses that
boundary honestly, blending between two separate colour tables.

Both tables and the ten process bands live in `content.py`
(`TEMPER_COLOURS`, `GLOW_COLOURS`, `TEMP_BANDS`). `verify.py` checks the bands
tile the full 150–1300 °C range with no gap or overlap.

---

## Changing things

**All copy, contact details, processes, grades and temperatures live in
`content.py`.** `build.py` is a generator containing no client-visible strings,
and `verify.py` fails the build if any creep in.

```bash
python3 build.py      # regenerate all 16 pages
python3 verify.py     # links, contrast, alt text, noindex, temperature data
```

| Flag in `content.py` | Concept | Live |
|---|---|---|
| `NOINDEX` | `True` | `False` |
| `SHOW_CONCEPT_NOTE` | `True` | `False` |

---

## Media

```bash
python3 fetch_media.py   # download images + self-hosted fonts
python3 assets.py        # -> assets/img/*.webp  (45 MB -> 5 MB)
python3 media.py         # the client's own photos and videos -> assets/
```

Photography is used sparingly and on purpose: the open-licence pool for modern
heat-treatment shops is poor, so the visual language is generative instead.
The four micrographs on the homepage (ferrite + pearlite, austenite,
martensite, tempered martensite) are credited reference images from Commons.

**Every image is a placeholder.** Credits and licences in
[CREDITS.md](CREDITS.md). Replace with the company's own photographs of their
plant, furnaces and parts; drop correctly-named files into `build_src/img/`
and re-run `assets.py`.

A missing image degrades to a heat-gradient block rather than a broken icon,
so a failed download never wrecks the page.

---

## Local preview

```bash
python3 -m http.server 4323
```

## Deploying

Generated HTML is committed at the repo root; GitHub Pages serves `main` root.
Push and it is live.

## Files

| File | Purpose |
|---|---|
| `content.py` | **All copy, contacts, processes, grades, temperature data** |
| `build.py` | Page generator — layout only |
| `styles.css` | Dark palette, layout, the temperature bar |
| `script.js` | Temperature engine, materials filter, nav, reveals |
| `verify.py` | Pre-flight checks — run before sending the link |
| `fetch_media.py` / `assets.py` / `media.py` | Image and font pipeline |
