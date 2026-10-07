# Ref A: "Rapport annuel 2025" (navy annual report)

Source: `.claude/skills/report-design/references/images/ref-A.jpeg` (736 x 1104 px collage, 18 thumbnails).
Method: each thumbnail was cropped and upscaled 4x with PIL and viewed one by one. Colours are medians of sampled regions,
or the darkest or brightest percentile of each region for thin text. Geometry is measured as fractions of the detected page
rectangle and then converted to A4 (210 x 297 mm). The board is a photographed mockup, so the light pages read
as #E4E3E5 to #EBE9EA because of lighting. The JPEG is small, so body text is unreadable and fine detail is soft.
Tags: [seen] = visible in the image, [inferred] = deduced from what is visible, [uncertain] = a guess.

---

## 1. Identity

A two-tone corporate annual report: deep navy (#1A2E5F) on white, and almost nothing else. Navy is used as **whole pages
and full-height panels** (cover, back cover, contents, leader's message, outlook). It is never used as thin decoration. These navy pages alternate with
airy white pages where navy shows up only as heavy ALL-CAPS headings, solid icon discs and data marks. The recognisable moves are:
(a) a full-navy cover with a huge stacked caps title and **the year set in a lighter steel-cyan (#64A5C7)**, plus faint
arcs and diagonal facets in the background; (b) the **split page**, a navy panel with a white caps title and a short intro next to a
light content area or a photo; (c) **data in one hue only**: bars that fade from pale periwinkle to deep navy, a navy donut in 4 shades,
a vertical navy "stat rail" with stacked big numbers; (d) **centred KPI rows**, each with a navy disc icon, a large numeral, a two-line
grey caption and hairline dividers between items. The mood is calm, institutional and trustworthy, close to a bank, an insurer or an engineering group.
Type is one geometric sans in bold caps for titles and the same family in regular for text. There are no serifs, no rules under headings and no gradients
except inside the bars and the cover art.

---

## 2. Evidence (every thumbnail)

The spreads have aspect ratios of 1.35 to 1.48, against 1.414 for an A4 spread, so the rows of three are **two-page portrait spreads** [inferred].
The bottom two rows are smaller re-arrangements of the same pages and contain obvious template errors (see the notes), so they carry less weight.

Measured navy share per page = pixels within ΔRGB 30 of #1A2E5F.

| # | Thumbnail | What it shows | Navy share | Tag |
|---|---|---|---|---|
| 1 | **Front cover** (top left) | Full navy field. Title "RAPPORT / ANNUEL" in white bold caps on 2 lines; "2025" below in steel-cyan, larger than the caps; 2-line tagline in white regular; 3-word value list (Transparence / Engagement / Performance) bottom left in periwinkle. Background: a large faint circle arc, fine parallel diagonal lines top right, translucent diagonal facets lower right. All text is left-aligned on one axis at ~9.5% of page width. | 85% | [seen] |
| 2 | **Back cover** | Full navy. 3-line sign-off in white regular at mid-height ("Ensemble, construisons la confiance de demain."), a short white rule below it, concentric arc lines top right, a halftone dot grid fading in at bottom left, a white QR code bottom right with a 3-line right-aligned caption. | 90% | [seen] |
| 3 | **Mot de la direction** (row 1, left) | Left page full navy: white caps title (2 lines), 2 paragraphs of body in white, a row of 3 outline-circle icons with labels at the bottom. Right page light: executive portrait cut out inside a large circle arc, quote below it with a big navy “66” quotation mark and the quote in navy ~1.5x body size. | 39% | [seen] |
| 4 | **Notre mission et nos valeurs** | Light spread. Caps title in dark navy-black top left with an intro paragraph below it; a mountain photo with a navy flag fills the right page and bleeds across the gutter (no frame, the image fades into the page); along the bottom, 4 values, each a solid navy disc with a white line icon and a bold label. | 1% | [seen] |
| 5 | **Faits marquants de l'année** | Light spread. Caps title top left; 4 KPI columns spread across both pages: navy disc icon, large bold numeral (+18%, +250, 98%, +120), 2–3 line grey caption, all centred, thin vertical hairlines between the columns. Decoration: translucent navy and pale-blue rounded blobs bleeding off the top right, a halftone dot patch bottom left. | 8% | [seen] |
| 6 | **Aperçu financier** (row 2, left) | Split: a navy panel (~30% of the spread width) with a white caps title and intro text. Light area: a stacked list of 4 KPIs (navy outline line icon, small grey label, bold numeral such as "642 M€") on the left; a 5-bar column chart (2021–2025) on the right with value labels above, year labels below and a caption line under the axis. The bars fade vertically from pale to deep; the 2025 bar is the most saturated royal blue. A thin vertical axis line and a baseline; no gridlines. | 28% | [seen] |
| 7 | **Répartition des revenus** | Left page light: caps title, a donut chart in 4 navy shades (ring ≈ half the radius), legend on the right with a coloured dot, a bold % and a small grey label for each segment. Right page: a full-bleed greyscale architecture photo. | 2% | [seen] |
| 8 | **Notre portée mondiale** | Light spread. Caps title; a world map made of navy dots (halftone) across the left page and the gutter; a 2-line bold tagline below it; on the right, a thick vertical **stat rail** (top ~30% brighter royal #255B9C, the rest navy) with 3 stacked stats (bold numeral + small grey label). | 1% | [seen] |
| 9 | **Structure organisationnelle** (row 3, left) | Light spread. Caps title; org chart: one navy head box (white caps, 2 lines) centred, grey hairline connectors, 4 navy child boxes (same navy, not tinted) with white caps labels, a 3-item bullet list under each, hairline vertical dividers between the columns; a dot-grid patch top right. | 7% | [seen] |
| 10 | **Notre engagement RSE** | Left page light: caps title; 3 stacked items, each a mid-blue duotone line icon, a bold navy label and a 2-line grey description. Right page: a photo of hands holding a seedling, inset on a lighter mat (not full bleed). | 0% | [seen] |
| 11 | **Perspectives pour 2026** | Left page navy: white caps title, intro text, then 4 **step cards**. Each card is a light rounded rectangle with a circular number badge (01–04, white disc, navy ring) overlapping its top-left corner and a bold 2-line label. The 4th card crosses onto the right page, which is a full-bleed **navy-duotone mountain photo**. | 42% | [seen] |
| 12 | Sommaire (row 4, 1st) | **Contents**: full navy, "SOMMAIRE" in white caps, 10 entries in white regular with 2-digit page numbers in a column at about 60% of the panel width, no leaders. The executive portrait in a circular arc on the right with a short white quote below it. | 65% | [seen] |
| 13 | Mot de la direction, variant | Navy panel (~37%) with title and text, the mountain photo upper right, 3 navy-disc value icons on a light band below. Shows the same components re-arranged. | 31% | [seen] |
| 14 | Faits marquants, variant | Single light page, 4 KPIs in a row with dividers. Confirms the KPI component on its own. | 3% | [seen] |
| 15 | Structure, variant | Same org chart, smaller. | 5% | [seen] |
| 16 | Notre engagement RSE, variant (row 5, 1st) | Navy panel version: the same 3 icon items in white on navy, plus a full-height photo. Shows the panel works in both polarities. | 38% | [seen] |
| 17 | "Notre portée des revenus", variant | Light page: title, a paragraph, then **4 steps as solid navy discs with white numbers** (01–04) and bold labels below. No cards. The title is a template mash-up. | 1% | [seen] |
| 18 | Perspectives + closing (row 5, wide) | Left: the map + stat rail block (wrongly titled "Perspectives pour 2026"). Right: a **closing page**, full navy with faint facets and a dot grid, "Merci pour votre confiance." in white bold and a 2-line sign-off in regular, placed lower left. | 41% | [seen] |

Notes:
- **Not on the board** [seen as absent]: a data table, a narrative text page with long running text, footnotes or citations, running
  headers and footers, folios (page numbers on the pages), a timeline with dates, and an appendix. Every recipe for these below is [inferred].
- Thumbnails 17 and 18 have titles that do not match their content, which is typical of a template or AI collage [inferred]. Use them for components only.
- Body copy is greeked or unreadable everywhere. Paragraphs are short (4–7 lines) and sit under the title [seen]. The reference has no long-form reading pages.

---

## 3. Palette (measured)

Measurement notes: panel colours are medians of 20 to 60 px regions. Text colours are the median of the darkest 8% of pixels in a heading box, because anti-aliasing lightens small text.
Light pages measure #E4E3E5 to #EBE9EA, but that is white paper under mockup lighting [inferred], so the print ground is white.
Contrast is WCAG 2.x relative luminance, computed.

| Role | HEX | Where measured | Contrast on white | Contrast on navy #1A2E5F | Use |
|---|---|---|---|---|---|
| **Accent deep** (panel navy) | **#1A2E5F** | Panels #1A2F60 to #1D3364, covers #192B5C to #223360, pooled page median #182C5C | **13.13:1** | n/a | Panels, covers, head boxes, headings on white (AAA) |
| Accent deepest (discs, bar bottoms) | #142468 | KPI icon discs; bar and donut darkest #12265A to #0F2751 | 14.17:1 | 1.08 | Icon discs, darkest data series |
| **Accent bright** (royal) | **#2B4693** | Most saturated part of the 2025 bar; donut royal #183385 to #193B8A | **8.75:1** | 1.50 (do not put on navy) | The highlighted data series, small accents on white |
| Accent bright, lighter step | #255B9C | Top segment of the stat rail | 6.87:1 | 1.91 | 2nd data series, rail cap; also OK for text on white |
| **Highlight** (cover year) | **#64A5C7** | Brightest 10% of the "2025" numerals (overall median #5399BA) | **2.71:1** (fails for text on white) | **4.84:1** (AA on navy) | Only on navy: the cover year, big numerals on navy panels. Never as text on white |
| Periwinkle (text on navy) | #8FA0C8 | Cover value list, brightest pixels | 2.62:1 | 5.02:1 | Secondary text and labels on navy |
| **Tint mid** (data) | #7A94C0 | Bar tops; donut mid #5B77A8, light #8A9DB9 | 3.08:1 | 4.27 | Lighter data series, map dots (#5B6E9A, 5.07:1); fills only |
| Tint pale (fill) | #E8EDF7 | **Not measured, not seen** as a flat fill [inferred] | 1.17:1 | 11.18 | Zebra rows, callout ground, step-card fill on white |
| **Ground** | **#FFFFFF** | Mockup reads #E4E3E5 to #EBE9EA [inferred white] | n/a | 13.13 | Page ground |
| Surface (optional band) | #ECEBEE | Brightest light-page median | 1.19:1 | 11.05 | Optional cool-grey band or card; use sparingly |
| **Ink** (headings and body on white) | **#1B1D2E** | Darkest pixels of titles on light pages: #17192C to #1B1C2B | **16.64:1** | 1.27 | Titles on white are a navy-black, not pure black |
| **Secondary text** | **#5A5F6E** [inferred] | Captions measure #919092, but they are too thin to resolve; true value is likely darker | **6.37:1** | 2.06 | Captions, KPI labels, legend labels |
| White text on navy | #FFFFFF | Title white measures #ECF1FB | 13.13:1 (on navy) | n/a | All text on panels |

**Area share** (pooled over every page rectangle on the board, 18 thumbnails): navy (±30) **39.0%**, light ground **36.6%**,
photo and neutral greys **12.8%**, mid and bright blues (charts, icons, map, facets) **8.3%**, dark ink **3.3%**.
The light-to-dark split is almost 50/50, but by page it is bimodal: navy pages are 28–90% navy and light pages are 0–8% navy.
The rhythm, not an even spread, is what produces the balance.

**Palette rules**
- One hue family only. All data colours are shades of navy and royal blue; no second hue anywhere [seen].
- #64A5C7 and #8FA0C8 belong on navy. On white they fail AA for text (2.7:1 and 2.6:1).
- Data ramp, deep to light, for up to 4 series: `#12265A, #2B4693, #5B77A8, #8A9DB9` (adjacent steps differ clearly in lightness) [seen as the donut].

---

## 4. Typography

**Observations** [seen]: a single sans family throughout. Titles are set in **bold (about 700) ALL CAPS**, a geometric grotesque with a near-circular O,
an R whose leg is straight and leaves from the bowl, a pointed A, and moderately wide caps. Lowercase is double-storey "a",
single-storey "g", flat-topped "t" and a fairly large x-height. Numerals are lining with a flat-based 2. Body text and taglines are regular, and KPI numerals are bold.
Caps tracking is about normal (0 to +2%) and title leading is tight: the two cover lines step at 1.0x the cap size.

**Best-guess family** [uncertain]: a commercial geometric grotesque in the Gilroy / Avenir Next / "Mont" class.

**OFL substitute** (compared side by side against the cover crop):
- **Figtree 700** (`@fontsource/figtree`, OFL-1.1, v5.3.0 on npm) is the **closest**: matching straight-leg R, round O, similar lowercase and x-height.
  Use it for both headings and body (400). Fontsource ships only .woff/.woff2. Convert to TTF for LibreOffice with fontTools
  (`TTFont(woff); f.flavor=None; f.save('Figtree-700.ttf')`, which works in this venv) and install it in `~/.fonts`.
- **Poppins 600/700** (`@fontsource/poppins`; TTF already installed in `/root/.fonts`) is the next best. It is more geometric and wider, with a rounder "a".
- Montserrat 600/700 (installed) is too wide and makes long report titles overflow.
- Body alternative: Inter 400 (installed) if Figtree body text reads too round at 9.5–10pt.

**Roles and sizes.** Measured fractions of page height are converted to A4. The pt values in the recipes are the recommended print sizes.

| Role | Measured on board | A4 equivalent | Recommended (pt) | Case / colour |
|---|---|---|---|---|
| Cover title | cap height 6.9% H, line pitch 10.1% H, width 55–60% W | ≈ 20.5 mm cap, about 84 pt | **72–84 pt / leading 1.0**, max 3 lines in 125 mm | CAPS, white, bold |
| Cover year / issue | numeral height 9.5% H | about 110 pt | **96–110 pt** | Highlight #64A5C7 on navy, bold |
| Cover tagline | 2 lines, pitch about 4% H | about 18–20 pt | **18 pt / 26 pt** | Sentence case, white, regular |
| Cover value list | 3 lines, pitch 2.7% H (8 mm) | about 12 pt | **11 pt / 22 pt** | Title case, #8FA0C8 |
| Feature/section heading | cap height 4.0–4.3% H, top at 10–11% H, 2 lines | about 48–52 pt | **36–44 pt / 1.1**, wrap to 2 lines | CAPS, bold; white on navy, ink #1B1D2E on white |
| Page heading (text pages) | not on board | n/a | **24–26 pt / 1.1** | CAPS, bold, ink |
| Sub-heading | KPI/RSE labels | n/a | **12–13 pt bold** | Sentence case, navy #1A2E5F |
| Body | greeked; ~4–7-line blocks | n/a | **9.5–10 pt / 15 pt** | Regular, ink; white on navy |
| KPI numeral | about the same height as the heading | about 40–48 pt | **30–36 pt** (row), **24 pt** (stacked list) | Bold, ink or navy |
| Caption / KPI label | small grey, 2–3 lines | n/a | **8.5 pt / 11 pt** | Sentence case, #5A5F6E |
| Quote | ~1.5x body, navy | n/a | **15–16 pt / 22 pt** + 48 pt quote mark | Navy |
| Labels in boxes (org) | tiny caps white | n/a | **8 pt bold caps, +4% tracking** | White on navy |

Caps usage [seen]: **every** page title and the org-box labels are caps. Nothing else is: body, captions, taglines and step labels are sentence case.
Titles are always on 2 lines, broken by meaning ("FAITS MARQUANTS / DE L'ANNÉE"). There are no kickers or eyebrow labels above titles.

---

## 5. Layout recipes, A4 portrait (210 x 297 mm)

**Global grid** [inferred from measurements]: the left text axis on the board is 9.5% W (cover) and 12–13% W (inner pages), i.e. 20–27 mm.
For a report use **L 22 / R 20 / T 24 / B 20 mm**, giving a content width of 168 mm on a 12-column grid with 4 mm gutters (column 10.3 mm).
The **navy panel is 70 mm wide** (one third, full bleed left, full height), and next to it the content runs from 82 to 190 mm (108 mm).
Titles start at y = 28–32 mm, matching the measured 10–11% H. Folios at 7.5 pt, #5A5F6E, bottom outer corner at y = 285 mm
[inferred; the board has no folios]. Navy pages carry no header or footer.

### 5.1 Cover (full navy) [seen]
- Page: navy #1A2E5F full bleed. Optional background art PNG at 210 x 297 mm: a faint large circle (r ≈ 150 mm, centre around (75, 150) mm, fill 4% lighter navy),
  3–6 hairline diagonals top right (#2B4693 at 40%), one translucent facet lower right.
- Title block left edge x = 20 mm. Title cap top y = 69 mm (23% H), **80 pt caps white**, leading 1.0, 2–3 lines, width ≤ 125 mm.
- Year/issue line right under the title (cap top ≈ 129 mm, 43.5% H): **104 pt #64A5C7**. If the report has no year, use the edition or a short code word.
- Tagline at y ≈ 171 mm (57.6% H): **18/26 pt white regular**, ≤ 2 lines, ≤ 100 mm wide.
- Value list or meta (client, date, author) at y ≈ 242–258 mm: **11/22 pt #8FA0C8**, 3 lines. For a real report put the metadata here.

### 5.2 Back cover [seen]
- Full navy, with the dot-grid PNG bottom left (0–90 x 200–297 mm, dots 0.6 mm on a 2.5 mm pitch, opacity fading upward) and concentric arcs top right.
- Sign-off at x = 22 mm, y = 119–140 mm: **18/30 pt white regular**, 3 lines max; a white rule 28 x 0.75 pt at y = 157 mm.
- Bottom-right block at x = 158–179 mm, y = 235–262 mm: a QR code (21 mm) **only if there is a real URL**. Otherwise use organisation name, address and URL,
  **8/11 pt white, right-aligned** to x = 179 mm.

### 5.3 Contents ("Sommaire") [seen, as a navy page]
- Variant A, full navy (as seen): title "CONTENTS" at x = 22, y = 30 mm, **40 pt caps white**. The list starts at y = 70 mm and is a 2-column table
  (titles 110 mm, numbers 14 mm, left-aligned at x = 140 mm), **11/16 pt white regular**, numbers in **#8FA0C8, 2-digit (02, 04)**, row pitch 9 mm,
  section entries bold and sub-entries regular and indented 6 mm. No leader dots. The right column (x 150–210) takes an optional portrait or quote, or is left empty.
- Variant B, split (for long contents of 15+ entries): navy panel 0–70 mm with "CONTENTS" in white 36 pt plus a 2-line intro. The list sits on white at x 82–190 in ink,
  with numbers in #2B4693.

### 5.4 Section opener / break page [seen as split pages and the closing page]
- Navy panel 0–70 mm, full height. Inside it (x 14–60 mm): a **section number "01" at 60 pt #64A5C7** at y = 40 mm,
  the **title 36 pt caps white** at y = 70 mm (2–3 lines), then a 3–5-line lede, **10/15 pt white**, at y ≈ 120 mm.
- Right area (70–210 mm): a full-bleed photo (cover-cropped, optionally navy duotone), **or** without a photo, the **"In this section"** list
  (3–5 items, 13 pt bold navy + 9 pt grey descriptions) at x 82–190, y 40 mm, plus one hero KPI (36 pt) near the bottom.
- Alternative full-navy break page: one sentence at **28/36 pt white**, x = 22, y = 130 mm, ≤ 140 mm wide. Use it every 4–6 pages at most.

### 5.5 Executive summary / KPI page [seen: Faits marquants + Aperçu financier]
- White page. Title **36 pt caps ink**, 2 lines, x = 22, y = 28 mm.
- Lede 11/16 pt, 120 mm wide, at y = 62 mm.
- **KPI row** at y = 95–150 mm: 4 columns of 42 mm (or 3 of 56 mm), centred inside each column. Icon disc 14 mm, then 4 mm, then numeral **32 pt bold ink**,
  then 2 mm, then caption **8.5/11 pt #5A5F6E**, ≤ 3 lines. 0.5 pt #D5D8E0 vertical dividers between columns, inset 6 mm top and bottom.
- Below, from y = 165 mm: 3–5 key findings in a 2-column grid (82 mm each), each a 12 pt bold navy heading and a 9.5/14 pt body. Optionally, a navy band at the page bottom
  (y 250–297, full bleed) holding the single conclusion sentence in **14 pt white**.

### 5.6 Narrative text page [inferred: not on the board]
- White, margins as above. Running header: nothing at top. Folio bottom outer.
- Page title **24 pt caps ink** at y = 28 mm (if the page starts a topic). H2 **13 pt bold navy**, 10 pt space before.
  Body **10/15 pt ink**, a single 168 mm column, or 2 columns of 82 mm for dense text.
- **Side-rail variant**, which carries the reference's split look onto text pages: a 46 mm left column at x 22–68 holds the H2 (13 pt bold navy), pull-figures
  (24 pt bold navy + 8.5 pt caption), and notes; body runs at x 76–190 (114 mm, about 75 characters per line, which reads well).
- Pull quote (5.10/6.7): a 48 pt navy quote mark plus 15/22 pt navy text, max one per spread.

### 5.7 Chart page [seen: Aperçu financier, Répartition, Portée mondiale]
- Variant A, split: navy panel 0–70 mm with title (36 pt white caps) and a 4–6-line lede. On white at x 82–190: a **stacked KPI list** at the top (y 30–110, 2 x 2 or 1 x 4;
  navy outline icon 8 mm, label 8.5 pt grey, numeral 24 pt bold ink), then a **chart PNG 108 x 110 mm** at y 125–235, then a source line at 7.5 pt grey.
- Variant B, white: title 36 pt at the top; a chart at full width 168 x 100 mm; below it, the legend and a 2-column interpretation (82 mm each).
- Variant C, donut + legend: donut Ø 70 mm at x 22–92; the legend to its right at x 104–190 (dot 3 mm, % in 16 pt bold ink, label 8.5 pt grey, row pitch 14 mm).
- Variant D, stat rail: a 6 mm wide vertical bar at x = 150, y 80–200 mm (top 30% #255B9C, the rest #1A2E5F), with 3 stats to its right at x 160
  (numeral 24 pt bold, label 8.5 pt grey). The left of the page holds a figure or map.

### 5.8 Table page [inferred: no table on the board]
- White. Title 26–36 pt caps ink. Table at 168 mm width.
- **Header row**: fill #1A2E5F, **8 pt bold caps white, +4% tracking**, 3 mm vertical padding. Body rows: 9 pt ink, 2.2 mm padding,
  **zebra #E8EDF7** on alternate rows, no vertical rules, a 0.5 pt #D5D8E0 bottom border on each row, and a 1 pt navy rule under the last row.
- Numbers right-aligned with tabular figures (Figtree has `tnum`, but LibreOffice may ignore OpenType features in DOCX, so right alignment is what keeps the columns legible).
  The highlighted column or total row is bold #2B4693.
- Optional left panel version for appendix tables is **not recommended**, because it wastes 70 mm of table width.

### 5.9 Org / structure page [seen]
- White. Title 36 pt caps at y = 28 mm. Optional intro at y = 62.
- Head box: 60 x 16 mm, centred at x 75–135, y 85 mm, fill navy, **9 pt bold caps white, 2 lines, centred**.
- Connector: 0.75 pt #A7AEBD. A vertical drop of 6 mm, a horizontal bus across the child centres, and 6 mm drops into the children.
- Children: 4 boxes of 38 x 11 mm (gap 5.3 mm across 168 mm) at y = 113 mm, **the same navy fill**, 8 pt bold caps white.
- Under each child: 3–5 bullets, 9 pt ink, a "·" bullet in navy, 1.5 mm indent; 0.5 pt #D5D8E0 vertical dividers between the columns from y 130 to 180.
- For more than 4 units, use 2 tiers or switch to a table (unit / lead / remit).

### 5.10 Steps / roadmap page [seen: Perspectives pour 2026 + the disc variant]
- Variant A, navy (as seen): navy panel full width at y 0–150 mm, or full page. Title 36 pt white caps at y = 28, lede 10/15 white at y = 62.
  **4 step cards** at y = 100 mm: each 38 x 40 mm with a white fill (on navy) and an 18 pt bold number "01" in a 12 mm white disc with a 1 pt navy ring,
  overlapping the card's top-left corner by 6 mm; label **11 pt bold ink**, 2 lines; optional 8.5 pt description.
- Variant B, white (disc steps): 4 navy discs Ø 14 mm with **14 pt bold white numbers**, centred over 42 mm columns at y = 100 mm, a 0.75 pt #A7AEBD line joining the discs
  [inferred: no line was seen, but it helps read sequence], a 11 pt bold ink label below and a 9 pt grey description.
- For a dated roadmap, add a 8 pt bold #2B4693 date or quarter above each label.

### 5.11 Closing page [seen]
- Full navy (or navy panel over the bottom 50%). "Thank you" or the key takeaway sentence in **26 pt bold white** at x = 22, y ≈ 190 mm.
  Then a 2-line sign-off, **13/19 pt white regular**, 6 mm below it. Faint facet/dot-grid art in the top right.
  For a report, use this page for "Next steps / Contact": 3 contact lines at 9 pt #8FA0C8.

### 5.12 Leader's message / foreword [seen: Mot de la direction]
- Navy panel 0–110 mm (a heavier split than other pages, as seen) with the title 36 pt white, the letter 10/15 white (max about 250 words), and the signature line 9 pt #8FA0C8.
- Right 110–210 mm: a portrait in a circular crop Ø 90 mm at y 30–120, then the pull quote (48 pt navy quote mark, 15/22 pt navy) at y 150–220.

---

## 6. Signature components (build specs)

1. **Navy panel / split page**. A full-bleed column 70 mm (standard) or 110 mm (foreword), full height, #1A2E5F; inner padding 14 mm left, 10 mm right;
   text in white. It always holds the page title and intro, never data tables. Pair it with a white content area or a photo.
2. **Caps title**. Bold caps, 2 lines, leading 1.1, ink #1B1D2E on white or white on navy. No rule, kicker or underline. Left-aligned at the text axis.
3. **KPI row**. 3–4 equal columns, centred content: 14 mm navy disc (#142468) with a white 1.2 pt line icon, then the numeral 30–36 pt bold, then the caption 8.5 pt grey on ≤ 3 lines.
   0.5 pt #D5D8E0 vertical dividers between the columns. No boxes, cards or shadows.
4. **Stacked KPI list**. Rows of an 8 mm navy outline icon, a label 8.5 pt grey above, and the numeral 24 pt bold below, with 10 mm between rows.
5. **Column chart** (PNG). 4–6 bars, width = 55% of the slot, **each bar a vertical gradient** from #7A94C0 (top) to #172F66 (bottom); the latest or highlighted bar
   runs #2C4C95 to #1D3460. Value labels above the bars 8 pt ink, category labels below 8 pt grey, one 0.5 pt grey baseline and one thin vertical axis line, **no gridlines, no y tick labels**.
   Caption centred below, 7.5 pt grey. A flat-fill fallback (no gradient) is the ramp #8A9DB9 → #2B4693 by recency.
6. **Donut** (PNG). Inner radius 0.52 of the outer; segments clockwise from 12 o'clock, largest first, in `#12265A, #2B4693, #5B77A8, #8A9DB9`; 1 pt white separators;
   legend to the right with a dot, a % in 16 pt bold and a label in 8.5 pt grey. No labels on the ring.
7. **Stat rail**. A vertical bar 6 mm x 110–130 mm; the top 30% #255B9C and the rest #1A2E5F; 3 stats stacked to its right, aligned with the bar's thirds.
8. **Org chart**. A navy head box, navy child boxes (not tinted), hairline grey connectors, bullet lists below, dividers between columns (see 5.9).
9. **Steps**. (a) Light rounded cards (r ≈ 2 mm) with a ringed number badge overlapping the top-left, on navy; (b) solid navy discs with white numbers on white. Always 3–5 steps, numbered "01".
10. **Icon disc**. A solid navy circle with a white single-weight line glyph (Lucide- or Tabler-style), always the same size per row. On navy: a white 1 pt ring with a white glyph.
11. **Quote**. A 48 pt navy "“" quote mark (bold, set tight), the quote in 15/22 pt navy regular, max 3 lines; beside or below a circular portrait.
12. **Cover art**. One large faint circle arc, a few hairline diagonals and translucent facets, all within 4–10% lightness of navy. It must stay subtle, because the type carries the cover.
13. **Dot-grid texture**. Halftone dots (0.6 mm, 2.5 mm pitch) in a corner patch about 60 x 60 mm, white at 15–25% on navy or navy at 10–15% on white. Use at most one per page.
14. **Dot-matrix map** (PNG). A world or region map rendered as navy dots (#5B6E9A to #1A2E5F) on white, with a 2-line bold caption below it.

---

## 7. Photo dependency

| Layout | Photo on board | Needed? | No-photo fallback |
|---|---|---|---|
| Cover | No (abstract navy art) | No | n/a, already photo-free |
| Back cover / closing | No | No | n/a |
| Contents | Portrait + quote (right) | Optional | Leave the right column navy; or show the 3 headline KPIs there in white (numerals in #64A5C7) |
| Leader's message | Circular portrait | Yes (seen) | Replace the portrait with an oversized quote mark and the quote at 20 pt navy; or a signature block plus a key KPI |
| Mission & values | Hero landscape | Yes (seen) | Make the top half a **navy band** (y 0–140) with the mission statement at 22 pt white; the values row stays below on white |
| Section opener | Photo right of panel | Optional | "In this section" list plus one hero KPI (5.4); or the cover-art PNG cropped to the area |
| Chart page (donut) | Architecture photo | No | Interpretation text and a stacked KPI list in the freed area |
| RSE / topic page | Seedling photo | Optional | A 2-column grid of the icon items with longer descriptions; or a pale-tint #E8EDF7 panel holding a pull figure |
| Steps / roadmap | Duotone mountain | Optional | Navy panel full width; cards sit fully on navy; the bottom third white with milestones or dates |
| KPI, financial, map, org, table, narrative | None | No | n/a |

About 6 of 18 thumbnails depend on photos, and **every one of them works without a photo** if the photo is replaced with navy area or a tint panel.
If photos are used, apply a navy duotone (multiply #1A2E5F, or a greyscale image tinted toward #2B4693) so they belong to the palette, as the outlook spread does [seen].

---

## 8. Best for / avoid for

- **Best for**: annual and activity reports, CSR/ESG reports, investor or board updates, corporate profiles, institutional and public-sector
  reports (ministries, agencies, foundations), consultancy summaries for finance, insurance, energy, engineering and logistics clients, and grant and impact reports.
- **Tone**: sober, confident, trustworthy, "establishment". Audience: executives, boards, shareholders, funders, regulators, the general public.
- **Length**: 8–40 pages. It is strongest when the content is KPI-heavy with short text blocks. Above 40 pages, use the side-rail narrative variant and keep navy pages to openers.
- **Avoid for**: academic or long analytical papers that are text- and footnote-heavy (navy panels waste measure), creative or youth brands (too corporate),
  healthcare or wellbeing (a cold navy reads as bank-like, so a teal or aqua ref fits better), urgent or alert documents, and anything printed on office printers in quantity
  (heavy navy coverage costs toner and bands). Avoid it too where the client's brand colour is not blue: the system only works as a monochrome scheme, so swap the whole ramp, not just one colour.

---

## 9. Do not copy

- **Stock-photo clichés**: the arms-crossed CEO, the mountain with a summit flag, the seedling in cupped hands, the glass-facade "architecture" shot. These are signals of a purchased template, and a real report needs its own imagery or none.
- **The QR code** on the back cover, unless there is a real URL to link to.
- **Translucent glossy blobs** (Faits marquants, top right) and **lens-flare diagonals**. They are template decoration that dates fast and needs DrawingML or transparency; keep the cover art very faint or drop it.
- **Icon discs on everything**. On the board, icons sit above KPIs, values, RSE items and panel footers. Use them in one component per page at most, never as bullet replacements.
- **Value-word triplets** ("Transparence / Engagement / Performance") and fluffy taglines. Replace them with real metadata (client, date, version).
- **Huge titles on every page**. A 48–52 pt equivalent works for 2-word French titles; real report headings are longer, so cap at 36–44 pt on feature pages and 24–26 pt on text pages.
- **Greeked or very short body copy**, which fakes airiness. Real narrative pages need the side-rail or two-column recipe (5.6).
- **Mismatched titles** and duplicated spreads (thumbnails 17 and 18), which are collage artefacts.
- **The dot-matrix world map with no data behind it**. Only use a map when geography is part of the message.

---

## 10. DOCX implementability (python-docx + LibreOffice)

| Component | Method | Notes / difficulty |
|---|---|---|
| Full-navy cover / back / closing / contents page | **Native**: a zero-margin section and a 1-cell table shaded #1A2E5F with exact row heights totalling **≤ 295 mm** | The existing `reportkit.cover()` already does this with row heights 60+155+80 = 295 mm. Above 295 mm, LibreOffice pushes the mandatory trailing paragraph onto a blank page; make that paragraph 1 pt. Cover art goes in as an inline PNG in the cell or as an anchored image behind the text (see below). |
| Cover art, dot grid, facets | **Image** (PNG rendered with PIL/matplotlib at 300 dpi) | Either as the cell content or anchored `behindDoc` in the section header so it repeats across the section; header-anchored images render in LibreOffice but need testing, so it is moderate risk. |
| Navy panel / split page (70 mm left) | **Native**: a zero-margin section, a 2-column table [70, 140 mm], the left cell shaded, exact row height ≤ 295 mm, cell padding as margins | Content in the right cell cannot flow to the next page. Use it for one-page layouts only (openers, KPI, chart pages). A panel repeated on flowing pages needs a header-anchored PNG strip (image, moderate risk). |
| Caps titles, body, captions | **Native** styles; `w:caps` or uppercase text; Figtree TTF installed | Fonts must be installed as TTF before rendering. Check embedding with `pdffonts`. |
| KPI row | **Native** table with no borders except left borders on cells 2–n (0.5 pt #D5D8E0); icon disc as an **inline PNG** (14 mm) | Easy. Render icon discs from Lucide/Tabler SVGs (npm `lucide-static`, ISC) → PNG with ImageMagick `convert`, which is installed. cairosvg and rsvg-convert are **not** installed. |
| Stacked KPI list / stat rail | **Native** table; the rail is a narrow 6 mm column split into 2 shaded rows (#255B9C / #1A2E5F) | Exact row heights keep the rail continuous. Easy. |
| Column chart with gradient bars, donut, dot map | **Image** (matplotlib PNG; gradients via `imshow` clipped to the bar patches) | Gradients are impossible natively. The dot map needs coastline data: none is bundled (no cartopy); use a pre-made world bitmap sampled to a dot grid, or skip it. |
| Org chart | **Native but fiddly**: a table with navy cells for boxes and connector rows drawn with cell top and side borders. **Image** is more robust | Connector alignment across merged cells is brittle in LibreOffice. A matplotlib PNG is recommended for more than 4 children. |
| Step cards (square) and disc steps | **Native**: shaded cells; the number disc as an inline PNG or bold text in a cell | Easy if square. |
| Rounded cards, overlapping badges, circular photo crops | **Shape** (DrawingML `roundRect`, anchored, overlapping); **fragile in LibreOffice** | Avoid. Use square cells (r = 0) or render the whole steps row as one PNG. Pre-mask circular portraits with PIL (alpha PNG), which counts as an image. |
| Quote mark + quote | **Native** paragraphs (48 pt quote mark with negative after-spacing) | Easy. |
| Data table (navy header, zebra) | **Native** cell shading and borders; header-row repeat via `w:tblHeader` | Easy. Tabular figures are unreliable, so right-align. |
| Section openers / page rhythm | **Native** section breaks (NEW_PAGE) with per-section margins and headers | Navy pages need their own section (zero margins, no footer). |
| Photos with duotone | **Image** (PIL: greyscale, then a colour map from #12265A to #E8EDF7) | Easy. Full-bleed means a zero-margin cell. |
| Translucent blobs / overlapping transparent facets | Image only | Drop them (see 9). |

**Hard parts**: (1) full-bleed colour on pages whose text flows, because a table cell cannot break naturally across pages with a fixed height, so flowing pages must stay white;
(2) overlaps (badge over card, card over photo) are not native; flatten them into one PNG or drop them; (3) the ≤ 295 mm total row height rule against the blank-page overflow;
(4) the font: Figtree needs WOFF→TTF conversion and local install, or the layout falls back to a different face and reflows.

---

## 11. Quick-select card

- **Name**: Navy Annual (ref A, "Rapport annuel 2025")
- **Mood**: calm, institutional, trustworthy; corporate two-tone
- **Accent**: navy #1A2E5F (13.1:1) + royal #2B4693; highlight #64A5C7 on navy only; ink #1B1D2E
- **Best for**: annual, CSR/ESG, investor and board reports; KPI-heavy, 8–40 pages
- **Needs photos?**: No; every photo slot has a navy or tint fallback
- **Signature move**: full-navy cover and split pages with bold caps titles, plus one-hue data (gradient bars, centred KPI row with navy icon discs)
