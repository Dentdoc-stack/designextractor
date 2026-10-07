#!/usr/bin/env python3
"""Automated print checks on a rendered PDF, plus a contact sheet.

usage: check_pdf.py report.pdf [contact_sheet.png]
Flags: text outside the live area, near-empty pages, headings stranded at a page bottom,
non-embedded or fallback fonts, tables/images crossing the right margin.
"""
import sys

import pymupdf

pdf = pymupdf.open(sys.argv[1])
issues = []
MM = 72 / 25.4
FULL_BLEED_MAX_TEXT = 400  # cover/opener/closing pages are allowed to be sparse

fonts = set()
for i, pg in enumerate(pdf, 1):
    w, h = pg.rect.width, pg.rect.height
    text = pg.get_text("dict")["blocks"]
    nchar = len(pg.get_text().strip())
    sparse = nchar < 120
    spans = [(s, b) for b in text if b["type"] == 0 for l in b["lines"] for s in l["spans"]]
    for s, b in spans:
        fonts.add(s["font"])
        x0, y0, x1, y1 = s["bbox"]
        if x1 > w - 5 * MM or x0 < 5 * MM and nchar > 0 and i > 1:
            if x0 < 5 * MM or x1 > w - 5 * MM:
                issues.append(f"p{i}: text near/over page edge: {s['text'][:40]!r}")
        if y1 > h - 5 * MM:
            issues.append(f"p{i}: text over bottom edge: {s['text'][:40]!r}")
    body = [(s, b) for s, b in spans if s["size"] < 40]
    if body:
        last_y = max(s["bbox"][3] for s, _ in body)
        bottom_spans = [s for s, _ in body if s["bbox"][3] > last_y - 2 and s["size"] >= 13]
        if bottom_spans and last_y > h - 40 * MM:
            issues.append(f"p{i}: heading-sized text is the last item on the page: {bottom_spans[0]['text'][:40]!r}")
    if sparse and i not in (1, len(pdf)):
        issues.append(f"p{i}: very little text ({nchar} chars); intentional opener or an accidental blank page?")
    if not sparse and body and i not in (1, len(pdf)):
        content_bottom = max((s["bbox"][3] for s, _ in body if s["bbox"][3] < h - 25 * MM), default=0)
        if content_bottom < h * 0.3 and nchar < 700:
            issues.append(f"p{i}: content ends in the top third ({nchar} chars); possible orphan spill from the previous page")
    for im in pg.get_images(full=True):
        for r in pg.get_image_rects(im[0]):
            if r.x1 > w - 5 * MM and r.width < w * 0.9:
                issues.append(f"p{i}: image crosses right margin")

print("pages:", len(pdf))
print("fonts:", ", ".join(sorted(fonts)))
bad = [f for f in fonts if not any(k in f for k in ("Plex",))]
if bad:
    issues.append("non-Plex fonts present (fallback?): " + ", ".join(sorted(bad)))
print("issues:" if issues else "no automated issues")
for x in issues:
    print(" -", x)

if len(sys.argv) > 2:
    from PIL import Image
    thumbs = [Image.frombytes("RGB", (p.get_pixmap(dpi=40).width, p.get_pixmap(dpi=40).height), p.get_pixmap(dpi=40).samples) for p in pdf]
    cols = 5
    tw, th = max(t.width for t in thumbs), max(t.height for t in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 12) + 12), (150, 150, 150))
    for n, t in enumerate(thumbs):
        sheet.paste(t, (12 + (n % cols) * (tw + 12), 12 + (n // cols) * (th + 12)))
    sheet.save(sys.argv[2])
    print("contact sheet:", sys.argv[2])
