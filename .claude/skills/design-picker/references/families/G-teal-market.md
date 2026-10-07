# Ref G: "Market"

Source: `.claude/skills/report-design/references/images/ref-G.jpeg` (736 × 1257 px collage, 12 slide thumbnails in a 2 × 6 grid, each about 308 × 173 px, so 16:9).
Method: I cropped each thumbnail with PIL and upscaled it 4× to view. I measured colours as medians over flat patches, and I measured geometry from pixel edge scans. I tested the DOCX methods by building small A4 files, rendering them with LibreOffice and measuring the PDFs with pymupdf `get_drawings`. Tags: [seen] means visible in a crop, [inferred] means reasoned from what is visible, [uncertain] means a guess.

---

## 1. Identity

Market is a bright corporate template: teal on white, built on one structural idea. A thin light-grey outline frame sits inset from the page edge [seen]. Solid teal shapes are then placed so they deliberately break that frame: a rounded tag hanging from the top edge of the page [seen], full-bleed teal panels and bands that run from the page edge across the frame line [seen], and a pill-shaped vertical tab with rotated caps text [seen]. Headings are short, heavy, all-caps sans words ("MARKET", "PROJECT NAME", "COMPANY PURPOSE") [seen]. Kickers are tiny, widely tracked caps [seen]. The board is photo-led (10 of 12 slides carry stock photography) [seen]. Rounding is everywhere: pill ends, a stadium-shaped frame, rounded cards and circular portraits [seen]. The mood is friendly, tidy and approachable. Its distinctive move is the contrast between a hairline frame and solid teal objects that overlap it.

## 2. Evidence (every slide)

Numbering runs left to right, top to bottom. Crops are saved as `s01.png` … `s12.png` in my scratch dir.

| # | What it shows | Tag |
|---|---|---|
| s01 Cover | Full inset frame. A teal tag hangs from the slide top edge at the left, crossing the frame's top line, 10.4% of slide width wide, extending 26% of width down, with a semicircular bottom and a white bank-building icon. Kicker "BUSINESS TEMPLATE" in tiny tracked caps above "MARKET" in heavy black caps. A photo fills the right 37% inside the frame, with a dark-teal circular gear chip overlapping it. Two-line small body text at bottom left. | [seen] |
| s02 Overview, 2×2 lists | Frame. Kicker "BUSINESS PRESENTATION" at top left. A photo starts at the slide's left edge and crosses the frame. A deep-teal band (#01766E at its clean end) is laid over the photo's lower part with "WWW.EXAMPLE.COM" in white caps. On the right, a 2×2 grid of teal caps subheads (MARKETING / PURPOSE / SERVICES / AGENTS), each with 2–3 small bullets. | [seen] |
| s03 Section / two features | Frame lines run only across the middle band and are interrupted by a central, full-height photo strip carrying a translucent teal vertical band. Inside it, "TRADING" is set in large white caps rotated 90° and reads bottom to top, with "WWW.EXAMPLE.COM" below. Each side has a teal caps subhead, a photo and two lines of text. | [seen] |
| s04 Project title | Frame. Big two-line caps "PROJECT NAME" at left, a paragraph and four bullets. A photo bleeds off the right half and covers the frame. A bright-teal pill button "WWW.EXAMPLE.COM" sits on the photo. A soft grey vertical gradient sits behind the left half. | [seen] |
| s05 Statement | Frame. Centred caps "ENTREPRENEUR" above a full-width photo band that crosses the frame. A wide translucent teal pill holds two centred lines of white text. Footer kicker "WWW.EXAMPLE.COM". | [seen] |
| s06 Three options | Three full-bleed vertical columns: bright teal (0–34%), white (36–66%), light grey #EEEEEE (67–100%). A thin grey stadium-shaped outline (rounded-end frame) is inset and crosses all three. Each column has a centred sentence-case "Lorem option" heading and four centred lines. The teal column uses white text. No photo. | [seen] |
| s07 Testimonials | A photo band (office) fills the top 2/3 and bleeds. Two rounded-square teal cards (corner radius about 15% of card width) hang over it. A circular portrait overlaps each card's top edge. The cards carry centred white text and a name/role line. The frame is faintly visible in the white lower third. | [seen] |
| s08 Quote | Frame. "SLIDE." in heavy caps with the kicker "PRESENTATION" below. A tall teal tag with a round bottom hangs from the top edge (about 21% of width wide, 64% of height long) and holds a white quotation mark and four lines of white text. A cut-out portrait sits in an arch-shaped (top-rounded) frame. "WWW.EXAMPLE.COM" in black is rotated 90° next to it. Four bullet items use bright-teal circle chips. | [seen] |
| s09 Team | The frame covers only the top half, with a grey-to-white gradient inside. Its bottom line runs through four circular portraits (a "string of beads"). Each portrait carries a small teal icon chip on its lower edge, then a bold name and a tiny role. The centred caps line reads "LOREM IPSUM DOLOR SIT AMET TEAM MEMBERS". | [seen] |
| s10 Purpose, two images | Frame. A teal tag hangs off the top edge at the right (14% of width wide, 17% of width long, right edge 25 px inside the frame) with a white icon. Caps "COMPANY PURPOSE" with a teal tracked kicker "WWW.EXAMPLE.COM" under it. Two equal photos, each with two lines of text below. | [seen] |
| s11 Section opener | A photo fills the left 65%. White panel on the right with a short paragraph. A D-shaped bright-teal panel (flat left end at the slide edge, round right end) crosses the frame and photo, with "COMMERCE" in white caps. | [seen] |
| s12 Points / closing | Photo on the left 56%. A full-bleed bright-teal panel covers the right 44%, with a small triangular notch pointing left. Inside: "POINTS." in white caps and three white check-chips, each with two lines of text. On the left, a vertical teal pill tab (4.9% of width wide, 61% of height tall) holds rotated white caps "BUSINESS PRESENTATION". No frame is visible. | [seen] |

Patterns across the board:
- The frame is present on 10 of 12 slides, but its geometry varies: full rectangle (s01, s02, s04, s05, s08, s10, s11), partial middle band (s03), stadium (s06), top half (s09) [seen].
- Something solid always crosses the frame [seen].
- Content is left-aligned on narrative slides and centred on statement, option and team slides [seen].

## 3. Palette (measured)

Measured on the 12 slide crops. Pixel shares come from assigning each slide pixel to its nearest class. The board-wide figure in CONTEXT.md (6%) includes the grey collage background.

| Role | HEX | Source | On white | White on it | #111111 on it |
|---|---|---|---|---|---|
| Accent bright (fills) | `#02A19A` | flat fills s01 tag #01A29A, s06 column #02A29A, s10 tag #04A19A, s12 panel #02A19A [seen] | 3.20 | 3.20 | 5.91 |
| Accent deep (measured) | `#01766E` | s02 band, clean left end [seen]. The band darkens to #023F3A over the photo [seen]; the s01 gear chip is ≈#116B54 [seen, JPEG noise] | 5.50 | 5.50 | 3.43 |
| Accent deep, text token (proposed) | `#00625C` | darker than anything flat on the board, chosen to give 7:1 [inferred] | 7.24 | 7.24 | 2.61 |
| Overlay teal (translucent bands on photos) | `#058A80` | s05 pill, s07 cards (#03938C), s03 strip (#07908A) [seen] | 4.24 | 4.24 | 4.45 |
| Tint, neutral | `#EEEEEE` | s06 third column [seen]. Grey gradients run #F6F6F6→#DEDEDE (s04, s08, s09) [seen] | 1.16 | — | 16.28 |
| Tint, teal (proposed) | `#E6F6F5` | not on the board [inferred, for callouts and table zebra] | 1.11 | — | 16.96 |
| Ground | `#FFFFFF` | [seen] | — | — | 18.88 |
| Ink | `#111111` | heading pixels median #090909 [seen]. #111111 is proposed for print | 18.88 | — | — |
| Secondary text | `#5C6166` (proposed) | body text is too small to measure; blurred pixels read #A7A7A7–#B9B9B9, which is lighter than the true colour [uncertain] | 6.26 | — | — |
| Frame line | `#B4B4B4` at 0.5 pt (proposed) | the line is under 1 px and antialiased, measuring #C8C8C8–#D3D3D3, so the true line is darker and thinner [inferred]. #B4B4B4 at 0.5 pt reproduces the look in a render | 2.07 (decorative, exempt) | — | — |

Area share on the slides (nearest class): white 39.5%, light grey 24.4%, mid grey and photo neutrals 18.0%, accent bright 11.0%, accent deep and overlay 5.2%, ink 2.0%. Pixels with any teal chroma make up 15.2%. Per slide this ranges from 0.8% (team, s09) to 46.5% (s12 panel). In report terms: about 10–15% teal overall, concentrated in one or two big shapes per page, never spread thinly.

Contrast rules (computed, WCAG 2.x):
- `#02A19A` bright: 3.20:1 against white either way. Use it for fills, large numerals, and text ≥14 pt bold or ≥18 pt regular (the large-text 3:1 rule). On a bright fill, prefer **ink text** (5.91:1, passes AA) over small white text.
- The board's small white text on bright teal (s06, s12) fails AA: do not copy.
- `#01766E` deep: 5.50:1, AA for body text, and white on it passes AA.
- `#00625C`: 7.24:1, AAA. Use it for teal caps subheads at 8–10 pt and for text-bearing panels with white text.
- Deep `#00625C` on `#EEEEEE` is 6.24:1, and on teal tint 6.5:1. Secondary `#5C6166` on `#EEEEEE` is 5.39:1.

## 4. Typography

Observations [seen]:
- Titles: heavy sans, all caps, slight positive tracking, set in short words. Cap height of "MARKET" is 10 px on a 173 px slide (5.8% of height, about 31 pt cap height on a 7.5 in slide, so roughly a 44 pt font).
- Two-line titles are tight: "PROJECT NAME" has leading of about 1.05.
- Some titles end in a full stop ("SLIDE.", "POINTS.").
- Kickers are tiny caps with very wide tracking (about +20%), in ink or teal ("BUSINESS TEMPLATE", "WWW.EXAMPLE.COM").
- Subheads are small teal caps with wide tracking (MARKETING, REMOTE SIGNING).
- Option headings are sentence case, semibold (s06).
- Body text is small and light, set 2–4 lines at a time.
- Rotated text appears both in display caps ("TRADING") and as tiny tracked caps on tabs.

Best-guess family [uncertain]: a neo-grotesque or humanist bold, slightly narrower than Montserrat (something like Open Sans ExtraBold or Nunito Sans Black). I compared upscaled "MARKET" against renders: Montserrat Bold is wider than the original, and Inter Display Bold with +6% tracking is close in width but lighter. The thumbnail cannot settle it.

OFL substitutes. Montserrat, Poppins and Inter are already installed on this machine (Montserrat and Poppins as TTF in `/root/.fonts`).
- **Headings: Montserrat Bold / ExtraBold** (OFL). It is installed, embeds in LibreOffice PDFs (verified: `Montserrat-Bold` embedded in a test render) and matches the template's geometric-corporate genre. npm sources: `@expo-google-fonts/montserrat` (v0.4.2) **ships .ttf files**, which is what LibreOffice and DOCX need. `@fontsource/montserrat` ships only .woff/.woff2, which is not suitable for LibreOffice.
- Closer-width alternative: **Inter Display ExtraBold** with +4% tracking (installed).
- **Body: Inter Regular/Medium** (OFL; installed; npm `@expo-google-fonts/inter` for TTF).

Type roles for A4 print. Sizes are scaled from slide proportions and adjusted for reading distance [inferred]:

| Role | Font | Size / leading | Case, tracking | Colour |
|---|---|---|---|---|
| Display (cover) | Montserrat ExtraBold | 40 / 42 pt | CAPS, +3% (w:spacing 24) | ink |
| H1 (section opener) | Montserrat Bold | 28 / 30 pt | CAPS, +3% | white on deep, or ink |
| H2 (page title) | Montserrat Bold | 18 / 20 pt | CAPS, +4% | ink |
| H3 (subhead) | Montserrat Bold | 9 / 12 pt | CAPS, +12% (w:spacing 22) | deep `#00625C` |
| Kicker | Montserrat SemiBold | 7.5 / 9 pt | CAPS, +20% (w:spacing 30) | secondary or deep |
| Body | Inter Regular | 9.5 / 14 pt | sentence | ink |
| Lead | Inter Regular | 12 / 17 pt | sentence | ink |
| KPI numeral | Montserrat Bold | 30 / 30 pt | lining figures | deep (or bright at ≥24 pt) |
| Caption / source | Inter Regular | 7.5 / 10 pt | sentence | secondary |
| Tab / rotated label | Montserrat Bold | 7.5 pt | CAPS, +20% | white on bright, at 7.5 pt only on deep (white on bright needs ≥14 pt bold) |
| Footer / page number | Montserrat SemiBold | 7 pt | CAPS, +15% | secondary |

Caps usage: caps for display, H1, H2, H3, kickers and tabs. Sentence case for body text, option headings and names. Ratio is about 1.5 between steps (9 → 12 → 18 → 28 → 40). Drop the trailing full stop on headings except, if wanted, one closing page.

## 5. Layout recipes, A4 portrait (210 × 297 mm)

Shared grid for all pages (unless a recipe says otherwise):
- **Frame:** rectangle 10,10 → 200,287 mm (190 × 277), 0.5 pt `#B4B4B4`, no fill. A 3.9%-of-width inset on the slides scales to about 13 mm on a 13.33 in slide. 10 mm is chosen for A4 [inferred].
- **Text area:** left 24, right 24, top 28, bottom 26 mm, giving 162 × 243 mm. Text starts about 14 mm inside the frame, which matches the slides, where text sits about 2× the frame inset from the edge [seen s02, s10].
- **Footer:** inside the frame, baseline about 280 mm. Page number at right (x 186), running title at left (x 24), 7 pt caps.
- **Tag (default):** 16 × 34 mm, top at y = 0 (page edge), bottom semicircle r = 8 mm. Placed at x = 170–186 (right-aligned to the text margin, as on s10) or x = 24–40 (s01). It carries a white glyph or a 2-digit section number, Montserrat Bold 11 pt, centred at y ≈ 25 mm.
- **Vertical tab (default):** 9 × 70 mm pill, centred on the left frame line (x 5.5–14.5), y 113–183. Rotated text reads bottom to top.
- **Columns:** 12 columns of 162 mm with a 6 mm gutter (col ≈ 8 mm).

**R1 Cover**
- Frame.
- Long tag at x 24–42, 18 mm wide, y 0–64 mm, white mark or logo at y ≈ 52.
- Kicker (report type, 7.5 pt) at y 78.
- Title Display 40 pt, 1–3 lines, y 84–130.
- Subtitle Lead 12 pt at y 138, max 110 mm wide.
- Photo block inside the frame, 10–200 × 160–287 (full frame width, sits on the frame bottom), with a 16 mm deep-teal circle chip overlapping the photo's top edge at x 168, y 152.
- Author, date and client (8 pt) at bottom-left above the photo, y 148.

**R2 Contents**
- Frame. Default tag at right with "00".
- H2 "CONTENTS" at y 40.
- Entries every 16 mm from y 62: number Montserrat Bold 18 pt bright teal (x 24–40), title H3-style caps 10 pt ink (x 44), one-line description 8.5 pt secondary, page number right-aligned at x 186 (9 pt bold).
- 0.5 pt `#D9D9D9` rule under each entry.
- Vertical tab on the left frame line carrying the report title.

**R3 Section opener (panel crossing the frame, s12/s11)**
- Frame.
- Full-bleed panel at x 118–210, y 0–297, deep `#00625C`. It covers the frame on three sides.
- Inside the panel (x 128–196): section number Montserrat Bold 48 pt white at y 40; H1 28 pt caps white at y 70, max 3 lines; lead paragraph 11 pt white at y 120; 3 check-chip points (6 mm white circle with deep tick, 9.5 pt white text) from y 170, every 24 mm.
- Small notch (4 × 8 mm triangle, same fill) on the panel's left edge at y 210.
- Left area (x 24–108): a photo inside the frame, or the no-photo fallback (§7).
- Alternative (s11 D-shape): a pill from x −30 to 120, y 120–150 mm, with the left end off-page, bright fill, H1 in ink 24 pt.

**R4 Executive summary / KPI (s02)**
- Frame.
- Band from the page's left edge across the frame: x 0–120, y 30–58, deep fill, H2 "EXECUTIVE SUMMARY" in white 18 pt at x 24.
- Lead paragraph 12 pt at y 70–110 (x 24–186).
- KPI row at y 122: 3 or 4 cells across 162 mm. Each cell has an 8 mm bright circle chip with a white glyph, the numeral 30 pt deep, and a label 7.5 pt caps secondary (2 lines). No boxes.
- 2 × 2 findings grid at y 175: H3 teal caps subhead plus 2–4 bullets at 9.5 pt, columns of 78 mm with a 6 mm gutter, rows 50 mm.

**R5 Narrative**
- Frame. Default tag at right with the section number.
- H2 at y 32, kicker below it in deep teal caps (the running section name, replacing "WWW.EXAMPLE.COM").
- Text column x 24–150 (126 mm, about 70 characters per line at 9.5 pt Inter).
- Rail x 156–186 (30 mm) for margin notes, 8 pt, deep teal, each topped by a 0.5 pt teal rule.
- H3 subheads with 10 pt space before. Pull figures or inline images span the full 162 mm.

**R6 Chart**
- Frame. H2 plus kicker.
- Chart image 162 × 95 mm at y 52, drawn as a 300 dpi PNG. Bars in `#CFCFCF`, the highlighted series bright `#02A19A`, the current period deep `#00625C`. Direct labels, no gridlines, 7.5 pt axis labels in Inter.
- Caption and source 7.5 pt secondary at y 150.
- Key takeaway in a D-shaped pill from the left page edge: x −30 to 140, y 165–189, bright fill, 12 pt bold **ink** text (5.91:1), with a 24 mm left inset so the text starts at x 24.
- Supporting paragraph below, from y 200.

**R7 Data table** (no table on the board, so the style is [inferred] from the system)
- Frame. H2.
- Table 162 mm wide.
- Header row: deep `#00625C` fill, white Montserrat Bold 7.5 pt caps, +10% tracking, 7 mm tall.
- Body rows 6.5 mm, Inter 8.5 pt, 0.5 pt `#D9D9D9` bottom rule. Optional zebra in teal tint `#E6F6F5`.
- Numbers right-aligned, tabular figures. First column semibold.
- Totals row: 1 pt deep rule on top, bold.
- Source line 7 pt secondary.

**R8 Two/three-option comparison (s06)**
- No standard frame on this page.
- Three full-height columns that bleed top and bottom: x 0–70 deep `#00625C` (recommended option, white text); x 70–140 white; x 140–210 `#EEEEEE`.
- Stadium outline: x 14–196, y 70–230, 0.5 pt `#8C8C8C`, end radius 80 mm. It crosses all three columns.
- In each column, text measure 50 mm, centred at y 110: option heading Montserrat SemiBold 14 pt sentence case; 3–5 lines of 9.5 pt; a "fit / cost / risk" mini list.
- Page H2 at y 30 inside column 1 (white) or above as a kicker.
- Two-option variant: x 0–105 deep, x 105–210 `#EEEEEE`, stadium x 14–196 kept.

**R9 Team (s09)**
- Half-frame: a box x 10–200, y 10–120 with a vertical gradient fill `#EFEFEF` → `#FFFFFF`. Draw it as a solid `#F2F2F2` in DOCX to avoid print banding.
- H2 centred at y 60.
- Its bottom line at y 120 runs through 4 circular portraits (28 mm diameter), centres every 41 mm from x 43.5. A 7 mm bright chip with a white glyph sits on each portrait's lower edge.
- Name 9 pt bold centred at y 146, role 7.5 pt secondary, 2-line bio 8 pt.
- A second row repeats on a hairline at y 200.

**R10 Quote / testimonial (s08, s07)**
- Frame. A tall tag hangs from the page top: x 112–176 (64 mm wide), y 0–120, bottom radius 32. Deep fill.
- Inside: a quotation mark Montserrat Bold 36 pt white at y 22, quote text 13 / 18 pt Inter Medium white (max 6 lines), attribution 8 pt caps at y 104.
- Left: H2 plus kicker at y 32. A portrait in a top-rounded arch (round2SameRect, 50 × 70 mm) at x 24, y 140.
- Rotated kicker (name or role) beside the arch.
- Bullets with 6 mm bright chips at x 112–186, y 200+.
- Multi-quote variant: two rounded cards, deep fill, 76 × 90 mm, corner radius 12 mm, with a 24 mm circle portrait overlapping each card's top edge by 50%.

**R11 Closing / contact (s12)**
- Vertical tab on the left (x 14–23, y 70–227) carrying the report title.
- Right panel x 118–210 full-bleed bright `#02A19A`. "THANK YOU" or "NEXT STEPS" 28 pt caps in ink or white (≥14 pt bold, so white passes 3:1).
- Three check-chips with 10 pt **ink** text.
- Contact block 9 pt, white on the panel only at ≥14 pt bold, otherwise ink.
- Left area: photo, or the fallback.

## 6. Signature components (build specs)

1. **Inset frame.** Rectangle 190 × 277 mm at 10,10, 0.5 pt `#B4B4B4`, no fill. It stays constant on every text page. It is omitted on R8, the closing page and full-panel openers. It sits at the lowest z-order so teal shapes visibly cover it. Text never touches it: keep 14 mm clear inside.
2. **Hanging tag.** A rectangle with only its bottom corners rounded (round2SameRect flipped vertically; radius = width/2), anchored at page y = 0 so it starts at the paper edge and crosses the frame's top line. Sizes: page tag 16 × 34 mm, cover tag 18 × 64 mm, quote tag 64 × 120 mm. Fill bright for pure markers, deep for tags with text. Content: one white glyph (6 mm) or a 2-digit number at 11 pt bold. Position: aligned to the text margin (x 24 or right edge at x 186).
3. **Vertical rotated tab.** A pill (roundRect, adj 50%) 9 × 70 mm, centred on the left frame line (x 5.5–14.5), vertically at y 113–183 or on the page midline. Text: Montserrat Bold 7.5 pt caps, +20% tracking, rotated 270° (reads bottom to top, as on the board). Use white text only on a deep fill at this size.
4. **Panel crossing the frame.** A solid deep or bright rectangle anchored to the page that runs to at least one page edge (full bleed), covering the frame line where it crosses. Variants: right panel (x 118–210, full height), top band (x 0–120 × 28 mm), D-shaped pill (left end off-page, right end round). Text inside gets ≥10 mm padding from the panel edge and stays inside the text area.
5. **Option columns plus stadium outline.** Three equal full-bleed columns (deep / white / `#EEEEEE`) with a stadium (roundRect, adj 50%) hairline crossing all of them. The recommended option always goes in the deep column.
6. **Check-chip list.** A 6 mm circle (white on panel, bright on white) with a tick glyph. Text 9.5 pt, 2 lines max, 24 mm pitch.
7. **Icon chip.** An 8 mm bright circle with a white line glyph, used on KPI cells, team portraits and bullets.
8. **Portrait bead line.** Circular portraits threaded on a 0.5 pt hairline, which is the frame's bottom edge or a free rule.
9. **Kicker line.** 7.5 pt caps, +20% tracking, directly under or over an H2. It replaces the board's "WWW.EXAMPLE.COM" with meaningful text (section name, date, client).

## 7. Photo dependency

The board is heavily photo-dependent: 10 of 12 slides use stock photos, and only s06 (options) and s09 (team, which needs portraits) work without scenery [seen]. Reports often have no photography, so every layout needs a fallback:

| Layout | Needs photo? | No-photo fallback |
|---|---|---|
| R1 Cover | yes (lower block) | Replace the photo block with a deep `#00625C` block (10–200 × 160–287) holding a 3-line value statement in white 14 pt bold, or a bright block with ink text. Optional: a large outline stadium in 0.75 pt white inside it. |
| R2 Contents | no | — |
| R3 Section opener | left area | `#EEEEEE` field (x 10–118 inside the frame) with the section number at 120 pt Montserrat Bold in white, or a teal-tint numeral, as a graphic. |
| R4 Exec summary | no (band only) | — |
| R5 Narrative | optional inline image | A chart, a KPI pair, or a pull quote in a teal-tint box. |
| R6 Chart / R7 Table | no | — |
| R8 Options | no | — |
| R9 Team | portraits | Initials in 28 mm bright circles (Montserrat Bold 16 pt white), same bead line. |
| R10 Quote | portrait arch | Fill the arch with teal tint `#E6F6F5` and a large deep quotation mark, or drop the arch and let the tag carry the quote. |
| R11 Closing | left area | `#EEEEEE` field with the contact block, or the vertical tab only on white. |

Rule: never substitute generic stock (laptop, plant, smiling headset). A flat grey or tint field is cleaner than an irrelevant photo.

## 8. Best for / avoid for

- **Best for:** business plans, market or opportunity analyses, sales and service proposals, capability statements, SME or startup annual reviews, project pitch reports, partner or investor briefings, internal strategy summaries for non-specialist readers.
- **Industries:** professional services, real estate and property, fintech and retail banking marketing, logistics and trade, B2B SaaS, consultancies.
- **Tone:** friendly corporate, optimistic, tidy, approachable.
- **Audience:** clients, prospects, executives, investors.
- **Length:** short to medium (8–30 pages). It works best with 1–2 idea units per page.
- **Avoid for:**
  - Dense academic, technical or regulatory documents, and long data appendices (the frame and generous margins cut text area to 162 × 243 mm, and caps headings tire over many pages).
  - Heavily cited research.
  - Sombre or crisis topics, where bright teal reads too cheerful.
  - Medical or clinical documents (ref E/F fit better).
  - Luxury and editorial branding, where a hairline frame reads as template.
  - Documents that will be heavily edited by others in Word (the floating shapes are easy to break).

## 9. Do not copy

- **"WWW.EXAMPLE.COM" as decoration on every slide.** Filler that carries no information. Use a meaningful kicker.
- **Small white text on bright teal** (s06, s12, s07 cards). It measures 3.20:1 and fails AA. Use a deep fill or ink text.
- **Translucent teal overlays on photos** (s03, s05, s07). They produce muddy colour and are unpredictable in print and in LibreOffice. Use solid fills next to or over photos instead.
- **Stock-photo clichés** (laptop and plant, headset smile, hands on blueprints). They read as template and cost credibility in a report.
- **Headings with trailing full stops** ("SLIDE.", "POINTS."): a slide-deck mannerism.
- **Centred multi-line body text** (s05, s06, s07) slows reading. Centre only short headings and figures.
- **Changing the frame geometry on every page** (partial, stadium, half). In a report the frame is the constant. Reserve variants for one or two special pages (options, team).
- **Grey gradients behind text.** They band in print and PDF. Use flat `#F2F2F2`.
- **Generic icons** (bank building, gear) in tags. Use a section number, or a glyph that means something.

## 10. DOCX implementability

Tested on this machine: LibreOffice headless to PDF, measured with pymupdf `get_drawings`. Test scripts are in my scratch dir (`refG/frametest.py`, `ft2.py`–`ft6.py`).

**Frame bug: root cause found.** `w:pgBorders offsetFrom="page" space="28"` renders correctly (all edges at 10.0 / 287.0 mm) **unless the section has a footer part with a footer distance under the border offset**. LibreOffice moves the bottom border down so the footer area stays inside the border. Measured bottom-edge y by footer distance:

| footer_distance | footer part present | bottom edge y |
|---|---|---|
| 0 mm | yes | 296.9 mm (page edge) |
| 5 mm | yes | 291.9 mm |
| 10 mm | yes | 286.9 mm |
| 12 mm | yes | 287.0 mm |
| 0 mm | no footer | 287.0 mm |

Header distance 0 does **not** move the top edge.

The engine's `opener()` calls `section(..., running=None, frame=True)`, and `_header_footer` then sets `footer_distance = Mm(0)` while still leaving a (tiny) footer paragraph (`reportkit.py` line 476). That is exactly the failing case.

`offsetFrom="text"` is worse: with a footer at 12 mm, the bottom edge lands at 295 mm.

There is a second limit. Page borders are painted **above** all shapes, including in-front shapes: a teal panel crossing a red test border left the border visible on top. So pgBorders cannot give Market's "panel crosses the frame" effect at all.

**Recommended frame method: a page-anchored DrawingML rectangle in the section header**, `behindDoc=1`, lowest `relativeHeight`. Measured result: exactly 10.0, 10.0 → 200.0, 287.0 mm on every page, independent of margins and footer, and covered by later shapes as intended. If pgBorders are kept for other styles, the minimal engine fix is to set `footer_distance` ≥ 11 mm (keeping the tiny paragraph) when `frame=True`.

Load-bearing shape XML. It goes in a run in the header paragraph; mm × 36000 = EMU. The namespaces were declared inline in the test and LibreOffice accepted them.
```xml
<w:drawing><wp:anchor behindDoc="1" relativeHeight="1" simplePos="0" locked="0" layoutInCell="1" allowOverlap="1" distT="0" distB="0" distL="0" distR="0">
 <wp:simplePos x="0" y="0"/>
 <wp:positionH relativeFrom="page"><wp:posOffset>360000</wp:posOffset></wp:positionH>
 <wp:positionV relativeFrom="page"><wp:posOffset>360000</wp:posOffset></wp:positionV>
 <wp:extent cx="6840000" cy="9972000"/><wp:effectExtent l="0" t="0" r="0" b="0"/><wp:wrapNone/>
 <wp:docPr id="101" name="Frame"/><wp:cNvGraphicFramePr/>
 <a:graphic><a:graphicData uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">
  <wps:wsp><wps:cNvSpPr/><wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="6840000" cy="9972000"/></a:xfrm>
   <a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/>
   <a:ln w="6350"><a:solidFill><a:srgbClr val="B4B4B4"/></a:solidFill></a:ln></wps:spPr>
   <wps:bodyPr/></wps:wsp></a:graphicData></a:graphic></wp:anchor></w:drawing>
```

| Component | Method | LibreOffice result (tested?) | Notes |
|---|---|---|---|
| Inset frame | Shape (DrawingML rect in header) | exact, repeats per page (**tested**) | Preferred. pgBorders only with footer_distance ≥ 11 mm, and it can't be overlapped. |
| Hanging tag | Shape: `round2SameRect`, `flipV="1"`, adj1=50000, adj2=0, anchored at y=0 | correct, rounded bottom, crosses the frame (**tested**) | The glyph is a small inline PNG in a text box, or a text number. Word rendering [uncertain, not tested]. |
| Vertical rotated tab | Shape: `roundRect` adj=50000 + text box `bodyPr vert="vert270"` | correct, reads bottom to top, Montserrat embedded (**tested**) | Native fallback: table cell `w:textDirection btLr` with cell shading (engine already has `text_direction`). Square corners only. Needs fixed table layout or the cell widths are ignored (seen in test: the cell rendered 85 mm wide). |
| Panel crossing frame | Shape: rect anchored to page, higher z than the frame | covers the frame line (**tested**) | Put long text in normal flow (a table cell in the text area) rather than in the shape's text box. LibreOffice text boxes don't flow or paginate. |
| D-shaped pill (s11) | Shape: `roundRect` adj=50000 with x negative (left end off-page), or `round2SameRect` rot=90° | both correct (**tested**) | Avoid `flowChartDelay`: it renders as a half-ellipse when wide (**tested**). Text in a rotated shape rotates too, so use the off-page pill with a left inset. |
| Stadium outline (s06) | Shape: `roundRect` adj=50000, noFill, 0.5 pt line | correct (**tested**) | — |
| Option columns | Shapes (3 full-bleed rects) + text in a 3-column borderless table | rects tested; table native | Or a zero-margin section with a 3-cell table shaded per cell (native, but it can't bleed past the page margins unless margins are 0). |
| Notch triangle | Shape `triangle` rot=270 | renders, small (**tested**) | Optional; drop if fragile. |
| Rounded cards (s07) | Shape `roundRect` adj≈18000 | correct (**tested**) | Card text in a text box: keep it short (≤6 lines). |
| Circular portraits, arch | Image: pre-crop to a circle or arch PNG with alpha (PIL), inline or anchored | — | Safer than DrawingML picture geometry masks. |
| Icon chips, check-chips | Image (PNG 300 dpi) or a shape `ellipse` + glyph text | — | Images are the most robust. |
| KPI row, 2×2 grid, contents list, table | Native tables (borderless, cell padding, shading, bottom rules) | native | Engine already supports these patterns. |
| Gradients | Avoid; flat fill `#F2F2F2` | — | — |
| Kicker tracking | Native `w:spacing` (twentieths of a point: 30 = +1.5 pt) | native | — |

General shape cautions [inferred]:
- Put recurring page furniture (frame, tags, tab) in the **section header**, so it repeats and doesn't shift with body reflow. Use per-section headers for page-specific panels (one section per opener).
- Anchors in the body move with their paragraph. Always use `relativeFrom="page"`.
- Word normally wraps `wps` in `mc:AlternateContent` with a VML fallback. Plain `wps` in `w:drawing` rendered in LibreOffice; Word 2010+ behaviour is [uncertain, not tested here].

## 11. Quick-select card

- **Name:** Market (ref G): teal frame-break corporate.
- **Mood:** friendly, clean, optimistic business.
- **Accent:** `#02A19A` fills / `#00625C` text (7.24:1), on white with `#EEEEEE` neutrals.
- **Best for:** business plans, proposals, market analyses, capability statements, 8–30 pages.
- **Needs photos?** It wants them (10/12 slides), but every layout has a flat-colour fallback.
- **Signature move:** a hairline frame 10 mm in, broken by a hanging tag, a rotated pill tab and full-bleed teal panels.
