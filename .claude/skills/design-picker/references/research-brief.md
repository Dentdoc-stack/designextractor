# Shared context for research agents

Goal: build an "ultimate" Claude Code skill that tells the user WHICH design to use for a given report/document,
based on 7 reference boards, and gives buildable specs for each design.

Repo: /home/user/designextractor (branch claude/hopeful-thompson-vnac52)
- Reference images: .claude/skills/report-design/references/images/ref-A.jpeg … ref-G.jpeg
  A = "Rapport annuel 2025" navy annual report (portrait covers + spreads) — the only real report
  B = "Breakslide" dark green slides      C = "Business Plan Presentation" green/black/white
  D = "Prism" teal, rounded slabs         E = "Clinicare" aqua medical
  F = "Docoro" royal blue healthcare      G = "Market" teal, inset frame, vertical tab
  Images are small JPEG collages (474–736 px wide). Crop and upscale individual thumbnails with PIL
  (save crops to your own scratch dir) and view them with the Read tool to see details.
- Existing skill: .claude/skills/report-design/ (SKILL.md, references/design-spec.md, references/reference-analysis.md,
  assets/tokens.json, scripts/reportkit.py = python-docx layout engine, build_report.py, render.sh, check_pdf.py).
  Its "Slab & Rule" style (serif, hairlines, dark green) deliberately REJECTED the references' look; the user dislikes it.
- .claude/skills/design-picker/references/user-design-notes.md: the user's preferred analysis (verified: its hex values and contrast ratios are accurate).
  Known gaps in it: no page size/pt sizes, no no-photo fallback, no report structures (contents/findings/citations),
  rounded shapes not addressed for DOCX, invented table style, Windows source path.

Environment:
- Python venv with python-docx, matplotlib, pymupdf, pillow: /home/user/designextractor/.venv/bin/python
- LibreOffice (soffice), pdftoppm, pdffonts installed. IBM Plex and Inter fonts installed system-wide.
- Network: npm registry (registry.npmjs.org) and PyPI reachable. github.com, Google Fonts, jsdelivr BLOCKED.

Measured accent colours (share of pixels within ΔRGB 30): A #1A2E5F 29%, B #005B58 31% (+#177664 10%),
C #5AB14D 2.7%, D #349B86 15%, E #4DCCD4 6%, F #05369F 11%, G #01A198 6%.

Rules for all agents:
- Write ONLY your assigned output file(s) under .claude/skills/design-picker/. Do not edit other repo files. Do not commit.
- Tag claims [seen] / [inferred] / [uncertain]. Never present guesses (font names, exact mm) as facts.
- Target output: A4 report documents built as DOCX (python-docx) and rendered with LibreOffice, not slides.
