# Report Design System, from 7 Pinterest references

Source: `D:\Claudecode\design-refs\` (7 boards, 2026-10-07). Hex values were measured from the image pixels, not estimated.

## 1. What the board has in common
All 7 references use the same approach: **a single strong accent colour on a white or light-grey page, carried by big blocks of colour.** The colour is not in thin borders or icons. Six of the seven are template-shop decks; only the "Rapport Annuel" pin is an annual report. So the visual language is a strong fit, but you have to turn the slide patterns into page layouts yourself.

| Ref | Accent (measured) | Signature move |
|---|---|---|
| Rapport Annuel 2025 | navy `#1A2E5F` (33% of pixels) | Navy cover and section panels; KPI rows of big numbers with tiny captions; one bar chart in shades of a single colour |
| Business Plan (green) | `#5AB14D` (4%) | Mostly black and white photos; green used sparingly on cut-corner photo masks and big numerals |
| PRISM | `#349B86` | Pill and rounded-slab shapes holding text; "break slides" as full colour panels |
| Clinicare | `#4DCCD4` | Light tint panels (`#E9F8F8`), circular photo crops |
| Dark green | `#005B58` / `#177664` | Dark mode; tall vertical colour bars over photos; three-dot motif |
| MARKET | `#01A198` | Thin outline frame inset from the edge; a vertical tab with rotated text; a tag hanging off the top edge |
| DOCORO | `#05369F` | Electric blue blocks that cut through photos; large stat figures |

## 2. Palette tokens
Pick ONE accent family for each report. Every accent has a **deep** shade for text and a **bright** shade for fills.

```
--ink:        #1F2328   /* body text, 15.8:1 on white */
--ink-soft:   #5B6270   /* captions, 6.1:1 */
--paper:      #FFFFFF
--paper-alt:  #F2F3F4   /* page-band grey seen in every ref */
--rule:       #D9DBDB

/* Option A: navy (Rapport Annuel / Docoro) */
--accent-deep:   #1A2E5F   /* 13.1:1, safe for text */
--accent:        #05369F   /* 10.3:1 */
--accent-tint:   #E8EDF7

/* Option B: teal (Prism / Market / dark green) */
--accent-deep:   #005B58   /* 8.0:1, safe for text */
--accent:        #01A198   /* 3.2:1: fills and 24pt+ numerals ONLY */
--accent-tint:   #E6F5F3
```
**Contrast rule (measured):** the bright teal `#01A198`, green `#5AB14D` and aqua `#4DCCD4` all score below 4.5:1 against white. Never use them for body text or for white text on a small chip. Use them for fills, for big numbers, or for white text at 18pt bold and above (teal only).

## 3. Type
The references use geometric sans in heavy weights with strong contrast between heading and body.
- Headings: **Poppins** or **Montserrat** 700, ALL CAPS for section titles (Rapport, Market), tight leading (1.05)
- Body: **Inter** 400, 10–11pt in print, leading 1.45
- Stat numerals: heading font 700, 3–4× body size, in the accent colour
- Labels: 7–8pt, caps, letter-spacing +8%, `--ink-soft`
- Type scale ratio ≈ 1.333 (perfect fourth)

## 4. Layout grammar
- **Split page**: a 1/3 accent panel (title + intro) next to a 2/3 white content area. This is the most repeated pattern on the board.
- **Bleeds**: photos and colour blocks run off at least one page edge. Text never does.
- **Margins**: generous, about 8% of page width; content uses a 12-column grid.
- **Inset frame** (Market): a 0.5pt rule frame 6mm in from the page edge; colour blocks cut across it on purpose.
- **Rhythm**: about every 4–6 pages, a full-colour "break page" with one sentence on it.

## 5. Components
1. **Cover**: full accent field, huge title stacked on 2–3 lines, year in the bright accent, tagline small, 3-word value line bottom-left.
2. **Section opener**: split page, caps title in the panel, one-paragraph lede.
3. **KPI row**: 3–4 numbers, each with a round icon chip above, a big numeral, and a 2-line caption. No boxes around them.
4. **Chart**: bars in shades of one hue (light→deep, most recent = deep), no gridlines, values labelled directly.
5. **Numbered steps**: `01 02 03 04` in rounded tiles with outline chips, joined by a line (Perspectives / Milestones).
6. **Org/structure**: accent header box, children as tinted pills, bullet lists under each.
7. **Quote/callout**: oversized quotation mark, text in `--accent-deep`, set beside a photo cutout.
8. **Data table**: header row in `--accent-deep` with white caps labels, zebra stripes in `--paper-alt`, numbers right-aligned in tabular figures.

## 6. Never do (generic AI-report habits these references avoid)
- No gradient blobs, glassmorphism or rainbow palettes. One hue, several shades.
- No emoji bullets. Icons are single-weight line glyphs inside solid circles.
- No centring everything. Alignment is left and the grid is asymmetric.
- No shadows on cards. Depth comes from colour blocks overlapping photos.
- No walls of bullets. Use a KPI row, steps or a table instead.
- Don't spread the accent thinly. Use it in large areas or not at all.
