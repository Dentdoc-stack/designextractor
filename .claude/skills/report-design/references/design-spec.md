# Design specification: "Slab & Rule"

Single source of numeric values: `assets/tokens.json`. This document explains the rules and why. Evidence references (A–G, P1–P24) point to `reference-analysis.md`.

## 1. Identity in one paragraph

A restrained editorial system: one deep green accent, near-black ink on white, serif for reading and numerals, a small-caps sans for everything that *labels or measures*. Structure comes from **slabs** (solid blocks), **rules** (hairlines) and **whitespace**, never from cards, shadows, gradients or icons. Pages alternate between airy (openers, summary) and dense (data, appendix) so a long report has rhythm.

Derived from: single-hue discipline (P1, P2), anchoring column/band (P3), dense/airy alternation (P4), oversized numerals (P5), caps micro-labels (P7), hairline dividers (P8), frame (P9). Rejected: P20–P24.

## 2. Color

| Role | Token | HEX | Use | Never |
|---|---|---|---|---|
| Ink | `ink` | `#17211E` | Text, rules, cover slab, closing slab | Pure `#000` |
| Paper | `paper` | `#FFFFFF` | Page | Tinted page backgrounds (print waste) |
| Accent | `accent` | `#0B5D4F` | Short rule under titles, highlight bar/series, key numeral, summary slab, kickers | More than ~10% of any page's area; body text |
| Accent tint | `accent_tint` | `#E3ECE8` | Text on accent slab (labels) | Large fills |
| Tint | `tint` | `#F1F2EE` | Highlighted table column, image placeholders | Cards |
| Signal | `signal` | `#B4591B` | Reserved for warnings or negative variance in data (optional) | Decoration |
| Grey | `grey` | `#5E6663` | Secondary text, captions, notes (contrast on white ≈ 6:1) | Body text |
| Rule | `rule` / `hairline` | `#B9BFBB` / `#D5D9D6` | Dividers, table row lines | Thick borders |

Rules:
1. **One accent.** If a second hue is needed (e.g. a brand color), replace `accent` wholesale; do not add.
2. **Highlight, don't rainbow.** Charts show the series that carries the argument in accent and everything else in grey tints (from refs A, C, F: P13). Multi-series charts use `chart_series` order: accent, ink, grey, light grey.
3. **Accent budget.** Per page: ≤ 1 slab or ≤ 1 large accent numeral, plus the short title rule and kickers.
4. Text/background contrast ≥ 4.5:1 (ink on white ≈ 16:1; white on accent ≈ 8:1).
5. Brand override: swap `accent` and `ink` in `tokens.json`; nothing else changes.

## 3. Typography

| Face | Role | Why |
|---|---|---|
| IBM Plex Serif (Regular, Italic, Bold) | Headlines, body, lead, numerals, quotes | Sturdy text serif with distinct numerals; free (OFL); reads well in print at 10 pt |
| IBM Plex Sans (Regular, Italic, Bold) | Kickers, labels, captions, tables, margin notes, headers/footers | Neutral, tabular figures for data, compact in caps |

Reference note: the references use a heavy geometric sans throughout (Montserrat/Poppins-like **[uncertain]**) in caps. This system deliberately inverts that: a quiet serif for headlines (editorial, differentiates from template look) and reserves sans caps for the micro-label role seen in B, C, D, G (P7).

Fallbacks when fonts are not installed: Georgia (serif) and Calibri (sans). Layouts are measured with Plex; fallbacks run wider, so re-check page breaks.

### Scale (pt) and leading

| Style | Size | Leading | Notes |
|---|---|---|---|
| Display (cover/opener title) | 44 | 1.02 | Regular weight; ≤ 3 lines |
| Numeral XL (opener number) | 120 | 1.0 | Accent |
| Numeral L (finding number) | 34 | 1.0 | Accent if High priority, else ink |
| Numeral M (KPI) | 26 | 1.0 | Unit at 14 pt beside it |
| H1 | 28 | 1.05 | Regular; followed by 22 mm accent rule |
| Lead | 13 | 1.32 | Measure ≤ 135 mm |
| H2 | 14 bold | 1.2 | 14 pt before, 4 after, keep with next |
| H3 / Kicker / Label | 7.5 bold caps, tracking +0.12 em | n/a | Kicker is accent; Label is grey |
| Body | 10 | 1.38 | Left-aligned, ragged right, no justification |
| Quote | 16 italic | 1.25 | Accent, with 1 pt accent rule above |
| Table | 8.5 (7.5 dense) | 1.2 | Header 7 bold caps |
| Caption / note | 7.5 / 8 | 1.3–1.35 | Grey |
| Reference | 8 | 1.35 | Hanging indent 6 mm |

Rules:
- Ratio headline : body ≈ 2.8 : 1; ≥ 3 distinguishable levels per page, never more than 5.
- Measure: body 55–75 characters. Single column text is capped at 118–130 mm by right indent, not by full width.
- Headings sentence case. Only labels use caps, and only with tracking.
- Numerals in running text are in the text face; tables and KPIs align numbers right.
- Do not underline, do not center body text, do not mix more than one italic role per page (quote or emphasis).

## 4. Page, grid and spacing

- A4 portrait 210 × 297 mm. Margins: top 24, bottom 20, left 22, right 18 (live width 170 mm). Header at 11 mm, footer at 10 mm.
- Three grids, chosen per layout:
  - **Reading grid** (narrative): text 122 mm | margin column 48 mm with hairline between (P8, G).
  - **Slab grid** (summary): slab 52 mm | content 118 mm (A, B: P3).
  - **Strip grid** (data, findings): full 170 mm divided into equal KPI cells or `20 | 104 | 46` for findings.
- Baseline rhythm: spacing in multiples of 2 pt; paragraph gap 6 pt; section gaps 14 pt.
- Landscape (257 mm live width) only for tables with ≥ 8 columns.
- Whitespace is a feature: openers and covers may be 70% empty. Dense pages keep ≥ 18 mm outer margin.
- Rules: 0.5 pt hairlines between rows and columns, 1 pt ink at table tops/bottoms and KPI strips, 3 pt accent only for the 22 mm title rule and callout bars.
- Frame: an inset 0.5 pt hairline (10 mm from the page edge) appears only on **section openers** (P9, ref G). Not on content pages.

## 5. Components

### Kicker + title + rule
Kicker (accent caps) → H1 → 22 mm accent rule → optional lead. Identical across content pages so the reader recognises the system; position of the page's other content varies.

### KPI strip
Equal cells with 1 pt ink rule across the top, 0.5 pt hairlines between cells, numeral M above a caption. At most 5 cells; one may be accent to mark the number that matters (P5, C).

### Tables
- Top and bottom 1 pt ink, header separated by 1 pt ink, rows by 0.5 pt hairline. No vertical lines, no zebra, no cell fills except an optional **highlight column** in `tint` with bold figures (echoes P13: emphasise the current period).
- Header: 7 pt bold caps, bottom-aligned. Body 8.5 pt (7.5 pt if > 6 columns or > 18 rows).
- Numeric columns right-aligned (auto-detected), text columns left. Column widths proportional to content, clamped.
- Header row repeats across pages; rows never split. Total row: bold, 1 pt rule above.
- Caption: "Table n — Title" above (caps label); source and notes below in caption style.
- ≥ 8 columns: landscape section.

### Charts (generated PNG, 300 dpi)
- Plex Sans 7–7.5 pt, no top/right/left spines, no gridlines on bar charts, direct value labels, no legend box (single-series), legend inline above plot for multi-series.
- Single series: all bars light grey, the argument bar in accent (default: last bar; override with `highlight`).
- Line charts label series at the line end. Units appear as a small grey line at top-left of the plot.
- Figure label above ("Figure n — Title"), source below.
- No 3D, no pies/donuts, no shadows, no rounded bars. If shares are needed use a ruled table or a single stacked horizontal bar.

### Callout
3 pt accent bar on the left, caps label (e.g. "What this means", "Decision"), 11 pt serif text. One per page maximum.

### Pull-quote
16 pt italic serif in accent, 1 pt accent rule above, attribution in caps label. Lives in the margin column of a narrative page.

### Margin note
Sans 8 pt grey with optional caps label (Definition, Data quality…). Attached to the passage's table row so it stays beside it.

### Numbered findings
Row table: numeral | title and body | meta (Priority, Owner, Timing, Effect). Ink rules between rows (P6, C). Numeral turns accent when priority is High.

### Citations
Superscript numerals referencing the numbered reference list. The builder warns if a cited number has no entry.

### Images
- Never decorative stock photography. Use supplied photographs, maps, screenshots, charts.
- Crop rectangles only (no circles, no rounded corners). Full text-column width or full bleed on covers; captions below in caption style.
- Photographs overlapped by a slab or band (B, F, G: P14) are an option for covers and openers when the client supplies imagery.
- Missing image: a `tint` panel with a caps "Image to be supplied" label plus alt text; never an invented stand-in.

### Header and footer
Running header: short title left, current section right, 0.5 pt rule below, 7 pt caps grey (P10). Footer: confidentiality or sample note left, page number right in serif. Covers, openers and closing pages have neither.

## 6. Layout family

Each layout has a job, a grid, and a **variation lever**. Layout names are the `type` values in the content JSON.

| Layout (`type`) | Job | Composition | Variation levers |
|---|---|---|---|
| `cover` | Identity | `slab`: 34 mm ink column on the left with rotated client/date, title low on the page above a metadata strip. `band`: white field with title, ink band at bottom holding metadata | `variant`; kicker text |
| `contents` | Navigation | Title and note in left 52 mm; entries right with dotted leaders. Level 1 serif 15 pt (numbered for openers), level 2 sans 9.5 pt | Auto-generated; page numbers via two-pass render |
| `summary` | Decide in one page | Accent slab (52 mm, full height) with 2–4 key figures; right: lead, numbered points separated by hairlines, optional callout | Figures, points, `after` items |
| `opener` | Pace and orient | Framed page; numeral XL top-left, title bottom-left with accent rule, rotated section label, 2-line intro | `number`, `label`, `intro` |
| `narrative` | Long text | `layout: margin` (text + margin notes/quote), `measure` (single narrow column, whitespace right), `twocol` (two text columns under a one-column heading) | `layout`; choose by length: ≤ 1 page → margin or measure, > 1.5 pages → twocol |
| `data` | Evidence | Kicker/title/lead, KPI strip, chart, table, takeaway callout, in any order via `items` | `landscape`; chart kind; `kpis` optional |
| `findings` | Decisions | Numbered row table with meta column | Number of items (3–6); priority drives numeral color |
| `references` | Sources | One-column heading, then two-column list at 8 pt | Number of entries |
| `appendix` | Backup | Same header; any `items`; small tables; landscape when needed | `landscape` |
| `closing` | Colophon | Full-bleed ink band with a closing line, notes below | `headline`, `notes` |

### Variation rules (the anti-formula rules)
1. No layout type three times in a row; the builder prints a warning.
2. At least one airy page (opener, cover, closing) per ~6 content pages.
3. Consecutive content pages must differ in at least one of: grid (slab/reading/strip), dominant element (text, chart, table, numerals), or density.
4. Do not give every section an opener. Short reports (< 8 pages) get none; 8–20 pages get openers only for the 2–4 major sections.
5. Alternate where the visual weight sits: slab left (summary), text left with note right (narrative), full-width strip (data).

## 7. Handling hard cases

| Case | Behaviour |
|---|---|
| Very long paragraph | Text column keeps measure; widow/orphan control on; consider splitting at the claim boundary; do not edit supplied wording |
| Dense table (> 18 rows) | 7.5 pt, repeating header, rows never split; > 8 columns → landscape block |
| Table with long text cells | Give explicit `widths`; text columns left-aligned |
| Missing image | Tint placeholder with alt text; report lists the missing assets to the user |
| Page break | Headings keep with next; callouts and figures stay with captions; check `check_pdf.py` for stranded headings and near-empty pages |
| Last page orphan (a few lines on a new page) | Trim a sentence of design-level whitespace (e.g. remove callout), or move content to the margin column; never cut supplied facts |
| Missing numbers or citations | Leave the cell/citation as supplied; add nothing; warn the user |
| Word vs LibreOffice | Layout uses only tables, section breaks, exact row heights and paragraph borders. Re-check in Word if the client uses Word; fonts must be installed |

## 8. Anti-patterns (hard rejects)

Rounded rectangles or pills; icon circles; emoji or icon bullets; gradient fills; drop shadows; glossy overlays; stock photos of handshakes, laptops or plants; centered body text; more than one accent hue; chart rainbow palettes; 3D or donut charts; identical card grids; every page having the same header-image-bullets structure; decorative dots; all-caps paragraphs; underlined links in print; tables with full grids.
