#!/usr/bin/env python3
"""Regenerate the blurred, dark-blue environment plates behind each product.

Each plate is derived from that product's own studio shot: blurred, normalised to the
full tonal range, then mapped onto a single duotone ramp so all chapters share one
lighting register. Requires the original (uncropped) product photographs.

    python3 tools/make_env_plates.py <photo-dir>

where <photo-dir> holds optic.png, elixir.png, sonar.png.
"""
import sys, pathlib
from PIL import Image, ImageFilter
import numpy as np

SHADOW = np.array([2, 6, 12], float)     # near-black blue
HIGH   = np.array([26, 62, 102], float)  # dark brand-derived blue

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
out = pathlib.Path(__file__).resolve().parent.parent / "img"

for name in ("optic", "elixir", "sonar"):
    path = src / f"{name}.png"
    if not path.exists():
        print(f"skip {name}: {path} not found"); continue
    im = Image.open(path).convert("RGB")
    im = im.resize((round(im.width * 900 / im.height), 900), Image.LANCZOS)
    im = im.filter(ImageFilter.GaussianBlur(24))
    lum = np.asarray(im.convert("L")).astype(float) / 255.0
    lum = (lum - lum.min()) / max(1e-6, lum.max() - lum.min())
    rgb = SHADOW + (HIGH - SHADOW) * np.power(lum, 0.95)[..., None]
    Image.fromarray(rgb.clip(0, 255).astype(np.uint8), "RGB").save(
        out / f"{name}-env.jpg", quality=86, optimize=True)
    print("wrote", out / f"{name}-env.jpg")
