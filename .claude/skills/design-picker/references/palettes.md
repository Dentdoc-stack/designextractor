# Colour system for the 7 reference boards (ref-A … ref-G)

Output files: `.claude/skills/design-picker/assets/palettes.json` (tokens) and `.claude/skills/design-picker/scripts/palettes_measure.py` (the script that produced every number here). Run `.venv/bin/python -I .claude/skills/design-picker/scripts/palettes_measure.py tables`, then the same with `derive` (which rewrites `palettes.json`).

Tags: **[seen]** means measured from pixels or visible on the board. **[inferred]** means a conclusion or design decision drawn from what was measured. **[uncertain]** means a measurement that is limited by the JPEG or the mock-up rendering.

## 0. Summary

- The 7 boards reduce to **6 palette families**: **navy** (A), **royal** (F), **teal** (G and D), **forest** (B), **aqua** (E) and **green** (C). D and G are near-duplicates (ΔE2000 5.9 between their accents), so they merge, and G `01A19A` is kept as the canonical colour. [inferred]
- Only **navy `1C2E60`, royal `0339A6` and forest `005A58`** are safe as text colours on white and on the grey band (≥ 7:1). Teal `01A19A` (3.20), green `57B848` (2.51) and aqua `4CC0CB` (2.16) **fail 4.5:1**. Use them as fills, or as numerals at 24 pt and above. Each of these families gets an OKLCH-darkened `accent_deep` at ≥ 7:1 on `paper_alt`. [seen + inferred]
- The darkened teal `005955` is effectively the same colour as B's measured slab colour `005A58` (ΔE2000 1.0). The 7:1 teal is therefore a colour that already appears on the boards, not an invented one. [seen]
- **Engine warning:** `scripts/reportkit.py` currently uses `C["accent"]` for 7.5 pt Kicker and Heading 3 text, for quotes and for numerals. With the teal, aqua or green families, `accent` is a fill colour that fails contrast. Those styles must read `accent_deep` instead (see §6.2). [seen in code]
- **Print:** the grey bands measured on the boards (`F2F3F4`, `F5F5F5`) are only 4 % K. That is at the edge of what an office printer reproduces. The derived `paper_alt` and `accent_tint` values are darkened to at least 6 % and 7 % ink (§7). [inferred]

## 1. Method

1. **Separating page content from the Pinterest background.** Each board was split into its thumbnails. A, B and C use a recursive XY-cut on a per-board "background-like" mask: A is neutral grey 120–228, B is the board green `023F3A` or darker, and C is neutral grey 120–226. D, E, F and G use hand-fixed grids taken from row and column gutter profiles. I drew every set of boxes onto the board and checked the overlay by eye. Each box is then inset by 3–6 px, which drops drop-shadows and F's grey mock-up frames. Measured area: A 14 boxes (some spreads are split, all inside the page), B 11, C 24, D 27, E 24, F 30, G 12. Pixels on the board background are never counted. [seen]
2. **Flat versus photo.** A pixel counts as *flat* when the local 5×5 standard deviation (maximum over R, G and B) is below 4. Flat pixels are graphic fills (slabs, panels, page ground). Non-flat pixels are photos, small text and anti-aliased edges, and they are excluded from the colour clusters. This keeps skin tones and photo greens out of the accent measurements.
3. **Chromatic clusters.** Flat pixels with CIELAB C* > 12 go into k-means (k = 7, k-means++ seeded, in Lab space, 20 k-pixel sample). Clusters closer than ΔE76 7 are merged. Each reported hex is the per-channel **median** of the cluster's members.
4. **Tints.** Flat pixels with L* > 88, 3 ≤ C* ≤ 20 and a Lab hue within 25° of the main cluster's hue.
5. **Neutrals.** Flat pixels with C* < 5, banded by L*: paper ≥ 97.5, page grey 90–97.5, light grey 75–90, mid grey 40–75, dark < 40. The table reports the band median (the mode is also computed).
6. **Ink.** The median of the darkest 2 % of near-neutral pixels (C* < 8), flat or not. Body text at 474–736 px board width is 2–4 px tall, so its cores never reach the true ink colour. **All ink and secondary-grey values are [uncertain]**, and the ink token is a design decision (§5).
7. **Colour maths.** WCAG 2.x relative luminance and contrast `(L1+0.05)/(L2+0.05)`. The contrast ratio is symmetric, so "colour on white" and "white text on the colour" are the **same number**; the tables give it once and add *ink on the colour* instead. ΔE is CIEDE2000. Derived shades are built in **OKLCH**: hue fixed, lightness moved, and chroma reduced by bisection only when the colour leaves the sRGB gamut. Nothing is mixed with black. Colour-vision checks use Machado et al. 2009 (severity 1.0, applied in linear RGB) for deutan and protan simulation.
8. **Print model.** The script uses a naive RGB → CMYK conversion (full GCR, no ICC profile). No CMYK ICC profile is installed in this environment. The naive conversion understates total ink under dark colours compared with a real FOGRA or GRACoL conversion, so treat its TAC figures as **lower bounds**. [uncertain]

**Limits.** All boards are re-compressed Pinterest JPEGs of rendered mock-ups. A's spreads sit under simulated lighting, so its page reads `E7E6E7` when the design intent is probably white or a very light grey. F's photo pages carry blue duotone washes (`325AAA`, `5A73A4`, `8397CA`, `B0BFDD`), which the clusters capture as "blue" even though they are photo overlays. Expect roughly ±2–4 ΔE2000 on any single value. [uncertain]

**Cross-check.** These values agree with the accents in CONTEXT.md, which were measured a different way (ΔRGB 30). ΔE2000: A 0.4, B 0.6, C 2.3, D 0.5, E 3.3, F 1.2, G 0.8. E's tint `E0FEFE` differs from DESIGN-user's `E9F8F8` by ΔE 4.9. E's tint varies from slide to slide, and both values are plausible. [seen]

## 2. Per-board measurements

"area %" is the share of all in-thumbnail pixels. "% of chromatic flat" is the share among flat chromatic pixels only. A FAIL on a light colour is expected: those colours are grounds, not text.

#### ref-A — 14 thumbnails, 596,903 px; flat 49%, photo/text/edges 51%; page grey used for contrast: #E7E6E7

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `172A5C` | 26.8 | 95 | 0.301 0.093 266 | 13.80 AAA | 11.08 AAA | 1.19 FAIL | 75/54/0/64 |
| chromatic cluster | `8295B3` | 0.7 | 3 | 0.666 0.050 260 | 3.04 large/graphics | 2.45 FAIL | 5.42 AA | 27/17/0/30 |
| chromatic cluster | `3B548A` | 0.7 | 2 | 0.452 0.094 264 | 7.44 AAA | 5.98 AA | 2.21 FAIL | 57/39/0/46 |
| accent tint | `E3E2E9` | 0.2 |  | 0.916 0.009 293 | 1.29 FAIL | 1.03 FAIL | 12.81 AAA | 3/3/0/9 |
| neutral page grey (L* 90-97.5) | `E7E6E7` | 12.2 |  | 0.926 0.002 326 | 1.24 FAIL | 1.00 FAIL | 13.24 AAA | 0/0/0/9 |
| neutral light grey (L* 75-90) | `DBDADE` | 6.7 |  | 0.890 0.006 298 | 1.39 FAIL | 1.12 FAIL | 11.85 AAA | 1/2/0/13 |
| neutral mid grey (L* 40-75) | `ADAFB4` | 0.6 |  | 0.754 0.007 269 | 2.19 FAIL | 1.76 FAIL | 7.51 AAA | 4/3/0/29 |
| neutral dark (L*<40) | `363438` | 0.6 |  | 0.329 0.007 308 | 12.32 AAA | 9.89 AAA | 1.34 FAIL | 4/7/0/78 |
| ink estimate [uncertain] | `1B1C22` |  |  | 0.228 0.012 278 | 16.99 AAA | 13.65 AAA | 1.03 FAIL | 21/18/0/87 |

#### ref-B — 11 thumbnails, 553,428 px; flat 59%, photo/text/edges 41%; page grey used for contrast: #F6F6F7

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `005A58` | 28.2 | 76 | 0.423 0.073 192 | 8.07 AAA | 7.47 AAA | 2.04 FAIL | 100/0/2/65 |
| chromatic cluster | `118A6B` | 4.7 | 13 | 0.565 0.109 169 | 4.31 large/graphics | 3.99 large/graphics | 3.82 large/graphics | 88/0/22/46 |
| chromatic cluster | `08715E` | 2.7 | 7 | 0.491 0.090 175 | 5.94 AA | 5.50 AA | 2.77 FAIL | 93/0/17/56 |
| chromatic cluster | `51AC8E` | 0.7 | 2 | 0.680 0.099 169 | 2.75 FAIL | 2.54 FAIL | 6.00 AA | 53/0/17/33 |
| neutral paper (L*>=97.5) | `FFFFFF` | 18.4 |  | 1.000 0.000 90 | 1.00 FAIL | 1.08 FAIL | 16.48 AAA | 0/0/0/0 |
| neutral dark (L*<40) | `060B08` | 2.3 |  | 0.142 0.011 160 | 19.83 AAA | 18.36 AAA | 1.20 FAIL | 45/0/27/96 |
| ink estimate [uncertain] | `020403` |  |  | 0.101 0.008 165 | 20.56 AAA | 19.04 AAA | 1.25 FAIL | 50/0/25/98 |

#### ref-C — 24 thumbnails, 574,942 px; flat 54%, photo/text/edges 46%; page grey used for contrast: #F5F5F5

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `57B848` | 0.8 | 46 | 0.700 0.176 141 | 2.51 FAIL | 2.31 FAIL | 6.56 AA | 53/0/61/28 |
| chromatic cluster | `021B04` | 0.6 | 36 | 0.195 0.056 145 | 18.09 AAA | 16.59 AAA | 1.10 FAIL | 93/0/85/89 |
| chromatic cluster | `0B2A13` | 0.2 | 14 | 0.255 0.056 149 | 15.50 AAA | 14.22 AAA | 1.06 FAIL | 74/0/55/84 |
| chromatic cluster | `3C7F3C` | 0.1 | 3 | 0.536 0.121 144 | 4.89 AA | 4.49 large/graphics | 3.37 large/graphics | 53/0/53/50 |
| accent tint | `FAFFF8` | 0.2 |  | 0.994 0.011 137 | 1.01 FAIL | 1.08 FAIL | 16.27 AAA | 2/0/3/0 |
| neutral paper (L*>=97.5) | `FFFFFF` | 49.4 |  | 1.000 0.000 90 | 1.00 FAIL | 1.09 FAIL | 16.48 AAA | 0/0/0/0 |
| neutral page grey (L* 90-97.5) | `F5F5F5` | 0.3 |  | 0.970 0.000 90 | 1.09 FAIL | 1.00 FAIL | 15.12 AAA | 0/0/0/4 |
| neutral light grey (L* 75-90) | `D7D7D7` | 0.4 |  | 0.879 0.000 90 | 1.44 FAIL | 1.32 FAIL | 11.45 AAA | 0/0/0/16 |
| neutral dark (L*<40) | `030303` | 1.4 |  | 0.097 0.000 90 | 20.62 AAA | 18.92 AAA | 1.25 FAIL | 0/0/0/99 |
| ink estimate [uncertain] | `010101` |  |  | 0.067 0.000 90 | 20.87 AAA | 19.15 AAA | 1.27 FAIL | 0/0/0/100 |

#### ref-D — 27 thumbnails, 641,250 px; flat 43%, photo/text/edges 57%; page grey used for contrast: #ECECEE

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `379A86` | 8.4 | 99 | 0.623 0.096 177 | 3.43 large/graphics | 2.90 FAIL | 4.81 AA | 64/0/13/40 |
| accent tint | `F5FFFC` | 0.1 |  | 0.992 0.011 176 | 1.02 FAIL | 1.16 FAIL | 16.16 AAA | 4/0/1/0 |
| neutral paper (L*>=97.5) | `FFFFFF` | 30.0 |  | 1.000 0.000 90 | 1.00 FAIL | 1.18 FAIL | 16.48 AAA | 0/0/0/0 |
| neutral page grey (L* 90-97.5) | `ECECEE` | 1.1 |  | 0.944 0.003 286 | 1.18 FAIL | 1.00 FAIL | 13.97 AAA | 1/1/0/7 |
| neutral light grey (L* 75-90) | `CFCFD0` | 1.5 |  | 0.855 0.001 286 | 1.56 FAIL | 1.32 FAIL | 10.59 AAA | 0/0/0/18 |
| neutral mid grey (L* 40-75) | `777371` | 0.9 |  | 0.558 0.006 49 | 4.69 AA | 3.98 large/graphics | 3.51 large/graphics | 0/3/5/53 |
| neutral dark (L*<40) | `464547` | 0.8 |  | 0.392 0.004 308 | 9.53 AAA | 8.08 AAA | 1.73 FAIL | 1/3/0/72 |
| ink estimate [uncertain] | `0C0B0B` |  |  | 0.151 0.002 17 | 19.66 AAA | 16.66 AAA | 1.19 FAIL | 0/8/8/95 |

#### ref-E — 24 thumbnails, 259,588 px; flat 33%, photo/text/edges 67%; page grey used for contrast: #EDEFEF

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `4CC0CB` | 3.1 | 95 | 0.747 0.104 204 | 2.16 FAIL | 1.87 FAIL | 7.62 AAA | 63/5/0/20 |
| chromatic cluster | `D2FBFC` | 0.2 | 5 | 0.960 0.042 198 | 1.11 FAIL | 1.04 FAIL | 14.87 AAA | 17/0/0/1 |
| accent tint | `E0FEFE` | 4.0 |  | 0.976 0.031 197 | 1.06 FAIL | 1.09 FAIL | 15.52 AAA | 12/0/0/0 |
| neutral paper (L*>=97.5) | `FFFFFF` | 25.0 |  | 1.000 0.000 90 | 1.00 FAIL | 1.15 FAIL | 16.48 AAA | 0/0/0/0 |
| neutral page grey (L* 90-97.5) | `EDEFEF` | 0.9 |  | 0.951 0.002 197 | 1.15 FAIL | 1.00 FAIL | 14.28 AAA | 1/0/0/6 |
| neutral light grey (L* 75-90) | `D1D6D8` | 0.4 |  | 0.873 0.006 223 | 1.47 FAIL | 1.27 FAIL | 11.24 AAA | 3/1/0/15 |
| ink estimate [uncertain] | `222426` |  |  | 0.259 0.005 248 | 15.57 AAA | 13.49 AAA | 1.06 FAIL | 11/5/0/85 |

#### ref-F — 30 thumbnails, 637,584 px; flat 32%, photo/text/edges 68%; page grey used for contrast: #F2F2F2

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `0339A6` | 4.2 | 61 | 0.396 0.182 262 | 9.81 AAA | 8.77 AAA | 1.68 FAIL | 98/66/0/35 |
| chromatic cluster | `325AAA` | 0.8 | 12 | 0.482 0.136 262 | 6.61 AA | 5.90 AA | 2.49 FAIL | 71/47/0/33 |
| chromatic cluster | `8397CA` | 0.7 | 10 | 0.680 0.079 268 | 2.90 FAIL | 2.59 FAIL | 5.69 AA | 35/25/0/21 |
| chromatic cluster | `5A73A4` | 0.6 | 9 | 0.557 0.082 263 | 4.75 AA | 4.24 large/graphics | 3.47 large/graphics | 45/30/0/36 |
| chromatic cluster | `B0BFDD` | 0.4 | 6 | 0.803 0.046 264 | 1.85 FAIL | 1.65 FAIL | 8.90 AAA | 20/14/0/13 |
| chromatic cluster | `162639` | 0.1 | 2 | 0.264 0.042 254 | 15.32 AAA | 13.69 AAA | 1.08 FAIL | 61/33/0/78 |
| accent tint | `E4E6F1` | 0.1 |  | 0.927 0.015 278 | 1.24 FAIL | 1.11 FAIL | 13.26 AAA | 5/5/0/5 |
| neutral paper (L*>=97.5) | `FFFFFE` | 23.1 |  | 1.000 0.001 106 | 1.00 FAIL | 1.12 FAIL | 16.47 AAA | 0/0/0/0 |
| neutral page grey (L* 90-97.5) | `F2F2F2` | 0.5 |  | 0.961 0.000 90 | 1.12 FAIL | 1.00 FAIL | 14.72 AAA | 0/0/0/5 |
| neutral light grey (L* 75-90) | `D2D7DA` | 0.7 |  | 0.876 0.007 234 | 1.45 FAIL | 1.30 FAIL | 11.36 AAA | 4/1/0/15 |
| neutral mid grey (L* 40-75) | `A8ADAF` | 0.3 |  | 0.744 0.006 223 | 2.27 FAIL | 2.03 FAIL | 7.27 AAA | 4/1/0/31 |
| ink estimate [uncertain] | `202022` |  |  | 0.244 0.004 286 | 16.26 AAA | 14.53 AAA | 1.01 FAIL | 6/6/0/87 |

#### ref-G — 12 thumbnails, 599,985 px; flat 55%, photo/text/edges 45%; page grey used for contrast: #EEEEEE

| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |
|---|---|---|---|---|---|---|---|---|
| chromatic cluster | `01A19A` | 5.4 | 78 | 0.640 0.111 189 | 3.20 large/graphics | 2.76 FAIL | 5.15 AA | 99/0/4/37 |
| chromatic cluster | `018780` | 1.4 | 20 | 0.562 0.097 188 | 4.39 large/graphics | 3.79 large/graphics | 3.75 large/graphics | 99/0/5/47 |
| accent tint | `E8F3F2` | 0.1 |  | 0.956 0.012 190 | 1.13 FAIL | 1.02 FAIL | 14.55 AAA | 5/0/0/5 |
| neutral paper (L*>=97.5) | `FFFFFF` | 29.3 |  | 1.000 0.000 90 | 1.00 FAIL | 1.16 FAIL | 16.48 AAA | 0/0/0/0 |
| neutral page grey (L* 90-97.5) | `EEEEEE` | 10.0 |  | 0.949 0.000 90 | 1.16 FAIL | 1.00 FAIL | 14.21 AAA | 0/0/0/7 |
| neutral light grey (L* 75-90) | `D7D6D6` | 6.5 |  | 0.877 0.001 17 | 1.45 FAIL | 1.25 FAIL | 11.36 AAA | 0/0/0/16 |
| neutral mid grey (L* 40-75) | `9A9492` | 0.7 |  | 0.671 0.008 39 | 2.99 FAIL | 2.58 FAIL | 5.51 AA | 0/4/5/40 |
| ink estimate [uncertain] | `343536` |  |  | 0.328 0.002 248 | 12.29 AAA | 10.59 AAA | 1.34 FAIL | 4/2/0/79 |


### 2.1 Reading the boards

- **A (navy).** `172A5C` covers 26.8 % of the page area and makes up 95 % of the chromatic pixels. It is on the covers, the left-hand panels and the icon chips. A flat sample from the cover reads `1C2E60` (ΔE 1.3 from the cluster), and that value is used as the canonical colour [seen]. The bright accent `5398BA` was sampled from the "2025" numerals [seen]. It scores 3.20:1 on white and 4.08:1 on navy, so it works only for large numerals. Chart shades measured on the board, light to deep: bars `778FB4 → 4A6E9F → 2A447E → 1B2E5A`, and donut `889BBB / 56719A / 1A3783 / 142958` [seen]. This is the single-hue ramp pattern the derived ramps follow. A has no flat pixels at L* ≥ 97.5: the "white" pages render as `E7E6E7` because of the mock-up shading [uncertain]. For that reason A's grey band uses DESIGN-user's `F2F3F4`, darkened for print.
- **B (forest, dark mode).** `005A58` is the page ground and slab colour (28 % of area). `118A6B`, `08715E` and `51AC8E` are the tall bars and their gradient, which runs towards about `22B380` [seen]. White panels take 18 %. Text on the dark ground is white at 8.07:1. `118A6B` on `005A58` is only 1.87:1, so it is a decorative contrast and must not carry text. The near-black `060B08` is photo shadow.
- **C (green).** The accent `57B848` covers only 0.8 % of the area. The board is mostly a white page (49 %), black-and-white photos and **pure black tiles** (`030303`, 1.4 %) [seen]. `021B04` and `0B2A13` are green-tinted near-blacks on the diagonal cover and "Thank You" shapes [seen]. Whether those are a photo overlay is [uncertain]. In C, black acts as the second "accent", which is why the green family's ink is `141414` rather than `1F1F1F`.
- **D (teal, Prism).** It has one flat accent, `379A86` (8.4 % of area, 99 % of the chromatic pixels), and no measured second shade. The charcoal `464547` fills the pricing tiles [seen].
- **E (aqua).** `4CC0CB` takes 3.1 % of the area, but the **tint `E0FEFE` takes 4.0 %**. The pale panels carry more of the colour than the accent itself [seen]. The board puts white text on aqua at 2.16:1 [seen], which is not acceptable in print.
- **F (royal).** `0339A6` is 61 % of the chromatic pixels and 4.2 % of the area. The lighter blues are duotone washes over photos, not flat brand colours [inferred].
- **G (teal, Market).** `01A19A` takes 5.4 % of the area and `018780` 1.4 %; the second is a darker shade of the same hue (4.39:1, just short of AA) [seen]. The page grey `EEEEEE` covers 10 % and light grey `D7D6D6` 6.5 %. These are the grey slide grounds and mock-up gradients [seen; how much is lighting is uncertain].

## 3. Families and canonical colours

ΔE2000 between candidate accents: D `379A86` ↔ G `01A19A` **5.9**; B `005A58` ↔ G deep `018780` 15.6; B bright `118A6B` ↔ D 7.4; A ↔ F 11.4; E ↔ G 12.2. OKLCH hue: A 266°, F 262°, G 189°, B 192° (slab) and 169° (bars), D 177°, E 204°, C 141°.

| family id | source refs | canonical accent (measured) | why |
|---|---|---|---|
| `navy` | ref-A | `1C2E60` | The only real report. It shares a hue with F (266° vs 262°) but differs a lot in lightness and chroma (ΔE 11.4), so it is not a duplicate. |
| `royal` | ref-F | `0339A6` | Electric royal blue. It is text-safe (9.81:1) on its own, so `accent_deep = accent`. |
| `teal` | ref-G, ref-D | `01A19A` (G) | D and G are 5.9 ΔE apart, which office printing will not separate. G is canonical because its hue (189°) matches B's measured dark teal, so the 7:1 deep shade is anchored to a measured colour. Variant: D `379A86` (3.43:1, slightly greener) is recorded in `variants`. |
| `forest` | ref-B | `005A58` | A dark-mode board. Its slab colour is ≈ teal's `accent_deep` (ΔE 1.0). It stays a separate family because it has its own bright green (`118A6B`, hue 169°) and its dark-ground identity. |
| `aqua` | ref-E | `4CC0CB` | The lightest accent (2.16:1). It is the one family that is built around a tint. |
| `green` | ref-C | `57B848` | High-chroma green used sparingly, paired with black. |

If the skill offers fewer choices, the nearest merges are teal + forest (they share the deep shade `005955`/`005A58`) and navy + royal (same hue). Each merge loses a signature colour: the bright green for forest, the electric blue for royal. [inferred]

## 4. How the token sets were derived

- `paper` is `FFFFFF`. `paper_alt` is the measured page grey of the board(s), darkened in OKLCH until it carries at least **6 % ink**. The measured values `F2F3F4`, `F5F5F5` and `F2F2F2` are 4–5 % K (§7). For A, the measured `E7E6E7` was rejected as lighting.
- `ink` is `1F1F1F`, and `141414` for green. It is an exactly neutral R = G = B value on purpose (§7, K-only printing). The measured ink estimates (`1B1C22`, `202022`, `222426`, `010101`) are [uncertain] and close to neutral. `ink_soft` is `5C5C5C` (6.69:1 on white, 5.8:1 on `paper_alt`), replacing DESIGN-user's `5B6270` with a neutral value of the same strength.
- `rule` is `BFBFBF` (25 % K) and `hairline` is `D9D9D9` (15 % K). Both are neutral. The rule is the minimum for a 0.5 pt line on a laser printer (§7).
- `accent` is the measured brand fill. `accent_deep` is the accent itself when it already reaches 7:1 on **both** white and `paper_alt` (navy, royal, forest). Otherwise it is the highest OKLCH lightness at the accent's hue that reaches 7:1 on both (teal, aqua, green).
- `accent_bright` is a measured brighter shade where one exists (navy `5398BA`, forest `118A6B`). Otherwise it equals `accent`, which is already the bright colour.
- `accent_tint` is the measured tint where it covers a meaningful area (aqua `E0FEFE`). Otherwise it is OKLCH L 0.955 with C = min(0.04, 0.35·C_accent) at the accent hue. Every tint is darkened until it reaches **≥ 7 % ink** on its strongest channel.
- `on_accent` is white when white on the accent reaches ≥ 3:1, which allows white text at **14 pt bold / 18 pt regular and above** only. Otherwise it is ink. White body text on a fill must use an `accent_deep` fill instead.
- `chart_series` holds 5 OKLCH steps from **light to deep**, all at the accent's hue. The lightest step is L 0.87 and the deepest is `accent_deep`. When the brand accent sits between those two, it is pinned to the inner step (1–3) that gives the largest minimum ΔE between neighbours. Chroma tapers to 55 % of the accent at the light end. The values are listed light→deep as requested, but `reportkit.py` takes `chart_series[0]` as the first series (§6.2).
- `signal` (negative values) is searched over OKLCH hue 345–60°. For each hue the script takes the lightest shade that reaches ≥ 4.5:1 on white, `paper_alt` and `accent_tint`. It then picks the hue that maximises the minimum ΔE2000 to `accent`, `accent_deep` and `accent_bright` under normal, deutan and protan vision, with a penalty of 0.3 per degree away from 30°. Five families get a vermilion near `CE2E09`. **Green gets the raspberry `C0318F`**: a red there was only 12.5–16 ΔE from the greens under deutan and protan simulation, while raspberry keeps at least 35.7.
- `tint` and `grey` are legacy keys that `reportkit.py` reads. They are set to `paper_alt` and `ink_soft`. Forest also has `dark_ground` (`005A58`) for the dark-mode pages.

## 5. Derived token sets with contrast checks

Contrast is shown against white, `paper_alt` and `accent_tint`, plus ink on the colour. Print columns use the naive CMYK model (TAC = total ink, a lower bound).

#### navy (refs ref-A)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `1F1F1F` | 16.48 | 14.32 | 14.42 | 1.00 | 0/0/0/88 (88) | 82.5 |
| ink_soft | `5C5C5C` | 6.69 | 5.81 | 5.85 | 2.46 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.15 | 1.14 | 16.48 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `EEEFF0` | 1.15 | 1.00 | 1.01 | 14.32 | 1/0/0/6 (7) | 3.3 |
| rule | `BFBFBF` | 1.84 | 1.60 | 1.61 | 8.96 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.23 | 1.23 | 11.68 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `1C2E60` | 13.05 | 11.34 | 11.42 | 1.26 | 71/52/0/62 (185) | 72.8 |
| accent | `1C2E60` | 13.05 | 11.34 | 11.42 | 1.26 | 71/52/0/62 (185) | 72.8 |
| accent_bright | `5398BA` | 3.20 | 2.78 | 2.80 | 5.16 | 55/18/0/27 (100) | 33.1 |
| accent_tint | `E9F0FF` | 1.14 | 1.01 | 1.00 | 14.42 | 9/6/0/0 (15) | 7.5 |
| on_accent | `FFFFFF` | 1.00 | 1.15 | 1.14 | 16.48 | 0/0/0/0 (0) | 0.0 |
| signal | `CE2E09` | 5.23 | 4.54 | 4.57 | 3.15 | 0/78/96/19 (193) | 49.8 |

chart ramp light→deep: `C5D4F7` → `93A8D6` → `657CB5` → `3F548A` → `1C2E60`  
adjacent ΔE2000: 12.0, 14.5, 15.1, 12.5 (deuteranope-simulated: 12.3, 14.8, 14.8, 12.3)  
contrast of each step on white: 1.49, 2.38, 4.11, 7.38, 13.05  
signal vs accent ΔE2000 normal/deutan/protan: 46.1 / 55.8 / 46.3; signal vs accent_deep: 46.1 / 55.8 / 46.3
  
measured chart shades on the board: `778FB4`, `4A6E9F`, `2A447E`, `1B2E5A`

#### royal (refs ref-F)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `1F1F1F` | 16.48 | 14.46 | 14.51 | 1.00 | 0/0/0/88 (88) | 82.5 |
| ink_soft | `5C5C5C` | 6.69 | 5.87 | 5.89 | 2.46 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.14 | 1.14 | 16.48 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `F0F0F0` | 1.14 | 1.00 | 1.00 | 14.46 | 0/0/0/6 (6) | 3.0 |
| rule | `BFBFBF` | 1.84 | 1.61 | 1.62 | 8.96 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.24 | 1.24 | 11.68 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `0339A6` | 9.81 | 8.61 | 8.64 | 1.68 | 98/66/0/35 (199) | 65.1 |
| accent | `0339A6` | 9.81 | 8.61 | 8.64 | 1.68 | 98/66/0/35 (199) | 65.1 |
| accent_bright | `0339A6` | 9.81 | 8.61 | 8.64 | 1.68 | 98/66/0/35 (199) | 65.1 |
| accent_tint | `E9F1FF` | 1.14 | 1.00 | 1.00 | 14.51 | 9/5/0/0 (14) | 7.2 |
| on_accent | `FFFFFF` | 1.00 | 1.14 | 1.14 | 16.48 | 0/0/0/0 (0) | 0.0 |
| signal | `CF3103` | 5.13 | 4.50 | 4.52 | 3.21 | 0/76/99/19 (194) | 49.5 |

chart ramp light→deep: `BED5FF` → `82AEFF` → `4A84F7` → `285FCE` → `0339A6`  
adjacent ΔE2000: 12.0, 12.4, 14.2, 12.7 (deuteranope-simulated: 13.3, 13.6, 13.4, 11.8)  
contrast of each step on white: 1.48, 2.22, 3.54, 5.80, 9.81  
signal vs accent ΔE2000 normal/deutan/protan: 49.1 / 64.3 / 54.9; signal vs accent_deep: 49.1 / 64.3 / 54.9

#### teal (refs ref-G, ref-D)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `1F1F1F` | 16.48 | 14.21 | 14.65 | 1.00 | 0/0/0/88 (88) | 82.5 |
| ink_soft | `5C5C5C` | 6.69 | 5.76 | 5.94 | 2.46 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.16 | 1.12 | 16.48 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `EEEEEE` | 1.16 | 1.00 | 1.03 | 14.21 | 0/0/0/7 (7) | 3.5 |
| rule | `BFBFBF` | 1.84 | 1.58 | 1.63 | 8.96 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.22 | 1.25 | 11.68 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `005955` | 8.20 | 7.07 | 7.29 | 2.01 | 100/0/4/65 (169) | 56.9 |
| accent | `01A19A` | 3.20 | 2.76 | 2.84 | 5.15 | 99/0/4/37 (140) | 36.3 |
| accent_bright | `01A19A` | 3.20 | 2.76 | 2.84 | 5.15 | 99/0/4/37 (140) | 36.3 |
| accent_tint | `D4F9F5` | 1.12 | 1.03 | 1.00 | 14.65 | 15/0/2/2 (19) | 13.6 |
| on_accent | `FFFFFF` | 1.00 | 1.16 | 1.12 | 16.48 | 0/0/0/0 (0) | 0.0 |
| signal | `CE2E09` | 5.23 | 4.50 | 4.64 | 3.15 | 0/78/96/19 (193) | 49.8 |

chart ramp light→deep: `A6E2DC` → `69C1BB` → `01A19A` → `007C77` → `005955`  
adjacent ΔE2000: 10.0, 11.1, 13.0, 11.9 (deuteranope-simulated: 9.7, 11.3, 12.7, 10.9)  
contrast of each step on white: 1.44, 2.11, 3.20, 5.06, 8.20  
signal vs accent ΔE2000 normal/deutan/protan: 58.3 / 35.7 / 35.6; signal vs accent_deep: 51.3 / 35.9 / 24.0

#### forest (refs ref-B)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `1F1F1F` | 16.48 | 14.32 | 14.59 | 1.00 | 0/0/0/88 (88) | 82.5 |
| ink_soft | `5C5C5C` | 6.69 | 5.81 | 5.92 | 2.46 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.15 | 1.13 | 16.48 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `EEEFF0` | 1.15 | 1.00 | 1.02 | 14.32 | 1/0/0/6 (7) | 3.3 |
| rule | `BFBFBF` | 1.84 | 1.60 | 1.63 | 8.96 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.23 | 1.25 | 11.68 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `005A58` | 8.07 | 7.01 | 7.14 | 2.04 | 100/0/2/65 (167) | 56.4 |
| accent | `005A58` | 8.07 | 7.01 | 7.14 | 2.04 | 100/0/2/65 (167) | 56.4 |
| accent_bright | `118A6B` | 4.31 | 3.74 | 3.82 | 3.82 | 88/0/22/46 (156) | 42.7 |
| accent_tint | `DEF6F4` | 1.13 | 1.02 | 1.00 | 14.59 | 10/0/1/4 (15) | 10.1 |
| on_accent | `FFFFFF` | 1.00 | 1.15 | 1.13 | 16.48 | 0/0/0/0 (0) | 0.0 |
| signal | `CE2E09` | 5.23 | 4.54 | 4.63 | 3.15 | 0/78/96/19 (193) | 49.8 |
| dark_ground | `005A58` | 8.07 | 7.01 | 7.14 | 2.04 | 100/0/2/65 (167) | 56.4 |

chart ramp light→deep: `B7DDDB` → `87BCBA` → `549C99` → `317A78` → `005A58`  
adjacent ΔE2000: 9.6, 10.9, 12.6, 11.4 (deuteranope-simulated: 9.5, 10.9, 12.9, 10.9)  
contrast of each step on white: 1.46, 2.11, 3.19, 5.02, 8.07  
signal vs accent ΔE2000 normal/deutan/protan: 50.8 / 36.9 / 24.6; signal vs accent_deep: 50.8 / 36.9 / 24.6

#### aqua (refs ref-E)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `1F1F1F` | 16.48 | 14.28 | 15.52 | 1.00 | 0/0/0/88 (88) | 82.5 |
| ink_soft | `5C5C5C` | 6.69 | 5.79 | 6.30 | 2.46 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.15 | 1.06 | 16.48 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `EDEFEF` | 1.15 | 1.00 | 1.09 | 14.28 | 1/0/0/6 (7) | 3.5 |
| rule | `BFBFBF` | 1.84 | 1.59 | 1.73 | 8.96 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.22 | 1.33 | 11.68 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `005960` | 8.08 | 7.00 | 7.61 | 2.04 | 100/7/0/62 (169) | 56.0 |
| accent | `4CC0CB` | 2.16 | 1.87 | 2.04 | 7.62 | 63/5/0/20 (88) | 28.5 |
| accent_bright | `4CC0CB` | 2.16 | 1.87 | 2.04 | 7.62 | 63/5/0/20 (88) | 28.5 |
| accent_tint | `E0FEFE` | 1.06 | 1.09 | 1.00 | 15.52 | 12/0/0/0 (12) | 11.2 |
| on_accent | `1F1F1F` | 16.48 | 14.28 | 15.52 | 1.00 | 0/0/0/88 (88) | 82.5 |
| signal | `CB3300` | 5.23 | 4.53 | 4.93 | 3.15 | 0/75/100/20 (195) | 49.8 |

chart ramp light→deep: `A8E0E5` → `4CC0CB` → `1C9EA9` → `0D7B83` → `005960`  
adjacent ΔE2000: 11.8, 10.1, 12.5, 11.7 (deuteranope-simulated: 11.9, 10.4, 12.4, 10.9)  
contrast of each step on white: 1.45, 2.16, 3.22, 5.03, 8.08  
signal vs accent ΔE2000 normal/deutan/protan: 57.0 / 44.4 / 48.7; signal vs accent_deep: 48.1 / 40.9 / 31.3

#### green (refs ref-C)

| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |
|---|---|---|---|---|---|---|---|
| ink | `141414` | 18.42 | 16.17 | 16.31 | 1.00 | 0/0/0/92 (92) | 91.2 |
| ink_soft | `5C5C5C` | 6.69 | 5.87 | 5.92 | 2.76 | 0/0/0/64 (64) | 47.4 |
| paper | `FFFFFF` | 1.00 | 1.14 | 1.13 | 18.42 | 0/0/0/0 (0) | 0.0 |
| paper_alt | `F0F0F0` | 1.14 | 1.00 | 1.01 | 16.17 | 0/0/0/6 (6) | 3.0 |
| rule | `BFBFBF` | 1.84 | 1.61 | 1.63 | 10.02 | 0/0/0/25 (25) | 14.4 |
| hairline | `D9D9D9` | 1.41 | 1.24 | 1.25 | 13.05 | 0/0/0/15 (15) | 8.1 |
| accent_deep | `105E00` | 8.01 | 7.02 | 7.09 | 2.30 | 83/0/100/63 (246) | 58.5 |
| accent | `57B848` | 2.51 | 2.21 | 2.23 | 7.33 | 53/0/61/28 (142) | 34.9 |
| accent_bright | `57B848` | 2.51 | 2.21 | 2.23 | 7.33 | 53/0/61/28 (142) | 34.9 |
| accent_tint | `E2F7DE` | 1.13 | 1.01 | 1.00 | 16.31 | 9/0/10/3 (22) | 13.9 |
| on_accent | `141414` | 18.42 | 16.17 | 16.31 | 1.00 | 0/0/0/92 (92) | 91.2 |
| signal | `C0318F` | 5.15 | 4.52 | 4.56 | 3.58 | 0/74/26/25 (125) | 48.4 |

chart ramp light→deep: `B1E5A9` → `57B848` → `389A27` → `247B14` → `105E00`  
adjacent ΔE2000: 16.7, 9.4, 11.2, 9.7 (deuteranope-simulated: 16.6, 9.5, 11.2, 9.4)  
contrast of each step on white: 1.43, 2.51, 3.61, 5.36, 8.01  
signal vs accent ΔE2000 normal/deutan/protan: 83.5 / 37.4 / 55.9; signal vs accent_deep: 76.5 / 35.7 / 45.0


### 5.1 Contrast pass and fail at a glance (accent roles, on white / on `paper_alt`)

| family | accent_deep | accent | accent_bright | white text on accent | accent_bright on accent |
|---|---|---|---|---|---|
| navy | 13.05 / 11.34 AAA | = deep | 3.20 / 2.78: large or graphics on white only | 13.05 AAA | 4.08: large numerals OK |
| royal | 9.81 / 8.61 AAA | = deep | = accent | 9.81 AAA | n/a |
| teal | 8.20 / 7.07 AAA | 3.20 / 2.76: fill; large text on white only | = accent | 3.20: ≥ 14 pt bold only (ink on teal 5.15 AA is the small-text option) | n/a |
| forest | 8.07 / 7.01 AAA | = deep | 4.31 / 3.74: large or graphics | 8.07 AAA | 1.87: decoration only |
| aqua | 8.08 / 7.00 AAA | 2.16 / 1.87: **fill only, never text** | = accent | 2.16 FAIL → ink on aqua (7.6:1) | n/a |
| green | 8.01 / 7.02 AAA | 2.51 / 2.21: **fill only, never text** | = accent | 2.51 FAIL → ink on green (7.3:1) | n/a |

The signal colour reaches ≥ 4.5:1 on white, `paper_alt` and `accent_tint` in every family. White on `accent_deep` reaches ≥ 8:1 in every family, which makes it the safe table-header combination.

## 6. Usage rules

### 6.1 Where each role may appear

| token | allowed | not allowed |
|---|---|---|
| `ink` | Body text, table text, axis labels, numerals in tables; the solid black tiles in the green family | — |
| `ink_soft` | Captions, labels, footnotes, running heads, source lines (≥ 7 pt) | Text on accent fills; on `accent_tint` it reaches 5.8:1, which is fine |
| `paper_alt` | Page bands, zebra rows, sidebar panels, KPI strips | Behind `accent`-coloured text in teal, aqua or green |
| `rule` | 0.5–0.75 pt rules: table rules, separators, the inset frame (G) | — |
| `hairline` | Rules of 0.75 pt and up, gridlines, zebra fill | 0.5 pt lines (they break up on lasers, §7) |
| `accent_deep` | **All accent-coloured text**: headings, kickers, 7.5 pt labels, quotes, links, stat numerals under 24 pt; table header fill with white text; the last chart step; small chips that carry white text | — |
| `accent` | Large fills (cover, 1/3 split panel, break page, slabs, pills, bars); stat numerals ≥ 24 pt only where accent on white ≥ 3:1 (navy, royal, forest, teal) | Teal, aqua and green: any text under 24 pt and any white body text on it. Aqua and green: no text in accent at any size on white (below 3:1) |
| `accent_bright` | Navy: the year or big numerals on the navy cover (4.08:1). Forest: decorative bars on the dark ground. Elsewhere it equals `accent` | Text under 24 pt; any text on the dark ground in forest |
| `accent_tint` | Callout and KPI panels, highlighted table rows, pill backgrounds. Text on it: `ink`, `ink_soft` or `accent_deep` (≥ 7:1) | `accent` text on it (fails in teal, aqua, green) |
| `on_accent` | Text on an `accent` fill. White only at ≥ 14 pt bold / 18 pt in teal (ink 5.15:1 for smaller text); ink in aqua and green | — |
| `signal` | Negative values and deltas only, **always with a non-colour cue** (− sign, ▼, parentheses) | Fills on dark accents, decoration, headings |
| `dark_ground` (forest) | Full-page dark ground for cover or break pages. Text on it is white, or ramp step 1 `B7DDDB` for secondary text (5.52:1) | Body pages (§7, ink coverage) |

### 6.2 Mapping to the current engine (`scripts/reportkit.py`) [seen in code]

- These styles set `color=C["accent"]`: `Heading 3`, `Kicker` (7.5 pt), `Quote`, `NumXL` and `NumL`, the 8 pt bold accent runs (around lines 618, 759 and 790), the accent rule borders and `shade(a, C["accent"])`. With teal, aqua or green, the **text** styles must switch to `accent_deep`. Fills and borders may keep `accent`. `NumXL` (≥ 24 pt) may keep `accent` only in navy, royal, forest and teal.
- `chart_series` in `palettes.json` is ordered **light → deep**, as the brief asked. The engine assigns `palette[i]` to series *i*, so a single-series chart would draw in the lightest step. The engine should use `chart_series[::-1]` (deep first), or `accent_deep`/`accent` for the highlighted bar plus a lighter step for the others. The hard-coded `#8E9692` and `#C9CFCB` greys at line 346 should come from the ramp.
- Bars in `accent` pass the 3:1 non-text contrast on white only in navy, royal, forest and teal. In **aqua (2.16) and green (2.51)** the highlighted bar should use ramp step 3 or 4 (≥ 3.2:1), or every bar should carry a direct value label.

### 6.3 Chart ramp rules

- Adjacent steps are **9.4–16.7 ΔE2000** apart. Deutan simulation gives nearly the same figures, because the ramps are lightness-driven. All of them are clearly distinguishable.
- Only steps 3–5 reach 3:1 on white (step 3 is 3.19–4.11 depending on the family). Steps 1–2 must be **directly labelled** or outlined with a 0.5 pt `accent_deep` line. In shades-of-one-hue charts the boards label the values directly (A's bars and donut) [seen].
- Order the steps by meaning: most recent or most important = deep (A's 2025 bar is the deepest) [seen].
- In greyscale printing, `signal` (L* ≈ 46) prints as the same grey as ramp step 4 in teal, forest, aqua and green (L* 45–47). Never rely on the signal hue alone.

## 7. Print notes (A4, office laser and inkjet)

**Ink coverage of large dark fills** (naive CMYK, so lower bounds):

| fill | naive C/M/Y/K | TAC | note |
|---|---|---|---|
| navy `1C2E60` | 71/52/0/62 | 185 % | A real profile conversion would add C, M and Y under K, probably 230–280 % [inferred]. A full-page navy cover is acceptable; navy body pages are not. |
| royal `0339A6` | 98/66/0/35 | 199 % | Likely **out of CMYK gamut**: saturated RGB blues usually print duller and shifted towards violet [inferred]. Proof before committing. |
| forest `005A58` | 100/0/2/65 | 167 % | B's all-dark pages would put about 167 % ink coverage over the whole sheet. Print the forest family **light-mode**: white paper, `005A58` slabs, `dark_ground` only for cover and break pages. |
| teal `01A19A` / green `57B848` / aqua `4CC0CB` | 99/0/4/37 · 53/0/61/28 · 63/5/0/20 | 140 / 142 / 88 % | Mid-tone solids show **banding** on lasers more than dark solids do [inferred]. Keep solid panels ≤ 1/3 of a page. |

Rules [inferred]: at most one full-bleed dark page per 6–8 pages (cover, back cover, break pages). Section openers use the 1/3 split panel, not a full page. Office printers cannot print to the edge (≈ 4–5 mm unprintable margin), so a "bleed" prints with a white border. Either accept that, or end colour blocks 5 mm inside the trim when the document is meant for desk printing. For a "print-light" variant, replace solid panels with an `accent_tint` panel, an `accent_deep` heading and a 3 pt `accent` bar.

**Do light tints survive?** (max ink on the strongest channel; < 4 % tends to vanish on office printers)

| tint | source | max ink | ΔE2000 vs white | verdict |
|---|---|---|---|---|
| `F5F5F5` | C measured | 4 % K | 2.0 | Likely to disappear |
| `F2F3F4` | DESIGN-user / A | 4 % K | 2.5 | Borderline |
| `F2F2F2` | F measured | 5 % K | — | Borderline |
| `EEEEEE` / `EEEFF0` / `EDEFEF` / `F0F0F0` | G measured / derived | 6–7 % | 3.0–3.5 | OK (used as `paper_alt`) |
| `E9F8F8` | DESIGN-user aqua | 6 % C | 6.8 | OK but faint |
| `E8EDF7` / `E6F5F3` | DESIGN-user navy / teal | 6 % | 6.1 / 7.3 | OK but faint |
| `E9F0FF` · `E9F1FF` · `D4F9F5` · `DEF6F4` · `E0FEFE` · `E2F7DE` | derived `accent_tint` | 9–15 % | 7.2–13.9 | OK |
| `D9D9D9` hairline | derived | 15 % K | 8.1 | Fills fine; **0.5 pt lines dither into dots**. Use ≥ 0.75 pt, or `rule` `BFBFBF` for 0.5 pt |

Other print notes [inferred]:
- Keep `ink`, `ink_soft`, `rule` and `hairline` exactly neutral (R = G = B). Many office printer drivers then render them with **black toner only**, which gives sharp small text and no colour fringes. A slightly cool grey like `5B6270` is printed as a CMY+K mix.
- The derived `accent_tint` values are deliberately more saturated than the screen-subtle tints on the boards (E9F8F8-type). On screen they look a step stronger, and on paper they come out about where the boards look on screen.
- Every `accent_deep` reaches ≥ 7:1, which leaves headroom for the contrast lost in toner-saving or draft print modes.

## 8. Script

The full measurement and derivation script is `.claude/skills/design-picker/scripts/palettes_measure.py`. It needs only numpy and Pillow. Thumbnail box definitions, the segmentation, k-means, the CIELAB, OKLCH and CIEDE2000 maths, the WCAG contrast check, the Machado CVD simulation, the naive CMYK conversion, and the per-family derivation (`FAMILIES` dict, which records the canonical measured hex values and their provenance) all live in that one file.

```
.venv/bin/python -I .claude/skills/design-picker/scripts/palettes_measure.py measure   # JSON of all measurements (stdout)
.venv/bin/python -I .claude/skills/design-picker/scripts/palettes_measure.py tables    # the section-2 tables
.venv/bin/python -I .claude/skills/design-picker/scripts/palettes_measure.py derive    # section-5 tables + writes .claude/skills/design-picker/assets/palettes.json
```
