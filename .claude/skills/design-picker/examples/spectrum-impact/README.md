# Test report: H Spectrum (multicolour)

A 14-page illustrative impact report built to `DESIGN.md` §4.H. All names and figures are invented.

```bash
.venv/bin/python .claude/skills/design-picker/examples/spectrum-impact/build.py out
soffice --headless --convert-to pdf --outdir out out/spectrum-impact-test.docx
```

Uses the shared helpers in `../../scripts/docxkit.py` and Figtree from `../../assets/fonts`. Install the fonts in `~/.fonts`, run `fc-cache -f` and delete `~/.cache/matplotlib`. Needs `python-docx`, `matplotlib`, `pillow` and `cairosvg`. The icons are Lucide (ISC licence, in `icons/LICENSE-lucide.txt`).

Each section owns one colour, in a fixed order: Education blue, Health coral, Environment teal, Communities saffron, Finance plum. The spectrum strip at the top of each page drops a tab in the current section's colour. All five colours appear together only on the cover, contents, overview, finance and back-cover pages. The palette passed the dataviz validator, and every text and fill pairing meets WCAG AA.

Pages:
1. Bar-chart cover
2. Colour-coded contents
3. Foreword with "five moments"
4. Overview tiles and spend donut
5. Education (band page, then a chart page)
6. Health (band page, then a table page)
7. Environment (band page, then a line chart and steps)
8. Communities (band page, then bars, a case study and steps)
9. Finance: stacked columns and an income/spend table
10. Back cover

Built and checked in LibreOffice 24.2: 14 pages, Figtree embedded. Not checked in Word.
