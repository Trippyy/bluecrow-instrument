# Bluecrow — Instrument

A video-led product-discovery experience for Bluecrow. Three full-screen product
chapters on one continuous scroll, each routing into its own product page.

Built mobile-first; the desktop layout is the same components re-anchored, driven by
container queries rather than a separate stylesheet.

## Run

No build step is needed to view it — `index.html` is self-contained apart from `img/`.

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Opening the file directly also works, though some
browsers restrict local image loading.

## Build

`index.html` is generated from three partials in `src/`.

```bash
python3 src/build.py
```

Edit `src/styles.html`, `src/markup.html` or `src/behaviour.html` — never `index.html`
directly, it is overwritten.

## The design

**Depth on black.** Each product is an alpha cutout composited over a defocused,
duotoned plate made from its own studio shot. The Mencken headline sits *between* those
two layers, so the product name passes behind the object. Nothing is masked and nothing
is doubled.

**Two registers.** Chapters are photographic and atmospheric. Product pages switch to an
analytical one — a technical grid ground of crosshairs, cell lines, a dot field and a
drifting hatch, with a cell that lights up and slides to whichever feature you inspect.

**Restraint.** Blue appears as the active navigator cell, the route label and the
purchase border. One hairline weight divides the top bar, the rail, the specification
rows and the purchase block, and nothing else.

**Contrast.** Every text pair meets WCAG 2.1 AA (4.5:1), and interactive boundaries meet
1.4.11 (3:1), measured against the real backdrop each sits on — including the brightest
point of a product plate under its scrim. The neutral scale is three deliberate steps:
`--white` 18.5:1, `--grey` 7.5:1, `--dim` 4.9:1.

**The name is an outline until you engage.** Each product name sits as a hairline stroke
over the scene. Hovering the product floods it solid left to right, so the headline
belongs to the object rather than sitting behind it. The product itself is the control:
it is a button, it tilts toward the cursor, and it opens its own page. Devices without
hover fill the name as each chapter arrives instead.

**Motion.** Chapter entry settles the environment before the product, so depth reads
before detail. Products tilt toward the cursor in 3D while the headline drifts a few
pixels the other way, making the parallax real. Everything is gated behind
`(hover:hover)` and collapses under `prefers-reduced-motion`.

## Layout

```
index.html                   generated — do not edit
img/                         product cutouts and environment plates
src/build.py                 assembles index.html, inlines Mencken outlines
src/words.json               pre-extracted Mencken glyph outlines
src/{styles,markup,behaviour}.html
tools/mencken_to_svg.py      regenerate words.json from the font
tools/make_env_plates.py     regenerate the environment plates
```

## Typography

Headlines are **Mencken Std Head Compress ExtraBold** (Typofonderie, Jean François
Porchez). They ship as inlined SVG outlines rather than a webfont, so the page loads no
font file for display type. Interface type is IBM Plex Mono and IBM Plex Sans from
Google Fonts.

## Before this ships

- **Mencken is not yet licensed for the web.** The outlines in `src/words.json` were
  rendered from a desktop licence synced through Adobe Fonts. That covers producing
  artwork; it does not cover distributing the letterforms in a shipped site. A
  Typofonderie web licence is required before launch — no design impact, but it carries
  a lead time.
- **Product photography is client-supplied** and remains the property of Bluecrow.
- **Product imagery is low resolution.** The supplied cutouts are roughly 470–530 px on
  their long edge. The desktop product page now scales them 1.3–1.5x to fill the
  composition, which holds up at standard density but is visibly soft on Retina
  displays. Exports at roughly 1400 px on the long edge would clear this, and are a
  drop-in replacement — no code change needed.
- **A fourth product (Ignis) was specified but removed** pending photography. Restoring
  it means adding a chapter to `src/markup.html`, an entry to the product data in
  `src/behaviour.html`, its cutout and plate to `img/`, and updating the `/ 03` counters.
