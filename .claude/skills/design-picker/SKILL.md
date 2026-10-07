---
name: design-picker
description: Decide which report or document design to use, from seven design families researched from the user's reference boards (Navy Annual, Forest Breakslide, Leaf & Black, Prism Rounded, Clinicare Aqua, Docoro Royal Block, Market Frame). The skill gives a primary and an alternate family with reasons, plus the palette with contrast checks, fonts, signature motif, layout recipes, a page-by-page plan and a rhythm check. Use when asked which design, style, look, template, colours or layouts to use for a report, annual report, ESG report, business plan, proposal, consultancy deliverable, white paper, healthcare or patient report, brochure, company profile or portfolio, or to make a document look like the reference boards. Pairs with report-design, which builds the DOCX.
---

# Design picker

Seven design families were extracted from the reference boards in `../report-design/references/images/ref-A…G.jpeg`. This skill decides which family a document should use and turns that into concrete instructions: colours, fonts, motif, layouts per page, and the page order. The decision is deterministic. `scripts/pick_design.py` implements the scoring, hard rules and rhythm checks in `references/selection-framework.md`, so the same brief always gives the same answer.

## The seven families

| | Family | Board | Mood | Accent (fill / text) | Type (heading / body) | Corners | Photos needed | Best for |
|---|---|---|---|---|---|---|---|---|
| **A** | Navy Annual | Rapport annuel 2025 | calm, institutional | `#1C2E60` / same | Figtree / Figtree | square | low (2/5) | annual, ESG, grant/public-sector, board reports |
| **B** | Forest Breakslide | Breakslide | premium, eco-modern, dark | `#005A58` / same | Montserrat / Inter | one 45° chamfer | high (5/5) | dark-mode portfolios, agency or eco profiles, screen only |
| **C** | Leaf & Black | Business Plan | confident, start-up | `#57B848` / `#105E00` | Roboto / Roboto | diagonal / diamond | medium (3/5) | business plans, pitch documents, investor and ops updates |
| **D** | Prism Rounded | Prism | friendly, approachable | `#379A86` / `#005955` | IBM Plex Sans | rounded | high (4/5) | marketing, company profiles, portfolios |
| **E** | Clinicare Aqua | Clinicare | clinical, reassuring | `#4CC0CB` / `#005960` | Nunito Sans | circles | high (4/5) | clinical, patient and public-health reports |
| **F** | Docoro Royal Block | Docoro | bold, service-led | `#0339A6` / same | Poppins / Inter | square | high (5/5) | healthcare services brochures, KPI-led reviews |
| **G** | Market Frame | Market | composed, corporate | `#01A19A` / `#005955` | Montserrat / Inter | square + pill tabs | medium (3/5) | consulting, white papers, proposals, ops reviews |

Every family has a no-photo fallback for each layout. "Photos needed" says how much the look loses without photos, and the selector uses it to score.

Each family's full build spec is in `references/families/<letter>-*.md`. Every spec has the same 11 sections: identity, evidence, palette, typography, layout recipes on A4 (in mm and pt), signature components, photo fallbacks, best-for and avoid-for, do-not-copy, DOCX implementability, and a quick-select card.

## Workflow

1. **Intake.** Infer what you can from the request and content. Then ask **one round of at most five questions**, and only for fields that change the outcome:
   1. Document type and audience.
   2. Photos available (none, few or plenty). Never assume stock photos.
   3. Brand colour (hex) or fonts.
   4. Screen, office print or professional print.
   5. Whether the DOCX will be edited afterwards, and any accessibility duty (public sector, patients).

   Never ask about length, sections or layout preferences; working those out is this skill's job.
2. **Write a brief** (`brief.json`, schema below). Add `sections` to get a page plan. `examples/brief-hospital.json` is a complete example.
3. **Run the picker.**
   ```bash
   python3 .claude/skills/design-picker/scripts/pick_design.py brief.json            # recommendation in markdown
   python3 .claude/skills/design-picker/scripts/pick_design.py brief.json --json     # for further processing
   python3 .claude/skills/design-picker/scripts/pick_design.py brief.json --tokens-out out/tokens.json
   ```
4. **Tell the user**, in a few lines:
   - the primary family, the alternate and the deciding reasons (the "beats … on" line);
   - any hard rule that fired and any excluded family;
   - every default applied;
   - the variants to apply.

   If a rule overrides the points ranking (for example healthcare → E while A has more points), say so in one line and offer the alternate.
5. **Design from the spec.** Open the chosen family file and follow the recipe listed for each page in the plan. Use only that family's motif, corner style and photo treatment (mixing rules below). Use the palette roles exactly as the picker prints them.
6. **Check the plan** after any change: `pick_design.py --check-plan "COV TOC SUM OPN CHT …"` (add `--print-light` for office print, `--brochure` for brochures).
7. **Build** (see "Building it"), render, and inspect every page.

## Brief schema

| Field | Values | Default |
|---|---|---|
| `title`, `description` | free text; `doctype` is inferred from keywords when missing | n/a |
| `doctype` | `annual_report esg_report consulting business_plan investor_update clinical_report patient_info health_brochure white_paper ops_review grant_public proposal marketing company_profile portfolio` | inferred, else `consulting` |
| `audience` | list of `regulator board shareholders investors clients management staff public patients customers creative` | per doctype |
| `industry` | `finance healthcare tech environment industrial public creative professional general` | `general` or per doctype |
| `pages` | number | from the plan, else 12 |
| `words_per_page`, `tables`, `text_share` | numbers (`text_share` = prose words ÷ all words) | 300, 0, 0.5 |
| `photos` | `none few plenty` | `none` |
| `output` | `screen office_print pro_print` | `screen` |
| `a11y` | `standard strict` | `strict` for patient and public-sector types |
| `editable` | true/false | true |
| `brand_hex` | `#RRGGBB` | none |
| `tone` | `conservative expressive` (only to break near-ties) | none |
| `dark` | true to ask for dark mode (the only way B becomes primary) | false |
| `family` | `A`–`G` to force a family; the picker warns if a rule would exclude it | none |
| `sections` | `[{title, items:[{type, title, …}]}]`; item types below | none |

Item types and their size fields:
- `summary`, `foreword`, `case`, `photo`, `appendix`, `pricing`: no size field.
- `figures` (count), `timeseries` (points, series), `comparison` (items, attributes, precise).
- `parts` (count), `ranked` (count, values), `steps` (count), `org` (levels, children).
- `quote` (words, count, portrait), `text` (words, no_figures), `table` (columns, rows, reference).
- `swot` (max_bullets), `timeline` (count), `team` (count), `recommendations` (count).
- `risks` (count), `map` (image: true if a map image exists).

## How the choice is made (summary)

The full rules are in `references/selection-framework.md` §4. Exclusions are applied first:
- B is excluded under strict accessibility, office printing, or a brand colour below 4.5:1.
- B and F are excluded when there are no photos.
- B and D are excluded for more than 40 pages or a text share above 0.6.

Ten weighted criteria are then scored. Document type has the biggest weight (5) and brand hue the smallest (1). A family is chosen by **structure**, and the brand colour is swapped in afterwards.

Overrides apply in this order:
1. Dark mode requested → B.
2. Annual report → A.
3. Healthcare → the better of E and F.

Ties are broken by document-type points, then lower ink, then lower photo dependency, then the order A G C E F D B.

Quick human version (the script wins if they disagree):
- Annual, ESG, grant and public-sector reports → **A** (alternate G).
- Consulting, white papers, proposals, company profiles, investor updates → **G** (alternate A).
- Business plans and pitch documents → **C** (alternate G). Ops reviews go to **G** or **C**.
- Healthcare data, board and patient documents → **E** (alternate A). Healthcare services and marketing with photos → **F** (alternate E).
- Marketing and portfolios → **D**. **B** only when dark mode is asked for on screen.

## Rules that apply to every family

**Colour** (`assets/palettes.json`, `references/palettes.md`):
- Small accent text (kickers, labels, numerals under 24 pt, links) always uses `accent_deep`, which is 7:1 or better on white.
- The bright accents fail as text: teal 3.2:1, green 2.5:1, aqua 2.2:1. Use them only as fills, and as numerals of 24 pt and up where they reach 3:1.
- Text on aqua and green fills is ink (`on_accent`), never white.
- One accent hue per document, in its deep, bright and tint shades. Black is a second colour only in C.
- Charts use the 5-step ramp. The series that carries the argument goes in the deepest step, and steps 1–2 need direct labels.
- `signal` is only for negative values.

**Mixing**:
- One family per document; the alternate is an alternative, not a source of extra pages.
- One signature motif and one corner geometry. Never mix rounded and cut corners.
- One type pairing with at most 4 weights. Caps only for titles and labels.
- One photo treatment: colour, black and white (C), or duotone (F).
- One icon style: line glyphs in solid circles, never emoji.
- A brand overrides colour and fonts, never structure.

**Rhythm** (enforced by `--check-plan`):
- R1: never 3 identical layouts in a row (TXT, TAB and APX may run to 3).
- R2: at most 3 dense pages in a row.
- R3: colour pages at most 25%, or 15% under `print_light`.
- R4: openers and break pages at least 3 pages apart.
- R6: a contents page from 8 pages up (not brochures).
- R7: every opener is followed by 2 content pages.
- Decision documents put the executive summary in the first 3 content pages.

**Content → layout** (`selection-framework.md` §6.2):
- 3–4 headline figures → KPI strip; 5–8 → KPI page; more than 8 → table.
- One time series with up to 12 points → column chart; otherwise a line chart.
- 3 or more items with 3 or more attributes → table; fewer → comparison columns.
- 3–5 steps → step tiles.
- More than 600 words of text → reading page; more than 1,500 words with no figures → two columns.
- 8–12 columns → landscape table.
- Long ranked lists and large teams → tables.

**Integrity**: never invent facts, figures, quotes or photos. Missing photos use the family's no-photo fallback, and missing data gets a visible placeholder. Break pages carry a supplied sentence, never filler.

## Building it

**Fonts.** All are OFL and bundled in `assets/fonts/`: Figtree, Montserrat, Poppins, Inter, Roboto and Nunito Sans. IBM Plex is in `../report-design/assets/fonts/`. Install them before rendering:

```bash
mkdir -p ~/.fonts && cp .claude/skills/design-picker/assets/fonts/*.ttf .claude/skills/report-design/assets/fonts/*.ttf ~/.fonts/ && fc-cache -f
rm -rf ~/.cache/matplotlib   # otherwise charts fall back to DejaVu until matplotlib rescans fonts
```

**Word and LibreOffice behaviour** (`references/docx-techniques.md`): every technique below was proven in LibreOffice 24.2, with proof renders in `assets/proofs/`. Word itself is untested.

| Technique | Method | Watch out |
|---|---|---|
| Fonts | Bold uses the base family + `w:b`; SemiBold and ExtraBold use their own family name ("Poppins SemiBold") | Set leading in **exact pt**; "auto" makes Poppins and Inter far too loose |
| Full-bleed panel, cover, band, dark break page | Header-anchored rectangle shape (`relativeFrom=page`, behind text) | Full-page tables leave 1 mm gaps and can add a blank page |
| Rounded slabs and pills with text | DrawingML `roundRect` + text box, `adj = r / min(w,h) × 100000` | Small shapes need zero insets |
| Photo masks (circle, diamond, chamfer, rounded) | PIL RGBA mask at 300 dpi | Crop to the box ratio first |
| Vertical tab text | Table cell `btLr`/`tbRl` or shape `vert270` | Shape rotation does not rotate the text |
| Inset frame | Header-anchored rectangle at 10 mm | Page borders need a footer distance of 10 mm or more |
| Icons | `lucide-static` SVG → 300 dpi PNG on an accent circle | Ship the licence (`assets/icons-sample/`) |
| Single-hue charts | matplotlib at 300 dpi, family fonts, ramp from the deep token | Pale steps need direct labels |

**Engine status.** `../report-design/scripts/reportkit.py` still produces only the "Slab & Rule" layouts. `--tokens-out` writes a `tokens.json` it can read; that file uses the text-safe accent, deep-first chart series and the family fonts. Pass it with `REPORT_TOKENS=out/tokens.json python .claude/skills/report-design/scripts/build_report.py …`. That changes colours and fonts only, not the layouts. To get a family's real look, build its pages from the spec's recipes with the techniques above. The engine changes needed before it can carry these families are listed in `references/docx-techniques.md` §11 and `references/palettes.md` §6.2:
- a theme object instead of module-global tokens;
- exact-pt leading;
- accent text read from `accent_deep`;
- a frame footer distance of 10 mm or more;
- `check_pdf.py` accepting non-Plex fonts.

## Files

| Path | What it is |
|---|---|
| `scripts/pick_design.py` | Selector, page planner, rhythm checker, token export. `--list`, `--examples` (regression test of the 7 worked examples) |
| `references/selection-framework.md` | Reader expectations for 15 document types, family profiles, intake, scoring, decision tree, layout vocabulary, rhythm, mixing, worked examples, sources |
| `references/families/A…G-*.md` | Per-family build specs (11 sections each) |
| `references/palettes.md`, `assets/palettes.json` | Measured colours, contrast tables, token sets, chart ramps, print notes; `scripts/palettes_measure.py derive` reproduces the JSON |
| `references/docx-techniques.md` | Tested python-docx + LibreOffice code for every technique, plus the engine audit |
| `references/user-design-notes.md` | The user's own analysis of the boards (verified accurate; gaps noted in `research-brief.md`) |
| `references/research-brief.md` | The brief all 10 research agents worked from |
| `assets/fonts/`, `assets/icons-sample/`, `assets/proofs/` | OFL fonts, Lucide icon samples and licence, proof renders |
| `examples/brief-hospital.json` | Complete brief with sections |

## Evidence and limits

- The boards are slide templates; only A is a real report. Data tables, long reading pages, citations and appendices appear on none of them, so those recipes are tagged **[inferred]** in the specs. Font names are best guesses tagged **[uncertain]**; the OFL substitutes were compared against crops.
- Scores and thresholds are practice-based defaults. Tune them in `pick_design.py`, and keep `--examples` passing (or update its expectations on purpose).
- A royal blue near `#0339A6` may fall outside CMYK; proof-print family F before a professional run.
