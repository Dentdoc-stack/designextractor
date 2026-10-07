#!/usr/bin/env python3
"""Test report in design A "Navy Annual" (DESIGN.md section 4.A), built with python-docx.

usage: build.py OUTDIR      -> OUTDIR/navy-annual-test.docx (+ chart/icon PNGs)
Render:  soffice --headless --convert-to pdf --outdir OUTDIR OUTDIR/navy-annual-test.docx

All names and figures are invented (illustrative sample). Fonts: Figtree from ../../assets/fonts.
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
import docxkit as kit  # noqa: E402
from docxkit import (P, T, cell_p, cell_style, hexc, inline_pic, page, picture, r_xml,  # noqa: E402
                     row_no_split, shape, table, text_box)

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")

# ----------------------------------------------------------------------------- tokens (DESIGN.md 4.A)
NAVY, ROYAL, DISC, INK, SOFT = "1A2E5F", "2B4693", "142468", "1B1D2E", "5A5F6E"
ON_NAVY, HILITE, DIVIDER, ZEBRA, WHITE = "8FA0C8", "64A5C7", "D5D8E0", "E8EDF7", "FFFFFF"
CONNECT = "A7AEBD"
F, FSB, FXB = "Figtree", "Figtree SemiBold", "Figtree ExtraBold"
SHORT = "HARBOURLINE WATER · ANNUAL REPORT 2025 · ILLUSTRATIVE SAMPLE"

doc = kit.configure(OUT, font=F, ink=INK, soft=SOFT, footer=SHORT, icons=HERE / "icons")


def icon(name, fill=DISC, size_mm=14):
    return kit.icon(name, fill, size_mm)


def column_chart(path, cats, vals, w_mm, h_mm, fmt="{:,.0f}"):
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4), dpi=300)
    ax = fig.add_axes([0.02, 0.12, 0.96, 0.8])
    top_c, bot_c = ["#7A94C0", "#172F66"], ["#2C4C95", "#1D3460"]
    vmax = max(vals) * 1.16
    bw = 0.55
    for i, v in enumerate(vals):
        cols = bot_c if i == len(vals) - 1 else top_c
        cmap = LinearSegmentedColormap.from_list("g", [cols[1], cols[0]])
        grad = [[j] for j in range(256)]
        ax.imshow(grad, extent=[i - bw / 2, i + bw / 2, 0, v], aspect="auto", cmap=cmap, origin="lower", zorder=2)
        ax.text(i, v + vmax * 0.02, fmt.format(v), ha="center", va="bottom", fontsize=8, color=hexc(INK),
                fontweight="bold" if i == len(vals) - 1 else "normal")
    ax.set_xlim(-0.6, len(vals) - 0.4)
    ax.set_ylim(0, vmax)
    ax.set_xticks(range(len(vals)), cats, fontsize=8, color=hexc(SOFT))
    ax.set_yticks([])
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#B9BFCB")
    ax.spines["bottom"].set_linewidth(0.5)
    ax.tick_params(length=0, pad=4)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def hbar(path, cats, vals, avg, w_mm, h_mm, highlight=0):
    fig = plt.figure(figsize=(w_mm / 25.4, h_mm / 25.4), dpi=300)
    ax = fig.add_axes([0.16, 0.05, 0.78, 0.9])
    ramp = ["#8A9DB9", "#5B77A8", "#2B4693"]
    cols = [hexc(NAVY) if i == highlight else ramp[min(i, 2)] for i in range(len(vals))]
    y = list(range(len(vals)))[::-1]
    ax.barh(y, vals, color=cols, height=0.56)
    for yi, v in zip(y, vals):
        ax.text(v + 1.2, yi, f"{v}", va="center", fontsize=8, color=hexc(INK))
    ax.axvline(avg, color=hexc(ROYAL), lw=0.8, ls=(0, (3, 2)))
    ax.text(avg + 0.8, len(vals) - 0.45, f"company {avg}", fontsize=7, color=hexc(ROYAL))
    ax.set_yticks(y, cats, fontsize=8, color=hexc(INK))
    ax.set_xticks([])
    ax.set_xlim(0, max(vals) * 1.15)
    for s in ("top", "right", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#B9BFCB")
    ax.spines["left"].set_linewidth(0.5)
    ax.tick_params(length=0, pad=6)
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def dot_png(col, mm=3):
    px = round(mm / 25.4 * 300) * 4
    im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    ImageDraw.Draw(im).ellipse([0, 0, px - 1, px - 1], fill="#" + col)
    out = OUT / f"dot-{col}.png"
    im.resize((px // 4, px // 4), Image.LANCZOS).save(out)
    return out


def donut(path, shares, d_mm=70):
    fig = plt.figure(figsize=(d_mm / 25.4, d_mm / 25.4), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.pie(shares, colors=["#12265A", "#2B4693", "#5B77A8", "#8A9DB9"], startangle=90, counterclock=False,
           wedgeprops=dict(width=0.48, edgecolor="white", linewidth=1.2))
    ax.set_aspect("equal")
    fig.savefig(path, dpi=300, transparent=True)
    plt.close(fig)


def cover_art(path, w=210, h=297, dots=False):
    px = lambda mm: int(mm / 25.4 * 300)
    im = Image.new("RGBA", (px(w), px(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if not dots:
        d.ellipse([px(-75), px(0), px(225), px(300)], fill=(36, 58, 112, 70))          # faint large circle
        for i in range(5):                                                              # hairline diagonals
            o = px(110 + i * 9)
            d.line([(o, 0), (o + px(110), px(110))], fill=(43, 70, 147, 150), width=3)
        d.polygon([(px(140), px(297)), (px(210), px(205)), (px(210), px(297))], fill=(23, 40, 96, 140))
    else:
        for gx in range(int((w - 4) / 2.5)):          # halftone patch, fading out towards the top
            for gy in range(int((h - 4) / 2.5)):
                x, y = px(4 + gx * 2.5), px(4 + gy * 2.5)
                a = int(120 * (gy / ((h - 4) / 2.5)) ** 1.5 * (1 - gx / ((w - 4) / 2.5)) ** 0.7)
                if a > 4:
                    d.ellipse([x, y, x + px(0.6), y + px(0.6)], fill=(255, 255, 255, a))
    im.save(path)


# ----------------------------------------------------------------------------- content (invented)
KPIS = [("droplets", "312 M", "litres of drinking water supplied per day"),
        ("users", "1.4 M", "customers served across 38 towns"),
        ("gauge", "99.96%", "of samples met drinking-water standards"),
        ("leaf", "−11%", "operational carbon emissions vs 2024")]

column_chart(OUT / "chart-revenue.png", ["2021", "2022", "2023", "2024", "2025"], [412, 438, 471, 509, 548], 108, 98)
donut(OUT / "donut.png", [56, 24, 12, 8])
hbar(OUT / "hbar-leakage.png", ["North", "Coast", "Central", "Valley"], [97, 92, 74, 71], 84, 168, 46)
cover_art(OUT / "cover-art.png")
cover_art(OUT / "dots.png", 94, 97, dots=True)

# ============================================================================= p1 cover
page(folio=False, top=20, left=20, right=20, header_shapes=[
    lambda r: shape(r, 0, 0, 210, 297, fill=NAVY, behind=True, z=1),
    lambda r: picture(r, OUT / "cover-art.png", 0, 0, 210, 297, behind=True, z=2)])
a = P(doc, "")
run = a.add_run()
text_box(run, 20, 26, 150, 10, [T("ILLUSTRATIVE SAMPLE · ALL NAMES AND FIGURES ARE INVENTED", 7.5, ON_NAVY, FSB, track=30)])
text_box(run, 20, 66, 175, 70, [T("ANNUAL\nREPORT", 76, WHITE, FXB, lead=0.98)])
text_box(run, 20, 136, 150, 42, [T("2025", 100, HILITE, FXB, lead=1.0)])
text_box(run, 20, 178, 110, 24, [T("Reliable water for a growing region", 18, WHITE, F, lead=1.4)])
text_box(run, 20, 242, 120, 22, [T("Harbourline Water\nPublished April 2026\nFor customers, regulators and the public", 10.5, ON_NAVY, F, lead=1.9)])

# ============================================================================= p2 contents (full navy)
page(folio=False, top=30, left=22, right=20, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=NAVY, behind=True, z=1)])
P(doc, "CONTENTS", 40, WHITE, FXB, lead=1.0, after=40)
toc = [("Foreword from the chair", "03", True), ("2025 at a glance", "04", True),
       ("01  Service and finance", "05", True), ("How we performed", "06", False), ("Revenue and investment", "07", False),
       ("Where the money goes", "08", False), ("Key figures by service area", "09", False), ("Customers and complaints", "10", False),
       ("02  Organisation and outlook", "11", True), ("How we are organised", "12", False), ("Risk and governance", "13", False),
       ("Priorities for 2026", "14", False), ("Method and glossary", "15", True)]
tt = table(doc, [118, 18], len(toc))
for row, (title, num, main) in zip(tt.rows, toc):
    row_no_split(row)
    cell_p(row.cells[0], title, 12 if main else 10.5, WHITE, FSB if main else F, lead=1.3,
           before=9 if main else 3, after=3 if main else 2, left_indent=0 if main else 6)
    cell_p(row.cells[1], num, 12 if main else 10.5, ON_NAVY, FSB if main else F, lead=1.3,
           before=9 if main else 3, after=3 if main else 2)

# ============================================================================= p3 foreword (110 mm panel)
page(left=122, right=20, top=34, header_shapes=[lambda r: shape(r, 0, 0, 110, 297, fill=NAVY, behind=True, z=1)])
a = P(doc, "")
letter = ("Twelve months ago we promised to cut leakage, keep bills affordable and prepare the network for the "
          "next twenty years of growth. This report shows how far we have come.\n\n"
          "Leakage fell for the third year running, and our teams repaired more mains in a single year than ever "
          "before. Water quality stayed at the level our customers expect, and complaints dropped by a fifth.\n\n"
          "None of this happened by accident. It came from a steady programme of investment, better data from "
          "the network and, above all, the people who work in it every day.\n\n"
          "The year ahead asks more of us. Demand is rising, summers are drier and our oldest assets are reaching "
          "the end of their life. Our plan for 2026 sets out how we will respond, and how you can hold us to it.")
text_box(a.add_run(), 14, 30, 86, 250, [
    T("FOREWORD", 7.5, ON_NAVY, FSB, track=30, after=8),
    T("A YEAR OF\nSTEADY\nDELIVERY", 30, WHITE, FXB, lead=1.05, after=16),
    *[T(par, 10, WHITE, F, lead=1.5, after=8) for par in letter.split("\n\n")],
    T("Miriam Okafor\nChair of the Board", 9, ON_NAVY, FSB, lead=1.5, before=10)])
P(doc, "“", 72, NAVY, FXB, lead=0.9, after=0)
P(doc, "Every litre we stop losing is a litre we do not have to take from a river.", 16, NAVY, F, lead=1.4, after=14)
P(doc, "MIRIAM OKAFOR, CHAIR", 7.5, SOFT, FSB, track=30, after=40)
mono = table(doc, [68], 1)
c = mono.rows[0].cells[0]
cell_p(c, "KEY NUMBER", 7.5, SOFT, FSB, track=30, after=4)
cell_p(c, "18%", 44, NAVY, FXB, lead=1.0, after=4)
cell_p(c, "less water lost to leaks than in 2022, our baseline year.", 9.5, INK, F, lead=1.45)
cell_style(c, borders={"top": (1, NAVY)})

# ============================================================================= p4 at a glance
page(top=26)
a = P(doc, "2025 AT A GLANCE", 36, INK, FXB, lead=1.1, after=10)
P(doc, "Water quality held at record levels while leakage, complaints and carbon all fell. Investment rose for the "
       "fourth year, funded without a real-terms rise in bills.", 11, INK, F, lead=1.45, right_indent=48, after=26)
k = table(doc, [42, 42, 42, 42], 1, cell_margin=(3, 0, 3, 0))
for i, (cell, (ic, num, cap)) in enumerate(zip(k.rows[0].cells, KPIS)):
    cell_style(cell, borders={"left": (0.5, DIVIDER) if i else None})
    inline_pic(cell, icon(ic), 14, after=4)
    cell_p(cell, num, 26, INK, FXB, lead=1.15, align="center", after=3)
    cell_p(cell, cap, 8.5, SOFT, F, lead=1.3, align="center")
P(doc, "", 6, after=16)
findings = [("Leakage is down 18% since 2022", "Active pressure management in 61 zones and faster repairs cut losses to 84 litres per property per day."),
            ("Bills stayed flat in real terms", "The average household bill was 412 a year, 0.4% below inflation, while the social tariff reached 31,000 homes."),
            ("Complaints fell by a fifth", "Written complaints dropped to 2,960. Most of the fall came from billing, after the new account system went live."),
            ("Investment reached a new high", "We invested 214 million in mains, treatment and storage, 9% more than in 2024 and ahead of plan.")]
g = table(doc, [82, 4, 82], 2)
for idx, (h, b) in enumerate(findings):
    cell = g.rows[idx // 2].cells[(idx % 2) * 2]
    cell_p(cell, h, 12, NAVY, F, bold=True, lead=1.3, after=3, before=6)
    cell_p(cell, b, 9.5, INK, F, lead=1.47, after=10)
text_box(a.add_run(), 0, 250, 210, 47, [T("The network is in better shape than at any point in the last decade, and it now needs "
                                          "to be ready for a hotter, busier region.", 14, WHITE, FSB, lead=1.4)],
         fill=NAVY, anchor="ctr", inset=(22, 0, 30, 0), z=5)

# ============================================================================= p5 opener 01
def opener(num, title, lede, items, hero, hero_cap):
    page(left=82, right=20, top=40, folio=False, header_shapes=[lambda r: shape(r, 0, 0, 70, 297, fill=NAVY, behind=True, z=1)])
    a = P(doc, "IN THIS SECTION", 7.5, SOFT, FSB, track=30, after=14)
    text_box(a.add_run(), 14, 40, 50, 230, [
        T(num, 60, HILITE, FXB, lead=1.0, after=18),
        T(title, 24, WHITE, FXB, lead=1.1, after=18),
        T(lede, 10, WHITE, F, lead=1.5)])
    for h, d, pg in items:
        P(doc, h, 13, NAVY, F, bold=True, lead=1.3, keep=True, runs=[r_xml(h, F, 13, NAVY, True), r_xml("   " + pg, FSB, 9, SOFT)])
        P(doc, d, 9, SOFT, F, lead=1.45, after=14, right_indent=10)
    P(doc, "", 10, before=40)
    P(doc, hero, 40, NAVY, FXB, lead=1.0, after=4)
    P(doc, hero_cap, 9, SOFT, F, lead=1.45, right_indent=30)


opener("01", "SERVICE\nAND\nFINANCE",
       "How the network performed, what it cost to run and where the money went in 2025.",
       [("How we performed", "Quality, leakage, supply interruptions and the work behind them.", "06"),
        ("Revenue and investment", "Five years of income and capital spending.", "07"),
        ("Where the money goes", "How each pound of a customer bill is spent.", "08"),
        ("Key figures by service area", "The year's numbers for each of our four regions.", "09"),
        ("Customers and complaints", "What customers told us, and what we changed.", "10")],
       "214 M", "invested in pipes, treatment works and storage in 2025, the highest in our history.")

# ============================================================================= p6 narrative with side rail
page(top=26)
P(doc, "HOW WE PERFORMED", 26, INK, FXB, lead=1.1, after=16)
rail_rows = [
    ("Quality", "99.96%", "of 48,200 samples met the drinking-water standard.",
     ["Water quality is the measure our customers care about most, and it held at the level of the last three years. "
      "Of 48,200 samples taken at treatment works, reservoirs and customer taps, 19 failed a standard, none of them "
      "for a substance that affects health.",
      "Each failure was traced and closed within 48 hours. Twelve were linked to old iron mains in two towns, which "
      "are now first in line for replacement in the 2026 programme."]),
    ("Leakage", "84 l", "lost per property per day, down from 102 in 2022.",
     ["Leakage fell for the third year in a row. Pressure management now covers 61 of our 74 supply zones, which "
      "reduces the stress on old pipes at night when demand is low.",
      "Repair crews fixed 9,840 leaks, 14% more than in 2024, and the average time from report to repair dropped "
      "from 4.1 to 2.9 days. Acoustic loggers on 1,100 km of main now find leaks before they reach the surface."]),
    ("Supply", "6 min", "average interruption per property, against a target of 8.",
     ["Planned and unplanned interruptions together averaged six minutes per property. Two large bursts in February "
      "accounted for a third of the total; both areas were back in supply within five hours.",
      "We now carry bottled water stocks for 40,000 people at three depots, and every vulnerable customer on our "
      "register is contacted within two hours of an outage."]),
    ("Carbon", "−11%", "operational emissions against 2024, to 61,400 tonnes.",
     ["Pumping and treatment use most of our energy. New high-efficiency pumps at nine stations and solar arrays at "
      "four treatment works cut electricity use by 7%, and 38% of the power we use is now generated on our own sites.",
      "Process emissions from sludge treatment fell after the anaerobic digester at Eastbrook returned to full "
      "operation in May. Our target is net zero operational emissions by 2035."])]
rt = table(doc, [46, 8, 114], len(rail_rows))
for row, (h, fig, cap, paras) in zip(rt.rows, rail_rows):
    row_no_split(row)
    rc, bc = row.cells[0], row.cells[2]
    cell_p(rc, h, 13, NAVY, F, bold=True, lead=1.3, after=6, before=4)
    cell_p(rc, fig, 24, NAVY, FXB, lead=1.1, after=2)
    cell_p(rc, cap, 8.5, SOFT, F, lead=1.4, after=12)
    for i, par in enumerate(paras):
        cell_p(bc, par, 10, INK, F, lead=1.5, before=4 if i == 0 else 0, after=8)
    cell_style(rc, borders={"top": (0.5, DIVIDER)})
    cell_style(bc, borders={"top": (0.5, DIVIDER)})

# ============================================================================= p7 chart page (split)
page(left=82, right=20, top=30, header_shapes=[lambda r: shape(r, 0, 0, 70, 297, fill=NAVY, behind=True, z=1)])
a = P(doc, "")
text_box(a.add_run(), 14, 30, 50, 240, [
    T("REVENUE AND\nINVESTMENT", 22, WHITE, FXB, lead=1.12, after=16),
    T("Income grew in line with the customer base and the price limits set by the regulator. "
      "Capital investment rose faster, funded by efficiency savings and long-term green bonds.", 10, WHITE, F, lead=1.5)])
sk = table(doc, [12, 42, 12, 42], 2)
stacked = [("banknote", "Revenue", "548 M"), ("building-2", "Capital investment", "214 M"),
           ("wrench", "Operating costs", "291 M"), ("trending-up", "Efficiency savings", "19 M")]
for idx, (ic, lab, num) in enumerate(stacked):
    row = sk.rows[idx // 2]
    ic_cell, tx_cell = row.cells[(idx % 2) * 2], row.cells[(idx % 2) * 2 + 1]
    inline_pic(ic_cell, icon(ic, size_mm=8), 8, align="left", before=2)
    cell_p(tx_cell, lab, 8.5, SOFT, F, lead=1.3, before=0)
    cell_p(tx_cell, num, 22, INK, FXB, lead=1.15, after=16)
P(doc, "FIGURE 1 — REVENUE, 2021–2025 (MILLIONS)", 7.5, SOFT, FSB, track=30, before=12, after=4)
inline_pic(doc, OUT / "chart-revenue.png", 108, align="left")
P(doc, "Source: Harbourline Water audited accounts (illustrative). 2025 is the deepest bar.", 7.5, SOFT, F, lead=1.4, before=4)

# ============================================================================= p8 donut + stat rail
page(top=26)
a = P(doc, "WHERE THE\nMONEY GOES", 30, INK, FXB, lead=1.1, after=10)
P(doc, "How each pound of an average household bill was spent in 2025.", 11, INK, F, lead=1.45, after=18)
dt = table(doc, [76, 12, 80], 1)
inline_pic(dt.rows[0].cells[0], OUT / "donut.png", 70, align="left")
legend = [("12265A", "56%", "Running the network: treatment, pumping, repairs"), ("2B4693", "24%", "Paying for investment in pipes and works"),
          ("5B77A8", "12%", "Customer service and billing"), ("8A9DB9", "8%", "Environmental schemes and catchment work")]
lg = table(dt.rows[0].cells[2], [8, 72], 4)
for row, (col, pct, lab) in zip(lg.rows, legend):
    cell_style(row.cells[0], valign="center")
    inline_pic(row.cells[0], dot_png(col), 3, align="left", before=9)
    cell_p(row.cells[1], pct, 16, INK, FXB, lead=1.15, before=5)
    cell_p(row.cells[1], lab, 8.5, SOFT, F, lead=1.35, after=6)
P(doc, "", 8, before=12)
rail = table(doc, [100, 10, 58], 1)
cell_p(rail.rows[0].cells[0], "Why the running share is falling", 13, NAVY, F, bold=True, lead=1.3, after=6)
cell_p(rail.rows[0].cells[0], "Five years ago, running the network took 63 pence of every pound. Lower energy use at "
       "the two largest treatment works and fewer emergency repairs have brought that down to 56 pence, freeing money "
       "for investment without raising bills.", 10, INK, F, lead=1.5, after=8)
cell_p(rail.rows[0].cells[0], "The shift matters because investment today avoids larger repair bills later. Every "
       "kilometre of main we replace now removes, on average, four bursts over the next decade.", 10, INK, F, lead=1.5)
sr = rail.rows[0].cells[2]
for fig, cap in [("63p", "running share in 2020"), ("56p", "running share in 2025"), ("4", "bursts avoided per km replaced")]:
    cell_p(sr, fig, 24, NAVY, FXB, lead=1.1, before=4, left_indent=10)
    cell_p(sr, cap, 8.5, SOFT, F, lead=1.35, after=14, left_indent=10)
cell_style(sr, borders={"left": (4.5, NAVY)})

# ============================================================================= p9 table
page(top=26)
P(doc, "KEY FIGURES BY\nSERVICE AREA", 30, INK, FXB, lead=1.1, after=10)
P(doc, "Our four regions in 2025. North and Coast carry most of the older iron mains, which is where leakage and "
       "interruptions remain highest.", 11, INK, F, lead=1.45, right_indent=40, after=18)
P(doc, "TABLE 1 — PERFORMANCE BY REGION, 2025", 7.5, SOFT, FSB, track=30, after=5)
hdr = ["Region", "Customers", "Supply (Ml/d)", "Leakage (l/prop/d)", "Interruptions (min)", "Complaints"]
data = [("North", "382,000", "84.1", "97", "8.2", "1,040"), ("Coast", "296,000", "66.4", "92", "7.1", "760"),
        ("Central", "448,000", "98.7", "74", "4.6", "690"), ("Valley", "274,000", "62.8", "71", "4.9", "470")]
widths = [38, 26, 26, 28, 28, 22]
tb = table(doc, widths, 1 + len(data) + 1, cell_margin=(2.5, 3, 2.5, 3))
for i, h in enumerate(hdr):
    c = tb.rows[0].cells[i]
    cell_style(c, fill=NAVY, valign="bottom")
    cell_p(c, h.upper(), 7.5, WHITE, F, bold=True, lead=1.25, track=8, align="left" if i == 0 else "right")
row_no_split(tb.rows[0], header=True)
for r_i, rowv in enumerate(data, 1):
    row = tb.rows[r_i]
    row_no_split(row)
    for i, v in enumerate(rowv):
        c = row.cells[i]
        cell_style(c, fill=ZEBRA if r_i % 2 == 0 else None, borders={"bottom": (0.5, DIVIDER)})
        cell_p(c, v, 9, INK, FSB if i == 0 else F, lead=1.3, align="left" if i == 0 else "right")
tot = ("All regions", "1,400,000", "312.0", "84", "6.0", "2,960")
for i, v in enumerate(tot):
    c = tb.rows[-1].cells[i]
    cell_style(c, borders={"top": (1, NAVY), "bottom": (1, NAVY)})
    cell_p(c, v, 9, ROYAL, F, bold=True, lead=1.3, align="left" if i == 0 else "right")
P(doc, "Ml/d = million litres per day. Leakage per property per day, three-year average. Figures are illustrative.",
  7.5, SOFT, F, lead=1.4, before=6, after=24)
nt = table(doc, [82, 4, 82], 1)
cell_p(nt.rows[0].cells[0], "Reading the table", 12, NAVY, F, bold=True, lead=1.3, after=4)
cell_p(nt.rows[0].cells[0], "Central and Valley sit below the company leakage figure because most of their mains were "
       "replaced in the 1990s. North is 13 litres above average, and two of its largest towns are in the 2026 "
       "replacement programme.", 9.5, INK, F, lead=1.47)
cell_p(nt.rows[0].cells[2], "What changes next year", 12, NAVY, F, bold=True, lead=1.3, after=4)
cell_p(nt.rows[0].cells[2], "From 2026 we will report each region against its own target, set from the age and "
       "material of its pipes, rather than one company-wide figure that hides the gap between them.", 9.5, INK, F, lead=1.47)
P(doc, "FIGURE 2 — LEAKAGE BY REGION, LITRES PER PROPERTY PER DAY", 7.5, SOFT, FSB, track=30, before=22, after=6)
inline_pic(doc, OUT / "hbar-leakage.png", 168, align="left")
P(doc, "Source: Harbourline Water leakage returns (illustrative). The dashed line is the company figure.", 7.5, SOFT, F, lead=1.4, before=4)

# ============================================================================= p10 customers (narrative + quote)
page(top=26)
P(doc, "CUSTOMERS AND\nCOMPLAINTS", 30, INK, FXB, lead=1.1, after=16)
cq = table(doc, [104, 10, 54], 1)
body = ["Written complaints fell to 2,960, a fifth fewer than in 2024. Billing complaints fell fastest, by 38%, "
        "after the new account system went live in March and customers could see their usage online for the first time.",
        "Complaints about water pressure rose slightly, mostly in the north, where pressure management lowered night-time "
        "pressure in older streets. We reviewed every one of the 410 cases and raised pressure again in 37 roads where "
        "upstairs taps were affected.",
        "We now answer 92% of calls within a minute and resolve 81% of contacts first time. Customers on our priority "
        "services register, now 52,000 households, get a named contact and a call before any planned work.",
        "Satisfaction in our independent survey rose from 7.6 to 8.1 out of 10. The largest gain was on trust: 74% of "
        "customers said they believe we will do what we say, up from 66%."]
for i, par in enumerate(body):
    cell_p(cq.rows[0].cells[0], par, 10, INK, F, lead=1.5, after=9)
qc = cq.rows[0].cells[2]
cell_p(qc, "“", 48, NAVY, FXB, lead=0.9, before=6)
cell_p(qc, "The engineer phoned before the work started and again when it was done. That is all I wanted.", 14, NAVY, F, lead=1.45, after=8)
cell_p(qc, "CUSTOMER, VALLEY REGION", 7.5, SOFT, FSB, track=30, after=30)
cell_p(qc, "8.1", 30, NAVY, FXB, lead=1.1)
cell_p(qc, "out of 10 overall satisfaction, up from 7.6.", 8.5, SOFT, F, lead=1.4)
cell_style(qc, borders={"top": (1, NAVY)})
P(doc, "SERVICE IN NUMBERS", 7.5, SOFT, FSB, track=30, before=18, after=8)
ks = table(doc, [42, 42, 42, 42], 1, cell_margin=(4, 2, 4, 0))
for i, (cell, (num, cap)) in enumerate(zip(ks.rows[0].cells, [("92%", "of calls answered within a minute"),
        ("81%", "of contacts resolved first time"), ("52,000", "households on the priority services register"),
        ("−38%", "billing complaints after the new account system")])):
    cell_style(cell, borders={"left": (0.5, DIVIDER) if i else None, "top": (1, INK)})
    cell_p(cell, num, 24, NAVY, FXB, lead=1.15, before=6, after=3)
    cell_p(cell, cap, 8.5, SOFT, F, lead=1.35)

# ============================================================================= p11 opener 02
opener("02", "ORGANI-\nSATION\nAND\nOUTLOOK",
       "Who runs the company, how risk is managed, and what we will deliver in 2026.",
       [("How we are organised", "The board, the executive team and the four directorates.", "12"),
        ("Risk and governance", "The risks that matter most and how the board oversees them.", "13"),
        ("Priorities for 2026", "Four commitments and how we will measure them.", "14")],
       "4", "commitments for 2026, each with a published target and a quarterly progress report.")

# ============================================================================= p12 org chart
page(top=26)
a = P(doc, "HOW WE ARE\nORGANISED", 30, INK, FXB, lead=1.1, after=10)
P(doc, "The board sets strategy and holds the executive to account. Four directorates run the business day to day.",
  11, INK, F, lead=1.45, right_indent=48)
run = a.add_run()
text_box(run, 75, 92, 60, 16, [T("CHIEF EXECUTIVE\nOFFICER", 9, WHITE, F, bold=True, lead=1.25, align="center", track=10)],
         fill=NAVY, anchor="ctr")
shape(run, 104.87, 108, 0.26, 6, fill=CONNECT)
children = ["OPERATIONS", "ASSETS", "CUSTOMERS", "FINANCE"]
xs = [22 + i * (38 + 5.33) for i in range(4)]
shape(run, xs[0] + 19, 114, xs[3] - xs[0], 0.26, fill=CONNECT)
for x, name in zip(xs, children):
    shape(run, x + 18.87, 114, 0.26, 6, fill=CONNECT)
    text_box(run, x, 120, 38, 11, [T(name, 8, WHITE, F, bold=True, lead=1.2, align="center", track=10)], fill=NAVY, anchor="ctr")
remits = [["Treatment works", "Network and repairs", "Incident response", "Laboratories"],
          ["Capital programme", "Mains replacement", "Asset data", "Engineering"],
          ["Billing", "Contact centre", "Priority services", "Developer services"],
          ["Planning and treasury", "Regulation", "Procurement", "Risk and audit"]]
for i, (x, items) in enumerate(zip(xs, remits)):
    text_box(run, x, 137, 38, 50, [T("·  " + it, 9, INK, F, lead=1.55) for it in items])
    if i:
        shape(run, x - 2.8, 137, 0.18, 45, fill=DIVIDER)
text_box(run, 22, 200, 168, 60, [
    T("THE BOARD", 7.5, SOFT, FSB, track=30, after=6),
    T("Nine directors: the chair, five independent non-executives and three executives. Four committees report to the "
      "board: audit, risk, remuneration and a customer and environment committee chaired by an independent director.",
      10, INK, F, lead=1.5, after=8),
    T("In 2025 the board met nine times, with full attendance at seven meetings. Two new independent directors joined "
      "in June, bringing experience in climate adaptation and in consumer protection.", 10, INK, F, lead=1.5)])

# ============================================================================= p13 risk and governance (two columns)
page(top=26)
P(doc, "RISK AND GOVERNANCE", 26, INK, FXB, lead=1.1, after=16)
risks = [("Drought and demand", "Two dry summers in three years have lowered reservoir levels at the start of autumn. "
          "We have brought forward a new transfer main between Central and North, and our drought plan now triggers "
          "earlier, more gradual restrictions."),
         ("Ageing assets", "A quarter of our mains are more than 80 years old. The replacement rate rose to 0.9% a year "
          "in 2025 and will reach 1.2% by 2028, prioritised by burst history and material."),
         ("Cyber security", "Treatment works are run by control systems that must stay safe from attack. We completed an "
          "independent review in 2025 and separated the operational network from the office network at all sites."),
         ("Affordability", "Rising costs put pressure on bills. The social tariff now supports 31,000 homes, and we "
          "fund debt advice through two local charities."),
         ("People and skills", "Thirty percent of our engineers can retire within ten years. We doubled apprentice "
          "intake to 48 and launched a graduate scheme with the regional university.")]
rk = table(doc, [82, 4, 82], 1)
for i, (h, b) in enumerate(risks):
    c = rk.rows[0].cells[0 if i < 3 else 2]
    cell_p(c, h, 12, NAVY, F, bold=True, lead=1.3, before=0 if i in (0, 3) else 10, after=4)
    cell_p(c, b, 9.5, INK, F, lead=1.5, after=4)
cr = rk.rows[0].cells[2]
cell_p(cr, "How the board oversees risk", 12, NAVY, F, bold=True, lead=1.3, before=10, after=4)
cell_p(cr, "The risk committee reviews the full register every quarter and one principal risk in depth at each meeting. "
       "Internal audit reports directly to the audit committee chair.", 9.5, INK, F, lead=1.5)
P(doc, "TABLE 2 — PRINCIPAL RISKS AT A GLANCE", 7.5, SOFT, FSB, track=30, before=22, after=5)
rows = [("Drought and demand", "Rising", "Director of Operations", "High"), ("Ageing assets", "Stable", "Director of Assets", "High"),
        ("Cyber security", "Rising", "Chief Information Officer", "Medium"), ("Affordability", "Rising", "Director of Customers", "Medium"),
        ("People and skills", "Stable", "Chief People Officer", "Medium")]
rt2 = table(doc, [58, 30, 52, 28], 1 + len(rows), cell_margin=(2.5, 2.4, 2.5, 2.4))
for i, h in enumerate(["Risk", "Trend", "Owner", "Rating"]):
    c = rt2.rows[0].cells[i]
    cell_style(c, fill=NAVY)
    cell_p(c, h.upper(), 7.5, WHITE, F, bold=True, track=8, lead=1.25, align="right" if i == 3 else "left")
row_no_split(rt2.rows[0], header=True)
for r_i, rv in enumerate(rows, 1):
    for i, v in enumerate(rv):
        c = rt2.rows[r_i].cells[i]
        cell_style(c, fill=ZEBRA if r_i % 2 == 0 else None, borders={"bottom": (0.5, DIVIDER)})
        cell_p(c, v, 9, ROYAL if (i == 3 and v == "High") else INK, FSB if i == 0 else F, bold=(i == 3 and v == "High"),
               lead=1.3, align="right" if i == 3 else "left")

# ============================================================================= p14 priorities (navy band + steps)
page(top=170, header_shapes=[lambda r: shape(r, 0, 0, 210, 152, fill=NAVY, behind=True, z=1)])
a = P(doc, "HOW WE WILL TRACK PROGRESS", 7.5, SOFT, FSB, track=30, after=8)
run = a.add_run()
text_box(run, 22, 28, 168, 30, [T("PRIORITIES FOR 2026", 30, WHITE, FXB, lead=1.1)])
text_box(run, 22, 50, 130, 30, [T("Four commitments, each with a target we will publish and report on every quarter.",
                                  11, WHITE, F, lead=1.5)])
steps = [("01", "Cut leakage to\n78 litres", "per property per day, by replacing 95 km of main."),
         ("02", "Keep bills flat\nin real terms", "with the social tariff extended to 36,000 homes."),
         ("03", "Finish the north\ntransfer main", "to move water between regions in a drought."),
         ("04", "Halve the time\nto fix leaks", "from 2.9 to 1.5 days, using network sensors.")]
for i, (n, lab, desc) in enumerate(steps):
    x = 22 + i * (38 + 5.33)
    text_box(run, x, 92, 38, 46, [T(lab, 11, INK, F, bold=True, lead=1.3, after=4), T(desc, 8.5, SOFT, F, lead=1.4)],
             fill=WHITE, inset=(4, 12, 4, 3))
    text_box(run, x - 3, 85, 13, 13, [T(n, 13, NAVY, F, bold=True, lead=1.0, align="center")], fill=WHITE,
             line=(1, NAVY), geom="ellipse", anchor="ctr", z=30)
targets = [("Leakage, litres per property per day", "84", "78"), ("Customers on the social tariff", "31,000", "36,000"),
           ("North transfer main complete", "40%", "100%"), ("Average days to repair a leak", "2.9", "1.5")]
tg = table(doc, [100, 34, 34], 1 + len(targets), cell_margin=(0, 2.2, 0, 2.2))
for i, h in enumerate(["Measure", "2025", "2026 target"]):
    c = tg.rows[0].cells[i]
    cell_style(c, borders={"bottom": (1, NAVY)})
    cell_p(c, h.upper(), 7.5, SOFT, F, bold=True, track=8, lead=1.25, align="left" if i == 0 else "right")
for r_i, rv in enumerate(targets, 1):
    for i, v in enumerate(rv):
        c = tg.rows[r_i].cells[i]
        cell_style(c, borders={"bottom": (0.5, DIVIDER)})
        cell_p(c, v, 9.5, ROYAL if i == 2 else INK, F, bold=(i == 2), lead=1.3, align="left" if i == 0 else "right")

# ============================================================================= p15 method and glossary
page(top=26)
P(doc, "METHOD AND\nGLOSSARY", 30, INK, FXB, lead=1.1, after=16)
gl = [("Leakage", "Water lost between treatment works and customers' property boundaries, as a three-year average "
       "per property per day."),
      ("Supply interruption", "Average minutes per property without supply for three hours or more, planned or unplanned."),
      ("Ml/d", "Million litres per day, the unit for water put into supply."),
      ("Social tariff", "A reduced bill for households whose water costs exceed 5% of their income after housing costs."),
      ("Priority services register", "Customers who need extra help during an incident, such as bottled water delivery."),
      ("Capital investment", "Spending on new or replacement assets, excluding routine maintenance."),
      ("Efficiency savings", "Reductions in operating cost against the 2020 baseline, after inflation."),
      ("About this report", "This is an illustrative sample built to test the Navy Annual design. Harbourline Water, its "
       "people and every figure are invented.")]
gt = table(doc, [82, 4, 82], 1)
for i, (h, b) in enumerate(gl):
    c = gt.rows[0].cells[0 if i < 4 else 2]
    cell_p(c, h, 10, NAVY, F, bold=True, lead=1.35, after=2, before=0 if i in (0, 4) else 8)
    cell_p(c, b, 9, INK, F, lead=1.5)
P(doc, "DATA SOURCES AND ASSURANCE", 7.5, SOFT, FSB, track=30, before=26, after=6)
src = table(doc, [168], 1)
cs = src.rows[0].cells[0]
cell_style(cs, borders={"top": (1, NAVY)})
for par in ["Performance figures come from the regulatory returns submitted in March 2026. Water quality results are "
            "taken from the laboratory information system and checked by the drinking-water inspectorate. Financial "
            "figures are from the audited accounts for the year to 31 December 2025.",
            "An independent technical auditor reviewed leakage, supply interruptions and customer contact data. Where "
            "a measure changed method during the year, the previous year is restated on the same basis."]:
    cell_p(cs, par, 9.5, INK, F, lead=1.5, before=6, after=2)

# ============================================================================= p16 back cover
page(folio=False, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=NAVY, behind=True, z=1),
                                 lambda r: picture(r, OUT / "dots.png", 0, 200, 94, 97, behind=True, z=2)])
a = P(doc, "")
run = a.add_run()
text_box(run, 22, 112, 150, 50, [T("Water you can trust,\ntoday and for the\nnext generation.", 18, WHITE, F, lead=1.6)])
shape(run, 22, 160, 28, 0.27, fill=WHITE)
text_box(run, 110, 236, 79, 30, [T("Harbourline Water\n1 Quay Street, Harbourline\nharbourline-water.example", 8, WHITE, F,
                                   lead=1.45, align="right")])
text_box(run, 22, 278, 120, 8, [T("ILLUSTRATIVE SAMPLE · ALL NAMES AND FIGURES ARE INVENTED", 6.5, ON_NAVY, FSB, track=30)])

out = OUT / "navy-annual-test.docx"
doc.save(out)
print("wrote", out)
