#!/usr/bin/env python3
"""Build a DOCX report from a content JSON file.

usage: build_report.py content.json out.docx [--no-paginate]

Runs two passes when LibreOffice is available so the contents page carries real page numbers.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reportkit import Report  # noqa: E402


def _norm(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def find_pages(pdf, entries):
    import pymupdf
    doc = pymupdf.open(pdf)
    heads = []
    for pg in doc:
        spans = [s["text"] for b in pg.get_text("dict")["blocks"] if b["type"] == 0
                 for l in b["lines"] for s in l["spans"] if s["size"] >= 13]
        heads.append(_norm(" ".join(spans)))
    toc_page = next((i for i, h in enumerate(heads) if "contents" in h), 1)
    found = {}
    for e in entries:
        key = _norm(e["title"])
        for i in range(toc_page + 1, len(heads)):
            if key in heads[i]:
                found[e["title"]] = i + 1
                break
    return found


def to_pdf(docx, outdir):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(outdir), str(docx)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return Path(outdir) / (Path(docx).stem + ".pdf")


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(src.read_text())
    out.parent.mkdir(parents=True, exist_ok=True)
    base = src.parent
    for b in spec["blocks"]:  # resolve image paths relative to the content file
        for it in b.get("items", []):
            if isinstance(it, dict) and isinstance(it.get("image"), dict) and it["image"].get("path"):
                it["image"]["path"] = str((base / it["image"]["path"]).resolve())
    rep = Report(spec["meta"], out.parent)
    seq = rep.build(spec["blocks"], out)
    if "--no-paginate" not in sys.argv and shutil.which("soffice") and any(b["type"] == "contents" for b in spec["blocks"]):
        with tempfile.TemporaryDirectory() as tmp:
            pdf = to_pdf(out, tmp)
            pages = find_pages(pdf, rep.toc_entries)
        rep = Report(spec["meta"], out.parent, pages)
        seq = rep.build(spec["blocks"], out)
        missing = [e["title"] for e in rep.toc_entries if e["title"] not in pages]
        if missing:
            print("WARNING: no page found for contents entries:", missing)
    print("layout sequence:", " > ".join(seq))
    run = 1
    for a, b2 in zip(seq, seq[1:]):
        run = run + 1 if a == b2 else 1
        if run >= 3:
            print("WARNING: three consecutive pages share the layout", a)
    print("wrote", out)


if __name__ == "__main__":
    main()
