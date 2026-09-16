#!/usr/bin/env python3
"""Build index.html from the source partials.

Mencken headlines are inlined as SVG outlines (see tools/mencken_to_svg.py), so the
page needs no webfont at runtime. Non-ASCII is escaped for markup but converted to
\\uXXXX inside <script>, where HTML entities would be taken literally.

    python3 src/build.py
"""
import json, re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
PARTS = ["styles.html", "markup.html", "behaviour.html"]
LABEL = {"Bluecrow": "Bluecrow", "OPTIC": "Optic", "ELIXIR": "Elixir", "SONAR": "Sonar"}

words = json.loads((HERE / "words.json").read_text())
doc = "\n".join((HERE / p).read_text() for p in PARTS)

def glyph(m):
    """{{W:KEY}} is the labelled instance; {{WD:KEY}} is a decorative duplicate.

    The outline and fill copies of a headline are the same letterforms, so only the
    first carries the accessible name - otherwise every product is announced twice.
    """
    decorative, key = m.group(1) == "WD", m.group(2)
    w = words[key]
    naming = ('aria-hidden="true"' if decorative
              else 'role="img" aria-label="%s"' % LABEL[key])
    return ('<svg class="mk" viewBox="%s" xmlns="http://www.w3.org/2000/svg" %s>'
            '<path d="%s"/></svg>' % (w["viewBox"], naming, w["d"]))

doc, n = re.subn(r"\{\{(WD?):([A-Za-z]+)\}\}", glyph, doc)

esc_html = lambda t: "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in t)
esc_js   = lambda t: "".join(c if ord(c) < 128 else "\\u%04X" % ord(c) for c in t)
chunks = re.split(r"(<script>.*?</script>)", doc, flags=re.S)
doc = "".join(esc_js(c) if c.startswith("<script>") else esc_html(c) for c in chunks)

assert not re.findall(r"\{\{[^}]*\}\}", doc), "unresolved placeholder"
assert all(ord(c) < 128 for c in doc), "non-ascii escaped output expected"
(ROOT / "index.html").write_text(doc)
print("built index.html - %d glyphs, %d bytes" % (n, len(doc)))
