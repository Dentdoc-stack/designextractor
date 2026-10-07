#!/usr/bin/env python3
"""Test report in design H "Spectrum" (DESIGN.md section 4.H): a coordinated multicolour system.

usage: build.py OUTDIR      -> OUTDIR/spectrum-impact-test.docx (+ chart/icon PNGs)
Render:  soffice --headless --convert-to pdf --outdir OUTDIR OUTDIR/spectrum-impact-test.docx

Every section owns one colour; all five meet only on the cover, contents, overview, finance and back cover.
All names and figures are invented (illustrative sample). Fonts: Figtree from ../../assets/fonts.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import docxkit as kit  # noqa: E402
from docxkit import (P, T, cell_p, cell_style, hexc, inline_pic, page, row_no_split, shape,  # noqa: E402
                     table, text_box)

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")

# ----------------------------------------------------------------------------- tokens (DESIGN.md 4.H)
INK, SOFT, BAND, RULE, WHITE = "16213E", "5A5F6E", "F2EFEA", "D9D9D9", "FFFFFF"
F, FSB, FXB = "Figtree", "Figtree SemiBold", "Figtree ExtraBold"
SHORT = "LUMEN FOUNDATION · IMPACT REPORT 2025 · ILLUSTRATIVE SAMPLE"


def mix(h, t):
    """Mix a hex colour toward white by t (0 = colour, 1 = white)."""
    c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % round(v + (255 - v) * t) for v in c)


# fill = marks and bands; panel = fill carrying text (white unless on="ink"); deep = accent text on white (>= 7:1)
S = {
    "edu": dict(name="Education", fill="2559D6", panel="2559D6", deep="2150C2", tint="EBEFFA", on=WHITE),
    "hea": dict(name="Health", fill="E04F39", panel="D83A22", deep="A62C1A", tint="FAEDEB", on=WHITE),
    "env": dict(name="Environment", fill="009682", panel="008473", deep="006557", tint="EBFAF8", on=WHITE),
    "com": dict(name="Communities", fill="D4891A", panel="D4891A", deep="7B500F", tint="FAF4EB", on=INK),
    "fin": dict(name="Finance", fill="8A3FB0", panel="8A3FB0", deep="7E39A1", tint="F4ECF8", on=WHITE),
}
ORDER = ["edu", "hea", "env", "com", "fin"]          # categorical order, validated (dataviz validator: all checks pass)

doc = kit.configure(OUT, font=F, ink=INK, soft=SOFT, footer=SHORT, icons=HERE / "icons")


def icon(name, fill, size_mm=12, fg="#FFFFFF"):
    return kit.icon(name, fill, size_mm, fg=fg)


# ----------------------------------------------------------------------------- motif: the spectrum strip
def strip(current=None, h=3.0, tab=10.0, y=0):
    """Five equal segments across the top edge, 0.8 mm gaps; the current section drops down as a tab."""
    def draw(run):
        w = (210 - 4 * 0.8) / 5
        for i, key in enumerate(ORDER):
            shape(run, i * (w + 0.8), y, w, tab if key == current else h, fill=S[key]["fill"], behind=True, z=3)
    return draw


# ----------------------------------------------------------------------------- charts (single hue inside a section)
def _clean(ax, left=False):
    for s in ("top", "right", "left") if not left else ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0, pad=4, colors=hexc(SOFT))


def columns(path, cats, vals, key, w, h, fmt="{:,.0f}"):
    fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=300)
    ax = fig.add_axes([0.02, 0.12, 0.96, 0.82])
    cols = [hexc(mix(S[key]["fill"], 0.62))] * (len(vals) - 1) + [hexc(S[key]["fill"])]
    ax.bar(range(len(vals)), vals, color=cols, width=0.58)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.03, fmt.format(v), ha="center", va="bottom", fontsize=8.5, color=hexc(INK),
                fontweight="bold" if i == len(vals) - 1 else "normal")
    ax.set_xticks(range(len(vals)), cats, fontsize=8)
    ax.set_yticks([])
    ax.set_ylim(0, max(vals) * 1.18)
    _clean(ax)
    ax.spines["bottom"].set_color("#C9CCD3")
    ax.spines["bottom"].set_linewidth(0.6)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def line(path, cats, vals, key, w, h, unit=""):
    fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=300)
    ax = fig.add_axes([0.03, 0.14, 0.86, 0.8])
    x = list(range(len(vals)))
    ax.fill_between(x, vals, color=hexc(S[key]["tint"]), zorder=1)
    ax.plot(x, vals, color=hexc(S[key]["fill"]), lw=2, zorder=2)
    ax.plot(x[-1], vals[-1], "o", ms=6, color=hexc(S[key]["fill"]), mec="white", mew=1.5, zorder=3)
    ax.text(x[-1] + 0.15, vals[-1], f"{vals[-1]:,}{unit}", va="center", fontsize=9, fontweight="bold", color=hexc(INK))
    ax.text(x[0], vals[0] + max(vals) * 0.06, f"{vals[0]:,}{unit}", ha="left", fontsize=8, color=hexc(INK))
    ax.set_xticks(x, cats, fontsize=8)
    ax.set_yticks([])
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_xlim(-0.2, len(vals) - 0.6)
    _clean(ax)
    ax.spines["bottom"].set_color("#C9CCD3")
    ax.spines["bottom"].set_linewidth(0.6)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def hbars(path, cats, vals, key, w, h, fmt="{:,.0f}"):
    fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=300)
    ax = fig.add_axes([0.2, 0.04, 0.72, 0.92])
    y = list(range(len(vals)))[::-1]
    cols = [hexc(S[key]["fill"])] + [hexc(mix(S[key]["fill"], 0.55))] * (len(vals) - 1)
    ax.barh(y, vals, color=cols, height=0.6)
    for yi, v in zip(y, vals):
        ax.text(v + max(vals) * 0.015, yi, fmt.format(v), va="center", fontsize=8.5, color=hexc(INK))
    ax.set_yticks(y, cats, fontsize=8.5, color=hexc(INK))
    ax.set_xticks([])
    ax.set_xlim(0, max(vals) * 1.15)
    _clean(ax, left=True)
    ax.spines["left"].set_color("#C9CCD3")
    ax.spines["left"].set_linewidth(0.6)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def donut(path, shares, d=72):
    fig = plt.figure(figsize=(d / 25.4, d / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.pie(shares, colors=[hexc(S[k]["fill"]) for k in ORDER], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.34, edgecolor="white", linewidth=2.2))
    ax.text(0, 0.08, "48.6 M", ha="center", va="center", fontsize=17, fontweight="heavy", color=hexc(INK))
    ax.text(0, -0.17, "spent in 2025", ha="center", va="center", fontsize=7.5, color=hexc(SOFT))
    ax.set_aspect("equal")
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def stacked(path, years, series, w, h):
    """Stacked columns, categorical in fixed order, 2 px white gaps between segments."""
    fig = plt.figure(figsize=(w / 25.4, h / 25.4), dpi=300)
    ax = fig.add_axes([0.02, 0.12, 0.96, 0.84])
    bottom = [0] * len(years)
    for key in ORDER:
        vals = series[key]
        ax.bar(range(len(years)), vals, bottom=bottom, color=hexc(S[key]["fill"]), width=0.5,
               edgecolor="white", linewidth=1.4)
        bottom = [b + v for b, v in zip(bottom, vals)]
    for i, t in enumerate(bottom):
        ax.text(i, t + 1.2, f"{t:.1f} M", ha="center", va="bottom", fontsize=8.5, fontweight="bold", color=hexc(INK))
    ax.set_xticks(range(len(years)), years, fontsize=8.5)
    ax.set_yticks([])
    ax.set_ylim(0, max(bottom) * 1.15)
    _clean(ax)
    ax.spines["bottom"].set_color("#C9CCD3")
    ax.spines["bottom"].set_linewidth(0.6)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def dot_png(col, mm=3.2):
    from PIL import Image, ImageDraw
    px = round(mm / 25.4 * 300) * 4
    im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, px - 1, px - 1], radius=px // 6, fill="#" + col)
    out = OUT / f"sq-{col}.png"
    im.resize((px // 4, px // 4)).save(out)
    return out


columns(OUT / "edu.png", ["2021", "2022", "2023", "2024", "2025"], [18400, 22100, 26900, 31200, 38600], "edu", 104, 70)
line(OUT / "env.png", ["2021", "2022", "2023", "2024", "2025"], [3200, 5100, 7400, 9900, 13600], "env", 168, 62, " t")
hbars(OUT / "com.png", ["Northside", "Riverside", "Old Town", "Eastfield", "Harbour"], [2.4, 1.9, 1.6, 1.1, 0.8], "com",
      104, 58, "{:.1f} M")
donut(OUT / "donut.png", [34, 27, 18, 14, 7])
stacked(OUT / "fin.png", ["2023", "2024", "2025"],
        {"edu": [11.2, 13.6, 16.5], "hea": [9.8, 11.4, 13.1], "env": [5.1, 6.9, 8.7], "com": [4.4, 5.6, 6.8],
         "fin": [3.0, 3.2, 3.5]}, 104, 82)


# ----------------------------------------------------------------------------- reusable blocks
def kicker(container, text, color, after=6, before=0):
    P(container, text, 7.5, color, FSB, track=40, lead=1.3, after=after, before=before)


def band_page(key, num, title, lede, chip):
    """First page of a section: full-bleed colour band (0-112 mm) carrying number, title and lede."""
    s = S[key]
    page(top=126, header_shapes=[lambda r: shape(r, 0, 0, 210, 112, fill=s["panel"], behind=True, z=1),
                                 lambda r: shape(r, 0, 112, 210, 3, fill=s["fill"], behind=True, z=2)])
    a = P(doc, "")
    run = a.add_run()
    light = mix(s["panel"], 0.38) if s["on"] == WHITE else mix(s["panel"], 0.45)
    text_box(run, 20, 6, 120, 46, [T(num, 120, light, FXB, lead=0.95)])
    text_box(run, 22, 50, 150, 8, [T(f"PROGRAMME {num} · {s['name'].upper()}", 7.5, s["on"], FSB, track=40)])
    text_box(run, 22, 57, 160, 28, [T(title, 30, s["on"], FXB, lead=1.08)])
    text_box(run, 22, 88, 135, 20, [T(lede, 10.5, s["on"], F, lead=1.45)])
    chip_fill = "FFFFFF" if s["on"] == WHITE else INK
    chip_fg = "#" + (s["panel"] if s["on"] == WHITE else "FFFFFF")
    kit.picture(run, icon(chip, chip_fill, 18, fg=chip_fg), 170, 20, 18, 18, behind=False, z=30)
    return a


def kpi_row(container, key, items, widths=(56, 56, 56)):
    t = table(container, list(widths), 1, cell_margin=(0, 4, 0, 4))
    for i, (cell, (num, cap)) in enumerate(zip(t.rows[0].cells, items)):
        cell_style(cell, borders={"top": (1.5, S[key]["fill"]), "left": (0.5, RULE) if i else None})
        cell_p(cell, num, 28, S[key]["deep"], FXB, lead=1.15, before=6, after=2, left_indent=0 if i == 0 else 4)
        cell_p(cell, cap, 8.5, SOFT, F, lead=1.4, left_indent=0 if i == 0 else 4, right_indent=4)
    return t


def two_col_text(container, paras, gap=8):
    t = table(container, [80, gap, 80], 1)
    half = (len(paras) + 1) // 2
    for i, par in enumerate(paras):
        cell_p(t.rows[0].cells[0 if i < half else 2], par, 10, INK, F, lead=1.5, after=8)
    return t


def case_card(container, key, label, title, body, width=168):
    t = table(container, [width], 1, cell_margin=(7, 6, 7, 6))
    c = t.rows[0].cells[0]
    cell_style(c, fill=S[key]["tint"], borders={"left": (4.5, S[key]["fill"])})
    kicker(c, label, S[key]["deep"], after=4)
    cell_p(c, title, 13, INK, F, bold=True, lead=1.3, after=4)
    cell_p(c, body, 9.5, INK, F, lead=1.5)
    return t


def quote(container, key, text, by):
    P(container, "“", 54, S[key]["fill"], FXB, lead=0.85)
    P(container, text, 15, INK, F, lead=1.42, after=8)
    kicker(container, by, SOFT)


# ============================================================================= p1 cover
page(folio=False, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=INK, behind=True, z=1)])
a = P(doc, "")
run = a.add_run()
heights = [118, 96, 136, 80, 60]                     # the composition reads as a bar chart of the year
w = (210 - 4 * 1.2) / 5
for i, (key, hgt) in enumerate(zip(ORDER, heights)):
    shape(run, i * (w + 1.2), 297 - hgt, w, hgt, fill=S[key]["panel"], behind=True, z=3)
text_box(run, 20, 24, 170, 10, [T("LUMEN FOUNDATION · ILLUSTRATIVE SAMPLE", 7.5, mix(INK, 0.55), FSB, track=40)])
text_box(run, 20, 44, 175, 70, [T("IMPACT\nREPORT", 72, WHITE, FXB, lead=0.98)])
text_box(run, 20, 110, 120, 30, [T("2025", 60, S["com"]["fill"], FXB, lead=1.0)])
text_box(run, 20, 136, 130, 12, [T("Five programmes, one city, 214,000 people reached", 13, mix(INK, 0.7), F, lead=1.4)])
for i, key in enumerate(ORDER):
    text_box(run, i * (w + 1.2) + 4, 297 - heights[i] + 4, w - 8, 10,
             [T(S[key]["name"].upper(), 7, S[key]["on"], FSB, track=30)], z=40)

# ============================================================================= p2 contents
page(top=34, header_shapes=[strip()])
P(doc, "CONTENTS", 34, INK, FXB, lead=1.1, after=26)
toc = [(None, "Foreword", "A letter from the director", "03"), (None, "2025 at a glance", "The year in numbers", "04"),
       ("edu", "Education", "Reading, tutoring and school meals", "05"), ("hea", "Health", "Community clinics and mental health", "07"),
       ("env", "Environment", "Trees, retrofits and clean air", "09"), ("com", "Communities", "Grants, housing and local groups", "11"),
       ("fin", "Finance", "Where the money came from and went", "13")]
ct = table(doc, [16, 128, 24], len(toc), cell_margin=(0, 4, 0, 4))
n = 0
for row, (key, title, desc, pg) in zip(ct.rows, toc):
    row_no_split(row)
    c0, c1, c2 = row.cells
    for c in row.cells:
        cell_style(c, borders={"bottom": (0.5, RULE)}, valign="center")
    if key:
        n += 1
        inline_pic(c0, dot_png(S[key]["fill"], 10), 10, align="left", before=6, after=6)
    else:
        cell_p(c0, "", 10)
    cell_p(c1, title, 15, INK, FXB if key else FSB, lead=1.25, before=6)
    cell_p(c1, desc, 9, SOFT, F, lead=1.4, after=6)
    cell_p(c2, pg, 15, S[key]["deep"] if key else SOFT, FXB, lead=1.25, align="right")
P(doc, "", 6, before=26)
kicker(doc, "HOW TO READ THIS REPORT", SOFT, after=4)
P(doc, "Each programme has its own colour. The strip at the top of every page shows where you are: the current "
       "programme's colour drops down as a tab.", 9.5, INK, F, lead=1.5, right_indent=40)

# ============================================================================= p3 foreword
page(top=34, header_shapes=[strip()])
kicker(doc, "FOREWORD", SOFT, after=10)
P(doc, "“", 72, S["hea"]["fill"], FXB, lead=0.8)
P(doc, "We measure a good year by the number of people who no longer need us.", 26, INK, FXB, lead=1.18,
  right_indent=12, after=22)
two_col_text(doc, [
    "Lumen Foundation was set up eleven years ago with one idea: that a city's problems are connected, so the "
    "answers should be too. A child who reads well, a family in a warm home and a street with clean air are parts "
    "of the same story.",
    "In 2025 we reached 214,000 people through five programmes, more than in any previous year. We opened two new "
    "community clinics, planted our 50,000th tree and gave 640 grants to local groups, most of them under 5,000.",
    "This report is organised by programme. Each has its own colour, so you can follow one thread or read the "
    "whole picture. Every figure is checked by our independent evaluation partner.",
    "None of this would be possible without 3,400 volunteers, 61 partner organisations and the donors who trusted "
    "us with their money. Thank you. The work is not finished, and next year we will ask even more of ourselves."])
P(doc, "Dr Amara Lindqvist", 11, INK, F, bold=True, lead=1.3, before=10)
P(doc, "Director, Lumen Foundation", 9, SOFT, F, lead=1.4, after=24)
kicker(doc, "2025 IN FIVE MOMENTS", SOFT, after=8)
moments = [("edu", "FEB", "Maths tutoring pilot starts in six schools"), ("hea", "MAR", "Eastfield clinic opens its doors"),
           ("env", "JUN", "The 50,000th street tree is planted"), ("com", "SEP", "Harbour hub opens for local groups"),
           ("fin", "DEC", "Running costs stay below 8%")]
mt = table(doc, [32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4], 1)
for i, (key, mon, txt) in enumerate(moments):
    c = mt.rows[0].cells[i * 2]
    cell_style(c, borders={"top": (3, S[key]["fill"])})
    cell_p(c, mon, 16, S[key]["deep"], FXB, lead=1.2, before=6, after=2)
    cell_p(c, txt, 8.5, INK, F, lead=1.4, right_indent=2)

# ============================================================================= p4 at a glance
page(top=30, header_shapes=[strip()])
kicker(doc, "OVERVIEW", SOFT)
P(doc, "2025 AT A GLANCE", 34, INK, FXB, lead=1.1, after=16)
tiles = [("edu", "graduation-cap", "38,600", "children in reading and tutoring programmes"),
         ("hea", "heart-pulse", "92,400", "clinic visits across six community clinics"),
         ("env", "sprout", "13,600 t", "of CO₂ avoided through trees and retrofits"),
         ("com", "house-heart", "640", "grants to local groups, worth 6.8 million")]
gt = table(doc, [82, 4, 82], 2)
for i, (key, ic, num, cap) in enumerate(tiles):
    c = gt.rows[i // 2].cells[(i % 2) * 2]
    inner = table(c, [82], 1, cell_margin=(6, 6, 6, 6))
    ic_ = inner.rows[0].cells[0]
    cell_style(ic_, fill=S[key]["tint"], borders={"top": (3, S[key]["fill"])})
    inline_pic(ic_, icon(ic, S[key]["fill"], 11), 11, align="left", after=6)
    kicker(ic_, S[key]["name"].upper(), S[key]["deep"], after=2)
    cell_p(ic_, num, 30, S[key]["deep"], FXB, lead=1.12, after=2)
    cell_p(ic_, cap, 9, INK, F, lead=1.4)
    if i < 2:
        cell_p(c, "", 4, lead=1.0, after=8)
P(doc, "", 6, before=14)
dt = table(doc, [80, 10, 78], 1)
inline_pic(dt.rows[0].cells[0], OUT / "donut.png", 72, align="left")
lg = dt.rows[0].cells[2]
kicker(lg, "WHERE THE MONEY WENT", SOFT, before=4, after=8)
for key, pct in zip(ORDER, [34, 27, 18, 14, 7]):
    row = table(lg, [8, 54, 16], 1)
    inline_pic(row.rows[0].cells[0], dot_png(S[key]["fill"]), 3.2, align="left", before=4)
    cell_p(row.rows[0].cells[1], S[key]["name"] if key != "fin" else "Running the foundation", 10, INK, F, lead=1.4, before=1)
    cell_p(row.rows[0].cells[2], f"{pct}%", 10, INK, F, bold=True, lead=1.4, align="right", before=1)
    cell_style(row.rows[0].cells[1], borders={"bottom": (0.5, RULE)})
    cell_style(row.rows[0].cells[2], borders={"bottom": (0.5, RULE)})

# ============================================================================= p5-6 education (blue)
band_page("edu", "01", "Every child reading\nby age eleven",
          "Tutoring, libraries and breakfast clubs in 84 schools, focused on the neighbourhoods where reading scores lag.",
          "book-open")
kpi_row(doc, "edu", [("38,600", "children reached, up 24% on 2024"), ("84", "partner schools, 19 of them new"),
                     ("+9 pts", "rise in age-11 reading scores at partner schools")])
P(doc, "", 6, before=10)
two_col_text(doc, [
    "Reading by eleven is the single best predictor we have of how a child does at sixteen. That is why most of the "
    "education budget goes to one-to-one tutoring in the last two years of primary school.",
    "In 2025, 2,100 trained volunteers gave 146,000 hours of tutoring. Schools choose the children, and every child is "
    "tested at the start and end of the year so we can see what works.",
    "Breakfast clubs now run in 52 schools and serve 9,800 children a day. Teachers tell us that attendance and "
    "concentration in the first lesson have both improved.",
    "Next year we will add maths tutoring in 20 schools, using the same model and the same measurement."])

page(top=30, header_shapes=[strip("edu")])
kicker(doc, "PROGRAMME 01 · EDUCATION", S["edu"]["deep"])
P(doc, "MORE CHILDREN, EVERY YEAR", 22, INK, FXB, lead=1.15, after=14)
et = table(doc, [104, 8, 56], 1)
c = et.rows[0].cells[0]
kicker(c, "FIGURE 1 — CHILDREN REACHED, 2021–2025", SOFT, after=6)
inline_pic(c, OUT / "edu.png", 104, align="left")
cell_p(c, "Source: Lumen programme records (illustrative).", 7.5, SOFT, F, lead=1.4, before=4)
r = et.rows[0].cells[2]
cell_p(r, "Growth came from new schools, not bigger classes.", 12, INK, F, bold=True, lead=1.35, before=18, after=6)
cell_p(r, "Each school keeps the same tutor-to-child ratio of one to three, so quality holds as numbers rise.", 9.5,
       INK, F, lead=1.5)
P(doc, "", 6, before=18)
case_card(doc, "edu", "CASE STUDY · RIVERSIDE PRIMARY", "From the bottom ten to the city average in two years",
          "Riverside joined the programme in 2023 with one of the lowest reading scores in the city. Two years and "
          "3,800 tutoring hours later, 71% of its eleven-year-olds read at the expected level, against 74% across the "
          "city. The school now trains other schools' volunteers.")
P(doc, "", 6, before=16)
quote(doc, "edu", "My tutor never got bored of the same book. Now I pick my own.", "PUPIL, AGE TEN, RIVERSIDE PRIMARY")

# ============================================================================= p7-8 health (coral)
band_page("hea", "02", "Care close to home",
          "Six community clinics, a mental-health line and home visits for people who find it hard to get to a doctor.",
          "stethoscope")
kpi_row(doc, "hea", [("92,400", "clinic visits, 18% more than in 2024"), ("6", "community clinics, two opened in 2025"),
                     ("4 days", "average wait for a first appointment")])
P(doc, "", 6, before=10)
two_col_text(doc, [
    "Our clinics sit in community centres, not hospitals. They are open in the evening and on Saturdays, and most "
    "visits are booked by phone or simply by walking in.",
    "The two new clinics in Eastfield and Harbour opened in March and September. Together they saw 21,000 visits in "
    "their first months, mostly for long-term conditions such as diabetes and asthma.",
    "The mental-health line took 14,200 calls. Two thirds of callers were offered a follow-up session within a week, "
    "and 83% said the call helped.",
    "Home visits reached 1,900 older or disabled residents, many of whom had not seen a health professional in more "
    "than a year."])

page(top=30, header_shapes=[strip("hea")])
kicker(doc, "PROGRAMME 02 · HEALTH", S["hea"]["deep"])
P(doc, "CLINICS IN 2025", 22, INK, FXB, lead=1.15, after=14)
kicker(doc, "TABLE 1 — VISITS AND WAITING TIMES BY CLINIC", SOFT, after=6)
hdr = ["Clinic", "Opened", "Visits", "Change", "Wait (days)", "Satisfied"]
rows = [("Northside", "2016", "21,300", "+6%", "3", "94%"), ("Riverside", "2018", "18,900", "+4%", "4", "92%"),
        ("Old Town", "2019", "16,700", "+9%", "5", "91%"), ("Westgate", "2021", "14,500", "+12%", "4", "93%"),
        ("Eastfield", "2025", "12,800", "new", "3", "95%"), ("Harbour", "2025", "8,200", "new", "6", "90%")]
tb = table(doc, [40, 22, 28, 26, 26, 26], 2 + len(rows), cell_margin=(3, 2.6, 3, 2.6))
for i, h in enumerate(hdr):
    c = tb.rows[0].cells[i]
    cell_style(c, fill=S["hea"]["panel"], valign="bottom")
    cell_p(c, h.upper(), 7.5, WHITE, F, bold=True, track=10, lead=1.25, align="left" if i == 0 else "right")
row_no_split(tb.rows[0], header=True)
for r_i, rv in enumerate(rows, 1):
    for i, v in enumerate(rv):
        c = tb.rows[r_i].cells[i]
        cell_style(c, fill=S["hea"]["tint"] if r_i % 2 == 0 else None, borders={"bottom": (0.5, RULE)})
        cell_p(c, v, 9.5, INK, FSB if i == 0 else F, lead=1.3, align="left" if i == 0 else "right")
for i, v in enumerate(("All clinics", "", "92,400", "+18%", "4", "93%")):
    c = tb.rows[-1].cells[i]
    cell_style(c, borders={"top": (1.5, S["hea"]["fill"]), "bottom": (0.5, RULE)})
    cell_p(c, v, 9.5, S["hea"]["deep"], F, bold=True, lead=1.3, align="left" if i == 0 else "right")
P(doc, "Wait = average days from first contact to first appointment. Satisfaction from exit surveys. Illustrative.",
  7.5, SOFT, F, lead=1.4, before=5, after=20)
ht = table(doc, [80, 8, 80], 1)
case_card(ht.rows[0].cells[0], "hea", "WHAT CHANGED", "Evening sessions halved missed appointments",
          "Clinics that opened until 8 pm saw missed appointments fall from 14% to 7%, mostly among working parents.",
          width=80)
q = ht.rows[0].cells[2]
cell_p(q, "“", 54, S["hea"]["fill"], FXB, lead=0.85)
cell_p(q, "I came in on my way home from work. Nobody made me feel I was wasting their time.", 14, INK, F,
       lead=1.42, after=8)
cell_p(q, "PATIENT, EASTFIELD CLINIC", 7.5, SOFT, FSB, track=40)
P(doc, "", 6, before=18)
kpi_row(doc, "hea", [("2", "more clinics planned for 2026, in Westgate North and Millbrook"),
                     ("24/7", "mental-health line from April, with trained volunteers overnight"),
                     ("3 days", "target wait for a first appointment by the end of 2026")])

# ============================================================================= p9-10 environment (teal)
band_page("env", "03", "Cleaner air, warmer homes",
          "Street trees, home retrofits and school-run clean-air zones in the neighbourhoods with the worst air.",
          "trees")
kpi_row(doc, "env", [("50,000", "trees planted since 2019, 9,400 of them this year"), ("1,240", "homes insulated, saving 310 a year each"),
                     ("−22%", "nitrogen dioxide outside 30 schools")])
P(doc, "", 6, before=10)
two_col_text(doc, [
    "The environment programme works where pollution and fuel poverty overlap. In those streets, a tree, an insulated "
    "loft or a car-free school gate makes the biggest difference to health and household bills.",
    "Volunteers planted 9,400 street trees this year, chosen with residents. Survival after two years is 91%, well "
    "above the city's own planting.",
    "The retrofit scheme insulated 1,240 homes, all of them for households on low incomes, at no cost to the "
    "occupants. Average heating bills fell by 310 a year.",
    "Clean-air zones now cover the school run at 30 primary schools, with traffic closed for 45 minutes at each end "
    "of the day."])

page(top=30, header_shapes=[strip("env")])
kicker(doc, "PROGRAMME 03 · ENVIRONMENT", S["env"]["deep"])
P(doc, "CARBON AVOIDED IS GROWING FAST", 22, INK, FXB, lead=1.15, after=14)
kicker(doc, "FIGURE 2 — TONNES OF CO₂ AVOIDED EACH YEAR", SOFT, after=6)
inline_pic(doc, OUT / "env.png", 168, align="left")
P(doc, "Source: Lumen environment programme, independently verified (illustrative).", 7.5, SOFT, F, lead=1.4,
  before=4, after=18)
kicker(doc, "HOW A RETROFIT WORKS", S["env"]["deep"], after=8)
st = table(doc, [40, 2.67, 40, 2.67, 40, 2.67, 40], 1)
steps = [("01", "Referral", "From a GP, school or neighbour, or by calling us."), ("02", "Survey", "A free home survey within two weeks."),
         ("03", "Install", "Loft, wall and draught-proofing in one visit."), ("04", "Follow-up", "We check bills and comfort after one winter.")]
for i, (n_, h, d) in enumerate(steps):
    c = st.rows[0].cells[i * 2]
    cell_style(c, fill=S["env"]["tint"], borders={"top": (3, S["env"]["fill"])})
    cell_p(c, n_, 22, S["env"]["deep"], FXB, lead=1.15, before=8, left_indent=4)
    cell_p(c, h, 11, INK, F, bold=True, lead=1.3, left_indent=4, after=2)
    cell_p(c, d, 8.5, INK, F, lead=1.4, left_indent=4, right_indent=4, after=10)
P(doc, "", 6, before=18)
case_card(doc, "env", "CASE STUDY · ALDER STREET", "Forty homes, one street, one winter",
          "Alder Street was insulated house by house over six weeks in the autumn. Residents' heating bills fell by "
          "an average of 34%, and damp complaints to the housing association dropped from 17 to two.")

# ============================================================================= p11-12 communities (saffron, ink text)
band_page("com", "04", "Small grants,\nbig difference",
          "Grants, advice and space for the local groups that know their neighbourhoods best.", "hand-coins")
kpi_row(doc, "com", [("640", "grants awarded, 71% of them under 5,000"), ("6.8 M", "granted to local groups and projects"),
                     ("3,400", "volunteers active in the year")])
P(doc, "", 6, before=10)
two_col_text(doc, [
    "Most of our community grants are small, quick and simple to apply for. A group can apply in one page and hear "
    "back within three weeks.",
    "In 2025 we gave 640 grants. The most common uses were youth activities, food projects and help with energy "
    "bills, and two thirds went to groups run entirely by volunteers.",
    "We also gave 38 larger grants of up to 60,000 to organisations that run services all year, such as advice "
    "centres and lunch clubs for older people.",
    "Every grant holder can use our three community hubs free of charge, and 120 groups now meet there each month."])

page(top=30, header_shapes=[strip("com")])
kicker(doc, "PROGRAMME 04 · COMMUNITIES", S["com"]["deep"])
P(doc, "WHERE THE GRANTS WENT", 22, INK, FXB, lead=1.15, after=14)
cm = table(doc, [104, 8, 56], 1)
c = cm.rows[0].cells[0]
kicker(c, "FIGURE 3 — GRANTS BY NEIGHBOURHOOD, MILLIONS", SOFT, after=6)
inline_pic(c, OUT / "com.png", 104, align="left")
cell_p(c, "Source: Lumen grants database (illustrative). Darkest bar = largest share.", 7.5, SOFT, F, lead=1.4, before=4)
r = cm.rows[0].cells[2]
cell_p(r, "Northside receives most because it has the most groups, not the largest grants.", 12, INK, F, bold=True,
       lead=1.35, before=14, after=6)
cell_p(r, "The average grant is similar everywhere, around 9,000.", 9.5, INK, F, lead=1.5)
P(doc, "", 6, before=20)
gt2 = table(doc, [80, 8, 80], 1)
case_card(gt2.rows[0].cells[0], "com", "CASE STUDY · HARBOUR LARDER", "A food bank that became a café",
          "A 3,000 grant in 2023 bought a fridge. Today the Harbour Larder runs a pay-what-you-can café five days a "
          "week and employs four local people.", width=80)
q = gt2.rows[0].cells[2]
cell_p(q, "“", 54, S["com"]["fill"], FXB, lead=0.85)
cell_p(q, "The grant was small. What it said to us was: we trust you to get on with it.", 14, INK, F, lead=1.42, after=8)
cell_p(q, "VOLUNTEER, HARBOUR LARDER", 7.5, SOFT, FSB, track=40)
P(doc, "", 6, before=18)
kicker(doc, "HOW A SMALL GRANT WORKS", S["com"]["deep"], after=8)
st2 = table(doc, [54, 3, 54, 3, 54], 1)
for i, (n_, h, d) in enumerate([("01", "Apply", "One page, online or on paper, in any language."),
                                ("02", "Decide", "A panel of residents decides within three weeks."),
                                ("03", "Report", "Tell us what happened in a short call or a photo.")]):
    c = st2.rows[0].cells[i * 2]
    cell_style(c, fill=S["com"]["tint"], borders={"top": (3, S["com"]["fill"])})
    cell_p(c, n_, 22, S["com"]["deep"], FXB, lead=1.15, before=8, left_indent=4)
    cell_p(c, h, 11, INK, F, bold=True, lead=1.3, left_indent=4, after=2)
    cell_p(c, d, 8.5, INK, F, lead=1.4, left_indent=4, right_indent=4, after=10)

# ============================================================================= p13 finance (all colours)
page(top=30, header_shapes=[strip("fin")])
kicker(doc, "FINANCE", S["fin"]["deep"])
P(doc, "WHERE THE MONEY\nCAME FROM AND WENT", 26, INK, FXB, lead=1.12, after=14)
ft = table(doc, [104, 8, 56], 1)
c = ft.rows[0].cells[0]
kicker(c, "FIGURE 4 — SPENDING BY PROGRAMME, MILLIONS", SOFT, after=6)
inline_pic(c, OUT / "fin.png", 104, align="left")
r = ft.rows[0].cells[2]
kicker(r, "LEGEND", SOFT, before=14, after=6)
for key in ORDER:
    row = table(r, [7, 49], 1)
    inline_pic(row.rows[0].cells[0], dot_png(S[key]["fill"]), 3.2, align="left", before=3)
    cell_p(row.rows[0].cells[1], S[key]["name"] if key != "fin" else "Running the foundation", 9.5, INK, F, lead=1.6)
cell_p(r, "Running costs stayed below 8% of spending for the fifth year.", 10, INK, F, bold=True, lead=1.4, before=12)
P(doc, "", 6, before=14)
kicker(doc, "TABLE 2 — INCOME AND SPENDING, MILLIONS", SOFT, after=6)
inc = [("Donations and legacies", "21.4", "Education", "16.5"), ("Trusts and foundations", "14.9", "Health", "13.1"),
       ("Government contracts", "8.3", "Environment", "8.7"), ("Investment income", "4.6", "Communities", "6.8"),
       ("", "", "Running the foundation", "3.5")]
it = table(doc, [58, 24, 8, 54, 24], 2 + len(inc), cell_margin=(2.4, 0, 2.4, 0))
for i, h in enumerate(["Income", "", "", "Spending", ""]):
    c = it.rows[0].cells[i]
    if h:
        cell_style(c, borders={"bottom": (1.5, INK)})
        cell_p(c, h.upper(), 7.5, SOFT, F, bold=True, track=10, lead=1.3)
    elif i in (1, 4):
        cell_style(c, borders={"bottom": (1.5, INK)})
for r_i, (a1, a2, b1, b2) in enumerate(inc, 1):
    for i, v in zip((0, 1, 3, 4), (a1, a2, b1, b2)):
        c = it.rows[r_i].cells[i]
        if v or i in (0, 1):
            cell_style(c, borders={"bottom": (0.5, RULE)})
        cell_p(c, v, 9.5, INK, F, lead=1.3, align="right" if i in (1, 4) else "left")
for i, v in zip((0, 1, 3, 4), ("Total income", "49.2", "Total spending", "48.6")):
    c = it.rows[-1].cells[i]
    cell_style(c, borders={"top": (1.5, S["fin"]["fill"])})
    cell_p(c, v, 9.5, S["fin"]["deep"], F, bold=True, lead=1.3, align="right" if i in (1, 4) else "left")

# ============================================================================= p14 back cover
page(folio=False, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=INK, behind=True, z=1)])
a = P(doc, "")
run = a.add_run()
w = (168 - 4 * 1.2) / 5
for i, (key, pct) in enumerate(zip(ORDER, [34, 27, 18, 14, 7])):
    shape(run, 21 + i * (w + 1.2), 150, w, 6, fill=S[key]["fill"], z=5)
text_box(run, 21, 100, 168, 40, [T("Connected problems\nneed connected answers.", 24, WHITE, FXB, lead=1.2)])
text_box(run, 21, 166, 168, 30, [T("Lumen Foundation · 12 Mill Lane, Harbourline · lumen-foundation.example", 9,
                                   mix(INK, 0.6), F, lead=1.5)])
text_box(run, 21, 278, 168, 8, [T("ILLUSTRATIVE SAMPLE · ALL NAMES AND FIGURES ARE INVENTED", 6.5, mix(INK, 0.45), FSB, track=30)])

print("wrote", kit.save("spectrum-impact-test.docx"))
