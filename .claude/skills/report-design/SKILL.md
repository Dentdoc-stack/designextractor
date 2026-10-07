---
name: report-design
description: Build professional, editorially designed reports as DOCX (A4) with a coherent design system ("Slab & Rule"): serif/sans typography, one accent color, hairline tables, ruled charts and varied page layouts (cover, contents, summary, section openers, narrative, data, findings, references, appendix). Use when asked to design, write up, format or restyle a report, consultancy deliverable, briefing, white paper or analysis document, or to turn supplied content into a polished Word report. Not for slide decks.
---

# Report design skill

Turns supplied content into a designed DOCX report with a fixed design identity and deliberate page variation. Output is validated by rendering to PDF and inspecting every page.

**Choosing a design first.** "Slab & Rule" is one restrained style and does not follow the reference boards. To decide which of the seven board-derived design families a document should use, run the `design-picker` skill (`../design-picker/SKILL.md`). Its `--tokens-out` file can be passed to this engine with `REPORT_TOKENS=path/tokens.json`. That swaps colours and fonts; the layouts stay Slab & Rule until the engine gains per-family layouts.

## Files

| Path | Purpose |
|---|---|
| `references/design-spec.md` | The system: palette, type scale, grids, components, layout family, hard cases. Read before choosing layouts. |
| `references/reference-analysis.md` | Evidence from the 7 reference images (`references/images/ref-A…G.jpeg`) and how each decision traces back to them. |
| `assets/tokens.json` | Colors, fonts, sizes, margins. Edit to rebrand. |
| `assets/fonts/` | IBM Plex Serif and Sans (OFL). Must be installed on the machine that renders or opens the DOCX. |
| `scripts/reportkit.py` | Layout library on python-docx. |
| `scripts/build_report.py` | `content.json` → DOCX, with two-pass page numbers for the contents page. |
| `scripts/render.sh` | DOCX → PDF → PNG per page (LibreOffice + poppler). |
| `scripts/check_pdf.py` | Automated print checks + contact sheet. |
| `examples/sample-report.json` | A complete illustrative content file (fictional data). Copy and edit. |
| `examples/sample-report.docx`, `examples/render/` | Built example, PDF and page images. |

## Environment

Python 3 with `python-docx matplotlib pymupdf pillow`, plus `soffice` (LibreOffice Writer), `pdftoppm`, `pdffonts` (poppler-utils). Install fonts first:

```bash
mkdir -p ~/.fonts && cp .claude/skills/report-design/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f
```

The model must **view the rendered page PNGs itself** (image viewing is a capability of the AI environment, not of the build machine). If images cannot be viewed, say so, run `check_pdf.py`, and tell the user the visual inspection was not done.

## Workflow

1. **Intake.** Establish: audience and decision the report supports; length; output (DOCX default; PDF is rendered alongside); language; brand colors or fonts; which facts, figures, quotes and citations must be preserved verbatim; which images exist. Ask only for what is missing and cannot be inferred.
2. **Preserve content.** Never invent facts, figures, sources or quotes. Do not paraphrase supplied numbers, names or citations. If something is missing (image, source, number), leave a visible placeholder and report it. Sample or filler content must be labelled illustrative (`meta.illustrative: true` stamps the footer and cover).
3. **Structure.** Write the section list, then choose layouts with the table in the design spec (§6) and the variation rules. Defaults by length:
   - 1–4 pages: no cover/contents; summary + narrative/data + findings.
   - 5–12 pages: cover, contents, summary, 0–2 openers, mix of narrative/data, findings, references.
   - 13+ pages: add openers for major sections, appendix, closing.
4. **Write the content file** (`content.json`, schema below), starting from `examples/sample-report.json`. Put each supplied fact into the layout that suits it: headline figures → `summary.figures` or `data.kpis`; time series → chart; comparisons with ≥ 3 attributes → table; decisions → `findings`.
5. **Build.**
   ```bash
   python .claude/skills/report-design/scripts/build_report.py content.json out/report.docx
   ```
   Read the warnings (consecutive layouts, citations without references, contents entries not found).
6. **Render and inspect.**
   ```bash
   bash .claude/skills/report-design/scripts/render.sh out/report.docx out/render
   python .claude/skills/report-design/scripts/check_pdf.py out/render/report.pdf out/render/contact.png
   ```
   View `contact.png` for rhythm, then every `page-NN.png` (render at 90 dpi if needed: `pdftoppm -r 90 -png report.pdf page`). Fix and rebuild until the checklist below passes.
7. **Deliver** the DOCX and PDF with a short note: layouts used, anything missing (images, sources), fonts required.

## Content file schema

```json
{ "meta": { "title", "short_title", "subtitle", "type_label", "client", "author", "date", "version", "illustrative", "footer" },
  "blocks": [ { "type": "...", ... } ] }
```

Block types and fields (see the sample for every one in use):

| `type` | Fields |
|---|---|
| `cover` | `variant`: `slab` (default) or `band`; `kicker` |
| `contents` | `note`. Entries are generated from the other blocks (set `"toc": false` on a block to omit it) |
| `summary` | `title`, `kicker`, `lead`, `figures` [{value, unit, label}], `points` [text], `after` [flow items] |
| `opener` | `number`, `title`, `label`, `intro` |
| `narrative` | `title`, `kicker`, `lead`, `layout`: `margin`/`measure`/`twocol` (auto: margin if notes/quote present), `items` |
| `data` | `title`, `kicker`, `lead`, `landscape`, `kpis` [{value, unit, label, accent}], `items`, `takeaway`, `takeaway_label` |
| `findings` | `title`, `kicker`, `lead`, `items` [{title, body (string or list), meta {Priority, Owner, Timing, Effect…}}] |
| `references` | `title`, `items` [strings, numbered in order] |
| `appendix` | `title`, `kicker`, `landscape`, `items` |
| `closing` | `headline`, `notes` [[heading, text]] |

Flow `items` (one key per item): `p`, `lead`, `h`, `h3`, `bullets` [..], `quote` (+`by`), `callout` (+`label`), `note` (+`label`; margin layout only), `chart`, `image`, `table`, `kpis`, `pagebreak`.

- Inline: `**bold**`, `*italic*`, `[^3]` or `[^1,2]` for citations (superscript).
- `chart`: `{kind: bar|hbar|line, title, categories, series [{name, values}], highlight (index), format "{:.1f}", unit, source, caption, height_mm}`.
- `table`: `{title, header, rows, align?, widths?, highlight_col?, total_row?, note?, source?}`.
- `image`: `{title, path, alt, caption, source, height_mm}`. Missing/unreadable path produces a placeholder panel.

## Choosing and varying layouts

- Use the layout table in the design spec. Never three identical layout types in a row; alternate dense and airy pages; vary the grid (slab / reading / strip).
- `twocol` narrative only when there is more than about one and a half pages of text; short content looks unbalanced.
- Openers only for major sections of longer reports.
- Landscape `data`/`appendix` only for tables with 8 or more columns.
- Variation comes from content (what dominates the page), not from decoration.

## Quality criteria (all must pass)

Hierarchy and typography
- [ ] Each page has a clear entry point (title or numeral) and no more than 5 distinct text styles.
- [ ] Body 10 pt, measure 55–75 characters; no centered body text; no justified text.
- [ ] Only IBM Plex (or the configured fonts) in the PDF font list; all embedded.

Color and decoration
- [ ] One accent hue; accent under ~10% of any page.
- [ ] None of the rejected patterns: rounded cards, icons, gradients, shadows, stock imagery, decorative dots.

Layout
- [ ] Consecutive pages differ in grid or dominant element; the layout sequence printed by the builder has no triple repeats.
- [ ] No clipped or overflowing text, nothing outside the margins, no table crossing the right margin.
- [ ] No stranded heading at a page bottom; no near-empty page that is not an opener/cover/closing; no last-page orphan of a few lines.
- [ ] Tables: header repeats, rows do not split, numbers right-aligned; figure and table captions stay with their object.

Content integrity
- [ ] Every supplied figure, name, quote and citation appears unchanged; citation numbers all have reference entries.
- [ ] Missing assets shown as placeholders and listed to the user; sample content labelled illustrative.
- [ ] Contents page numbers match the PDF.

## Known limits and fixes

- Layouts rely on tables, section breaks and paragraph borders so they survive Word and LibreOffice; exact page breaks can differ in Word. Re-render in LibreOffice for validation and tell the user if Word pagination matters.
- Fonts are not embedded in the DOCX; install them or the file falls back to Georgia/Calibri and pagination changes.
- Two-column `twocol` flows are not balanced by LibreOffice; check the last page.
- A table row that is taller than the remaining space moves wholesale to the next page (rows never split); if this leaves large gaps, shorten the cell text or reduce meta lines.
- Keep-with-next on headings inside table cells chains rows in LibreOffice; the library disables it in cells. Do not re-enable it.
- A section's last element being a table needs a paragraph after it; the library inserts 1 pt carrier paragraphs. Do not delete them.
