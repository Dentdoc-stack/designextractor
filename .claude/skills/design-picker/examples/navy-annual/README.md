# Test report: A Navy Annual

A 16-page illustrative annual report built to `DESIGN.md` §4.A (all names and figures are invented).

```bash
.venv/bin/python .claude/skills/design-picker/examples/navy-annual/build.py out
soffice --headless --convert-to pdf --outdir out out/navy-annual-test.docx
```

Needs the Figtree TTFs from `../../assets/fonts` installed (`~/.fonts`, `fc-cache -f`, delete `~/.cache/matplotlib`),
plus `python-docx matplotlib pillow cairosvg`. Icons are Lucide (ISC, `icons/LICENSE-lucide.txt`).

Pages: cover · contents · foreword (110 mm panel) · at a glance (KPI row, findings, navy band) · opener 01 ·
performance with side rail · revenue (split page, stacked KPIs, gradient column chart) · donut + stat rail ·
regional table + leakage bars · customers (quote, KPI strip) · opener 02 · org chart · risk and governance ·
priorities (navy band, step cards, targets) · method and glossary · back cover (dot texture).

Built and checked in LibreOffice 24.2 (16 pages, Figtree embedded); not checked in Word.
