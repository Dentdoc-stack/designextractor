# DOCX feasibility: can python-docx + LibreOffice produce the boards' look?

I tested each technique by building a small DOCX with python-docx 1.2, converting it with LibreOffice 24.2.7 (`soffice --headless --convert-to pdf`), and checking the result two ways: by eye (pdftoppm PNGs) and by measurement (pymupdf `get_drawings()`, `get_text('dict')`, `get_image_info()`, and `pdffonts`). The test scripts are in `/tmp/feas/` (scratch, not kept in the repo). Proof images are in `research/assets/proofs/`.

Tags: **[seen]** = rendered and measured here. **[inferred]** = follows from what I saw but was not tested directly. **[uncertain]** = not testable here. Microsoft Word is not available in this environment, so every Word-compatibility statement is [inferred] or [uncertain].

**Short answer: every technique on the boards can be built and renders correctly in LibreOffice.** There are three things the current engine gets wrong and must change:
1. **Leading must be set as exact points, not as "auto" multiples.** Poppins has a 1.50 em natural line height, so "auto 1.05" renders at 1.58 em. [seen]
2. **The page-frame bug comes from `footer_distance = 0`.** Keep it at 10 mm or more, or draw the frame as a shape. [seen]
3. **Use shapes, not tables, for full-bleed colour.** A full-page shaded table on a page that has a (blank) header or footer starts 1 mm below the top edge and stops 1 mm above the bottom. A shape anchored in the header has no gap. [seen]

---

## 1. Fonts: Poppins, Montserrat, Inter. **Works**

**Source.** I took the fonts from the npm registry: `@expo-google-fonts/poppins@0.4.1`, `@expo-google-fonts/montserrat@0.4.2` and `@expo-google-fonts/inter@0.4.2`. Each package ships static TTFs and an OFL-1.1 licence file (`LICENSE_FONT`). Tarball URL pattern: `https://registry.npmjs.org/@expo-google-fonts/poppins/-/poppins-0.4.1.tgz`.

**Saved to `research/assets/fonts/`.** For each family I kept 8 weights: Regular, Italic, Medium, SemiBold, SemiBoldItalic, Bold, BoldItalic, ExtraBold. Files are named `Family-Style.ttf`, with licences in `OFL-Poppins.txt`, `OFL-Montserrat.txt` and `OFL-Inter.txt`. Total size is 6.6 MB. Poppins and Montserrat are also installed in `~/.fonts` (then `fc-cache -f`). Inter was already installed system-wide as OTF (`/usr/share/fonts/opentype/inter/`). I bundled Inter TTFs anyway so the skill does not depend on the host machine.

**Embedding.** `pdffonts` shows that every face is embedded and subset: `Poppins-Regular/Italic/Medium/SemiBold/Bold/BoldItalic/ExtraBold`, `Montserrat-Regular/SemiBold/Bold/ExtraBold` (TrueType), and `Inter-*` (Type 1/CFF, from the system OTFs). [seen] Proof: `assets/proofs/01-fonts.png`.

**How to name the weights in python-docx.** I checked the name tables with fontTools [seen]. All three families use the same scheme:

| Weight wanted | `w:rFonts` value | `w:b` / `w:i` |
|---|---|---|
| 400 Regular | `Poppins` | none |
| 400 Italic | `Poppins` | `i` |
| 700 Bold | `Poppins` | `b` |
| 700 Bold Italic | `Poppins` | `b` + `i` |
| 500 Medium | `Poppins Medium` | none (or `i` for Medium Italic) |
| 600 SemiBold | `Poppins SemiBold` | none (or `i`) |
| 800 ExtraBold | `Poppins ExtraBold` | none |

Only Regular, Italic, Bold and Bold Italic are style-linked under the base family name. Every other weight is a separate legacy family, `"<Family> <Weight>"` (nameID 1), so it must be selected by name. **Never add `w:b` to a non-RIBBI family.** "Poppins SemiBold" plus `w:b` renders as a synthetic emboldened SemiBold, not as Bold. [seen] The same rule applies to `Montserrat …` and `Inter …`.

```python
def fonts(run, name):                       # same idea as reportkit._set_fonts
    rpr = run._r.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))           # note: never `find(...) or ...`; empty lxml elements are falsy
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('ascii', 'hAnsi', 'cs', 'eastAsia'): rf.set(qn('w:' + a), name)
r = p.add_run('2,4 M'); fonts(r, 'Poppins'); r.bold = True          # 700
r = p.add_run('KEY FIGURES'); fonts(r, 'Poppins SemiBold')            # 600, no r.bold
```

**Leading caveat. This one is important.** [seen] Fonts have very different natural line heights (hhea ascent − descent + lineGap):

| Font | Natural line height |
|---|---|
| Poppins | 1.50 em |
| Montserrat | 1.22 em |
| Inter | 1.21 em |
| IBM Plex | about 1.3 em |

LibreOffice multiplies the natural line height by the "auto" factor. I measured the baseline-to-baseline gap in the PDF:

| Setting | Measured gap |
|---|---|
| Poppins 26 pt, auto 1.05 | 1.58 em |
| Poppins 26 pt, exact 27.3 pt | 1.05 em |
| Montserrat, auto 1.05 | 1.28 em |
| Inter 10 pt, auto 1.45 | **1.75 em** |
| Inter 10 pt, exact 14.5 pt | 1.45 em |

So the tokens' `leading` must be converted to exact points: `pf.line_spacing = Pt(size * lead)` with `line_spacing_rule = EXACTLY`. Exact 1.05 on Poppins caps and descenders did not clip. Proof: `assets/proofs/11-leading.png`.

**Word portability.** The PDF is self-contained. A DOCX needs the fonts installed, or embedded. If you add `<w:embedTrueTypeFonts/>` to settings.xml and round-trip through LibreOffice (`--convert-to docx:"MS Word 2007 XML"`), LibreOffice embeds the fonts as `word/fonts/*.odttf`. [seen] They are embedded whole, not subset, so a 37 KB test file grew to 4.6 MB. Whether Word honours them is [uncertain].

## 2. Icons: Lucide line glyphs on solid accent circles. **Works**

- **Source:** `lucide-static@1.52.0` from npm. It has 2130 SVGs at 24×24 using `stroke="currentColor"`. Licence is ISC, plus MIT for the icons derived from Feather. The licence is saved as `research/assets/icons-sample/LICENSE-lucide.txt`.
- **Renderer:** `cairosvg` (`pip install cairosvg`). libcairo is present on the system.
- **Samples:** 5 icons at 12 mm and 300 dpi (142 px), white glyph on accent circle: `users.png`, `chart-column.png`, `heart-pulse.png`, `leaf.png`, `target.png` in `research/assets/icons-sample/`. They insert with `add_picture(width=Mm(10))`. Proofs: `assets/proofs/02-icon-chips.png` and `10-combined-split-page.png`. [seen]

```python
import re, cairosvg
def icon_chip(name, accent, out_png, size_mm=12, dpi=300, fg='#FFFFFF', stroke=1.75, pad=0.24):
    inner = re.search(r'<svg[^>]*>(.*)</svg>', (LUCIDE / f'{name}.svg').read_text(), re.S).group(1)
    s, off = 24 * (1 - 2 * pad), 24 * pad
    chip = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">'
            f'<circle cx="12" cy="12" r="12" fill="{accent}"/><g transform="translate({off} {off}) scale({s/24})" '
            f'fill="none" stroke="{fg}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{inner}</g></svg>')
    px = round(size_mm / 25.4 * dpi)
    cairosvg.svg2png(bytestring=chip.encode(), write_to=str(out_png), output_width=px, output_height=px)
```
Caveat: the stroke is scaled together with the glyph. With `stroke=1.75` and `pad=0.24`, the line is about 0.9 of the chip's 24 units, roughly 0.45 mm on a 12 mm chip. That reads as a single-weight line glyph, matching the boards [seen]. If you change `pad`, adjust `stroke` with it. Do not ship the whole 51 MB Lucide package; vendor only the SVGs you use.

## 3. Full-bleed colour blocks. **Works** (shapes preferred)

I tested three methods. Measured fills: [seen]

| Method | Result |
|---|---|
| **A. Table cell shading**, section margins 0, exact row height | Cover 210×297: fill exactly 0,0 to 210,297. Left panel 70 mm (2-column table): exact. Top band in a page with 20 mm margins plus `tblInd = −20 mm` and table width 210: bleeds left and right exactly (top margin 0). |
| **B. Anchored DrawingML rect in the header** (`wp:anchor`, `relativeFrom="page"`, `behindDoc="1"`, `wrapNone`) | 0,0 to 70,297 on **every page of the section**. Text flows normally beside it using ordinary margins (left margin 82 mm). The text box inside the shape renders. |
| **C. Anchored rect in a body paragraph** | Exact, appears once (on the anchor page). Good for a top band on one page. |

Pagination traps with method A: [seen]
- **Overflow to a blank page.** A full-page table cell (row exact 297 mm) creates a blank page if any normal paragraph follows it. It is safe when (a) the only following paragraph is the one that carries the section's `sectPr` (python-docx `add_section()` creates exactly that), or (b) the following paragraph has a hidden mark: `pPr/rPr/<w:vanish/>` plus 1 pt exact spacing. At the end of the document, use (b). A 1 pt "tiny" paragraph still overflows unless the row is ≤ 296.5 mm.
- **1 mm gaps.** In a section that has a header or footer part, even an empty one, a full-page table starts at y = 1.02 mm and ends at 296.0 mm. Hidden paragraphs and `titlePg` did not remove the gap. `titlePg` is worse: it inherits the previous section's running header. **The existing skill's closing page shows this gap** (measured 1.02 mm white strip at the top of `sample-report.docx` p13). The cover is clean only because it is the first section and has no header.
- **Rule:** use a table only on the first page, or on pages whose section has no header or footer reference. Everywhere else, put the colour in a header-anchored shape and use a borderless, unshaded table (or plain paragraphs) for the text layout on top of it.

Proof: `assets/proofs/03-bleed-blocks.png`, pages p1, p3–p8. p2 is the deliberate blank-page failure.

**Page background (`w:background`).** Adding `<w:background w:color="005B58"/>` plus `<w:displayBackgroundShape/>` in settings renders a 210×297 fill on **every page of the document**. [seen] It cannot be set per section, so it is only useful for a fully dark-mode document (ref B). For individual break pages, use method B.

### The core helper (worked for sections 3–8)
```python
EMU = 36000  # per mm
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
      'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" '
      'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"')
_ids = itertools.count(1000)

def _anchor_open(x, y, w, h, behind, rel_h, rel_v, z, name):
    i = next(_ids)
    return (f'<wp:anchor distT="0" distB="0" distL="0" distR="0" simplePos="0" relativeHeight="{z}" '
            f'behindDoc="{1 if behind else 0}" locked="0" layoutInCell="1" allowOverlap="1"><wp:simplePos x="0" y="0"/>'
            f'<wp:positionH relativeFrom="{rel_h}"><wp:posOffset>{int(x*EMU)}</wp:posOffset></wp:positionH>'
            f'<wp:positionV relativeFrom="{rel_v}"><wp:posOffset>{int(y*EMU)}</wp:posOffset></wp:positionV>'
            f'<wp:extent cx="{int(w*EMU)}" cy="{int(h*EMU)}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
            f'<wp:wrapNone/><wp:docPr id="{i}" name="{name} {i}"/><wp:cNvGraphicFramePr/>')

def shape(run, x, y, w, h, fill=None, geom='rect', adj=None, line=None, behind=True, rel_h='page', rel_v='page',
          z=1, text_xml=None, inset=(2, 2, 2, 2), anchor='t', vert='horz', autofit=False):
    av = f'<a:gd name="adj" fmla="val {adj}"/>' if adj is not None else ''
    fill_x = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    ln_x = (f'<a:ln w="{int(line[0]*12700)}"><a:solidFill><a:srgbClr val="{line[1]}"/></a:solidFill></a:ln>'
            if line else '<a:ln><a:noFill/></a:ln>')
    txbx = f'<wps:txbx><w:txbxContent>{text_xml}</w:txbxContent></wps:txbx>' if text_xml else ''
    l, t, r, b = (int(v*EMU) for v in inset)
    wsp = (f'<wps:wsp><wps:cNvSpPr/><wps:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(w*EMU)}" cy="{int(h*EMU)}"/></a:xfrm>'
           f'<a:prstGeom prst="{geom}"><a:avLst>{av}</a:avLst></a:prstGeom>{fill_x}{ln_x}</wps:spPr>{txbx}'
           f'<wps:bodyPr rot="0" vert="{vert}" wrap="square" lIns="{l}" tIns="{t}" rIns="{r}" bIns="{b}" anchor="{anchor}">'
           f'{"<a:spAutoFit/>" if autofit else "<a:noAutofit/>"}</wps:bodyPr></wps:wsp>')
    xml = (f'<mc:AlternateContent {NS}><mc:Choice Requires="wps"><w:drawing>'
           f'{_anchor_open(x, y, w, h, behind, rel_h, rel_v, z, "Shape")}<a:graphic><a:graphicData '
           f'uri="http://schemas.microsoft.com/office/word/2010/wordprocessingShape">{wsp}</a:graphicData></a:graphic>'
           f'</wp:anchor></w:drawing></mc:Choice></mc:AlternateContent>')
    run._r.append(parse_xml(xml))

# full-height panel on every page of a section:
shape(sec.header.paragraphs[0].add_run(), 0, 0, 70, 297, fill='1A2E5F', behind=True)
```
`text_xml` is ordinary `<w:p>` markup (`<w:rFonts w:ascii="Poppins" …/><w:color w:val="FFFFFF"/><w:sz w:val="52"/>`), so the text stays editable in the text box. The `NS` declared on `mc:AlternateContent` keeps the `wps` prefix in scope for `Requires`.

Word compatibility [uncertain]: Word normally writes the same markup plus a VML `mc:Fallback`. I did not include the fallback. A LibreOffice DOCX→DOCX round-trip adds one automatically: 6 `mc:Fallback`/`v:rect` elements were added, and the re-render had a mean pixel difference of 2.8/255 [seen]. That round-trip is the cheapest normalisation step if Word fidelity matters.

## 4. Rounded rectangles and pills holding editable text. **Works**

All of these were rendered and look correct [seen] (`assets/proofs/04-rounded-pills.png`):
- **`wps:wsp` `prstGeom="roundRect"` with a `txbx`.** The `adj` value sets the corner radius: 18000 gives a slab, 30000 a tile, 50000 a pill. Anchored `rel_h='margin'`, `rel_v='paragraph'`, `behind=False`. I tested a KPI slab (Poppins Bold 26 numeral plus Inter caption, vertically centred with `anchor="ctr"`), filled, tint and outline pills (`line=(1,'349B86')`), and numbered-step chips (outline roundRect "01–04") joined by a 0.6 mm rect "line" placed underneath with a lower `z`.
- **Other preset geometries also render:** `snip1Rect` (one cut corner), `round2SameRect` (top corners rounded), `round1Rect`, `ellipse`, `flowChartDelay` (half-pill tab).
- **Inline shape (`wp:inline` instead of `wp:anchor`):** renders and flows with the text like a character. It sits on the baseline, so it rises above the x-height of the following text. Use it for chips at the start of a line.
- **Grow to fit text:** replacing `<a:noAutofit/>` with `<a:spAutoFit/>` makes LibreOffice grow the box height to fit its text. A 10 mm box became 43.2 mm. [seen] Without it, the text overflows the fixed box.
- **PNG behind a table cell:** a PIL-drawn rounded-rect PNG, anchored `behindDoc=1`, `rel_h='column'`, `rel_v='paragraph'` inside the cell's first paragraph, with white text in the cell on top. This works and the cell text wraps normally. The box size is fixed by the PNG, so prefer `roundRect` shapes. Keep this method for gradient or texture backgrounds only.
- **Caveats** [seen]:
  - `wrapNone` shapes take no space in the flow, so reserve space with the anchor paragraph's `space_after`.
  - With `rel_v='paragraph'`, the offset is measured from the top of the paragraph *including* its `space_before`. In the combined proof, pills overlapped the paragraph above until I added the 6 mm `space_before` to `y`.
  - DOCX tables cannot have rounded corners.

## 5. Photo masks and overlaps. **Works**

PIL pre-processing produces an RGBA PNG at the final size × 300 dpi; it is then inserted inline or anchored. [seen] (`assets/proofs/05-photo-masks.png`)
```python
def _fit(src, w_mm, h_mm, dpi=300, gray=False):          # cover-crop to the exact box
    im = ImageOps.fit(Image.open(src).convert('RGB'), (round(w_mm/25.4*dpi), round(h_mm/25.4*dpi)), Image.LANCZOS, centering=(0.5, 0.4))
    return ImageOps.grayscale(im).convert('RGB') if gray else im
def _save(im, mask_4x, out):                              # 4x supersampled mask -> smooth edge
    im = im.convert('RGBA'); im.putalpha(mask_4x.resize(im.size, Image.LANCZOS)); im.save(out)
# circle:   ImageDraw.ellipse on the 4x mask
# rounded:  ImageDraw.rounded_rectangle(radius=r_mm * px_per_mm * 4)
# cut corner (Business Plan board): ImageDraw.polygon dropping chosen corners, e.g. corners=('tr','bl')
```
- **Inline circle, cut-corner (in black and white, as on the Business Plan board) and rounded masks:** clean anti-aliased edges.
- **Floating picture:** made with `run.part.new_pic_inline(...)`; its `a:graphic` is then moved into a `wp:anchor` built with the same `_anchor_open()` as above.
- **Behind-text photo (`behindDoc=1`) plus a shaded table cell overlapping it:** the cell shading paints over the photo. This is the "colour block cuts through photo" effect, with real editable text in the cell.
- **Photo in front (`behindDoc=0`, z=2) plus a DrawingML rect with text at z=3:** the z-order follows `relativeHeight`. The block sits on top of the photo. I also bled a photo off the top and right page edges, and placed an accent dot shape (z=4) on top of a circular photo.
- **Baked overlap** (`ImageDraw.rectangle` onto the photo) also works, but the block cannot be edited afterwards.
- **Caveats:**
  - Generate the PNG at the box's aspect ratio. The picture is stretched to the extent you give it. I made this mistake with a 60×70 source placed in a 110×110 box.
  - Front-anchored photos cover any text under them. With `wrapNone`, nothing reflows around them.
  - The test photo was matplotlib's `grace_hopper.jpg` sample. The skill needs a no-photo fallback: a tint panel or icon.

## 6. Rotated vertical text (tab). **Works** (2 of 3 methods)

Measured text direction vectors (`get_text('dict')`): [seen] (`assets/proofs/06-vertical-text.png`)

| Method | Result |
|---|---|
| Table cell `w:textDirection w:val="btLr"` | Text reads bottom to top (dir 0,−1), centred with `vAlign=center` and `jc=center`. **Works.** |
| Table cell `tbRl` | Reads top to bottom (dir 0,+1). **Works.** |
| Shape `wps:bodyPr vert="vert270"` | Reads bottom to top, centred. **Works.** Can be placed anywhere, including flush with the page edge (Market tab at x=196, w=14) or hanging from the top edge (a "2025" tag at y=0). |
| Shape `a:xfrm rot="-5400000"` with horizontal text | The shape rotates but **the text stays horizontal**, drawn outside the shape. **Fails.** |

Snippet: `shape(run, 196, 200, 14, 60, fill='01A198', vert='vert270', anchor='ctr', inset=(0,0,0,0), text_xml=para_xml('SECTION 02', 'Poppins', 10, 'FFFFFF', True, 'center', track=40))`.

Caveat: `check_pdf.py` flags any text within 5 mm of the page edge, so it will report an edge tab. That checker needs an allow-list for tabs.

## 7. Inset page frame. **Works**: the root cause is found and two fixes are verified

Measured stroke positions (mm from each page edge): [seen] (`assets/proofs/07-inset-frame.png`)

| Variant | L | R | T | B |
|---|---|---|---|---|
| A. `pgBorders offsetFrom=page space=28`, header and footer distance 0 (**current reportkit opener**) | 9.88 | 9.90 | 9.88 | **0.02** |
| B. Same, with a header and footer at 11 mm | 9.88 | 9.90 | 9.88 | 9.90 |
| C. `offsetFrom=text`, margins 20, space 28, no header or footer | 9.95 | 9.97 | **0.00** | **0.02** |
| D. `offsetFrom=text`, with header and footer | 9.95 | 9.97 | 0.95 | 0.97 |
| G. `offsetFrom=page`, tiny empty header and footer, **distances 10 mm** | 9.88 | 9.90 | 10.02 | 10.00 |
| H. Header distance 0, **footer distance 10** | 9.88 | 9.90 | 9.88 | 10.00 |
| E. **Header-anchored rect shape** `shape(hdr_run, 10, 10, 190, 277, line=(0.5,'D9DBDB'), behind=True)` | **10.00** | **10.00** | **10.00** | **10.00** |
| F. Body-anchored rect shape | 10.00 | 10.00 | 10.00 | 10.00 (anchor page only) |

**Root cause.** `footer_distance = 0`, which `Report._header_footer(running=None)` sets. LibreOffice then draws the bottom border at the page edge. `offsetFrom="text"` is worse.

**Fix 1 (one line in the engine).** Never set `footer_distance` below about 10 mm when `frame=True`. I patched `examples/sample-report.docx` in scratch (`footer_distance = Mm(10)` on the 2 framed sections). Openers p4 and p7 changed from B 0.01 to B 10.0 mm, and the page count stayed at 13.

**Fix 2 (preferred).** Draw the frame as a header-anchored `rect` shape. It gives exact millimetres, any colour or weight, and colour blocks can cut across it on purpose (z-order). `pgBorders` `space` is limited to whole points (≤ 31 pt), so 10 mm is not possible: 28 pt = 9.88 mm.

## 8. Dark break pages, page background and header suppression. **Works with caveats**

[seen] (`assets/proofs/08-break-pages.png`)
- **Break page via header-anchored full-page rect** (`shape(hdr, 0, 0, 210, 297, fill='1A2E5F')`, header and footer otherwise blank, top margin 150 mm): clean edge to edge. White Poppins Bold 30 pt and tinted Inter body flow as normal paragraphs and are selectable text in the PDF. **This is the recommended break or closing page.**
- **Break page via a full-page shaded table cell:** shows the 1.02 mm white strips at top and bottom (see section 3), because the section has a blank header and footer part.
- **Header and footer suppression:** setting `is_linked_to_previous = False` on the header and footer, with an empty paragraph in each, works. The break pages showed no running header or page number. The next section, with its own header and footer, restored the running header, and the PAGE field kept counting (p4 shows "page 4").
- **`titlePg` (different first page) does not suppress the header** if no section defines a first-page header. LibreOffice then shows the *previous section's default* header on that first page. Avoid it.
- **`w:background`:** document-wide only (see section 3).

## 9. Single-hue bar chart. **Works**

matplotlib output at 300 dpi (1417×732 px for 120×62 mm, `dpi` metadata 300). Fonts are registered from `research/assets/fonts` with `font_manager.addfont`. Bars use shades of one accent from light to deep, with the most recent bar the deepest. Values are labelled directly in Poppins SemiBold. There are no gridlines and no y-axis, and the baseline is `#D9DBDB`. The figure is saved with a transparent background and placed with `add_picture(width=Mm(120))`. [seen] (`assets/proofs/09-single-hue-chart.png`)
```python
def shades(deep, n, light=0.78):            # lightest first, last == deep
    d = to_rgb('#' + deep)
    return [tuple(c + (1 - c) * light * (1 - i / (n - 1)) for c in d) for i in range(n)]
ax.bar(cats, vals, color=shades('1A2E5F', len(vals)), width=0.62)
ax.text(x, v, f'{v:,}', ha='center', va='bottom', fontsize=9, fontfamily='Poppins', fontweight='semibold')
for s in ('top', 'right', 'left'): ax.spines[s].set_visible(False)
ax.set_yticks([]); ax.tick_params(length=0, colors='#5B6270'); fig.savefig(out, dpi=300, transparent=True)
```
Caveat [inferred]: the lightest shade (78 % white mix) of the bright accents (`#01A198`, `#4DCCD4`) becomes very pale on white. Mix from the *deep* token, as I did here, or cap `light` at about 0.65.

## 10. Combined proof

`assets/proofs/10-combined-split-page.png` is one A4 page that uses all of the techniques together:
- a 1/3 header-anchored navy panel with a caps Poppins title (exact leading) and an Inter lede in the text box;
- a 10 mm inset frame drawn as a shape;
- a KPI row of three Lucide icon chips above Poppins numerals in the accent, with Inter captions;
- filled and tint pills;
- Inter body copy;
- the single-hue chart;
- a black-and-white circular photo crop overlapped by an accent dot.

It renders cleanly. [seen]

## 11. Engine reuse audit (`.claude/skills/report-design/scripts/reportkit.py`)

**Reusable as-is.** These are pure OOXML plumbing with no theme values:
- `_rgb`, `_set_fonts`, `_track`, `shade`, `borders`, `pad`, `valign`, `text_direction`, `row_flags`, `p_border`, `make_table`, `set_row_height`, `tiny`, `fix_order` (its `_ORDER` already covers `tblInd`, `textDirection` and so on);
- the `_TOK`/`runs`/`para` inline-markup parser and citation tracking (`Cites`);
- `_Measure`;
- `build_report.py` two-pass pagination (`find_pages` keys on spans ≥ 13 pt; that threshold is fine for Poppins headings);
- `render.sh`.

**Reusable but must take theme parameters.** These read module globals `T`, `C`, `SERIF`, `SANS`, `PW/PH/M/CW` at import time, so only one theme can exist per process:

| Function | What is hard-coded |
|---|---|
| `setup_styles` | Font role per style (serif for body, H1, Display, numerals, Quote); `line=` passed as **auto multiples**, which must become exact pt (see section 1); SlabLabel/SlabNum/SlabText colours hard-coded `"FFFFFF"` (l.230–233); italic serif Quote. |
| `_style` | Default `font=SANS`, `line=1.2` auto. |
| `render_chart` | Loads every font in `ASSETS/fonts`; greys `#8E9692`/`#C9CFCB` hard-coded (l.346); highlight-one-bar logic instead of the light→deep ramp; gridlines toggled. |
| `_header_footer` | Page number font is `SERIF`; header rule; **sets header and footer distance 0 when `running is None`** (the frame bug and the 1 mm gap). |
| `section` | Frame implemented as `pgBorders` with colour `C["rule"]`. |
| `rule_para` | Accent rule. |
| `kpis` | Rules, not icon chips. |
| `callout`, `flow` | The quote has a top rule. |
| `check_pdf.py` | Hard-codes `"Plex"` as the only acceptable font family and flags edge text, so it would fail the Market tab and full-bleed designs. |

**Specific to Slab & Rule; replace per family.** These hold layout literals in mm: `cover` (34 mm slab, rows 60/155/80), `opener` (14 mm label column, rows 95/70/70, `pgBorders` frame), `summary` (52 mm slab), `contents`, `narrative` (margin-note layout), `findings` (20/46 mm columns), `closing` (shaded table on a header section, so it has the 1 mm gap).

**Proposed theme/family abstraction:**
```
families/<id>/tokens.json      # one per reference family (navy-annual, teal-prism, aqua-clinic, ...)
{
  "id": "navy-annual", "page": {"size_mm": [210, 297], "margin_mm": {...}, "header_mm": 10, "footer_mm": 10},
  "color": {"ink": "1F2328", "ink_soft": "5B6270", "paper": "FFFFFF", "paper_alt": "F2F3F4", "rule": "D9DBDB",
            "accent_deep": "1A2E5F", "accent": "05369F", "accent_tint": "E8EDF7", "on_accent": "FFFFFF"},
  "font": {"heading": "Poppins", "heading_semibold": "Poppins SemiBold", "body": "Inter", "numeral": "Poppins",
           "files": ["Poppins-*.ttf", "Inter-*.ttf"], "line_em": {"Poppins": 1.50, "Inter": 1.21}},
  "type_pt": {"display": 40, "h1": 26, "h2": 14, "body": 10, "label": 7.5, "numeral_xl": 40, ...},
  "leading": {"display": 1.05, "h1": 1.05, "body": 1.45},          # converted to EXACT pt by the engine
  "shape": {"radius_adj": 18000, "pill_adj": 50000, "frame": {"inset_mm": 10, "pt": 0.5} | null},
  "icon": {"set": "lucide", "chip_mm": 10, "stroke": 1.75},
  "chart": {"ramp_from": "accent_deep", "light_mix": 0.65, "label_font": "heading_semibold"},
  "layouts": {"cover": "full-field|split-third|photo-block", "opener": "split-third|break-panel",
              "kpi": "icon-chip-row|rounded-slabs", "callout": "big-quote-mark", "table": "deep-header-zebra"}
}
```
- **Engine:** `Theme(tokens)` is an object passed to `Report(meta, theme)`. Every style or helper reads `self.th`, and no module globals are used.
- **Style setup:** `setup_styles(doc, th)` maps roles (heading, body, numeral, label) to font names, applying the RIBBI rule from section 1, and uses exact leading.
- **Layout variants:** registered functions `LAYOUTS["cover"]["split-third"](report, block)`, so one content JSON can render in any family.
- **New primitives** (move from this test code into a `drawing.py` module): `shape()` / `inline_shape()` / `anchored_picture()` / `para_xml()`, `masks.py` (circle / rounded / cut-corner / grayscale), `icon_chip()`, `shades()`.
- **Section/page primitive:** `page_canvas(section, blocks=[...])` puts full-bleed panels, the frame and tabs into the section header, so they repeat on every page of that section.
- **check_pdf:** reads `theme.font.files` for the allowed fonts and an `edge_ok` allow-list (tabs, bleeds).

---

## Summary table

| Technique | Method | Status | Caveat |
|---|---|---|---|
| Poppins / Montserrat / Inter | npm `@expo-google-fonts/*` TTFs → `~/.fonts`; `rFonts` = family; 500/600/800 by family name ("Poppins SemiBold"), 700 = base family + `w:b` | Works | Leading must be **exact pt** (Poppins auto = 1.50 em/line). No `w:b` on non-RIBBI weights. DOCX needs fonts installed or embedded (via LibreOffice round-trip, +4.6 MB). |
| Line icons in solid circles | `lucide-static` SVG → cairosvg PNG 300 dpi, white stroke on accent circle | Works | Vendor only the used SVGs; ISC/MIT licence file. |
| Full-bleed cover / panel / band | Header-anchored `wps` rect (`relativeFrom=page`, behindDoc) **or** table cell shading with margins 0, `tblInd` negative | Works | Tables: blank page if a normal paragraph follows (use the sectPr paragraph or `vanish`); 1 mm gap on any section with a header or footer part, so use shapes there. |
| Document page colour | `w:background` + `displayBackgroundShape` | Works with caveats | Whole document only, not per page. |
| Rounded slabs / pills with text | `wps:wsp prstGeom=roundRect` (`adj` 18000–50000) + `txbx`; `spAutoFit` to grow | Works | `wrapNone` takes no flow space; paragraph-relative `y` includes `space_before`; Word untested. |
| Rounded PNG behind cell text | Anchored behind-text PNG in the cell's paragraph | Works with caveats | Fixed size; prefer shapes. |
| Cut-corner / rounded / circle photo | PIL RGBA mask at 300 dpi, inline or anchored | Works | Crop to the box aspect ratio before inserting. |
| Colour block over photo | Behind-text photo + shaded table cell, or photo z=2 + shape z=3 | Works | Front-anchored photos cover text; no reflow. |
| Vertical tab text | Cell `textDirection btLr/tbRl`, or shape `vert="vert270"` | Works | `xfrm rot` does not rotate the text (fails). `check_pdf` flags edge text. |
| Inset frame 10 mm | Header-anchored rect shape (exact 10.00 mm); or `pgBorders` with `footer_distance` ≥ 10 mm | Works | Current engine (`footer_distance=0`) puts the bottom edge at 0.02 mm; `pgBorders` gives at best 9.88 mm (whole-pt spacing). |
| Dark break page | Header-anchored full-page rect + white text paragraphs; blank unlinked header and footer | Works | Not `titlePg` (inherits the previous header); not a full-page table (1 mm gaps). |
| Header/footer suppression | `is_linked_to_previous=False` + empty paragraph; the next section re-defines its own | Works | PAGE numbering continues across suppressed pages. |
| Single-hue bar chart | matplotlib 300 dpi PNG, Poppins/Inter via `addfont`, light→deep ramp, direct labels | Works | Bright accents get too pale; ramp from the deep token. |
| Engine reuse | XML helpers, `para`/`runs`, `fix_order`, two-pass TOC reusable; styles, charts, layouts need a `Theme` object | Needs refactor | Module-global tokens; auto leading; `footer_distance=0`; `check_pdf` hard-codes Plex. |
