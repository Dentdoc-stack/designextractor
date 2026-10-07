# Ref B — "Breakslide" (dark green, stepped slabs)

Source: `.claude/skills/report-design/references/images/ref-B.jpeg` (736×1063 px JPEG collage, 10 slides at 16:9, each about 322×182 px).
Method: I cropped each slide, upscaled it 3× (Lanczos) and viewed it, then zoomed corners 12×. Colours come from PIL pixel sampling (5×5 px means, or the darkest/lightest percentile for text). Area shares come from nearest-role classification with max channel Δ ≤ 30. Contrast is WCAG 2.x relative luminance, computed here rather than estimated.
Tags: **[seen]** visible in pixels · **[inferred]** my interpretation or adaptation · **[uncertain]** guesses (fonts, exact sizes). Every mm and pt value in sections 5–6 is a **proposed A4 adaptation [inferred]**, not a measurement of the board.

---

## 1. Identity

Breakslide is a **monochrome-green "dark mode" system**. Its ground is one flat deep teal-green (`#005A58`) and its depth comes from **tall vertical slabs**. Each slab is a rectangle with a vertical gradient from bright green at the top to the ground colour at the bottom. The slabs step across the page at different widths and heights, and they **overlap photographs**. Photos are moody and green-graded (foliage, dim interiors, portraits against leaves), often with **one 45° clipped top corner**. A small **chamfered "stub" slab** overlaps a photo's lower corner. A **three-dot marker** (bright, mid, near-black green) sits by every title. Typography is a friendly geometric sans in white: medium-weight title-case headings, tiny very widely tracked caps labels, light-weight names, and a heavy tracked caps wordmark on the cover. About 6 of the 10 slides are dark and 4 are mostly white. On the white slides the title turns dark green and the slabs move into a side panel or a top band. That white-page grammar is what makes the system usable for a printed A4 report: **dark pages for cover, break and closing only; white content pages carrying a narrow slab rail, deep-green headings and the dot marker.** [seen / inferred]

---

## 2. Evidence (every slide)

Slides are numbered row by row, left then right (crop files `s01`–`s10`).

| # | Board position | What it shows | Tags |
|---|---|---|---|
| 1 | row 1 left, "Our Services" (dark) | Full `#005A58` ground. Title top-left (white, title case) with the three-dot marker on the title's centre line to its right. Three white line icons in a row (recycle, plant-in-hand, bulb). Caps label "SERVICE 001" and a justified body block about 7 lines deep. On the right, a bright slab runs from the top edge at x 54–81% of slide width, a rectangular photo (pillow "LIFE IS BEAUTIFUL") sits over it, and a chamfered stub slab overlaps the photo's bottom-right corner. Faint darker strips and a hairline at about x 91%. The photo corner is **not** clipped here. | [seen] |
| 2 | row 1 right, "Our Company *Investor*" | **50/50 split** (x 49.5%). Left half is white, with a bright-ramp slab on the left edge (x 0–16%) and a portrait photo **clipped top-right**. A chamfered stub slab overlaps the photo's bottom-left. Right half is deep green: two-line title, second line *italic*, then a light-weight name "Alexander Castillo", a caps label "THE KEY PEOPLE" and a 3-line body. The dots straddle the white/dark seam. | [seen] |
| 3 | row 2 left, "Our Team" (dark) | Four **full-height vertical columns** alternating ramp and ground, at widths of about 27 / 22 / 24 / 26% (edges at x 27, 49, 73%). Portrait photos sit in the bright columns. Names (light weight, 2 lines) and caps roles ("MARKETING", "PHOTOGRAPHER") with body sit in the dark columns. The footer has tracked italic caps "CREATIVE COMPANY", the dots and a long hairline. | [seen] |
| 4 | row 2 right, "Our Team" (top band) | Deep band across the top **0–36%** of slide height, with the title left and the dots right. Three **square photos straddle the band's bottom edge**. Below on white: names in a light grey-teal (darkest pixel `#A1B1AE`, low contrast), caps roles in dark grey, and very pale grey body (darkest pixel `#CFCFCF`). | [seen]; true text colours are lighter in the JPEG [uncertain] |
| 5 | row 3 left, "Our Services" (photo + slabs) | Top **0–55%**: a near-black foliage photo (`#010F06`) with **four bright gradient slabs** standing in it (about 12% wide each). The dots and the white title are centred over it. **Four circular chips** (deep fill, white ring, white glyph) straddle the photo/white boundary. Below: dark caps labels "SERVICE 001" and 3-line grey body, centred. | [seen] |
| 6 | row 3 right, "Our Portfolios" (white) | Mostly white (67% white pixels). A two-line title in **dark green-grey** (darkest pixels `#253C34`) bottom-left with the dots below it. A circular leaf photo near the centre. Caps label "PROJECT 002" with justified grey body. A right column at about x 64–86% holds a photo in its top two-thirds and a **bright-to-deep slab** (`#44B790` to `#076760`) in its bottom third. | [seen] |
| 7 | row 4 left, "Our Service" (white) | A left **ramp panel at 0–29.5%** width, then a darker strip (29.5–35.4%), then white. A photo **clipped top-left** straddles the panel/white seam, and a chamfered stub slab (top-right cut) overlaps its lower-left. The dots sit at the top of the seam. On the right, a **service list**: three rows, each a dark line icon with a caps label "SERVICE 001/002/003" and 2-line grey body. | [seen] |
| 8 | row 4 right, "Our Services" (dark + collage) | Left 49% is deep ground with the title, dots and two icon + caps label + body items. Right side: a photo collage (green interior with a lamp, two leaf photos) separated by bright vertical bands, with a stub slab overlapping at the bottom. | [seen] |
| 9 | row 5 left, "Our Services" (inset) | A white margin on the top (9%) and left (6%) frames a deep panel. A tall leaf photo **clipped top-left** at the left, with a bright slab rising from the bottom over it. Title white, dots below. Four **outline circle icons** (white 1 px ring) in a 2×2 grid at the right. Caps label and body bottom-centre. | [seen] |
| 10 | row 5 right, cover "BREAKSLIDE" | Deep ground. A thin vertical hairline at x≈10% carries rotated micro-text. A small "•••" in square dots precedes a **heavy, widely tracked caps wordmark** (cap height about 8.5% of slide height) that **crosses over the photo**. A widely tracked caps subtitle "PRESENTATION" sits in a barely visible teal (`#146E6C`). The dots are below. A full-height bright slab sits at x 79–100%, a mid slab at x 68–77% in the lower part, and a leaf photo **clipped top-right** overlaps both. | [seen] |

Cross-slide observations:
- Photos appear on all 10 slides. [seen]
- The dots appear on all 10 slides, in the same three colours every time. [seen]
- Slab gradients always run bright at the top to deep at the bottom. [seen]
- The chamfer leg is about 15–16% of the photo's width at 45° (measured on slides 2, 7 and 10). [seen, ±2 px]
- Stub slabs are chamfered on one top corner (slides 1, 2 and 7). [seen]
- Every heading is a placeholder ("Our Services" ×5, "Our Team" ×2), and every label reads "SERVICE 001". [seen]

---

## 3. Palette (measured)

The **board median** column is a direct pixel sample. The **report value** column is what I propose for print/DOCX; it differs from the board median where the board fails contrast or where a role does not exist on the board.

| Role | Board median (where sampled) | Report value | Contrast: colour as text on white | Contrast: white text on colour | Use |
|---|---|---|---|---|---|
| **Accent deep / dark ground** | `#005A58` (slides 1, 2, 3, 4, 8, 9, 10 all within ±3) | `#005A58` | **8.07** (AA+AAA any size) | **8.07** | Cover, break and closing grounds; table headers; H1 on white; KPI numerals |
| **Accent darkest** (3rd dot) | `#043637` (dots, 6 samples `#013635`–`#12312B`) | `#043637` | 13.22 | 13.22 | Third dot; optional ink for headings |
| **Slab low** (ramp step 3) | `#077060` (slab mid-heights, slides 5 and 10) | `#077060` | 6.01 | 6.01 | Stepped slab shades |
| **Slab mid** (ramp step 2) | `#10906F` (slab tops, slides 1, 3 and 7: `#10906F`/`#158F6F`/`#118F6E`) | `#10906F` | **4.01**: large text only (≥18 pt, or ≥14 pt bold) | 4.01: large only | Slabs, big numerals ≥18 pt |
| **Accent bright** (ramp step 1) | `#23B582` (slide 10 slab top; slide 6 `#44B790`, slide 2 `#57BA96`) | `#23B582` | **2.62: fails, never text** | 2.62: fails | Slab tops, chart highlight, dot 1 fill area only |
| **Dot bright** | `#2E9B64` (6 samples `#299C62`–`#32976A`) | `#2E9B64` | 3.51: large only | 3.51 | Dot 1 |
| **Dot mid / label green** | `#19816A` (6 samples `#178367`–`#257E65`) | `#19816A` | **4.78: AA body OK** | 4.78 | Dot 2; **the only bright-ish green safe for small caps labels on white** |
| **Tint** (not on board) | none; the board has no light tint | `#E6F2EF` (alt `#CFE8E1`) | 1.15 (not text) | 1.15 | KPI tiles, highlight rows, callouts on white pages. Ink on tint 10.70; deep on tint 7.03; `#19816A` on tint 4.17 (large only) |
| **Ground (content)** | `#FFFFFF` (24% of all slide pixels) | `#FFFFFF` | — | — | All content pages |
| **Ink** | Titles on white: darkest pixels `#253C34`/`#283835` (JPEG anti-aliasing lightens them; the original is probably darker) [uncertain] | `#1E3A35` (green-black); neutral alt `#1F2328` | **12.27** (neutral alt 15.80) | — | Body text, H2/H3 |
| **Secondary text** | On white: darkest pixels of body `#CFCFCF`, labels `#828687`. On dark: body `#66B0AF` (JPEG-blurred white) | `#5B6270` on white; `#CFE8E1` on deep | Board `#CFCFCF` **1.56 fails**, `#828687` 3.68 fails; report `#5B6270` **6.13** | `#CFE8E1` on `#005A58` = **6.25** | Captions, bios, footers |
| Hairline | not measurable | `#CFE0DC` | 1.37 | — | Table rules, 0.5 pt |

Other contrasts I computed:
- **On the deep ground:** bright `#23B582` on `#005A58` is 3.07 (≥24 pt numerals only); `#57BA96` on deep is 3.41; white on the darkest green `#043637` is 13.22.
- **Ink on the bright slab:** `#1E3A35` on `#23B582` is 4.68 (AA, so dark text on bright slabs works).
- **Ramp steps against each other:** deep→low 1.34, low→mid 1.50, mid→bright 1.53. Adjacent steps read clearly in colour but are subtle in greyscale, so the bright cap must be next to the deep for the step to survive mono print.
- **Board text that fails** (do not copy): the cover subtitle `#146E6C` on `#005A58` is 1.34; slide 4 names `#A1B1AE` on white are 2.23; slide 4/5 body `#CFCFCF` on white is 1.56.

**Area share** (10 crops, slide pixels only):

| Role | Share |
|---|---|
| Ground `#005A58` | **37.7%** (whole collage including the board's own outer background: 39.8%) |
| White | 24.0% |
| Slab family (low/mid/bright, gradient) | 13.9% (`#077060` 6.1%, `#0F8A6C` 6.6%, `#2BB283` 1.2%) |
| Near-black photo shadows | 10.4% |
| Other (photo midtones, text AA) | 14.0% |

Per-slide ground share runs from 67% (slide 1) to 2% (slide 6). **Dark-dominant slides: 1, 2, 3, 8, 9, 10 (6/10). White-dominant: 4, 6, 7 (3/10); slide 5 is split.** [seen]

**Data-viz ramp for charts [inferred]**: `#CFE8E1` → `#57BA96` → `#10906F` → `#005A58`, with the most recent or most important series in the deepest shade. That is at most 4 steps; past 4, switch to direct labels rather than adding a fifth shade.

---

## 4. Typography

**Observations [seen]**
- **Headings**: a geometric sans with round O/S and an open, wide stance, medium-to-semibold weight, **title case, not caps** ("Our Services"). The cap height is about 4.4% of slide height. Two-line titles sometimes set the second line in *italic* (slide 2 "*Investor*").
- **Cover wordmark**: ExtraBold/Black **caps**, tracked about +10–12%, cap height about 8.5% of slide height (≈2× the slide titles). It overlaps the photo.
- **Names**: light weight, mixed case, 1–2 lines (slides 2, 3, 4).
- **Labels**: tiny bold **caps with very wide tracking** (≈+25–35%): "SERVICE 001", "MARKETING", "THE KEY PEOPLE". The cap height is about 1–2 px, roughly 0.8× the body cap height but heavier.
- **Subtitle** "PRESENTATION": light caps with very wide tracking (≈+40%).
- **Body**: tiny, **justified**, line pitch about 5.7 px. That puts the title-cap : body-line ratio around 3.2:1.

**Family guess [uncertain]**: headings and wordmark look like **Montserrat** (SemiBold / ExtraBold). The light-weight names could be **Poppins Light** or Montserrat Light. The labels could be either family in Bold.

**OFL substitutes (npm)** [checked: `npm view` returns 5.3.0 for all three; Inter is OFL-1.1]:
- `@fontsource/montserrat` (OFL 1.1), for headings, labels and the wordmark.
- `@fontsource/inter` (OFL 1.1), for body text: narrower and more legible at 9–10 pt than Montserrat. This is my adaptation [inferred].
- `@fontsource/poppins` (OFL 1.1), an optional alternative for names.
- Montserrat Regular/Medium/SemiBold/Bold/ExtraBold, Poppins and Inter are installed in this container (`~/.fonts` / system). **No Light weight is installed**, so use Regular for "light" roles or install the 300 files from fontsource. In LibreOffice the non-standard weights resolve by family name ("Montserrat SemiBold", "Montserrat ExtraBold"), so python-docx must write those names in `w:rFonts`. [seen in fc-list]

**A4 roles [inferred]**

| Role | Font | Size / leading | Case / tracking | Colour |
|---|---|---|---|---|
| Display (cover) | Montserrat ExtraBold | 44–54 pt / 1.0 | CAPS, +10% (≈ +100 twentieths) | white on deep |
| Break-page number | Montserrat ExtraBold | 96–120 pt / 0.9 | figures | `#23B582` on deep (3.07, large) |
| H1 / section title | Montserrat SemiBold | 26–30 pt / 1.1 | Title case; optional italic 2nd line | `#005A58` on white, white on deep |
| H2 | Montserrat SemiBold | 14–15 pt / 1.2 | Sentence case | `#1E3A35` |
| H3 / list head | Montserrat Bold | 10.5 pt / 1.25 | Sentence case | `#1E3A35` |
| Label / kicker | Montserrat Bold | 7–7.5 pt | **CAPS, +25–30%** (≈ 40–45 twentieths at 7.5 pt) | `#19816A` (4.78) or `#5B6270` on white; `#CFE8E1` on deep |
| Name | Montserrat Regular (or Poppins Light) | 13 pt / 1.15 | Mixed case | `#005A58` |
| Body | Inter Regular | **9.5 pt / 14.5 pt**, **ragged right** (not justified) | — | `#1E3A35` |
| Caption / bio | Inter Regular | 8–8.5 pt / 12 pt | — | `#5B6270` |
| KPI numeral | Montserrat Bold | 30–36 pt | figures | `#005A58` |
| Folio / running head | Montserrat SemiBold | 7.5 pt | CAPS +25% | `#5B6270` |

Ratio check: the board's title-cap : body-line ratio of ≈3.2:1 maps to 28–30 pt titles over 9.5 pt body, consistent with the table.

---

## 5. Layout recipes — A4 portrait (210 × 297 mm)

**Page frame for all white content pages [inferred]**
- Margins: top 22, bottom 20, left 26, right 18 mm. That gives a content width of **166 mm**.
- Columns: a two-column field of main 112 mm + gutter 8 + side 46 mm.
- **Slab rail** on the left edge, full bleed:
  - `#005A58` at x 0–7 mm, full height.
  - `#23B582` cap at x 7–11 mm, y 0–60 mm (the "step").
  - Ink coverage ≈ 3.7% of the page.
- Running head at y 12 mm: dots (12.8 mm wide) at x 26, then section name in label style at x 42.
- Folio bottom-right at y 285 mm, label style, `#005A58`.

**Print budget [inferred]**
- Dark full-bleed pages are limited to the **cover, one break page per major section, and the closing page**. Never put two dark pages back to back except cover + inside-cover in a bound print run.
- Target an average ink coverage of ≤ 15% across the document. Every recipe below carries a `print-light` variant.

### R1 — Cover (dark)
- **Ground**: `#005A58`, full bleed. Zero-margin section; total row heights ≤ 295 mm so LibreOffice does not spill a blank page.
- **Slabs**:
  - Slab A: x 160–210 mm, y 0–297, ramp `#23B582` (top) → `#005A58` (bottom). 24% of the width, matching slide 10's 21%.
  - Slab B: x 128–152 mm, y 150–297, `#077060` → `#005A58`, shorter so it reads as a step.
- **Photo**: x 116–188, y 62–206 mm (72 × 144 portrait), **chamfer top-right at 11 mm**, overlapping both slabs.
- **Stub slab**: 26 × 60 mm, chamfered top-right at 5 mm, `#10906F` → `#077060`, overlapping the photo's bottom-left at x 108–134, y 170–230.
- **Text**:
  - Kicker (label, `#CFE8E1`) at x 22, y 70.
  - Title (Display 48 pt caps, white) at x 22, y 82–150, max width **88 mm**, 2–3 lines. In DOCX it does not cross the photo; see §9.
  - Subtitle: Inter 11 pt `#CFE8E1` (6.25:1), max width 84 mm.
  - Dots at x 22, y 172.
- **Vertical hairline**: x 12 mm, y 20–277, 0.5 pt `#2E8C80`, with rotated label "CLIENT · OCTOBER 2026" at 7 pt caps `#CFE8E1`.
- **Meta block**: bottom-left at y 262–280 (date, client, confidentiality), label style.
- **print-light**: white ground; Slab A and the photo remain; title in `#005A58`.

### R2 — Contents (white)
- **Frame**: page frame with rail. **Top-right tab slab**: x 182–210, y 0–90 mm, ramp (4% coverage).
- **Header**: label "CONTENTS" at y 30. H1 "Contents" 30 pt `#005A58` at y 36–50, dots right of the title on its centre line (slide 1 placement).
- **Entries** start at y 72, as table rows 14 mm tall:
  - Number "01" in Montserrat Bold 20 pt `#10906F` (large, 4.01).
  - Title in Montserrat SemiBold 12 pt ink.
  - Page number right-aligned in Montserrat SemiBold 10 pt `#005A58`.
  - Optional 1-line description: Inter 8.5 pt `#5B6270`.
  - Hairline 0.5 pt `#CFE0DC` under each row.
- Column widths 18 / 128 / 20 mm. Up to 12 entries.

### R3 — Section opener / break page (dark; the "Breakslide" page)
- **Full version (dark)**: four full-bleed **columns** (slide 3) at x 0–57 / 57–103 / 103–155 / 155–210 mm (27/22/25/26%), shaded ramp / ground / ramp / ground.
- The columns are split into three table rows:
  1. y 0–150: columns. Section number "02" in Montserrat ExtraBold 110 pt `#23B582` sits in column 2 (ground) at y 40. The figure is the large-text exception, 3.07:1.
  2. y 150–215: one **merged cell shaded `#043637`** that interrupts the columns like a band. It holds the H1 at 30 pt white (13.22:1) at x 22, plus the dots.
  3. y 215–295: columns again. A 1–2 sentence lede in Inter 11/16 `#CFE8E1` sits in a merged cell across columns 1–3, shaded `#005A58`. In that row the ramp only shows in column 4.
- **print-light** (slide 5 grammar, 37% coverage): columns only in y 0–110 mm over white; number, title and lede below on white in `#005A58` / ink.
- Use one per major section, and only when there are ≥ 3 sections.

### R4 — Executive summary / KPI (white with top band)
- **Band**: deep `#005A58`, y 0–52 mm (17.5% coverage; slide 4 used 36%, halved for print). Label "EXECUTIVE SUMMARY" `#CFE8E1` at y 18. H1 28 pt white at y 24–38. Dots right-aligned at x 179–192, on the title's centre line.
- **KPI step** (the straddle, done natively): a 4-column table with 6 mm gaps.
  - Row 1 (y 52–60): KPI cells `#10906F`, gap cells `#005A58`, so the band "steps down" into each tile.
  - Row 2 (y 60–98): KPI cells tint `#E6F2EF`. Each holds a numeral (Montserrat Bold 32 pt `#005A58`, 7.03 on tint), a unit, and a 2-line caption (Inter 8.5 pt ink).
  - Tile width (166 − 3×6)/4 = 37 mm.
- **Body** from y 112: summary text in two 79 mm columns, Inter 9.5/14.5. Then a "Key findings" list: each item is a 3.2 mm dot (the `#19816A` dot) + H3 + 2 lines.
- **Rail**: none on this page; the band replaces it.

### R5 — Narrative text (white; workhorse)
- **Frame**: page frame with rail.
- **Heading block** at y 30–58:
  - Label "SECTION 02 · MARKET" (7.5 pt caps `#19816A`).
  - H1 26 pt `#005A58`, ≤ 2 lines, with an optional *italic* second line (slide 2 move).
  - Dots on a line of their own under the H1 (slides 6/9 placement), 4 mm gap.
- **Columns**: body in the 112 mm main column at 9.5/14.5, ≈ 68–72 characters per line; H2 14 pt with 10 pt space before. The side column (46 mm) holds pull-quotes (Montserrat SemiBold 12 pt `#005A58`, with a 3 mm `#23B582` bar above), definitions and source notes (Inter 8 pt `#5B6270`).
- **Callout**: full-width (166 mm) tint `#E6F2EF` box, 8 mm padding, label + 10 pt text, left border 3 pt `#10906F`.
- No dark panels on narrative pages.

### R6 — Chart page (white)
- **Header**: label + H1 or H2 at y 30–48.
- **Chart**: matplotlib PNG at 300 dpi, 112 × 85 mm in the main column.
  - Bars use the ramp `#CFE8E1` / `#57BA96` / `#10906F` / `#005A58`, with the current year deepest.
  - No gridlines except a 0.5 pt baseline; direct value labels in Inter 8 pt ink; axis labels in Inter 7.5 pt `#5B6270`.
- **Insight slab** (slides 1 and 8 text-on-dark, scaled down): the side column (46 mm × 85 mm), shaded `#005A58`. It holds the label "WHAT IT MEANS" `#CFE8E1`, a 12 pt white takeaway, and a 4 mm `#23B582` cap row on top (the step). Coverage ≈ 6%.
- **Caption**: under the chart, "Figure 2.1 —" label + Inter 8 pt `#5B6270`, and a source line.
- A second chart or a table can follow lower on the page.

### R7 — Table (white)
- **Header**: label + H2 + dots above the table.
- **Table**: full content width, 166 mm.
  - Header row: shaded `#005A58`, labels in Montserrat Bold 7.5 pt caps +25% white (8.07), height 9 mm, cells padded 2.5/3 mm.
  - Body rows: Inter 9 pt ink at about 7.5 mm per row, bottom border 0.5 pt `#CFE0DC`; no vertical rules.
  - First column in Inter SemiBold (or Montserrat Medium 9 pt). Numbers right-aligned.
  - Highlight row: tint `#E6F2EF` with a left border 3 pt `#10906F`.
  - Total row: top border 1 pt `#005A58`, bold.
- **Note**: Inter's tabular figures need the OpenType `tnum` feature, which python-docx cannot switch on, so figure alignment may be proportional [uncertain]. Right-align columns and use the same decimals throughout.

### R8 — Team / people (white with band; slides 4 and 3)
- **Band**: deep `#005A58`, y 0–62 mm. H1 white at y 24, dots right.
- **Portrait strip** (rendered as **one PNG**, 166 × 62 mm at x 26, y 40–102): three portraits, 46 × 58 mm each, with 14 mm gaps. Each has a **6 mm chamfer top-right**. The strip's top 22 mm is filled `#005A58` so the photos straddle the band edge.
- **Per person, below the strip**:
  - Name: Montserrat Regular 13 pt `#005A58`. Do not use the board's light teal.
  - Role: label 7 pt caps `#5B6270`.
  - Bio: Inter 8.5/12 `#5B6270`, 4 lines max.
  - Native table, 3 columns × 46 mm.
- A second row of three people fits at y 190–280, without the band.
- **Leader / foreword variant** (slide 2): a 50/50 split is too ink-heavy. Instead use a right column panel x 140–210 mm, full height, `#005A58`, holding name, role and signature in white. The letter itself goes on the white left side at 112 mm measure, with the cut-corner portrait at the top of the panel. Coverage 33%: use once.

### R9 — Services / capabilities / recommendations (white; slides 5 and 7)
- **Variant A (slide 5)**: top field y 0–105 mm.
  - Deep ground, or a green-graded photo.
  - Four ramp slabs, 28 mm wide, centred on the four columns below.
  - H1 white, with dots, at y 30.
  - **Four circle chips**, 24 mm diameter: `#005A58` fill, a 1.5 pt white ring and a white line icon. They straddle y 105, so the field + chips are one PNG.
  - Below, a 4-column native table (37 mm columns, 6 mm gaps) from y 125:
    - Label "01 · ADVISORY" in 7.5 pt caps `#19816A`.
    - H3 10.5 pt ink.
    - Inter 8.5/12 `#5B6270`, 6 lines max.
- **Variant B (slide 7)**, lower ink and better for long lists:
  - Left ramp panel x 0–52 mm, full height, with a darker strip x 52–60 `#005A58`.
  - Photo 46 × 90 mm, chamfered top-left, straddling the seam at y 60–150, with a stub slab.
  - Right list x 72–192: rows of an 8 mm line icon (`#005A58`) + label + H3 + 2–3 lines body, 22 mm per row, up to 8 rows.
  - Coverage ≈ 29%: once per report.
- **No-photo variant B**: the panel holds a large numeral or a pull-quote in white instead of the photo.

### R10 — Closing / back cover (dark)
- **Ground**: `#005A58`, with the slabs mirrored to the **left** (Slab A x 0–50, Slab B x 58–82 from y 150).
- **Text**: a thank-you or next-steps line in Montserrat SemiBold 24 pt white at x 100, y 90. Contact block in Inter 9.5 pt `#CFE8E1` at y 220–260. Dots at x 100, y 200. Legal or imprint text 7 pt `#CFE8E1` at the bottom.
- **print-light**: a white page with only Slab A, and text in `#005A58`.

### R11 — Appendix / references (white; extra)
- Page frame with rail, no tab slab.
- Two columns of 79 mm, Inter 8/11.5. Entry numbers in Montserrat Bold 8 pt `#19816A`, hanging indent 6 mm.
- Labels only, no dots in the heading. Pages with dense content should drop decoration first.

---

## 6. Signature components (build specs)

**C1 — Stepped slab (ramp slab)**
- *Board* [seen]: vertical rectangles 12–27% of the page width, gradient from bright top (`#23B582`/`#10906F`) to deep bottom (≈ ground). Heights are staggered, so one slab starts at the top edge and the next starts lower. Slabs bleed off the top and/or bottom edges and overlap photos and each other.
- *Spec* [inferred]:
  - Width 24–50 mm.
  - Ramp stops `#23B582` → `#10906F` → `#077060` → `#005A58` (top to bottom).
  - Neighbouring slabs differ in start-y by ≥ 40 mm.
  - At most 3 slabs per page; always vertical, never horizontal.
- *Native build*: a full-bleed table column whose rows are shaded in **3–4 flat steps** (each ≥ 25 mm tall). A flat stepped version replaces the gradient, which avoids gradient fills in DOCX.
- *Image build*: PIL linear gradient PNG at 300 dpi, sized exactly to the cell, with no margins.

**C2 — Cut-corner photo**
- *Board* [seen]: a single 45° chamfer on one **top** corner. The leg is ≈ 15–16% of the photo width: top-right on slides 2 and 10, top-left on slides 7 and 9. Slide 1 has no chamfer, so it is not universal.
- *Spec*:
  - Leg = 15% of width, min 5 mm, max 12 mm.
  - One corner per document: top-right by default; mirror to top-left for photos on the right-hand side of a seam.
  - Portrait ratio 1:2 for covers, 4:5 for people.
- *Build*: PIL. Crop to the ratio, then `ImageDraw.polygon` a mask, then fill the cut triangle with the **underlying colour** (white or `#005A58`) rather than leaving it transparent. That keeps it predictable in LibreOffice PDF export and in print. Insert inline at the exact width.

**C3 — Stub slab overlap**
- *Board* [seen]: a short slab, ≈ 35% of the photo width and 40–45% of its height, overlapping the photo's lower-left or lower-right corner. Its top corner is chamfered and it carries the ramp.
- *Build*: composite into the **same PNG** as the photo (DOCX cannot overlap reliably). Chamfer leg 4–5 mm, ramp `#10906F` → `#077060`.

**C4 — Three-dot marker**
- *Board* [seen]: three circles, equal diameter, gap ≈ 0.5 × diameter, coloured `#2E9B64`, `#19816A`, `#043637`. Placed on the title's centre line after the title, under the title, or straddling a seam.
- *Spec*: diameter 3.2 mm, gap 1.6 mm (12.8 mm total width). One per page, at the H1.
- *Report meaning* [inferred, new]: a **part indicator**. In part 1 dot 1 is `#23B582` and the others are `#CFE0DC` outlines; part 2 lights dot 2, and so on. This gives the motif a job. On deep ground, swap the third dot to `#CFE8E1`, because `#043637` on `#005A58` is only 1.64:1.
- *Build*: a tiny PNG (300 dpi, 12.8 × 3.2 mm) placed inline. A fallback is three "●" (U+25CF) runs in DejaVu Sans, coloured, 9 pt, tracking +2 pt; Montserrat may lack the glyph [uncertain].

**C5 — Service / list item**
- *Board* [seen]: line icon → tracked caps label → 2–4 lines body. On dark: white icon. On white: deep icon.
- *Spec*:
  - Icon 8 mm (Variant B), or a 24 mm chip (Variant A: deep fill, white 1.5 pt ring, white glyph).
  - Label 7.5 pt caps +25% `#19816A`; H3 10.5 pt; body 8.5–9 pt.
  - The label must carry real content ("01 · ADVISORY"), not "SERVICE 001".
- *Build*: a native 2-column table (icon cell 12 mm, text cell). Icons as PNGs rendered from an SVG icon set on npm: `lucide-static` 1.52.0 (ISC) or `@tabler/icons` 3.49.0 (MIT), both checked with `npm view`.

**C6 — Column band (break-page columns)**
- *Board* [seen, slide 3]: alternating ramp and ground columns at full height.
- *Spec*: see R3. A merged middle row interrupts the columns to hold the title.
- *Build*: native table. Shading is per cell, row heights are exact, the section has zero margins.

**C7 — Straddle (photo or chip across a band edge)**
- *Board* [seen, slides 4 and 5]: elements sit half on the dark band and half on white.
- *Build*: render band-bottom + elements + white as **one PNG strip** (image). The native approximation is the R4 "KPI step": a `#10906F` cell row that continues the band only under the tiles.

**C8 — Dark text panel**
- *Board* [seen, slides 1, 2 and 8]: white heading and body on `#005A58`.
- *Spec*: report use is limited to ≤ 60 words (insight slab, contact block). White 10–12 pt; body in `#CFE8E1`. No paragraphs longer than 3 lines.
- *Build*: native shaded table cell, padding 6–8 mm.

**C9 — Hairline with rotated micro-text**
- *Board* [seen, slide 10 cover, slide 3 footer]: a thin vertical line with tiny rotated text.
- *Spec*: cover only. 0.5 pt line, 7 pt caps label rotated 90°.
- *Build*: a narrow table column with a left border, with the text in a cell using `w:textDirection btLr`. The existing `reportkit.text_direction()` already does this.

**C10 — Slab rail (white-page carrier)** [inferred, derived from slides 2 and 7]
- *Spec*: see the page frame in §5 (deep 7 mm + bright cap 4 × 60 mm).
- *Build*: the rail must bleed and repeat on every page, so it is best as a **PNG anchored in the header behind the text** (`wp:anchor behindDoc="1"`, positioned relative to the page at 0,0). The alternative is a zero-margin first column of a page-sized table, but that breaks text flow across pages.

---

## 7. Photo dependency

The board is **highly photo-dependent**: all 10 slides carry at least one photo, 10.4% of pixels are near-black photo shadow, and the photos are colour-graded dark green (foliage, dim interiors). Without photos, the slabs carry the identity alone, which works because the slab ramp is the strongest single move. [seen / inferred]

| Layout | Needs photo? | No-photo fallback |
|---|---|---|
| R1 Cover | Yes (the hero overlaps the slabs) | Add a third slab (`#10906F`, x 96–118, y 40–297) and enlarge the title. Optionally replace the hero with a **giant cut-corner tint rectangle** (`#077060`, 72 × 144 mm) holding the year "2026" in ExtraBold 72 pt `#23B582` |
| R2 Contents | No | — |
| R3 Break | No (slide 3 uses photos, the spec does not) | Already photo-free |
| R4 Summary/KPI | No | — |
| R5 Narrative | Optional inline photo (112 mm wide, cut corner) | Pull-quote in the side column |
| R6 Chart | No | — |
| R7 Table | No | — |
| R8 Team | Yes (portraits) | Strip PNG with **initial chips**: 46 × 58 mm cut-corner tiles in `#E6F2EF` with initials in Montserrat SemiBold 28 pt `#005A58`. Or drop the strip: names in 3 columns with a 3 × 20 mm `#23B582` bar above each |
| R9 Services | Variant A: photo optional (deep ground works). Variant B: photo in the seam | Variant A: deep field with slabs only. Variant B: a large numeral ("4 priorities") or a pull-quote in the panel |
| R10 Closing | No | — |
| R11 Appendix | No | — |

Photo rules if used [inferred]:
- Grade all images toward the palette (mild green duotone or a −20% saturation shift toward `#005A58` shadows) so they sit with the slabs.
- Render at 300 dpi at final size.
- Use **real** project, site or people photos. Stock models (slides 2–4) undermine a report's credibility.

---

## 8. Best for / avoid for

**Best for [inferred]**
- **Report types**: impact or ESG reports, sustainability and environmental assessments, annual reviews (narrative-led), agency or consultancy capability statements, project portfolios, proposals and pitch documents, landscape, architecture and real-estate project reports, hospitality or wellness brand reports, foundation or NGO reports.
- **Industries**: environment, energy transition, agriculture/food, forestry, landscape, architecture, design studios, property, hospitality, wellbeing.
- **Tone**: calm, premium, eco-modern, confident, "brand" more than "audit".
- **Audience**: external (clients, investors, donors, the public). Read on screen or printed as a short run.
- **Length**: 8–40 pages, with 3–6 sections so the break pages have rhythm.

**Avoid for**
- Dense technical, scientific or engineering reports, and audit, legal or regulatory filings. The decorative slabs and dark pages read as marketing.
- Financial statements dominated by tables.
- Reports that will be **office-printed in volume**. Dark pages band, waste toner and curl paper; use print-light.
- Mono printing. Ramp steps are 1.3–1.5:1 apart, so they merge in grey.
- Crisis or incident reports and sombre topics. The mood is too lifestyle.
- Healthcare clinical documents (use E/F instead).
- Brands whose accent is not green. The system is a single-hue ramp, so recolouring needs a whole new 4-stop ramp and new contrast checks.

---

## 9. Do not copy

- **Placeholder content**: "Our Services" ×5, "Our Team" ×2, "SERVICE 001" on every item, lorem ipsum, "CREATIVE COMPANY". Headings must say something ("Emissions fell 18%"), and labels must be real category names.
- **Low-contrast text**: body `#CFCFCF` on white (1.56:1), names `#A1B1AE` (2.23:1), subtitle `#146E6C` on deep (1.34:1), the third dot on deep (1.64:1). All fail WCAG and vanish in print.
- **Tiny justified body**: produces rivers at report measures. Use ragged right at 9.5 pt.
- **Dark mode for reading pages**: long white-on-green text is tiring and expensive to print. Keep dark pages for cover, breaks and closing.
- **Wordmark crossing the photo**: in DOCX the title would have to be baked into the image, which makes it non-editable, non-searchable and inaccessible. Keep titles in live text beside the photo.
- **Gradient on every slab, every page**: becomes wallpaper. Use flat steps on content pages, with gradients (PNG) on the cover and break pages only.
- **Eco icon clichés** (recycling arrows, plant-in-hand, lightbulb, speech bubble): use icons that encode the actual content, or none.
- **Stock-model portraits and generic leaf photos on every page**: they signal "template". Monstera leaves are this board's cliché.
- **Dots as pure decoration on every slide**: give them a job (C4 part indicator) or use them only at H1.
- **The 50/50 dark split (slide 2)** as a repeated content layout: 50% ink per page for no informational gain.

---

## 10. DOCX implementability

Legend:
- **native** = tables, cell shading, borders, section breaks, exact row heights (python-docx + small OXML). Robust in Word and LibreOffice.
- **image** = rendered PNG placed inline in a cell. Robust.
- **anchored image** = `wp:anchor` floating PNG. Generally OK in LibreOffice, but test.
- **shape** = DrawingML/VML shapes. Fragile in LibreOffice: avoid.

| Component | Method | Notes |
|---|---|---|
| Full-bleed dark page (cover/break/closing) | **native** | Zero-margin section + page-sized table with exact row heights summing to ≤ 295 mm (as `reportkit.cover()` already does). Cell shading `#005A58` |
| C1 stepped slab, flat steps | **native** | Table columns, per-row shading in 3–4 steps |
| C1 stepped slab, true gradient | **image** | PIL gradient PNG in a zero-padding cell; set cell margins to 0 |
| C2 cut-corner photo | **image** | PIL mask, corner filled with the underlying colour |
| C3 stub slab over photo | **image** | Composite with the photo; true overlap is not native |
| C4 three-dot marker | **image** (preferred) / native text fallback | 12.8 × 3.2 mm PNG inline; or coloured "●" runs (glyph fallback risk) |
| C5 service list item | **native** + icon **image** | 2-column table; icon PNG |
| C6 column band break page | **native** | Merged middle row; exact heights |
| C7 straddle (photos/chips over band edge) | **image** (strip PNG) / native approximation (KPI step) | Never use floating shapes for this |
| C8 dark text panel | **native** | Shaded cell, padding via `tcMar` |
| C9 hairline + rotated text | **native** | Cell border + `w:textDirection btLr` (`reportkit.text_direction`) |
| C10 slab rail on every content page | **anchored image** in the header (behindDoc), or **native** zero-margin table per page | The anchored header image repeats automatically. Verify its position after LibreOffice conversion (render + `check_pdf.py`). If it drifts, fall back to a left page-border line: `w:pgBorders` left, 24 pt `#005A58`, offset from the page, which is native but cannot do the bright step |
| Top band (R4/R8) | **native** | First table row shaded, exact height, zero-margin section; or a section with top margin 0 and a band row |
| Charts (ramp bars) | **image** | matplotlib PNG at 300 dpi; palette = ramp |
| Data table (deep header, hairlines, highlight row) | **native** | Cell shading + bottom borders + left border on the highlight row |
| KPI tiles | **native** | Tint cells; numerals as text |
| Tracked caps labels | **native** | `w:spacing` on runs (`reportkit._track`) |
| Italic emphasis line in H1 | **native** | Second run in Montserrat SemiBold Italic |
| Circle chips (24 mm, ring + icon) | **image** | A circle is not native in tables |
| Wordmark overlapping photo | avoid (image would be needed) | Keep as live text beside the photo |
| Any free-floating rectangle/slab shape | **shape**: avoid | Fragile z-order and anchoring in LibreOffice. Use tables or PNGs |

---

## 11. Quick-select card

- **Name**: Breakslide (Ref B) — "Stepped Slab, dark break pages".
- **Mood**: calm, premium, eco-modern; dark green at the edges, white in the middle.
- **Accent**: deep `#005A58` (8.07:1) + ramp `#077060` / `#10906F` / `#23B582`; labels `#19816A` (4.78:1).
- **Best for**: ESG/impact, sustainability, architecture/landscape, agency capability or portfolio reports, 8–40 pages.
- **Needs photos?** Preferred for the cover and team pages (green-graded); every layout has a slab-only fallback.
- **Signature move**: tall vertical slabs with a bright-top ramp stepping across a cut-corner photo, plus the three-dot part marker.
