# DESIGN.md: Report designs from the 7 reference boards

This file turns the seven Pinterest boards into **seven document designs** you can build, plus **H Spectrum**, a coordinated multicolour system for documents with several programmes or themes. Each design has measured colours, fonts and A4 page layouts in mm and pt, and is written for printed and PDF reports (DOCX or HTML), not slides.

Boards: `.claude/skills/report-design/references/images/ref-A … ref-G.jpeg`, the same files as the WhatsApp images in the repo root.
Evidence: every colour was measured from the image pixels and every contrast ratio was computed. Font names are best guesses (the thumbnails are too small to be sure), so each one has a free OFL substitute. Pages the boards never show (data tables, long reading pages, appendices) are marked *(inferred)*.

**How to use this file**
1. Pick a design with §2.
2. Apply the rules every design shares (§3).
3. Build the pages from that design's section (§4 A–G).
4. Check the build notes (§5) and the checklist (§6).

---

## 1. What the boards have in common

All seven use the same approach: **one strong accent colour on a white page, carried by big blocks of colour**. The colour is not in thin borders or decoration. The type is bold sans-serif, the numbers are big, and photos are cropped hard and sit across the edge of a colour block.

| Ref | Board | Accent (measured) | Signature move |
|---|---|---|---|
| A | Rapport annuel 2025 | navy `#1A2E5F` (39% of page area) | Full-navy cover, 1/3 navy split panels, centred KPI row with icon discs, one-hue charts |
| B | Breakslide | forest `#005A58` (38%) | Dark green pages, tall vertical slabs stepping from bright to deep, chamfered photos, three dots |
| C | Business Plan | green `#5AB14D` (5%) + black | B&W photos in 45° rounded diamonds bleeding off the edge, giant green numerals, green/black alternation |
| D | Prism | teal `#379A86` (16%) | Rounded panels and pills holding text, caps titles with a raised teal dot, full-colour break pages |
| E | Clinicare | aqua `#4DCCD4` (6%) + tint `#E0FEFF` | Airy white, pale aqua tint bands, circle photos with a white ring across a colour edge |
| F | Docoro | royal `#053AA6` (17%) | Hard royal blocks bleeding off the page that photos and stat cards straddle, big Poppins numerals |
| G | Market | teal `#02A19A` (11%) | Hairline frame 10 mm in, a tag hanging off the top edge, a rotated pill tab, panels crossing the frame |

Only **A is a real report**. B–G are slide templates, so their slides are translated into A4 portrait pages below.

---

## 2. Which design to use

| Document | Use | Alternate | Why |
|---|---|---|---|
| Annual report, ESG / sustainability, grant or public-sector report | **A Navy Annual** | G | Formal, holds dense data, works without photos |
| Consulting deliverable, white paper, proposal, company profile, investor update | **G Market Frame** | A | Best reading pages, lowest ink, robust in Word |
| Business plan, pitch document, ops review | **C Leaf & Black** | G | The board already has the business-plan pages (SWOT, milestones, team, market) |
| Clinical / quality report, patient information, public health | **E Clinicare Aqua** | A | Calm and clinical; use A if it's dense and board-level |
| Healthcare services brochure, KPI-led health review (with photos) | **F Docoro Royal Block** | E | Bold, photo-led, big numbers |
| Marketing brochure, product or agency profile | **D Prism Rounded** | G | Friendly, expressive, shapes carry the identity |
| Portfolio / profile **in dark mode, on screen** | **B Forest Breakslide** | D | Only when dark is asked for; never for office print or long text |
| Impact, annual or city report with **3–5 programmes, services or themes**, where colour-coding helps readers navigate | **H Spectrum** (multicolour) | A | Each section owns one colour; the colours meet only on overview pages |

Hard rules:
- **No photos** → don't use B or F.
- **More than 40 pages, or more than 60% prose** → don't use B or D.
- **Office printing or strict accessibility** → don't use B.
- **A brand colour** changes the accent only, never the structure: keep the design's grid, motif and shapes, and swap the accent roles (§3.2).

For a scored decision with a page-by-page plan, run `python3 .claude/skills/design-picker/scripts/pick_design.py brief.json`.

---

## 3. Rules every design shares

### 3.1 Page and grid
- **A4 portrait, 210 × 297 mm.** Landscape only for tables with 8 or more columns.
- Margins of about 18–24 mm, with a 12-column grid and 4 mm gutters. Each design gives its exact values.
- Colour blocks and photos may **bleed** off the page edge. Text never does: keep at least 14 mm from the trim.
- Text measure is 60–75 characters (about 110–130 mm at 10 pt). Use a side rail of 30–46 mm for notes, pull-figures and quotes.
- Body text is **left-aligned and ragged right**. Never justify it, never centre it (centring is fine for team grids and KPI cells).

### 3.2 Colour
- **One accent hue per document** (except H Spectrum, which uses one hue *per section*; see §4.H), in four roles:
  - `accent`: fills, panels, slabs.
  - `accent_deep`: **all small accent text**, and panels that carry small white text. It must be at least 4.5:1 on white, ideally 7:1.
  - `accent_bright`: large fills, numerals of 24 pt and up, the chart highlight.
  - `accent_tint`: background panels.
- **The bright colours fail as text.** They are only for fills or large numerals:

  | Colour | Contrast on white |
  |---|---|
  | teal `#02A19A` | 3.2:1 |
  | green `#5AB14D` | 2.7:1 |
  | aqua `#4DCCD4` | 1.9:1 |

- Text **on** aqua or bright green fills is dark ink, never white. White text on bright teal needs 14 pt bold or larger.
- Neutrals: ink `#1F1F1F`, secondary `#5C5C5C` (6.7:1), rule `#BFBFBF`, hairline `#D9D9D9`. Grey bands must be at least 6% grey, or they vanish on office printers.
- `signal` (vermilion, about `#CE2E09`) is only for negative values. Green documents use raspberry `#C0318F` instead.
- **Brand swap:**
  - If the brand colour is at least 7:1 on white, it becomes `accent_deep` and a lighter shade is derived for fills.
  - If it is lighter than that, it becomes the fill, and a deep shade is derived at 7:1 for text.
  - The tint is the same hue at about 94% lightness.

### 3.3 Type
- One sans-serif family, or one heading face plus one body face. At most 4 weights.
- ALL CAPS only for titles and labels, with tracking: +3–5% on titles, +12–30% on small labels.
- Scale ratio about 1.33–1.5. Body 9.5–10 pt / 14–15 pt; captions 7.5–8 pt; labels 7–7.5 pt.
- Leading must be set in **exact points**. "Auto" leading makes Poppins, Montserrat and Inter lines about 50% too tall.
- Numerals are big and bold: KPI figures 26–36 pt, hero figures 44–60 pt. Captions sit under them in 8–8.5 pt, at most 2–3 lines.

### 3.4 Shared components (re-skin them per design)
- **KPI row**: 3–4 equal cells, each with a figure, a unit and a 2-line caption, and optionally an icon chip above. There are hairline dividers between cells and **no boxes around numbers** (except D's tiles and B's step tiles).
- **Chart**:
  - Single hue: light to deep shades of the accent, with the series or bar that carries the argument in the deepest step.
  - Direct value labels, no gridlines on bars, one baseline, no legend box.
  - Never pies in 3D, rainbows or shadows. A donut only for shares that add up to 100%.
- **Table**:
  - Header row in an accent fill with white bold caps labels, about 7.5–8.5 pt.
  - Body 8.5–9 pt, hairline row rules, no vertical lines, numbers right-aligned.
  - The total row is bold with a 1 pt accent rule above. Zebra rows or one highlighted column are optional.
  - The header repeats on every page and rows never split.
- **Callout**: tint panel, 3 mm accent bar on the left, caps label, 10–11 pt text. One per page.
- **Icons**: single-weight line glyphs (Lucide or Tabler) in white on a solid accent circle or rounded square. One icon style per document, never emoji.

### 3.5 Page rhythm
- **Colour pages** (cover, openers, break pages, closing) are at most 25% of pages, or 15% for office print.
- Never 3 identical layouts in a row, and at most 3 dense pages (text, table) in a row.
- An opener or break page is followed by at least 2 content pages, and openers or break pages are at least 3 pages apart.
- **Structure by length:**

  | Length | Structure |
  |---|---|
  | 8 pages or more | Contents page |
  | 9–20 pages | One opener per major section (2–4) |
  | Decision documents | Executive summary in the first 3 content pages |

### 3.6 Content → layout

| Content | Layout |
|---|---|
| 1–2 headline figures | Stat call-out in the text rail |
| 3–4 figures | KPI strip |
| 5–8 figures | KPI page in two rows |
| More than 8 figures | Table |
| Time series, up to 12 points, one series | Column chart, latest in deep accent |
| Time series, longer or 2–3 series | Line chart |
| 4 or more series | Table or small multiples |
| 2 options | Two blocks (A./B.) |
| 3–4 options with up to 4 attributes | Comparison columns |
| More attributes or exact numbers | Table |
| Parts of a whole, up to 5 | Donut or 100% bar |
| Parts of a whole, more than 5 | Sorted horizontal bars |
| Process, 3–5 steps | Numbered step tiles |
| Process, 6–8 steps | Two-column numbered list |
| Timeline, up to 6 events | Horizontal |
| Timeline, 7–12 events | Vertical |
| Timeline, more than 12 events | Table |
| Team, up to 4 people | Row |
| Team, 5–12 people | Grid |
| Team, more than 12 people | Table |
| Long text, more than 600 words | Reading page with rail |
| Long text, more than 1,500 words and no figures | Two columns |
| SWOT, up to 5 bullets per quadrant | 2×2 matrix |

### 3.7 Never do
- Gradient blobs, glassmorphism, drop shadows, 3D charts, rainbow palettes.
- Emoji or icon bullets in body text, walls of bullets, everything centred.
- Stock photos of handshakes, laptops or plants. Never invent a photo, figure or quote: use the design's no-photo fallback or a visible placeholder.
- Mixing designs. Use one motif, one corner style (square, cut or rounded, never two), one photo treatment (colour, B&W or duotone) and one accent.
- Copying the templates' small white text on bright colour, light-grey body text, or placeholder labels ("SERVICE 001", "WWW.EXAMPLE.COM").

---

## 4. The seven designs

Colour values below are the design's own measured or derived values. For strict accessibility, `.claude/skills/design-picker/assets/palettes.json` holds a 7:1 version of every text colour.

### A. Navy Annual (Rapport annuel 2025)

**Identity.** A calm, institutional two-tone report. Navy fills whole pages and full-height side panels; white pages carry bold caps titles, centred KPI rows with navy icon discs, and data in shades of one hue. Each page is either mostly navy (28–90%) or almost white (0–8%).
**Use for** annual, ESG, investor, board and public-sector reports, 8–40 pages. Needs few photos: every photo slot has a navy or tint fallback.

```
--navy:        #1A2E5F  /* panels, covers; white text 13.1:1 */
--royal:       #2B4693  /* highlights, numbers in contents, chart mid (8.8:1) */
--disc:        #142468  /* icon discs */
--ink:         #1B1D2E  /* headings and body (16.6:1) */
--ink-soft:    #5A5F6E  /* captions (6.4:1) */
--on-navy-soft:#8FA0C8  /* meta and numbers on navy */
--highlight:   #64A5C7  /* year / section number ON NAVY ONLY (4.8:1 on navy, 2.7:1 on white) */
--divider:     #D5D8E0
--zebra:       #E8EDF7
--chart:       #8A9DB9 → #5B77A8 → #2B4693 → #12265A   /* oldest → latest */
```

**Type.** Figtree (OFL; the closest match, with Poppins next). One family throughout.

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 80 / 80 pt | Bold caps, white |
| Cover year | 104 pt | `--highlight` |
| Page title (H1) | 36 pt / 1.1 | Bold caps |
| Section title in panel | 36 pt | White caps |
| H2 | 13 pt | Bold, navy |
| Body | 10 / 15 pt | Regular |
| KPI figure | 32 pt | Bold |
| Caption | 8.5 / 11 pt | `--ink-soft` |

**Grid.** Margins L 22 / R 20 / T 24 / B 20 mm (content 168 mm). **Navy panel = 70 mm** (full bleed, left, full height); content beside it runs from x 82 to 190 mm. Navy pages have no header or footer.

**Signature components**
1. **Split page**: a navy panel 70 mm wide (110 mm on the foreword page) with 14 mm inner padding. It holds the title and intro, never tables.
2. **Caps title**: bold caps, 2 lines, leading 1.1, with no rule or underline.
3. **KPI row**: 3–4 centred columns. Each has a 14 mm navy disc with a white line icon, then a 32 pt bold figure and an 8.5 pt grey caption. Columns are split by 0.5 pt `#D5D8E0` dividers.
4. **One-hue column chart**: 4–6 bars, each graded from light at the top to deep at the bottom, or flat ramp steps. Value labels above the bars, no gridlines, no y-axis labels.
5. **Stat rail**: a 6 mm vertical bar (top 30% `#255B9C`, the rest navy) with 3 stats beside it.
6. **Org chart**: navy head box and **navy child boxes** (not tinted), joined by 0.75 pt grey connectors, with bullets under each box.
7. **Steps**: navy discs 14 mm across with white "01–04" numbers, joined by a hairline. On navy pages, use white cards with ringed number badges instead.
8. **Dot-grid texture**: 0.6 mm dots on a 2.5 mm pitch, in one corner patch per page at most.

**Pages**
- **Cover**:
  - Full navy page.
  - Title at x 20, y 69 mm, 80 pt caps white, 2–3 lines, at most 125 mm wide. The year sits under it at 104 pt in `--highlight`.
  - Tagline 18 pt white at y 171 mm. Metadata 11 pt `#8FA0C8` at y 242–258 mm.
  - Optional faint arc and hairline art, within 4–10% of navy's lightness.
- **Contents**: either a full navy page (title "CONTENTS" 40 pt white, list from y 70 mm, 11 pt white, numbers "02" in `#8FA0C8`, no leader dots), or a split page with the list on white.
- **Section opener**:
  - Navy panel holding the section number "01" (60 pt `--highlight`), the title (36 pt white caps) and a 10 / 15 pt white lede.
  - To the right, a full-bleed photo, or an "In this section" list plus one 36 pt hero KPI.
- **Break page**: full navy, one sentence at 28 / 36 pt white at y 130 mm. At most one every 4–6 pages.
- **Executive summary / KPI**:
  - White page, title 36 pt caps, lede 11 / 16 pt.
  - KPI row at y 95–150 mm, then 3–5 findings in two 82 mm columns.
  - Optional navy band at the foot (y 250–297 mm) carrying one conclusion sentence in 14 pt white.
- **Narrative** *(inferred)*: body 10 / 15 pt in one 168 mm column. Or the **side-rail variant**: a 46 mm rail (H2, 24 pt pull-figures, notes) next to a 114 mm text column. One pull quote per spread (48 pt navy quote mark plus 15 / 22 pt navy text).
- **Chart page**: either a split (navy panel with title; stacked KPI list and a 108 × 110 mm chart on white), a full-width 168 × 100 mm chart, a donut with legend, or a stat rail beside a figure or map.
- **Table** *(inferred)*: navy header row with 8 pt bold caps white; 9 pt body, zebra `#E8EDF7`, 1 pt navy rule under the last row.
- **Org chart**: head box 60 × 16 mm; four child boxes 38 × 11 mm; bullet columns under each.
- **Foreword**: navy panel 0–110 mm holding the letter (about 250 words, white); a 90 mm circle portrait and the pull quote on the right.
- **Closing / back cover**: full navy, sign-off 18 / 30 pt white, a short white rule, and contact details bottom right. A QR code only if there is a real URL.

**Don't copy:** circled icons used as decoration, rounded tiles over stock mountains, stock "leader" portraits.

---

### B. Forest Breakslide (dark green)

**Identity.** Premium, eco-modern dark mode. Deep green covers and break pages, tall vertical slabs that step from bright green at the top to deep at the bottom, photos with one 45° chamfer, and a three-dot marker. **In a report, dark pages are only the cover, one break page per section and the closing page.** Content pages are white with a thin green slab rail down the left edge.
**Use for** dark-mode screen documents: portfolios, agency, architecture or eco profiles, 8–40 pages. **Not** for office print, strict accessibility or long text.

```
--ground:      #005A58  /* dark pages, deep text (8.1:1) */
--slab-ramp:   #23B582 → #10906F → #077060 → #005A58   /* top → bottom; #23B582 is never text (2.6:1) */
--label:       #19816A  /* the only bright-ish green safe for small labels (4.8:1) */
--dots:        #2E9B64  #19816A  #043637  /* on dark ground swap the last to #CFE8E1 */
--on-dark:     #CFE8E1  /* secondary text on green (6.3:1) */
--ink:         #1E3A35
--ink-soft:    #5B6270
--tint:        #E6F2EF
--hairline:    #CFE0DC
--chart:       #CFE8E1 → #57BA96 → #10906F → #005A58
```

**Type.** Headings in Montserrat (SemiBold, ExtraBold for the cover), **Title Case**, with an optional italic second line. Body in Inter.

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 48 pt | ExtraBold caps, +10% tracking |
| H1 | 26–30 pt | SemiBold |
| H2 | 14 pt | SemiBold |
| Label | 7.5 pt | Bold caps, +25–30% tracking, `--label` |
| Body | 9.5 / 14.5 pt | Inter, ragged right |
| KPI figure | 30–36 pt | Bold |
| Break-page number | 110 pt | `#23B582` |

**Grid.** Margins T 22 / B 20 / L 26 / R 18 mm (content 166 mm). Main column 112 mm + 8 mm gutter + 46 mm side column. **Slab rail on every white page**: `#005A58` at x 0–7 mm, full height, plus a `#23B582` cap at x 7–11 mm, y 0–60 mm (about 4% ink).

**Signature components**
1. **Stepped slab**: 24–50 mm wide, ramp from top to bottom, at most 3 per page. Neighbouring slabs start at least 40 mm apart vertically. In Word, build it as **flat ramp steps** in table cells, not a gradient.
2. **Cut-corner photo**: one 45° chamfer on a top corner, leg 15% of the width (5–12 mm), the same corner throughout the document.
3. **Stub slab**: a short chamfered slab overlapping a photo's lower corner, composited into the same image.
4. **Three-dot marker**: 3.2 mm dots with 1.6 mm gaps, one per page at the H1. Use it as a **part indicator**: dot n lit for part n.
5. **Service list**: line icon, a label "01 · ADVISORY", a heading and 2–4 lines of body. Labels carry real content.

**Pages**
- **Cover (dark)**: `#005A58` ground with two slabs on the right (x 160–210 and x 128–152 mm from y 150). A chamfered portrait photo (72 × 144 mm) overlaps them. Title 48 pt caps white at x 22, at most 88 mm wide. A vertical hairline with rotated meta text.
- **Contents (white)**: rail, plus a tab slab at the top right (x 182–210, y 0–90 mm). Entries every 14 mm: "01" in 20 pt `#10906F`, title 12 pt, page number in `#005A58`.
- **Break page (dark)**:
  - Four full-bleed columns alternating ramp and ground.
  - A `#043637` band across y 150–215 mm holds the white 30 pt title.
  - The section number is 110 pt `#23B582`.
  - Print version: columns only at the top, text on white.
- **Executive summary**: a deep band (y 0–52 mm) with a white H1, then KPI tiles that "step down" out of the band: a `#10906F` top row, then tint tiles with 32 pt figures.
- **Narrative**: rail; label, then H1, then the dots; 112 mm body column; side column for pull quotes (12 pt with a 3 mm `#23B582` bar) and notes.
- **Chart**: a 112 × 85 mm chart in the main column, with a deep **insight slab** in the side column ("WHAT IT MEANS", 12 pt white).
- **Table** *(inferred)*: `#005A58` header with white 7.5 pt caps; highlighted row in tint with a 3 pt `#10906F` left bar.
- **Team**: a deep band with chamfered portraits straddling its edge (rendered as one image), then name, role and bio below.
- **Closing (dark)**: slabs mirrored to the left; thank-you line 24 pt white; contact in `#CFE8E1`.

**Don't copy:** light-grey body text (1.6:1), teal names (2.2:1), justified text, decorative circle icons.

---

### C. Leaf & Black (Business Plan)

**Identity.** Confident and numbers-forward. White pages, black-and-white photos cropped by **45° rounded diamonds** that bleed off the page, giant green numerals, and green and black alternating as a pair of accents. 67% of the page is white.
**Use for** business plans, pitch and funding documents, investor and ops updates, go-to-market strategies, 8–30 pages.

```
--green:       #5AB14D  /* FILLS ONLY (2.7:1); dark text on it 6.4:1 */
--green-mid:   #4C9541  /* numerals ≥ 24 pt and chart bars (3.7:1) */
--green-deep:  #366B2E  /* small green text, fills with white text (6.4:1); strict: #105E00 */
--green-tint:  #EBF6EA
--black:       #111111  /* second "colour": blocks, cards, table header; green on black 7.0:1 */
--ink:         #1C1C1C
--ink-soft:    #5C5C5C
--signal:      #C0318F  /* negatives (red is too close to green for colour-blind readers) */
```

**Type.** Roboto, all weights. Weight contrast is the main device: the cover pairs a Light line with a Bold line.

| Role | Size / leading | Style |
|---|---|---|
| Cover line 1 | 32 pt | Light, key word in `--green-mid` |
| Cover line 2 | 44 pt | Bold |
| H1 | 26 / 30 pt | Bold, mixed case (not caps) |
| Section opener title | 36 pt | Bold |
| H2 | 15 pt | Bold |
| Body | 10 / 14.5 pt | Regular |
| Big KPI | 54 pt | Bold, about 2.1× the title |
| Section numerals | 36 pt | Bold, alternating green and ink |
| SWOT letters | 96 pt | Bold or Black |

**Grid.** Margins 18 / 18 / 20 / 20 mm (content 174 mm), 6 columns. Optional side rail of 40 mm with a 128 mm text column. At most one **corner chip** per page, alternating corners and colours.

**Signature components**
1. **Rounded-diamond photo**:
   - A square rotated 45°, with corner radius about 12% of its side.
   - One or two corners fall off the page, leaving a straight 45° edge with one rounded tip inside.
   - Photos in greyscale, or a black → green duotone. A 4 mm white gap where shapes meet.
2. **Corner chip**: a right triangle in a page corner, with legs 22–30 mm and the inner tip rounded. Green or black.
3. **Big-number block**: H2 15 pt, a 54 pt numeral (`--green-mid` on white, `--green` on black), a 10.5 pt label and 2–3 lines. Pairs of blocks are split by a hairline.
4. **KPI circles**: 30 mm discs, 3 green with ink numbers and **one black with green numbers** marking the exception.
5. **SWOT letters**: 96 pt letters filled with a duotone photo, or solid (S/O green, W/T black).
6. **Milestone line**: a hairline with 12 mm nodes and small green dots between them; year above, value below (22 pt).
7. **A./B. slabs**: two equal blocks, one black and one green, with a 64 pt "A." / "B." at the bottom left.
8. **Square markers**: 2.5 mm squares alternating green and black instead of bullets.

**Pages**
- **Cover**: the top 165 mm is diamond artwork (a photo diamond, a solid black diamond and a green diamond) bleeding off the top and right. Title from y 180 mm (Light 32 pt plus Bold 44 pt). A meta row at y 262–279 mm. A green corner chip at the bottom right.
- **Contents**: 110 mm list with square markers and page numbers; a green duotone diamond bleeding off the right edge.
- **Section opener** *(inferred)*: diamond band across the top 120 mm; "02" at 72 pt `--green-mid`; title 36 pt; an "In this section" list.
- **Executive summary / KPI**: a pair of big-number blocks (54 pt), then a row of 4 KPI circles, then 4–6 findings with square markers.
- **Narrative**: an optional image band (174 × 70 mm); a 40 mm rail of green-deep labels and one margin numeral; body 10 / 14.5 pt; a pull quote as a black slab with 14 pt green text.
- **Chart (market analysis)**: grouped bars in green-mid, black and grey; a legend and commentary in 3 columns below.
- **Table** *(inferred)*: **black header** with white 8.5 pt bold caps; the "us" row in green tint with green-deep bold text.
- **SWOT**: a 2×2 grid of 84 × 95 mm cells with hairline cross rules and the giant letters.
- **Milestones**: horizontal for up to 5 points, vertical for 6–12.
- **Team**: black cards (84.6 × 58 mm) with B&W headshots, white names and green roles. The lead's card is green with ink text.
- **Closing**: a 3×3 takeaways grid, a contact strip with icon circles; the back cover mirrors the cover.

**Don't copy:** white text on green (fails at every size), more than one corner chip per page, silhouette placeholders.

---

### D. Prism Rounded (teal)

**Identity.** Friendly, modern and approachable. Teal **rounded panels and pills hold the text**, caps titles end in a raised teal dot, sections open on full-colour break pages, and photos get rounded or capsule crops.
**Use for** marketing, company profiles, proposals, impact and programme reports, 8–30 pages. Not for dense analytical or bad-news reports.

```
--teal:        #379A86  /* shapes, large type, break pages; white text only ≥ 14 pt bold (3.4:1) */
--teal-panel:  #2C7B6B  /* panels and chips with small white text (5.1:1) */
--teal-dark:   #1E554A  /* text on tint */
--charcoal:    #3C3D40  /* second tile colour */
--tint:        #E7F3F0  /* callouts, chart panels; zebra #EFF7F5 */
--ink:         #383838  /* headings and body */
--ink-soft:    #5F6368
--hairline:    #D3E5E0
```

**Type.** IBM Plex Sans (strong match: the board's capital I has slab bars).

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 60 / 62 pt | Bold caps, −0.5 pt tracking |
| Break-page title | 40 / 44 pt | Bold caps |
| H1 | 28 / 31 pt | Bold caps, exactly 1.1 leading |
| H2 | 16 pt | Bold caps |
| H3 | 12 pt | SemiBold, sentence case, `#2C7B6B` |
| Body | 9.5 / 14 pt | Regular |
| Label / pill | 7.5 pt | SemiBold caps, +2 pt tracking |

The **title dot**:
- **What it is**: a filled teal circle about 0.62× the cap height, raised to the cap-top line, placed after the first line of every H1 (white on teal grounds).
- **How to set it in Word**: Inter "•" at 1.4× the heading size, raised 0.28×. Plex's own bullet is square.

**Grid.** Margins 18 / 18 / 20 / 20 mm (content 174 mm), 12 columns. Main split 1/3 (55 mm) + 2/3 (115 mm). **Use only these radii:** panel 8 mm, card 4 mm, chip 2 mm, photo 5 mm; pills use half their height.

**Signature components**
1. **Pill**: radius = height / 2. Sizes: 6 mm tag, 8 mm button, 24–40 mm statement. Text never enters the round ends.
2. **Half-pill edge slab**: a pill flush with the page edge, 110 mm tall. Cover and closing only.
3. **Rounded panel**: r 8 mm, padding at least 8 mm, at most one large panel per page.
4. **Section number chip**: a white circle 16–18 mm across with a 12–14 pt bold teal number, centred **on the panel's edge**.
5. **KPI tiles**: 40.5 × 36 mm, r 4, alternating `#2C7B6B` and `#3C3D40`, white figures at 26 pt.
6. **Icon chip**: a 12 mm rounded square in `#2C7B6B` with a white line glyph.
7. **Timeline nodes**: 14–16 mm circles with the year split over two lines; connectors 1–1.5 pt teal.
8. **Corner blob**: a teal quarter-round, 80 mm, bleeding a corner behind a photo grid.

**Pages**
- **Cover**: photo full bleed across the top 178 mm. A **half-pill** teal slab (x 0–168, y 128–238 mm) overlaps it, holding a white overline pill, a 60 pt white caps title with its dot, and a date pill. A 3-column meta band at y 250–280 mm.
- **Contents**: H1 with dot. A **deep-teal rounded panel** holds rows every 18 mm: a white 11 mm chip with "01", a white title and description, and the page number.
- **Break page** (use one style per report):
  - Full teal with a white number chip and a 40 pt white title.
  - Or a white page with a rounded teal panel 174 × 150 mm and a chip on its bottom edge.
  - Or a rounded photo with a panel over it.
- **Executive summary**: a row of 4 KPI tiles; a "Key message" (12.5 pt) beside the summary text; up to 5 numbered findings with 8 mm chips.
- **Narrative**: 1/3 rail (section chip, pull quotes 13 pt `#2C7B6B`, notes) and a 2/3 text column; tint callout (r 4) with a label pill.
- **Chart**: the chart on a tint panel (174 × 110 mm, r 6) in teal and charcoal bars, with pill swatches instead of a legend. Two KPI chips below.
- **Table**: a **pill tag** above it ("TABLE 3 · REGIONAL REVENUE"); `#2C7B6B` header row, zebra `#EFF7F5`, square corners.
- **Timeline**: vertical by default (spine at x 36 mm, nodes every 30 mm); horizontal for up to 5 phases.
- **Services / recommendations**: a 2-column grid of icon chips with titles; priority pills (High = teal fill, Med = tint, Low = outline).
- **Portfolio / case studies**: a 3×3 photo grid (r 5) with one teal caption card and a corner blob behind.
- **Closing**: a half-pill from the right edge holding "NEXT STEPS" and contact pills.

**Don't copy:** small white text on bright teal, social-media circles, a space before "?" in headings, more than one large panel per page.

---

### E. Clinicare Aqua (medical)

**Identity.** Calm, hygienic and reassuring, with lots of white. A pale aqua tint, a single aqua fill, **circle photos with a white ring** placed across a white/aqua edge, and aqua blocks offset behind rectangular photos. No rounded rectangles: circles only.
**Use for** patient- and public-facing healthcare, wellbeing and public-health reports, service overviews, 8–30 pages.

```
--aqua:        #4DCCD4  /* FILLS ONLY (1.9:1), never text, ≤ 12% of a page */
--aqua-deep:   #0E757C  /* all accent text, stat panel (5.5:1); strict / small text: #0B6065 (7.3:1) */
--tint:        #E0FEFF  /* bands and panels */
--navy:        #0C132E  /* titles; text ON aqua (9.5:1) */
--ink:         #1E2733  /* body; also OK on aqua (7.8:1) */
--ink-soft:    #5C5C5C
--hairline:    #CDE7EA
```

**Type.** Nunito Sans (humanist and soft; Poppins and Montserrat don't match).

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 40 / 44 pt | 800 weight, navy; **last word in aqua-deep** (the "Clini/care" two-tone move) |
| H1 | 26 / 30 pt | 700, sentence case |
| H2 | 16 pt | 700 |
| Kicker | 7.5 pt | 700 caps, +12% tracking, aqua-deep, 3 mm above the heading |
| Body | 10 / 14.5 pt | 400, ink (never the board's pale grey) |
| Stat figure | 30 pt | 800 |

**Grid.** Margins 18 / 18 / 20 / 20 mm (content 174 mm), 12 columns of 10.83 mm. Footer at 287 mm with the page number in aqua-deep.

**Signature components**
1. **Tint panel**: square corners, either a full-bleed band behind a row of cards (content straddles its edge by 15–25 mm) or an inset callout with 6–8 mm padding.
2. **Circle photo with white ring**: a 3–4 mm ring. Hero circles 100–200 mm across always sit across a boundary; portraits are 24–38 mm.
3. **Stat badge**: an aqua disc 30–36 mm across overlapping a hero circle, with a 20 pt navy figure.
4. **Stat panel**: an aqua-deep rectangle with 3–4 white 30 pt figures and 40% white dividers, 45–55 mm tall.
5. **Offset aqua block**: 45–60% of the photo's size, shifted 8–12 mm out from one corner, behind the photo.
6. **Overlapping title box**: 90–100 × 35–40 mm, half over the bottom of a photo band, with a 9 mm square notch.
7. **Service grid**: 3×3 cells with the diagonal cells in aqua (navy text) and the rest white with hairline borders.
8. **Checklist**: 3.5 mm aqua-deep checks (aqua checks fail contrast) with 9.5 pt text.
9. **Dots**: 5–7 aqua discs 1.6–2.6 mm across, clustered near titles. Cover, openers and closing only.

**Pages**
- **Cover**: a 200 mm circle photo centred at (150, 92) mm, bleeding off the top and right. Aqua dots, a kicker, a 40 pt two-tone title at y 212 mm, a subtitle, and meta under a short aqua rule. **No photo**: a tint circle with a concentric aqua ring and an aqua badge disc.
- **Contents**: a full-bleed tint column (x 0–72 mm) holding the title; on the right, rows with 8 mm aqua circles holding navy numbers.
- **Section opener**: an aqua block across the top 185 mm, with a 100 mm ringed circle photo on it. Number 54 pt navy and title 30 pt **navy** (not white). Lede and "In this section" below.
- **Executive summary**: kicker and H1; an aqua-deep stat panel; then "Key findings" (checklist) and "What we recommend" (numbered) in two columns.
- **Narrative**: a 113 mm text column; a 42 mm rail with a tint pull-quote panel (3 mm aqua bar); an optional photo with an offset aqua block.
- **Chart** *(inferred)*: a full-bleed tint band holding the chart in a white card. Series in aqua-deep, navy and aqua (aqua only with direct labels).
- **Table**: tint header row with 8.5 pt bold ink, hairlines; highlighted row in aqua with navy bold text.
- **Team**: ringed circle portraits straddling a tint band's edge. **No photo**: initials discs, never silhouettes.
- **Services**: a 3×3 service grid over tint and aqua bands. Department pages use a photo band plus an overlapping title box.
- **Closing**: aqua across the bottom half with a white disc biting into it; contact text in navy on aqua.

**Don't copy:** white text on aqua, pale-grey body text, gradients, more than 12% aqua on a page.

---

### F. Docoro Royal Block (royal blue)

**Identity.** Clinical, confident and energetic. A white page cut by **hard-edged royal blue blocks that bleed off the page**, with photos, stat cards and portraits sitting across the block's edge. Heavy geometric headings and big numerals over tiny captions. 21 of 30 slides have a bled block.
**Use for** healthcare, health-tech and public-sector reviews, KPI-led impact reports, services brochures, 8–40 pages. Best with 2–4 strong photos; there are flat fallbacks.

```
--royal:       #053AA6  /* blocks; white on it 9.7:1 */
--deep:        #0E2965  /* small blue type, quote mark, figures on white (13.8:1) */
--on-royal:    #C8D4F0  /* captions on blue */
--divider-blue:#3764BB  /* dividers on blue */
--tint:        #F0F4FB  /* call-outs, bar tracks */
--context:     #B4C2DE  /* non-highlighted bars */
--ink:         #141414  /* (18.4:1) */
--ink-soft:    #6B6B70
--hairline:    #DCE4F4
```

**Type.** Poppins for display, headings, numerals and labels; **Inter** for body, tables and captions (Poppins is 12–15% wider).

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 54 / 56 pt | ExtraBold, white |
| Section title | 36 / 40 pt | Bold |
| H1 | 24 / 28 pt | Bold |
| H2 | 14 pt | SemiBold |
| Body | 10 / 15 pt | Inter |
| KPI figure | 32 pt (hero 44 pt) | Bold |
| KPI caption | 8 pt | Inter |
| Quote | 16 / 22 pt | SemiBold |
| Quote mark | 120 pt | ExtraBold |

**Grid.** Margins 18 / 18 / 20 / 18 mm (content 174 mm), 6 columns of 26 mm. Royal blocks always touch at least one page edge: a one-third slab is 99 mm; a full-width band is 36–48 mm; a corner block is 55–60% of the page width.

**Signature components**
1. **Bled corner block cutting a photo**:
   - A royal rectangle with square corners, touching 1–2 page edges.
   - A photo overlaps the block's edge by 30–50%. White text sits inset 12 mm on the block.
   - One block per page.
2. **Full-width band**: 36–48 mm tall, with a row of portraits, cards or stats centred on it and 4–10 mm taller than it, so the band reads as passing behind.
3. **Stat figure**: 32 pt bold, an optional lighter suffix ("187x", "+45.5%"), and an 8 pt caption. Rows are split by 0.5 pt dividers.
4. **Straddling white card**: square corners, a 0.75 pt `#DCE4F4` border, **no shadow**, half on blue and half on white.
5. **Oversized quote mark**: "“" at 120 pt Poppins ExtraBold in deep navy, inside the card's top-left corner.
6. **Highlighted card or column**: in a row of 3–4, exactly one is royal with white text ("recommended", "current", "us").
7. **Edge tab**: a 92 × 6 mm royal bar bled on the top or bottom edge. At small size it marks the page number.

**Pages**
- **Cover**: royal field from y 0 to 190 mm. Kicker 11 pt caps; title 54 pt ExtraBold white at y 120 mm. A photo (x 60–210, y 150–245 mm) straddles the field's bottom edge. Organisation and date on white below; edge tab at the foot.
- **Contents**: white page with a thin royal spine (x 0–8 mm). Entries: "01" 14 pt deep navy, title 11 pt, page number in royal. Optional KPI band at the foot.
- **Section opener**: royal block across the top 150 mm with the number and a 36 pt white title. Standfirst and "This section covers" on white below. Optional photo overlapping the block's edge.
- **Executive summary**: 2-column summary, then a **royal KPI band** (y 165–213 mm) with 3–4 white figures, then 3 numbered findings. Variant: a white card straddling the band.
- **Narrative**: **no blue blocks**, so narrative pages stay quiet. Two columns of 84 mm; a tint call-out with a 3 mm royal bar and a 28 pt stat.
- **Chart**: highlighted bars in royal, context bars in `#B4C2DE`, a 0.5 pt baseline, direct labels. Horizontal progress bars: deep navy on a tint track.
- **Table**: royal header with white 8 pt caps; the highlighted column royal down its full height, or tint with royal bold text.
- **Quote**: a royal block (x 30–105 mm) bled to the bottom; a white card over it with the 120 pt quote mark and 16 / 22 pt text.
- **Team**: a full-bleed royal band (36 mm) with rectangular portraits (36 × 44 mm) centred on it.
- **Findings**: numbered rows "01–05" in 28 pt royal. One can be promoted to a full-bleed royal row.
- **Closing**: full royal; "Thank you" or "Next steps" 44 pt white; a white URL bar bled off the right.

**Don't copy:** drop shadows, gradient photo washes (`#7593CD`: white text only 3.1:1), pill buttons, the near-invisible chart grey `#EFF3EF`. Proof-print royal before a professional run: it may fall outside CMYK.

---

### G. Market Frame (teal, framed)

**Identity.** Composed, clean, corporate-editorial. A **hairline frame 10 mm inside the page edge**, broken on purpose by a tag hanging off the top edge, a rotated pill tab on the left frame line, and full-bleed teal panels that cross the frame.
**Use for** consulting deliverables, white papers, proposals, market analyses, capability statements, ops reviews, 8–40 pages. The most robust design to build and edit in Word.

```
--teal:        #02A19A  /* fills, markers, chart highlight (3.2:1: white text ≥ 14 pt bold only) */
--teal-deep:   #00625C  /* teal text, panels carrying text, table header (7.2:1) */
--tint:        #E6F6F5  /* zebra, call-outs */
--grey-panel:  #EEEEEE
--frame:       #B4B4B4  /* 0.5 pt */
--ink:         #1F1F1F  /* also on bright teal (5.2:1) */
--ink-soft:    #5C5C5C
--hairline:    #D9D9D9
--chart:       #CFCFCF (context) · #02A19A (highlight) · #00625C (current)
```

**Type.** Montserrat Bold / ExtraBold for headings (or Inter Display ExtraBold, closer in width); Inter for body.

| Role | Size / leading | Style |
|---|---|---|
| Display | 40 / 42 pt | ExtraBold caps, +3% tracking |
| H1 (opener) | 28 / 30 pt | Bold caps |
| H2 (page title) | 18 / 20 pt | Bold caps |
| H3 | 9 / 12 pt | Bold caps, +12% tracking, `--teal-deep` |
| Kicker | 7.5 pt | SemiBold caps, +20% tracking |
| Body | 9.5 / 14 pt | Inter |
| Lead | 12 / 17 pt | Inter |
| KPI figure | 30 pt | Bold |
| Tab label | 7.5 pt | Bold caps, +20% tracking |

**Grid.** Frame at 10, 10 → 200, 287 mm. Text area L 24 / R 24 / T 28 / B 26 mm (162 × 243 mm), so text sits at least 14 mm inside the frame. 12 columns with 6 mm gutters. Footer inside the frame at y 280 mm.

**Signature components**
1. **Inset frame**: 190 × 277 mm, 0.5 pt `#B4B4B4`, on every text page, sitting at the lowest layer so teal shapes cover it. Omit it on comparison, closing and full-panel pages. In Word, draw it as a **shape anchored to the page**. Page borders draw the bottom edge at the page edge in LibreOffice.
2. **Hanging tag**: a rectangle starting at the paper's top edge with its bottom end rounded, crossing the frame. Sizes: page 16 × 34 mm, cover 18 × 64 mm, quote 64 × 120 mm. Content: a white glyph or a 2-digit section number.
3. **Vertical rotated tab**: a 9 × 70 mm pill centred on the left frame line, with 7.5 pt caps reading bottom to top (report title or section).
4. **Panel crossing the frame**: a full-bleed right panel (x 118–210 mm), a top band (x 0–120 mm × 28 mm), or a D-shaped pill whose left end is off the page.
5. **Option columns + stadium outline**: three full-bleed columns (deep / white / grey) with a hairline stadium shape crossing all three. The recommended option goes in the deep column.
6. **Check-chip list**: 6 mm circles with ticks and 9.5 pt text, 24 mm apart.
7. **Icon chip**: an 8 mm teal circle with a white glyph, on KPI cells, portraits and bullets.
8. **Kicker line**: 7.5 pt tracked caps under or over the H2, carrying real content (section, client, date).

**Pages**
- **Cover**:
  - Frame, with a long tag (x 24–42, y 0–64 mm).
  - Kicker at y 78 mm; title 40 pt at y 84–130 mm; lead 12 pt.
  - A photo inside the frame from y 160 mm to the frame bottom, with a 16 mm deep-teal chip overlapping its top edge.
- **Contents**: frame, a tag "00" at the right; entries every 16 mm (number 18 pt teal, title 10 pt caps, one-line description, page number); vertical tab with the report title.
- **Section opener**:
  - A full-bleed deep panel at x 118–210 mm covers the frame on three sides.
  - In the panel: number 48 pt white, H1 28 pt caps white, lead 11 pt, and 3 check-chip points.
  - On the left, a photo inside the frame or the no-photo fallback.
- **Executive summary**: a band from the left page edge across the frame (x 0–120, y 30–58 mm) holding the white H2; a 12 pt lead; a KPI row (8 mm chips, 30 pt deep figures); a 2×2 findings grid.
- **Narrative**: frame plus tag; a 126 mm text column (about 70 characters); a 30 mm rail with notes topped by teal rules.
- **Chart**: a 162 × 95 mm chart in grey, with highlight teal and the current period in deep. The key takeaway sits in a **D-shaped pill** from the left edge (bright teal, 12 pt bold **ink**).
- **Table** *(inferred)*: deep header with white 7.5 pt caps; body 8.5 pt with hairlines; optional tint zebra; total row with a 1 pt deep rule.
- **Options**: three full-bleed columns with the stadium outline; option headings 14 pt in sentence case.
- **Team**: a light-grey half-frame box whose bottom line threads through 28 mm circle portraits, each with a teal chip.
- **Quote**: a tall deep tag (64 × 120 mm) hanging from the top holding the white quote; an arch-cropped portrait at the left.
- **Closing**: vertical tab; bright right panel with "NEXT STEPS" 28 pt; check-chips with ink text.

**Don't copy:** small white text on bright teal, a frame shape that changes from page to page (keep it constant), the placeholder "WWW.EXAMPLE.COM" kicker, trailing full stops on every heading.

---

### H. Spectrum (multicolour)

**Identity.** A designer-grade multicolour system, not a rainbow. Dark ink and white carry the document; **each section owns one colour**, and the five colours appear together only where the whole is shown (cover, contents, overview, finance, back cover), always in the same order. It borrows A's full-colour cover and big-number KPIs, F's bled blocks, and G's tab-off-the-edge idea, turned into a wayfinding strip.
**Use for** impact reports, foundation, city or group annual reviews, and ESG reports organised by pillar: documents with 3–5 programmes, services or themes, 10–30 pages. Not for a single-topic report; use one accent there.

```
--ink:      #16213E   /* text, cover, back cover (15.9:1) */
--soft:     #5A5F6E   /* captions */
--rule:     #D9D9D9
/* section colours, in this fixed order (validated: lightness band, chroma, colour-blind separation ≥ 10.8 ΔE) */
/*            fill      panel (text on it)       deep (accent text, ≥ 7:1)  tint     */
--blue:     #2559D6   #2559D6 white 6.0:1       #2150C2                    #EBEFFA
--coral:    #E04F39   #D83A22 white 4.6:1       #A62C1A                    #FAEDEB
--teal:     #009682   #008473 white 4.6:1       #006557                    #EBFAF8
--saffron:  #D4891A   #D4891A INK   5.6:1       #7B500F                    #FAF4EB
--plum:     #8A3FB0   #8A3FB0 white 6.1:1       #7E39A1                    #F4ECF8
```
- `fill` is for marks, strips and chart bars; `panel` is the fill used behind text; `deep` is the only shade allowed for small coloured text on white.
- **Saffron never carries white text**: its panels use ink.
- Category order is fixed (blue, coral, teal, saffron, plum) and is never re-sorted by value. The palette passed the dataviz validator (lightness band, chroma floor, colour-blind separation, normal-vision floor). Saffron is below 3:1 against white as a mark, so every chart carries direct value labels.

**Type.** Figtree throughout.

| Role | Size / leading | Style |
|---|---|---|
| Cover title | 72 pt | ExtraBold caps; year 60 pt in saffron |
| Section number on band | 120 pt | ExtraBold, in the band colour mixed 38% toward white |
| Band title | 30 / 32 pt | ExtraBold, sentence case |
| Page title | 22 pt | ExtraBold caps |
| Kicker | 7.5 pt | SemiBold caps, +40 tracking, in the section's deep shade |
| KPI figure | 28 pt | ExtraBold, deep shade |
| Body | 10 / 15 pt | Regular |

**Grid.** Margins 22 / 20 mm, content 168 mm, two 80 mm text columns with an 8 mm gutter, chart + note split 104 / 8 / 56 mm.

**Signature components**
1. **Spectrum strip**: five equal segments across the top edge of every content page, 3 mm tall with 0.8 mm gaps. The current section's segment drops to a **10 mm tab**. This is the reader's map; on overview pages no tab drops.
2. **Section band**: the first page of each section has a full-bleed band (0–112 mm) in the section's `panel` colour. It holds a giant pale number, a kicker, a 30 pt title, a lede and a white icon chip, with a 3 mm `fill` line under the band.
3. **Bar-chart cover**: five full-height columns rising from the bottom edge in section order, with heights that echo the year's data. Section names sit at the top of each column.
4. **KPI row**: three figures under a 1.5 pt rule in the section colour, deep-shade numerals, hairline dividers.
5. **Tint card**: a case study on the section tint with a 4.5 pt left bar in the section `fill`.
6. **Step tiles**: tint tiles with a 3 pt top bar, a big deep-shade number, a bold label and two lines.
7. **Single-hue charts inside a section**: context bars at the fill mixed 55–62% toward white, the bar that matters in full `fill`, direct labels, one baseline.
8. **Multicolour moments only where the whole is shown**: the overview tiles (one per section), a donut of spend by section with 2 pt white gaps and the total in the centre, stacked columns with white gaps, and a five-colour timeline of the year's moments.

**Pages**
- **Cover**: ink page with the five-column composition in the lower half, title "IMPACT REPORT" 72 pt white, the year in saffron.
- **Contents**: rows with a 10 mm colour square per section, the title 15 pt, a description, and the page number in that section's deep shade.
- **Foreword**: a 26 pt pull quote with a coral quote mark, two text columns, then "2025 in five moments", one coloured top-rule cell per section.
- **At a glance**: a 2×2 grid of tint tiles (icon chip, kicker, 30 pt figure, caption) plus a donut and legend of spend by section.
- **Section, page 1**: section band, KPI row, two text columns.
- **Section, page 2**: the strip with the section's tab; a page title; then one of a chart + note, a table (section-colour header row, tint zebra, total row with a 1.5 pt colour rule), a line chart + step tiles, or bars + case card + quote.
- **Finance**: strip with the plum tab; stacked columns by section in the fixed order, legend, and an income/spend table.
- **Back cover**: ink page, one sentence, a five-colour segmented bar.

**Don't:**
- Give two sections the same colour, or use a section's colour inside another section.
- Put white text on coral, teal or saffron `fill`. Use `panel`, or ink on saffron.
- Use more than five colours.
- Colour bars by their value.
- Use the multicolour treatment on a single-topic report.

**Example:** `.claude/skills/design-picker/examples/spectrum-impact/` (14-page build script, DOCX, PDF, contact sheet).

---

## 5. Building it (Word / LibreOffice)

Every technique below was built with python-docx, rendered in LibreOffice 24.2 and measured. Code is in `.claude/skills/design-picker/references/docx-techniques.md`, and proof renders are in `.claude/skills/design-picker/assets/proofs/`. Word itself has not been tested.

| Need | How | Watch out |
|---|---|---|
| Fonts | TTFs in `.claude/skills/design-picker/assets/fonts/` (Figtree, Montserrat, Poppins, Inter, Roboto, Nunito Sans; IBM Plex is in the report-design skill). Install to `~/.fonts`, run `fc-cache -f`, delete `~/.cache/matplotlib` | Bold = base family + bold. SemiBold and ExtraBold are separate family names ("Poppins SemiBold"); don't add bold to them. **Exact-point leading.** |
| Full-bleed panel, band, cover, dark page | A rectangle shape anchored to the page in the section header, behind the text | Full-page shaded tables leave 1 mm gaps and can add a blank page |
| Rounded panels and pills with text | DrawingML `roundRect` with a text box; `adj = radius / min(w,h) × 100000` | Small shapes need zero text insets |
| Photo crops (circle, diamond, chamfer, rounded, capsule) | Pre-mask with PIL at 300 dpi | Crop to the box ratio first |
| Photo overlapped by a block, or straddling a band | Composite into one PNG, or stack an anchored photo and shape | Overlaps don't reflow |
| Rotated tab text | Table cell text direction `btLr`, or shape `vert270` | Rotating the shape doesn't rotate the text |
| Inset frame | Page-anchored rectangle in the header, 10 mm in | Page borders need a footer distance of 10 mm or more |
| Icons | `lucide-static` SVG → 300 dpi PNG, white on an accent circle | Ship the ISC licence |
| Charts | matplotlib at 300 dpi with the design's fonts; ramp built from the deep colour | Pale ramp steps need direct labels |
| Tables | Native Word tables; header row repeats; rows can't split | Square corners only (rounded = an image) |

---

## 6. Checklist before delivering

- [ ] One design, one accent hue, one motif, one corner style, one photo treatment.
- [ ] All small accent text uses the deep shade. No white text on aqua, bright green, or bright teal under 14 pt bold.
- [ ] Body 9.5–10 pt, left-aligned, 60–75 characters per line; exact-point leading; at most 5 text styles per page.
- [ ] Colour pages within budget (25%, or 15% for office print); no 3 identical layouts in a row; openers followed by 2 content pages.
- [ ] Every number right-aligned in tables; the table header repeats; charts in one hue with direct labels.
- [ ] Bleeds reach the trim; text is at least 14 mm from it; nothing overflows its panel.
- [ ] No invented photos, figures or quotes. Missing photos use the design's fallback; missing data has a visible placeholder.
- [ ] Fonts embedded in the PDF. Contents page numbers match.

---

*Full per-design specs (evidence for every slide, all layouts, no-photo fallbacks, DOCX notes):*
- *`.claude/skills/design-picker/references/families/A-navy-annual.md` … `G-teal-market.md`*
- *Measured palettes: `.claude/skills/design-picker/references/palettes.md`*
- *Selection logic and sources: `.claude/skills/design-picker/references/selection-framework.md`*
