#!/usr/bin/env python3
"""KP Rainwater Harvesting Implementation Report 2026, rebuilt in design H "Spectrum" (DESIGN.md 4.H).

usage: build.py SOURCE.docx OUTDIR   -> OUTDIR/KP_Rainwater_Harvesting_Implementation_Report_2026_Spectrum.docx (+ .pdf)

Every word, figure and table value is read from SOURCE.docx (see source.py); nothing is retyped except the
labels inside the source's diagram images, which are redrawn here in the Spectrum palette from the report's
own figures. Technical cross-sections, exhibits (letters, screenshots) and district photographs are reused.
Two passes: the second fills the contents page with real page numbers from a LibreOffice render.
"""
import io
import math
import re
import subprocess
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pymupdf
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
sys.path.insert(0, str(HERE))
import docxkit as kit  # noqa: E402
from docx.oxml import parse_xml  # noqa: E402
from docx.oxml.ns import qn  # noqa: E402
from docxkit import (P, T, cell_p, cell_style, hexc, inline_pic, r_xml, row_no_split, shape, table,  # noqa: E402
                     text_box)
from source import blocks, text_of  # noqa: E402

SRC, OUT = Path(sys.argv[1]), Path(sys.argv[2] if len(sys.argv) > 2 else "out")
NAME = "KP_Rainwater_Harvesting_Implementation_Report_2026_Spectrum"

INK, SOFT, RULE, WHITE, PAPER2 = "16213E", "5A5F6E", "D9D9D9", "FFFFFF", "F2EFEA"
F, FSB, FXB = "Figtree", "Figtree SemiBold", "Figtree ExtraBold"
FOOT = "PMRU · OFFICE OF THE CHIEF SECRETARY · RAINWATER HARVESTING INITIATIVE · MONSOON 2026"


def mix(h, t):
    c = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join("%02X" % round(v + (255 - v) * t) for v in c)


S = {  # DESIGN.md 4.H tokens, one part per colour, fixed order
    1: dict(name="Why and how", fill="2559D6", panel="2559D6", deep="2150C2", tint="EBEFFA", on=WHITE, icon="droplets"),
    2: dict(name="From direction to delivery", fill="E04F39", panel="D83A22", deep="A62C1A", tint="FAEDEB", on=WHITE, icon="landmark"),
    3: dict(name="In the districts", fill="009682", panel="008473", deep="006557", tint="EBFAF8", on=WHITE, icon="map-pin"),
    4: dict(name="Results and next steps", fill="D4891A", panel="D4891A", deep="7B500F", tint="FAF4EB", on=INK, icon="trending-up"),
    5: dict(name="Evidence", fill="8A3FB0", panel="8A3FB0", deep="7E39A1", tint="F4ECF8", on=WHITE, icon="book-open"),
}
CUR = [1]                                   # current part, used by the text helpers
B = blocks(str(SRC))
IMG = OUT / "img"
plt.rcParams["font.family"] = ["Figtree", "DejaVu Sans"]       # DejaVu only for glyphs Figtree lacks (≈)


def blk(i, prefix=""):
    b = B[i]
    if prefix:
        t = text_of(b[2]) if b[0] == "p" else text_of(b[1][0][0][0][0]) if b[1][0][0][0] else ""
        assert t.strip().startswith(prefix), (i, prefix, t[:60])
    return b


def media(name):
    for b in B:
        imgs = b[3] if b[0] == "p" else [x for row in b[1] for c in row for x in c[1]]
        for n, blob in imgs:
            if n == name:
                path = IMG / name
                if not path.exists():
                    im = Image.open(io.BytesIO(blob))
                    if im.mode in ("RGBA", "LA", "P") and name.endswith(".png") and name not in ("image1.png", "image2.png"):
                        bg = Image.new("RGBA", im.size, "white")
                        bg.alpha_composite(im.convert("RGBA"))
                        im = bg.convert("RGB")
                    im.save(path)
                return path
    raise KeyError(name)


# ----------------------------------------------------------------------------- text helpers
def s_(k=None):
    return S[k or CUR[0]]


def rx(runs, size=10, color=INK, bold_color=None, font=F, drop=0, upper=False):
    """Source runs -> run XML. Bold/italic kept; footnote refs become superscript numbers in the part colour."""
    out, skip = [], drop
    for t, b, i, sup in runs:
        if sup:
            out.append(r_xml(t, F, size, s_()["deep"], bold=True, sup=True))
            continue
        if skip:
            cut = min(skip, len(t))
            t, skip = t[cut:], skip - cut
        if not t:
            continue
        t = t.upper() if upper else t
        out.append(r_xml(t, font, size, (bold_color or color) if b else color, bold=b, italic=i))
    return out


def para(runs, size=10, color=INK, lead=1.5, before=0, after=7, container=None, **kw):
    return P(container or kit.doc, runs=rx(runs, size, color, kw.pop("bold_color", None), drop=kw.pop("drop", 0)),
             size=size, lead=lead, before=before, after=after, **kw)


def cpara(cell, runs, size=10, color=INK, lead=1.5, before=0, after=4, **kw):
    return cell_p(cell, runs=rx(runs, size, color, kw.pop("bold_color", None), drop=kw.pop("drop", 0),
                                upper=kw.pop("upper", False)), size=size, lead=lead, before=before, after=after, **kw)


def kicker(text, color=None, container=None, after=5, before=0, size=7.5):
    return P(container or kit.doc, text.upper(), size, color or s_()["deep"], FSB, track=40, lead=1.3,
             after=after, before=before, keep=True)


def h1_split(i):
    t = text_of(blk(i)[2])
    m = re.match(r"^(\S+)\s{2,}(.*)$", t)
    return (m.group(1), m.group(2)) if m else ("", t)


def top_rule(p, color, sz=2.0, space=8):
    """Paragraph top border (pBdr goes before w:spacing in pPr)."""
    ppr = p._p.get_or_add_pPr()
    bdr = parse_xml(f'<w:pBdr {kit.NS}><w:top w:val="single" w:sz="{int(sz * 8)}" w:space="{space}" w:color="{color}"/></w:pBdr>')
    sp = ppr.find(qn("w:spacing"))
    (sp.addprevious if sp is not None else ppr.append)(bdr)


def section_head(i, lede_i=None):
    """Numbered section heading as chained paragraphs (keep-with-next), so it never strands at a page foot."""
    num_, title = h1_split(i)
    k = P(kit.doc, f"PART {CUR[0]} · {s_()['name']}".upper(), 7.5, s_()["deep"], FSB, track=40, lead=1.3,
          before=20, after=4, keep=True)
    top_rule(k, s_()["fill"])
    P(kit.doc, runs=[r_xml(num_ + "   ", FXB, 20, s_()["fill"]), r_xml(title, FXB, 20, INK)], size=20, lead=1.15,
      after=4, keep=True)
    if lede_i is not None:
        para(blk(lede_i)[2], 12, INK, lead=1.42, before=4, after=12, keep=True)


def h2(i):
    P(kit.doc, text_of(blk(i)[2]), 13, s_()["deep"], F, bold=True, lead=1.3, before=14, after=6, keep=True)


def body(i, **kw):
    return para(blk(i)[2], **kw)


def caption(i, after=12):
    """'Figure 4  text   Source: …' -> caps label in the part colour + text in grey."""
    runs = blk(i)[2]
    out = []
    for n, (t, b, it, sup) in enumerate(runs):
        if n == 0 and b:
            out.append(r_xml(t.strip().upper() + "   ", FSB, 7.5, s_()["deep"], track=30))
        elif not sup:
            out.append(r_xml(t, F, 8, SOFT, bold=b, italic=it))
    return P(kit.doc, runs=out, size=8, lead=1.4, before=4, after=after)


def callout(rows, container=None, width=168):
    """Source 1-column table -> tint card with a bar in the part colour."""
    t = table(container or kit.doc, [width], len(rows), cell_margin=(6, 5, 6, 5))
    for row, src in zip(t.rows, rows):
        c = row.cells[0]
        row_no_split(row)
        cell_style(c, fill=s_()["tint"], borders={"left": (4.5, s_()["fill"])})
        for k, pr in enumerate(src[0][0]):
            cpara(c, pr, 9.5, INK, bold_color=s_()["deep"], lead=1.5, after=3 if k < len(src[0][0]) - 1 else 0)
    P(container or kit.doc, "", 1, lead=1.0, after=6)
    return t


def cells_of(tbl_block):
    """Non-empty cells of a source table (drops spacer cells and empty rows)."""
    return [[c for c in row if c[0] or c[1]] for row in tbl_block[1] if any(c[0] or c[1] for c in row)]


def nosplit(t):
    for row in t.rows:
        row_no_split(row)


def spacer(mm):
    P(kit.doc, "", 2, lead=1.0, before=mm * 2.835)


# ----------------------------------------------------------------------------- charts (single hue per part)
def fig(w, h):
    return plt.figure(figsize=(w / 25.4, h / 25.4), dpi=300)


def clean(ax, keep="bottom"):
    for sp in ("top", "right", "left", "bottom"):
        ax.spines[sp].set_visible(sp == keep)
    if keep:
        ax.spines[keep].set_color("#C9CCD3")
        ax.spines[keep].set_linewidth(0.6)
    ax.tick_params(length=0, pad=4, colors=hexc(SOFT), labelsize=8)


def save(f, name):
    p = IMG / name
    f.savefig(p, dpi=300, transparent=True)
    plt.close(f)
    return p


def chart_water_balance():                      # replaces image5 (Figure 1)
    c = S[1]
    f = fig(168, 74)
    a = f.add_axes([0.03, 0.2, 0.36, 0.66])
    a.bar([0, 1], [65, 55], color=[hexc(c["fill"]), hexc(mix(c["fill"], 0.55))], width=0.58)
    for x, v in enumerate([65, 55]):
        a.text(x, v + 2, f"{v} km³", ha="center", va="bottom", fontsize=9.5, fontweight="bold", color=hexc(INK))
    a.set_xticks([0, 1], ["Groundwater\nextracted / year", "Groundwater\nrecharged / year"])
    a.set_yticks([])
    a.set_ylim(0, 78)
    clean(a)
    a.set_title("Pakistan withdraws more than nature returns", loc="left", fontsize=9, fontweight="bold", color=hexc(INK), pad=10)
    f.text(0.03, 0.03, "Source: PIDE Working Paper 2026:07", fontsize=6.5, color=hexc(SOFT))
    b = f.add_axes([0.62, 0.2, 0.3, 0.66])
    labels = ["Khyber district\n(over a decade)", "Haripur district\n(over a decade)", "Peshawar district\n(over 30 years)"]
    vals, txt = [74, 62, 49], ["74 ft", "62 ft", "49 ft (≈15 m)"]
    y = [2, 1, 0]
    b.barh(y, vals, color=hexc(c["fill"]), height=0.56)
    for yy, v, t in zip(y, vals, txt):
        b.text(v + 1.5, yy, t, va="center", fontsize=8.5, fontweight="bold", color=hexc(INK))
    b.set_yticks(y, labels, fontsize=7.5, color=hexc(INK))
    b.set_xticks([])
    b.set_xlim(0, 98)
    clean(b, "left")
    b.set_title("Water tables are falling in KP", loc="left", fontsize=9, fontweight="bold", color=hexc(INK), pad=10, x=-0.38)
    f.text(0.47, 0.015, "Sources: Ministry reply to Parliament via Express Tribune (2026);\nThe Third Pole / Dialogue Earth",
           fontsize=6.5, color=hexc(SOFT), linespacing=1.2)
    return save(f, "fig01.png")


def chart_timeline():                            # replaces image8 (Figure 4)
    c = S[2]
    f = fig(168, 112)
    a = f.add_axes([0.01, 0.01, 0.98, 0.98])
    X = lambda d: (d - 4) / 36.0 * 0.78 + 0.18          # x = day of August; September = 31 + day
    a.set_xlim(0, 1)
    a.set_ylim(0, 1)
    a.axis("off")
    for y0, y1, col in [(0.64, 0.80, mix(c["fill"], 0.9)), (0.27, 0.41, mix(c["fill"], 0.94)), (0.02, 0.14, "F2EFEA")]:
        a.add_patch(plt.Rectangle((0, y0), 1, y1 - y0, color=hexc(col), lw=0, zorder=0))
    for d, lab in [(8, "08 Aug"), (15, "15 Aug"), (22, "22 Aug"), (29, "29 Aug"), (36, "05 Sep")]:
        a.text(X(d), 0.975, lab, ha="center", va="center", fontsize=7, color=hexc(SOFT))
        a.plot([X(d), X(d)], [0.02, 0.955], color="#E3E5EA", lw=0.5, zorder=0.5)
    a.annotate("", xy=(X(19), 0.93), xytext=(X(4), 0.93), arrowprops=dict(arrowstyle="<->", color=hexc(SOFT), lw=0.7))
    a.text((X(4) + X(19)) / 2, 0.94, "15-day review window set by the 4 Aug letter", ha="center", va="bottom",
           fontsize=6.6, style="italic", color=hexc(SOFT))
    yA = 0.72
    a.text(0.01, yA + 0.025, "TRACK A", fontsize=7.5, fontweight="bold", color=hexc(c["deep"]))
    a.text(0.01, yA - 0.045, "District pilot", fontsize=7.5, color=hexc(INK))
    a.plot([X(4), X(38)], [yA, yA], color=hexc(c["fill"]), lw=3, zorder=2, solid_capstyle="round")
    events = [(4, "04 Aug", "below", "Direction to all DCs:\none rooftop + one\nsurface-runoff system"),
              (8, "08 Aug", "above", "PMRU monitoring\ntask opened"),
              (19, "19 Aug", "below", "Task due, 3:00 PM;\nclosed 100% complete"),
              (38, "07 Sep", "below", "Review of\nimplementation\nto Chief Secretary")]
    for d, lab, where, txt in events:
        big = d == 38
        a.plot(X(d), yA, "o", ms=8 if big else 6.5, color=hexc(c["deep"] if big else c["fill"]), mec="white", mew=1.2, zorder=3)
        if where == "above":
            a.text(X(d), yA + 0.03, lab, ha="center", va="bottom", fontsize=7, fontweight="bold", color=hexc(c["deep"]))
            a.text(X(d), yA + 0.075, txt, ha="center", va="bottom", fontsize=6.4, color=hexc(INK), linespacing=1.15)
        else:
            a.text(X(d), yA - 0.03, lab, ha="center", va="top", fontsize=7, fontweight="bold", color=hexc(c["deep"]))
            a.text(X(d), yA - 0.07, txt, ha="center", va="top", fontsize=6.4, color=hexc(INK), linespacing=1.15)
    yB = 0.34
    a.text(0.01, yB + 0.025, "TRACK B", fontsize=7.5, fontweight="bold", color=hexc(c["deep"]))
    a.text(0.01, yB - 0.045, "Provincial policy", fontsize=7.5, color=hexc(INK))
    a.annotate("", xy=(0.995, yB), xytext=(X(10), yB), arrowprops=dict(arrowstyle="-|>", color=hexc(c["panel"]), lw=2.4))
    for d in (10, 11):
        a.plot(X(d), yB, "o", ms=6.5, color=hexc(c["panel"]), mec="white", mew=1.2, zorder=3)
    a.text(X(11) + 0.03, yB + 0.03, "11 Aug", ha="left", va="bottom", fontsize=7, fontweight="bold", color=hexc(c["deep"]))
    a.text(X(11) + 0.03, yB + 0.075, "Institutionalisation directions to all\nAdministrative Secretaries", ha="left",
           va="bottom", fontsize=6.4, color=hexc(INK), linespacing=1.15)
    a.text(X(10), yB - 0.03, "10 Aug", ha="center", va="top", fontsize=7, fontweight="bold", color=hexc(c["deep"]))
    a.text(X(10), yB - 0.07, "Weekly Review: PMRU\npresents RWH framework", ha="center", va="top", fontsize=6.4,
           color=hexc(INK), linespacing=1.15)
    a.text(0.985, yB + 0.03, "Continuing provincial policy measure;\nperiodic review by the Chief Secretary", ha="right",
           va="bottom", fontsize=6.4, style="italic", color=hexc(c["deep"]), linespacing=1.15)
    a.text(0.01, 0.095, "EVIDENCE", fontsize=7.5, fontweight="bold", color=hexc(SOFT))
    a.text(0.01, 0.035, "Field record", fontsize=7.5, color=hexc(INK))
    a.add_patch(plt.Rectangle((X(13), 0.055), X(23) - X(13), 0.05, color=hexc(mix(c["fill"], 0.55)), lw=0))
    a.text((X(13) + X(23)) / 2, 0.08, "GPS-stamped site photographs, 13–23 Aug", ha="center", va="center", fontsize=6.4,
           fontweight="bold", color=hexc(INK))
    a.text(X(38) - 0.018, 0.08, "Position at review:\n37 districts, 62 sites", ha="right", va="center", fontsize=6.4,
           color=hexc(INK), linespacing=1.15)
    a.add_patch(plt.Rectangle((X(38) - 0.008, 0.065), 0.016, 0.03, color=hexc(c["deep"]), lw=0))
    return save(f, "fig04.png")


def chart_cumulative():                          # replaces image13 (Figure 6)
    c = S[2]
    f = fig(78, 62)
    a = f.add_axes([0.15, 0.16, 0.8, 0.78])
    m = list(range(0, 25))
    a.plot(m, [30 * x for x in m], color=hexc(c["fill"]), lw=2)
    a.plot(m, [200] * 25, color=hexc(c["deep"]), lw=2)
    a.plot(m, [40] * 25, color=hexc(mix(c["fill"], 0.45)), lw=2)
    a.text(24, 720, "Rs 720k", ha="right", va="bottom", fontsize=7.5, fontweight="bold", color=hexc(INK))
    a.text(24.3, 200, "", fontsize=7)
    for y, t in [(560, "Water tankers\n(Rs 30,000 / month)"), (212, "RWH, new bore (Rs 200,000 once)"),
                 (52, "RWH, reused dry bore (Rs 40,000 once)")]:
        a.text(0.5 if y < 500 else 9.5, y, t, fontsize=6.4, color=hexc(INK), va="bottom", linespacing=1.1)
    a.set_xlim(0, 24.5)
    a.set_ylim(0, 790)
    a.set_xticks([0, 6, 12, 18, 24])
    a.set_yticks([0, 200, 400, 600])
    a.set_xlabel("Months", fontsize=7, color=hexc(SOFT))
    a.set_ylabel("Cumulative cost (Rs thousand)", fontsize=7, color=hexc(SOFT))
    a.grid(axis="y", color="#E6E7EB", lw=0.5)
    clean(a, "bottom")
    a.tick_params(labelsize=7)
    return save(f, "fig06.png")


def chart_built():                               # replaces image16 (Figure 8)
    c = S[3]
    cols = [hexc(c["deep"]), hexc(c["fill"]), hexc(mix(c["fill"], 0.5)), hexc(mix(c["fill"], 0.78))]
    groups = [("Districts by model\n(n = 37)", [(20, "Rooftop only"), (17, "Both models")]),
              ("Sites by model\n(n = 62)", [(45, "Rooftop"), (17, "Surface runoff")]),
              ("Sites by nature of works\n(n = 62)", [(52, "Recharge well"), (6, "Tank only"), (4, "Not declared")]),
              ("Sites by status\n(n = 62)", [(54, "Built"), (4, "In progress"), (3, "Not started"), (1, "Not stated")])]
    f = fig(168, 70)
    for k, (title, segs) in enumerate(groups):
        a = f.add_axes([0.015 + k * 0.25, 0.04, 0.22, 0.74])
        tot, base = sum(v for v, _ in segs), 0
        for j, (v, lab) in enumerate(segs):
            a.bar(0, v / tot, bottom=base, width=0.42, color=cols[j], edgecolor="white", linewidth=1.2)
            yc = base + v / tot / 2
            a.text(0.27, yc if v / tot > 0.08 else base + 0.02, f"{v}  {lab}", va="center", fontsize=7, color=hexc(INK))
            base += v / tot
        a.set_xlim(-0.25, 1.25)
        a.set_ylim(0, 1)
        a.axis("off")
        f.text(0.015 + k * 0.25, 0.86, title, fontsize=7.5, fontweight="bold", color=hexc(INK), va="bottom", linespacing=1.1)
    return save(f, "fig08.png")


REG = []                                          # district register rows, read from the source table


def register():
    rows = blk(110, "#")[1]
    out = []
    for r in rows[1:]:
        v = [text_of(c[0][0]) if c[0] else "" for c in r]
        out.append(v)
    return out


def num(s):
    s = s.replace(",", "").strip()
    return float(s) if s and s not in ("—",) else None


def chart_capacity():                            # replaces image18 (Figure 10), no dual axis: two aligned panels
    c = S[3]
    rec = [r for r in REG if r[7] == "Recharge"]
    rec = sorted(rec, key=lambda r: -num(r[4]))
    names = [r[1].replace("South Waziristan", "S. Waz.").replace("Kohistan", "Koh.") for r in rec]
    caps = [num(r[4]) / 1000 for r in rec]
    total = sum(num(r[4]) for r in REG if r[7] == "Recharge")
    cum, run = [], 0
    for r in rec:
        run += num(r[4])
        cum.append(run / total * 100)
    f = fig(168, 98)
    a = f.add_axes([0.07, 0.42, 0.92, 0.52])
    x = range(len(caps))
    a.bar(x, caps, color=[hexc(c["fill"]) if i < 7 else hexc(mix(c["fill"], 0.62)) for i in x], width=0.7)
    a.text(0, caps[0] + 30, "1,690k", ha="center", va="bottom", fontsize=7, fontweight="bold", color=hexc(INK))
    a.axvline(6.5, color=hexc(SOFT), lw=0.6, ls=(0, (3, 2)))
    a.text(6.9, 1450, "Top 7 districts:\n82% of capacity,\n11% of spend", fontsize=7, color=hexc(INK), va="top", linespacing=1.15)
    a.set_xticks([])
    a.set_xlim(-0.6, len(caps) - 0.4)
    a.set_ylim(0, 1850)
    a.set_yticks([0, 500, 1000, 1500])
    a.set_ylabel("Reported capacity\n(thousand litres)", fontsize=6.5, color=hexc(SOFT))
    a.grid(axis="y", color="#E6E7EB", lw=0.5)
    clean(a, "bottom")
    b = f.add_axes([0.07, 0.2, 0.92, 0.17])
    b.plot(list(x), cum, color=hexc(c["deep"]), lw=1.6, marker="o", ms=2.4)
    b.axvline(6.5, color=hexc(SOFT), lw=0.6, ls=(0, (3, 2)))
    b.text(6.7, cum[6] - 8, f"{cum[6]:.0f}%", fontsize=7, fontweight="bold", color=hexc(INK), va="top")
    b.set_xlim(-0.6, len(caps) - 0.4)
    b.set_ylim(0, 105)
    b.set_yticks([0, 50, 100], ["0", "50%", "100%"])
    b.set_ylabel("Cumulative\nshare", fontsize=6.5, color=hexc(SOFT))
    b.set_xticks(list(x), names, rotation=60, ha="right", fontsize=6.2)
    b.grid(axis="y", color="#E6E7EB", lw=0.5)
    clean(b, "bottom")
    return save(f, "fig10.png")


def chart_costs():                               # replaces image19 (Figure 11)
    c = S[3]
    rec = sorted([r for r in REG if r[7] == "Recharge"], key=lambda r: num(r[6]))
    f = fig(168, 72)
    a = f.add_axes([0.08, 0.3, 0.9, 0.62])
    for i, r in enumerate(rec):
        both = "surface" in r[2]
        v = num(r[6])
        a.plot([i, i], [100, v], color="#D9DCE2", lw=0.6, zorder=1)
        a.plot(i, v, "o", ms=4.6, zorder=3, mew=1.0, mfc=hexc(c["deep"]) if both else "white",
               mec=hexc(c["deep"] if both else c["fill"]))
    a.set_yscale("log")
    a.set_ylim(100, 150000)
    a.set_yticks([100, 1000, 10000, 100000], ["100", "1,000", "10,000", "100,000"])
    a.axhline(2836, color=hexc(c["deep"]), lw=0.7, ls=(0, (4, 2)))
    a.text(len(rec) - 0.5, 3300, "Average across recharging districts: PKR 2,836", ha="right", fontsize=7, color=hexc(c["deep"]))
    a.set_xticks(range(len(rec)), [r[1].replace("South Waziristan", "S. Waz.").replace("Kohistan", "Koh.") for r in rec],
                 rotation=60, ha="right", fontsize=6.2)
    a.set_xlim(-0.8, len(rec) - 0.2)
    a.set_ylabel("PKR per 1,000 litres (log scale)", fontsize=6.5, color=hexc(SOFT))
    a.grid(axis="y", color="#E6E7EB", lw=0.5)
    clean(a, "bottom")
    a.plot([], [], "o", ms=4.6, color=hexc(c["deep"]), label="Rooftop + surface")
    a.plot([], [], "o", ms=4.6, mfc="white", mec=hexc(c["fill"]), label="Rooftop only")
    a.legend(loc="upper left", frameon=False, fontsize=7, handletextpad=0.3)
    return save(f, "fig11.png")


def bar_png(frac, key, w=56, h=3.6):
    px = (round(w / 25.4 * 300), round(h / 25.4 * 300))
    im = Image.new("RGB", px, "#" + S[key]["tint"])
    d = ImageDraw.Draw(im)
    if frac > 0:
        d.rectangle([0, 0, max(6, int(px[0] * frac)), px[1]], fill="#" + (S[key]["fill"] if frac < 1 else S[key]["deep"]))
    else:
        d.rectangle([0, 0, 6, px[1]], fill="#" + S[key]["deep"])
    p = IMG / f"bar-{key}-{frac:.3f}.png"
    im.save(p)
    return p


def sq_png(col, mm=10):
    px = round(mm / 25.4 * 300) * 4
    im = Image.new("RGBA", (px, px), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, px - 1, px - 1], radius=px // 6, fill="#" + col)
    p = IMG / f"sq-{col}-{mm}.png"
    im.resize((px // 4, px // 4)).save(p)
    return p


# ----------------------------------------------------------------------------- page furniture
def strip(current=None):
    def draw(run):
        w = (210 - 4 * 0.8) / 5
        for i in range(1, 6):
            shape(run, (i - 1) * (w + 0.8), 0, w, 10 if i == current else 3, fill=S[i]["fill"], behind=True, z=3)
    return draw


def part_page(k, sec_i, lede_i):
    """New part: the first page carries the full-bleed band; following pages carry the strip with the tab."""
    CUR[0] = k
    s = S[k]
    num_, title = h1_split(sec_i)
    lede = text_of(blk(lede_i)[2])
    light = mix(s["panel"], 0.38) if s["on"] == WHITE else mix(s["panel"], 0.45)
    chip_fill = "FFFFFF" if s["on"] == WHITE else INK
    chip_fg = "#" + (s["panel"] if s["on"] == WHITE else "FFFFFF")

    def band(run):
        shape(run, 0, 0, 210, 112, fill=s["panel"], behind=True, z=1)
        shape(run, 0, 112, 210, 3, fill=s["fill"], behind=True, z=2)
        text_box(run, 20, 6, 120, 46, [T(num_, 120, light, FXB, lead=0.95)], z=20)
        text_box(run, 22, 50, 160, 8, [T(f"PART {k} · {s['name'].upper()}", 7.5, s["on"], FSB, track=40)], z=21)
        text_box(run, 22, 57, 165, 30, [T(title, 24, s["on"], FXB, lead=1.1)], z=21)
        text_box(run, 22, 86, 150, 24, [T(lede, 10.5, s["on"], F, lead=1.45)], z=21)
        kit.picture(run, kit.icon(s["icon"], chip_fill, 18, fg=chip_fg), 170, 18, 18, 18, behind=False, z=30)
    kit.page(top=28, header_shapes=[strip(k)], first_header_shapes=[band])
    spacer(88)


# ----------------------------------------------------------------------------- build
def build(pages):
    kit.configure(OUT, font=F, ink=INK, soft=SOFT, footer=FOOT, icons=HERE / "icons")
    plt.rcParams["font.family"] = ["Figtree", "DejaVu Sans"]
    IMG.mkdir(parents=True, exist_ok=True)
    doc = kit.doc

    # ---------------------------------------------------------------- cover
    kit.page(folio=False, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=INK, behind=True, z=1)])
    a = P(doc, "")
    run = a.add_run()
    shape(run, 0, 0, 210, 40, fill=WHITE, z=4)
    kit.picture(run, media("image1.png"), 18, 9, 22, 22, behind=False, z=6)
    kit.picture(run, media("image2.png"), 43, 9, 22, 22, behind=False, z=6)
    text_box(run, 72, 13, 125, 20, [p_ for p_ in (
        T(text_of(blk(1)[2]), 9, INK, FXB, track=30, lead=1.4),
        T(text_of(blk(2)[2]), 8, SOFT, F, lead=1.4))], z=7)
    title = text_of(blk(3, "Rainwater")[2])
    text_box(run, 20, 52, 175, 60, [T(title.upper().replace(" HARVESTING ", "\nHARVESTING\n"), 44, WHITE, FXB, lead=1.0)], z=7)
    text_box(run, 20, 106, 170, 12, [T(text_of(blk(4)[2]), 14, mix(INK, 0.72), F, lead=1.4)], z=7)
    meta = cells_of(blk(6))[0]
    w = 170 / 4
    for i, (paras, _) in enumerate(meta):
        text_box(run, 20 + i * w, 120, w - 4, 16, [T(text_of(paras[0]).upper(), 6.5, mix(INK, 0.6), FSB, track=30, lead=1.4),
                                                   T(text_of(paras[1]), 9.5, WHITE, F, bold=True, lead=1.3)], z=7)
    kit.picture(run, media("image3.jpg"), 0, 140, 210, 87.5, behind=False, z=5)
    text_box(run, 20, 229, 175, 8, [T(text_of(blk(7)[2]), 7, mix(INK, 0.6), F, italic=True, lead=1.3)], z=7)
    heights = [52, 40, 58, 34, 28]
    cw = (210 - 4 * 1.2) / 5
    for i in range(5):
        shape(run, i * (cw + 1.2), 297 - heights[i], cw, heights[i], fill=S[i + 1]["panel"], behind=True, z=3)
    for i in range(5):
        text_box(run, i * (cw + 1.2) + 4, 297 - heights[i] + 4, cw - 8, 12,
                 [T(f"PART {i + 1}\n" + S[i + 1]["name"].upper(), 6.5, S[i + 1]["on"], FSB, track=20, lead=1.35)], z=40)

    # ---------------------------------------------------------------- contents
    CUR[0] = 1
    kit.page(top=34, header_shapes=[strip()])
    P(doc, text_of(blk(8, "CONTENTS")[2]), 34, INK, FXB, lead=1.1, after=20)
    entries = []
    for i in range(9, 24):
        r = blk(i)[2]
        lab, ttl = r[0][0].strip(), "".join(t for t, *_ in r[1:-1]).strip()
        entries.append((lab, ttl))
    part_of = {"01": 1, "02": 1, "03": 2, "04": 2, "05": 2, "06": 2, "07": 2, "08": 3, "09": 3, "10": 4, "11": 4,
               "12": 4, "": 0, "A": 5}
    ct = table(doc, [14, 16, 116, 22], len(entries) + 1, cell_margin=(0, 2.4, 0, 2.4))
    last_part = None
    for row, (lab, ttl) in zip(ct.rows, entries):
        k = part_of.get(lab, 0)
        if ttl.startswith("Data notes"):
            k = 5
        row_no_split(row)
        for c_ in row.cells:
            cell_style(c_, borders={"bottom": (0.5, RULE)}, valign="center")
        c0, c1, c2, c3 = row.cells
        if k and k != last_part:
            inline_pic(c0, sq_png(S[k]["fill"], 8), 8, align="left")
        else:
            cell_p(c0, "", 8)
        last_part = k or last_part
        cell_p(c1, lab, 12, S[k]["deep"] if k else SOFT, FXB, lead=1.3)
        cell_p(c2, ttl, 11.5, INK, FSB if not lab or lab == "A" else F, lead=1.3)
        cell_p(c3, str(pages.get(ttl, "")), 11.5, S[k]["deep"] if k else SOFT, FXB, lead=1.3, align="right")
    legend = table(doc, [168], 1)
    lc = legend.rows[0].cells[0]
    cell_p(lc, "", 4, before=16)
    lt = table(lc, [33.6] * 5, 1)
    for i in range(5):
        c_ = lt.rows[0].cells[i]
        cell_style(c_, borders={"top": (3, S[i + 1]["fill"])})
        cell_p(c_, f"PART {i + 1}", 7, S[i + 1]["deep"], FSB, track=30, lead=1.3, before=5)
        cell_p(c_, S[i + 1]["name"], 9, INK, F, bold=True, lead=1.3, right_indent=2)

    # ---------------------------------------------------------------- executive snapshot (overview: all colours)
    kit.page(top=30, header_shapes=[strip()])
    P(doc, "OVERVIEW", 7.5, SOFT, FSB, track=40, lead=1.3, after=4)
    P(doc, text_of(blk(24, "EXECUTIVE")[2]), 30, INK, FXB, lead=1.1, after=8)
    para(blk(25)[2], 12.5, INK, lead=1.42, after=14, right_indent=20)
    kpis = [c_ for row in cells_of(blk(26)) + cells_of(blk(27)) for c_ in row]
    order = [3, 3, 3, 3, 3, 2, 3, 3]
    kt = table(doc, [40.5, 2.0, 40.5, 2.0, 40.5, 2.0, 40.5], 2, cell_margin=(0, 4, 0, 4))
    nosplit(kt)
    for n_, (paras, _) in enumerate(kpis):
        c_ = kt.rows[n_ // 4].cells[(n_ % 4) * 2]
        k = [1, 3, 3, 3, 3, 2, 3, 5][n_]
        cell_style(c_, fill=S[k]["tint"], borders={"top": (3, S[k]["fill"])})
        cell_p(c_, text_of(paras[0]), 18, S[k]["deep"], FXB, lead=1.15, before=7, after=2)
        cell_p(c_, text_of(paras[1]), 8.5, INK, F, lead=1.35, after=8)
    spacer(5)
    kicker(text_of(blk(28)[2]), SOFT, before=8)
    sb = table(doc, [168 * 30 / 37, 168 * 6 / 37, 168 * 1 / 37], 1)
    nosplit(sb)
    for c_, (txt, col, on) in zip(sb.rows[0].cells, [("30 districts recharging", S[3]["panel"], WHITE),
                                                     ("6", mix(S[3]["fill"], 0.55), INK), ("1", S[2]["panel"], WHITE)]):
        cell_style(c_, fill=col, borders={"left": (2, WHITE)}, valign="center")
        cell_p(c_, txt, 8.5, on, F, bold=True, lead=1.3, before=3, after=3, align="center")
    lg = table(doc, [168 * 30 / 37, 168 * 7 / 37], 1)
    cell_p(lg.rows[0].cells[1], "6 storage only  ·  1 undeclared", 7.5, SOFT, F, lead=1.3, before=3, align="right")
    P(doc, text_of(blk(30)[2]), 13, INK, F, bold=True, lead=1.3, before=14, after=6, keep=True)
    st = table(doc, [36, 132], len(blk(31)[1]), cell_margin=(0, 2.6, 0, 2.6))
    for k, (row, src) in enumerate(zip(st.rows, blk(31)[1])):
        row_no_split(row)
        col = S[[1, 1, 2, 3, 4][k]]
        for c_ in row.cells:
            cell_style(c_, borders={"top": (0.5, RULE)})
        cell_p(row.cells[0], text_of(src[0][0][0]).upper(), 7.5, col["deep"], FSB, track=20, lead=1.4, before=1)
        cpara(row.cells[1], src[1][0][0], 9.5, INK, lead=1.5)
    P(doc, text_of(blk(32)[2]), 13, INK, F, bold=True, lead=1.3, before=14, after=6, keep=True)
    ob = table(doc, [14, 154], 4, cell_margin=(0, 2.4, 0, 2.4))
    for k, i in enumerate(range(33, 37)):
        row = ob.rows[k]
        row_no_split(row)
        r = blk(i)[2]
        n_ = r[0][0].split()[0]
        cell_p(row.cells[0], n_, 20, S[[2, 3, 3, 4][k]]["fill"], FXB, lead=1.1)
        cpara(row.cells[1], r, 9.5, INK, bold_color=INK, lead=1.5, drop=len(n_) + 2)

    # ================================================================ PART 1 (blue): sections 01-02
    part_page(1, 37, 38)
    body(39)
    inline_pic(doc, chart_water_balance(), 168, align="left", before=4)
    caption(41)
    body(42)
    h2(43)
    cards = cells_of(blk(44))[0]
    ct2 = table(doc, [82, 4, 82], 1, cell_margin=(5, 5, 5, 5))
    nosplit(ct2)
    for c_, (paras, _) in zip([ct2.rows[0].cells[0], ct2.rows[0].cells[2]], cards):
        cell_style(c_, fill=S[1]["tint"], borders={"top": (3, S[1]["fill"])})
        cell_p(c_, text_of(paras[0]), 7.5, S[1]["deep"], FSB, track=40, lead=1.3, after=3)
        cell_p(c_, text_of(paras[1]), 12, INK, F, bold=True, lead=1.3, after=4)
        cell_p(c_, text_of(paras[2]), 9.5, INK, F, lead=1.5)
    spacer(4)
    callout([r for r in cells_of(blk(45))])
    section_head(46, 47)
    h2(48)
    inline_pic(doc, media("image6.png"), 168, align="left")
    caption(50)
    h2(51)
    inline_pic(doc, media("image7.png"), 168, align="left")
    caption(53)
    h2(54)
    rows = blk(55)[1]
    mt = table(doc, [34, 67, 67], len(rows), cell_margin=(2.4, 2.4, 2.4, 2.4))
    for r_i, (row, src) in enumerate(zip(mt.rows, rows)):
        row_no_split(row, header=r_i == 0)
        for c_i, (c_, (paras, _)) in enumerate(zip(row.cells, src)):
            txt = text_of(paras[0]) if paras else ""
            if r_i == 0:
                cell_style(c_, fill=S[1]["panel"] if c_i else None, borders={"bottom": (1, S[1]["fill"])})
                cell_p(c_, txt.upper(), 7.5, WHITE, F, bold=True, track=20, lead=1.3)
            else:
                cell_style(c_, fill=S[1]["tint"] if r_i % 2 == 0 else None, borders={"bottom": (0.5, RULE)})
                cell_p(c_, txt, 9, INK, FSB if c_i == 0 else F, lead=1.4)
    h2(56)
    body(57)
    calc = cells_of(blk(58))[0]
    cc = table(doc, [54, 3, 54, 3, 54], 1, cell_margin=(4, 4, 4, 4))
    nosplit(cc)
    for c_, (paras, _) in zip([cc.rows[0].cells[i] for i in (0, 2, 4)], calc):
        cell_style(c_, fill=S[1]["tint"], borders={"top": (3, S[1]["fill"])})
        cell_p(c_, text_of(paras[0]), 9, INK, F, bold=True, lead=1.35, after=3)
        cell_p(c_, text_of(paras[1]), 8.5, SOFT, F, lead=1.4, after=4)
        cell_p(c_, text_of(paras[2]), 20, S[1]["deep"], FXB, lead=1.15)
    caption(59, after=0) if False else para(blk(59)[2], 8, SOFT, lead=1.4, before=5)

    # ================================================================ PART 2 (coral): sections 03-07
    part_page(2, 60, 61)
    inline_pic(doc, chart_timeline(), 168, align="left")
    caption(63)
    body(64, bold_color=S[2]["deep"])
    body(65, bold_color=S[2]["deep"])
    h2(66)
    loop = [("DIRECTION", [("1", "Direction", "Chief Secretary approval"), ("2", "04 Aug letter", "HRM&A to all DCs")]),
            ("DELIVERY", [("3", "08 Aug task", "PMRU task, due 19 Aug"), ("4", "Execution", "DCs with PHE and C&W")]),
            ("ACCOUNTABILITY", [("5", "Site return", "Location, coordinates, specs, photos"),
                                ("6", "Consolidation", "PMRU register and ranking"),
                                ("7", "07 Sep review", "Findings to the Chief Secretary")])]
    lw = [22.4] * 7
    gaps = [1.6] * 6
    widths = [v for pair in zip(lw, gaps + [0]) for v in pair][:-1]
    lt2 = table(doc, widths, 2, cell_margin=(2, 2, 2, 2))
    nosplit(lt2)
    fills = [(S[2]["deep"], WHITE), (S[2]["panel"], WHITE), (S[2]["tint"], INK)]
    k = 0
    for g, (gname, steps) in enumerate(loop):
        for j, (n_, ttl, sub) in enumerate(steps):
            hc, cc_ = lt2.rows[0].cells[k * 2], lt2.rows[1].cells[k * 2]
            cell_style(hc, borders={"bottom": (2, S[2]["fill"])})
            cell_p(hc, gname if j == 0 else "", 6.5, S[2]["deep"], FSB, track=30, lead=1.3)
            fill, on = fills[g]
            cell_style(cc_, fill=fill, valign="top")
            cell_p(cc_, n_, 16, on if g < 2 else S[2]["deep"], FXB, lead=1.1, before=4)
            cell_p(cc_, ttl, 8.5, on, F, bold=True, lead=1.25, before=2, after=2)
            cell_p(cc_, sub, 7.2, on, F, lead=1.3, after=4)
            k += 1
    P(doc, "Feedback loop: review findings return to districts and departments as formal follow-up letters", 8,
      S[2]["deep"], F, italic=True, lead=1.4, before=6, align="center")
    caption(68)

    section_head(69, 70)
    t71 = cells_of(blk(71))[0]
    ex = table(doc, [64, 6, 98], 1)
    nosplit(ex)
    inline_pic(ex.rows[0].cells[0], media("image10.jpg"), 64, align="left")
    mc = ex.rows[0].cells[2]
    for pr in t71[1][0]:
        txt = text_of(pr)
        if txt.isupper():
            cell_p(mc, txt, 7, S[2]["deep"], FSB, track=30, lead=1.3, before=6, after=1)
        else:
            cpara(mc, pr, 9, INK, lead=1.45)
    caption(72)
    callout(cells_of(blk(73)))

    section_head(74, 75)
    inline_pic(doc, media("image11.jpg"), 168, align="left")
    caption(77)
    h2(78)
    tri = cells_of(blk(79))[0]
    tt = table(doc, [54, 3, 54, 3, 54], 1, cell_margin=(4, 4, 4, 4))
    nosplit(tt)
    for c_, (paras, _) in zip([tt.rows[0].cells[i] for i in (0, 2, 4)], tri):
        cell_style(c_, fill=S[2]["tint"], borders={"top": (3, S[2]["fill"])})
        cell_p(c_, text_of(paras[0]), 11, S[2]["deep"], F, bold=True, lead=1.3, after=3)
        cell_p(c_, text_of(paras[1]), 9, INK, F, lead=1.45)
    spacer(3)
    body(80)
    callout(cells_of(blk(81)))

    section_head(82, 83)
    t84 = cells_of(blk(84))[0]
    fx = table(doc, [86, 6, 76], 1)
    nosplit(fx)
    inline_pic(fx.rows[0].cells[0], media("image12.jpg"), 86, align="left")
    cpara(fx.rows[0].cells[0], t84[0][0][0], 7.5, SOFT, lead=1.4, before=4)
    rc = fx.rows[0].cells[2]
    cell_p(rc, text_of(t84[1][0][0]), 12, INK, F, bold=True, lead=1.3, after=5)
    for pr in t84[1][0][1:]:
        cpara(rc, pr, 9, INK, bold_color=S[2]["deep"], lead=1.45, after=4)
    h2(85)
    ph = cells_of(blk(86))[0]
    pt = table(doc, [40.5, 2, 40.5, 2, 40.5, 2, 40.5], 1, cell_margin=(4, 4, 4, 4))
    nosplit(pt)
    for c_, (paras, _) in zip([pt.rows[0].cells[i] for i in (0, 2, 4, 6)], ph):
        cell_style(c_, fill=S[2]["tint"], borders={"top": (3, S[2]["fill"])})
        cell_p(c_, text_of(paras[0]), 20, S[2]["deep"], FXB, lead=1.15)
        cell_p(c_, text_of(paras[1]), 9.5, INK, F, bold=True, lead=1.3, before=2, after=3)
        cell_p(c_, text_of(paras[2]), 8.5, INK, F, lead=1.4)
    body(87, before=8)
    h2(88)
    t89 = cells_of(blk(89))[0]
    fc = table(doc, [80, 8, 80], 1)
    nosplit(fc)
    inline_pic(fc.rows[0].cells[0], chart_cumulative(), 78, align="left")
    for pr in t89[1][0]:
        cpara(fc.rows[0].cells[2], pr, 9.5, INK, bold_color=S[2]["deep"], lead=1.5, after=6)
    caption(90)
    h2(91)
    rows = blk(92)[1]
    pp = table(doc, [44, 34, 90], len(rows), cell_margin=(2.4, 2.4, 2.4, 2.4))
    for r_i, (row, src) in enumerate(zip(pp.rows, rows)):
        row_no_split(row, header=r_i == 0)
        for c_i, (c_, (paras, _)) in enumerate(zip(row.cells, src)):
            txt = text_of(paras[0]) if paras else ""
            if r_i == 0:
                cell_style(c_, fill=S[2]["panel"])
                cell_p(c_, txt.upper(), 7.5, WHITE, F, bold=True, track=20, lead=1.3)
            else:
                cell_style(c_, fill=S[2]["tint"] if r_i % 2 == 0 else None, borders={"bottom": (0.5, RULE)})
                cell_p(c_, txt, 9, INK, FSB if c_i == 0 else F, lead=1.4)
    spacer(5)
    callout(cells_of(blk(93)))

    section_head(94, 95)
    t96 = cells_of(blk(96))[0]
    lx = table(doc, [70, 6, 92], 1)
    nosplit(lx)
    inline_pic(lx.rows[0].cells[0], media("image14.jpg"), 70, align="left")
    cpara(lx.rows[0].cells[0], t96[0][0][0], 7.5, SOFT, lead=1.4, before=4)
    mc = lx.rows[0].cells[2]
    for pr in t96[1][0]:
        txt = text_of(pr)
        if txt.isupper():
            cell_p(mc, txt, 7, S[2]["deep"], FSB, track=30, lead=1.3, before=6, after=1)
        else:
            cpara(mc, pr, 9, INK, lead=1.45)
    spacer(6)
    hub = table(doc, [168], 1, cell_margin=(6, 4, 6, 4))
    hc = hub.rows[0].cells[0]
    cell_style(hc, fill=S[2]["panel"])
    cell_p(hc, "RWH as a standing provincial policy measure", 13, WHITE, F, bold=True, lead=1.3, align="center")
    cell_p(hc, "11 August 2026 directions", 8.5, WHITE, F, lead=1.4, align="center")
    ws = [("(a)", "Planning & Development", "RWH / recharge component in PC-Is, weighed at appraisal, not a formality"),
          ("(b)", "Local Government", "Amend building byelaws; link compliance to plan approval and completion certificate"),
          ("(c)", "LG: TMAs and WSSCs", "Recharge pits at low-lying spots where stormwater collects; fold into road works"),
          ("(d)", "Housing & Development Authorities", "RWH at layout-plan / NOC stage; enforce KP Housing Schemes Regulations 2026"),
          ("(e)", "Agriculture, Forest, Irrigation", "Add retention and recharge to watershed, plantation and irrigation schemes"),
          ("(f)", "Information Department", "Province-wide behaviour-change strategy, beyond publicity of Government works")]
    wt = table(doc, [54, 3, 54, 3, 54], 2, cell_margin=(4, 4, 4, 4))
    nosplit(wt)
    for n_, (lab, ttl, sub) in enumerate(ws):
        c_ = wt.rows[n_ // 3].cells[(n_ % 3) * 2]
        cell_style(c_, fill=S[2]["tint"], borders={"top": (3, S[2]["fill"]), "bottom": (3, WHITE)})
        cell_p(c_, lab, 8, S[2]["deep"], FXB, lead=1.3)
        cell_p(c_, ttl, 9.5, INK, F, bold=True, lead=1.3, after=3)
        cell_p(c_, sub, 8.5, INK, F, lead=1.4)
    caption(98)
    callout(cells_of(blk(99)))

    # ================================================================ PART 3 (teal): sections 08-09
    REG[:] = register()
    part_page(3, 100, 101)
    inline_pic(doc, chart_built(), 168, align="left")
    caption(103)
    body(104)
    h2(105)
    divisions = [("MALAKAND DIVISION", ["Swat", "Bar Swat", "Dir Upper", "Dir Lower", "Chitral Upper", "Chitral Lower", "Buner",
                                        "Shangla", "Malakand", "Bajaur"]),
                 ("HAZARA DIVISION", ["Abbottabad", "Haripur", "Mansehra", "Battagram", "Torghar", "Kohistan Upper",
                                      "Kohistan Lower", "Kolai Palas"]),
                 ("PESHAWAR DIVISION", ["Peshawar", "Charsadda", "Nowshera", "Khyber", "Mohmand"]),
                 ("KOHAT DIVISION", ["Kohat", "Hangu", "Karak", "Kurram", "Orakzai"]),
                 ("MARDAN DIVISION", ["Mardan", "Swabi"]), ("BANNU DIVISION", ["Bannu", "Lakki Marwat", "North Waziristan"]),
                 ("D.I. KHAN DIVISION", ["D.I. Khan", "Tank", "South Waziristan Upper", "South Waziristan Lower"])]
    reg = {r[1]: r for r in REG}
    for dname, ds in divisions:
        kicker(dname, SOFT, before=5, after=3, size=6.5)
        rows_n = math.ceil(len(ds) / 5)
        g = table(doc, [32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4], rows_n, cell_margin=(2.6, 1.6, 2.6, 1.6))
        nosplit(g)
        for n_, d in enumerate(ds):
            r = reg[d]
            c_ = g.rows[n_ // 5].cells[(n_ % 5) * 2]
            outcome = r[7]
            fill, on = {"Recharge": (S[3]["panel"], WHITE), "Storage": (mix(S[3]["fill"], 0.55), INK)}.get(outcome, (S[2]["panel"], WHITE))
            cell_style(c_, fill=fill, borders={"bottom": (2, WHITE)})
            short = d.replace("North Waziristan", "N. Waziristan").replace("South Waziristan", "S. Waziristan")
            cell_p(c_, short, 8, on, F, bold=True, lead=1.25)
            cell_p(c_, f"{r[4]} L", 7.5, on, F, lead=1.25)
            cell_p(c_, f"#{r[0]} · {r[2]}", 6.2, on, F, lead=1.3)
    lgd = table(doc, [6, 50, 6, 50, 6, 50], 1, cell_margin=(0, 1.5, 0, 0))
    for i, (col, lab) in enumerate([(S[3]["panel"], "Recharge installed (30)"), (mix(S[3]["fill"], 0.55), "Storage tank only (6)"),
                                    (S[2]["panel"], "No system declared (1)")]):
        inline_pic(lgd.rows[0].cells[i * 2], sq_png(col, 3.2), 3.2, align="left", before=6)
        cell_p(lgd.rows[0].cells[i * 2 + 1], lab, 7.5, INK, F, lead=1.3, before=5)
    caption(107)
    h2(108)
    body(109)
    rows = blk(110)[1]
    rw = [8, 34, 25, 23, 21, 21, 19, 17]
    rg = table(doc, rw, len(rows), cell_margin=(1.6, 1.4, 1.6, 1.4))
    for r_i, (row, src) in enumerate(zip(rg.rows, rows)):
        row_no_split(row, header=r_i == 0)
        vals = [text_of(c_[0][0]) if c_[0] else "" for c_ in src]
        for c_i, (c_, v) in enumerate(zip(row.cells, vals)):
            right = c_i in (0, 4, 5, 6)
            if r_i == 0:
                cell_style(c_, fill=S[3]["panel"], valign="bottom")
                cell_p(c_, v.upper(), 6.5, WHITE, F, bold=True, track=10, lead=1.25, align="right" if right else "left")
                continue
            outcome = vals[7]
            band = {"Storage": S[3]["tint"], "None declared": S[2]["tint"]}.get(outcome)
            cell_style(c_, fill=band, borders={"bottom": (0.5, RULE)})
            if c_i == 7:
                col = {"Recharge": S[3]["deep"], "Storage": SOFT}.get(v, S[2]["deep"])
                cell_p(c_, v, 7.5, col, F, bold=True, lead=1.3)
            else:
                cell_p(c_, v, 7.8, INK, FSB if c_i == 1 else F, lead=1.3, align="right" if right else "left")
    body(111, size=8, color=SOFT, lead=1.4, before=5)
    h2(112)
    inline_pic(doc, chart_capacity(), 168, align="left")
    caption(114)
    body(115)
    h2(116)
    inline_pic(doc, chart_costs(), 168, align="left")
    caption(118)
    callout(cells_of(blk(119)))
    h2(120)
    flow = [("College drain", "Existing drain of the Govt College of Technology, Timergara"),
            ("Filtration tank", "Strips silt before the water goes down"),
            ("Dry tube well", "An existing well that had stopped yielding, reused"),
            ("Aquifer", "1,680,609 litres reported recharge capacity")]
    fl = table(doc, [38.25, 5, 38.25, 5, 38.25, 5, 38.25], 1, cell_margin=(4, 4, 4, 4))
    nosplit(fl)
    for n_, (ttl, sub) in enumerate(flow):
        c_ = fl.rows[0].cells[n_ * 2]
        fill, on = [(S[3]["tint"], INK), (mix(S[3]["fill"], 0.55), INK), (S[3]["panel"], WHITE), (S[3]["deep"], WHITE)][n_]
        cell_style(c_, fill=fill, valign="center")
        cell_p(c_, ttl, 10, on, F, bold=True, lead=1.3, align="center", before=2, after=3)
        cell_p(c_, sub, 7.8, on, F, lead=1.35, align="center", after=2)
        if n_ < 3:
            cell_style(fl.rows[0].cells[n_ * 2 + 1], valign="center")
            cell_p(fl.rows[0].cells[n_ * 2 + 1], "›", 16, S[3]["fill"], FXB, lead=1.0, align="center")
    caption(122)
    kp = cells_of(blk(123))[0]
    kt2 = table(doc, [40.5, 2, 40.5, 2, 40.5, 2, 40.5], 1, cell_margin=(0, 4, 0, 4))
    nosplit(kt2)
    for c_, (paras, _) in zip([kt2.rows[0].cells[i] for i in (0, 2, 4, 6)], kp):
        cell_style(c_, borders={"top": (1.5, S[3]["fill"])})
        cell_p(c_, text_of(paras[0]), 15, S[3]["deep"], FXB, lead=1.15, before=6, after=2)
        cell_p(c_, text_of(paras[1]), 8.2, SOFT, F, lead=1.35)
    spacer(4)
    body(124)
    h2(125)
    body(126)

    def photo_grid(tbl_i, start_caption=None):
        cells = [c_ for row in cells_of(blk(tbl_i)) for c_ in row]
        rows_n = math.ceil(len(cells) / 2)
        pg = table(doc, [82, 4, 82], rows_n)
        for n_, (paras, imgs) in enumerate(cells):
            c_ = pg.rows[n_ // 2].cells[(n_ % 2) * 2]
            row_no_split(pg.rows[n_ // 2])
            inline_pic(c_, media(imgs[0][0]), 82, align="left")
            cap = text_of(paras[0]) if paras else ""
            m = re.match(r"^(#\d+\s+[^\s].*?)\s{2,}(.*)$", cap)
            head, rest = (m.group(1), m.group(2)) if m else (cap, "")
            cell_p(c_, head, 9, INK, F, bold=True, lead=1.3, before=3)
            cell_p(c_, rest, 7.5, SOFT, F, lead=1.35, after=8)
    photo_grid(127)
    body(128, size=8, color=SOFT, lead=1.4)

    section_head(129, 130)
    inline_pic(doc, media("image25.jpg"), 168, align="left")
    caption(132)
    body(133)
    h2(134)
    gaps6 = [c_ for row in cells_of(blk(135)) for c_ in row]
    gt = table(doc, [54, 3, 54, 3, 54], 2, cell_margin=(4, 4, 4, 4))
    nosplit(gt)
    for n_, (paras, _) in enumerate(gaps6):
        c_ = gt.rows[n_ // 3].cells[(n_ % 3) * 2]
        cell_style(c_, fill=S[3]["tint"], borders={"top": (3, S[3]["fill"]), "bottom": (3, WHITE)})
        cell_p(c_, text_of(paras[0]), 18, S[3]["deep"], FXB, lead=1.15)
        cell_p(c_, text_of(paras[1]), 9.5, INK, F, bold=True, lead=1.3, before=2, after=3)
        cell_p(c_, text_of(paras[2]), 8.5, INK, F, lead=1.4)
    h2(136)
    body(137)
    rows = blk(138)[1]
    rt = table(doc, [10, 104, 54], len(rows), cell_margin=(2.4, 2.4, 2.4, 2.4))
    for r_i, (row, src) in enumerate(zip(rt.rows, rows)):
        row_no_split(row, header=r_i == 0)
        for c_i, (c_, (paras, _)) in enumerate(zip(row.cells, src)):
            txt = text_of(paras[0]) if paras else ""
            if r_i == 0:
                cell_style(c_, fill=S[3]["panel"])
                cell_p(c_, txt.upper(), 7.5, WHITE, F, bold=True, track=20, lead=1.3)
            else:
                cell_style(c_, borders={"bottom": (0.5, RULE)})
                cell_p(c_, txt, 11 if c_i == 0 else 9, S[3]["deep"] if c_i == 0 else INK, FXB if c_i == 0 else F, lead=1.4)
    body(139, size=8, color=SOFT, lead=1.4, before=5)

    # ================================================================ PART 4 (saffron): sections 10-12
    part_page(4, 140, 141)
    asked = [("District administrations that returned site data", 37, 37, "All DCs directed (4 Aug)"),
             ("Districts with recharge into the aquifer in place", 30, 37, "Purpose: groundwater recharge"),
             ("Districts with a surface-runoff system", 17, 37, "One per district directed"),
             ("Sites built by the review date", 54, 62, "Complete during the monsoon"),
             ("Sites with filtration in place", 59, 62, "First-flush / gravel beds specified"),
             ("Sites with a publicity campaign", 59, 62, "Social-media publicity directed"),
             ("Sites independently verified", 0, 62, "Self-certified returns only")]
    at = table(doc, [60, 52, 20, 36], len(asked) + 1, cell_margin=(2.2, 2, 2.2, 2))
    for i, h in enumerate(["Measure", "Achieved", "", "What was asked"]):
        cell_style(at.rows[0].cells[i], borders={"bottom": (1, INK)})
        cell_p(at.rows[0].cells[i], h.upper(), 7, SOFT, F, bold=True, track=20, lead=1.3)
    for r_i, (m, a_, n_, ask) in enumerate(asked, 1):
        row = at.rows[r_i]
        for c_ in row.cells:
            cell_style(c_, borders={"bottom": (0.5, RULE)}, valign="center")
        cell_p(row.cells[0], m, 9, INK, F, lead=1.35)
        inline_pic(row.cells[1], bar_png(a_ / n_, 4, w=48), 48, align="left")
        cell_p(row.cells[2], f"{a_} / {n_}", 9, S[4]["deep"], F, bold=True, lead=1.3)
        cell_p(row.cells[3], ask, 7.8, SOFT, F, italic=True, lead=1.35)
    caption(143)
    h2(144)
    body(145)
    body(146)
    rows = blk(147)[1]
    mt2 = table(doc, [36, 98, 34], len(rows), cell_margin=(2.4, 2.4, 2.4, 2.4))
    for r_i, (row, src) in enumerate(zip(mt2.rows, rows)):
        row_no_split(row, header=r_i == 0)
        for c_i, (c_, (paras, _)) in enumerate(zip(row.cells, src)):
            txt = text_of(paras[0]) if paras else ""
            if r_i == 0:
                cell_style(c_, fill=S[4]["panel"])
                cell_p(c_, txt.upper(), 7.5, INK, F, bold=True, track=20, lead=1.3)
            elif c_i == 2:
                full = txt == "Largely met"
                cell_style(c_, fill=S[4]["deep"] if full else S[4]["tint"], borders={"bottom": (0.5, RULE)}, valign="center")
                cell_p(c_, txt, 8.5, WHITE if full else S[4]["deep"], F, bold=True, lead=1.3)
            else:
                cell_style(c_, borders={"bottom": (0.5, RULE)})
                cell_p(c_, txt, 9, INK, FSB if c_i == 0 else F, lead=1.4)

    section_head(148, 149)
    stages = [("Coverage", "37 of 37 districts acted and reported; 30 recharging", "Largely achieved"),
              ("Quality", "No site independently verified; costs vary widely", "Next priority"),
              ("Scale", "Three ADP 2026-27 schemes; RWH in PC-Is (11 Aug)", "Instruments in place"),
              ("Sustainability", "Maintenance and water-table monitoring not yet in place", "Proposed (7 Sep)"),
              ("Institutionalisation", "Byelaws, housing rules and communication strategy", "Directed (11 Aug)")]
    sg = table(doc, [32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4, 1.5, 32.4], 1, cell_margin=(3.5, 3, 3.5, 3))
    nosplit(sg)
    for n_, (ttl, sub, status) in enumerate(stages):
        c_ = sg.rows[0].cells[n_ * 2]
        cell_style(c_, fill=S[4]["tint"], borders={"top": (3, S[4]["fill"])})
        cell_p(c_, f"0{n_ + 1}", 16, S[4]["deep"], FXB, lead=1.15)
        cell_p(c_, ttl, 8.5, INK, F, bold=True, lead=1.3, before=1, after=3)
        cell_p(c_, sub, 7.8, INK, F, lead=1.38, after=6)
        cell_p(c_, status.upper(), 6.5, S[4]["deep"], FSB, track=20, lead=1.3)
    caption(151)
    body(152)
    h2(153)
    P(doc, text_of(blk(154)[2]), 7.5, S[4]["deep"], FSB, track=30, lead=1.3, after=6, keep=True)
    phases = [("OCT – DEC 2026", "Verify and close", ["Independent, geo-tagged inspection of all 62 sites",
                                                       "Close North Waziristan, South Waziristan Upper and Mardan",
                                                       "One agreed method for stating recharge capacity"]),
              ("JAN – MAR 2027", "Standardise", ["Formal reference to PCRWR", "Standard designs and unit costs by site type",
                                                  "Piezometers in water-stressed districts"]),
              ("APR – JUN 2027", "Prepare for monsoon 2027", ["Pre-monsoon cleaning of screens, diverters, filters",
                                                               "Second round led by surface runoff in high-rainfall areas",
                                                               "Convert storage-only sites to recharge where feasible"]),
              ("JUL – SEP 2027", "Measure and report", ["Water-table readings and recharge estimates",
                                                         "District scorecard compiled by PMRU",
                                                         "Progress on the six 11 August workstreams"])]
    rm = table(doc, [40.5, 2, 40.5, 2, 40.5, 2, 40.5], 1)         # one row: the roadmap never splits
    nosplit(rm)
    for n_, (dates, ttl, items) in enumerate(phases):
        col = table(rm.rows[0].cells[n_ * 2], [40.5], 1 + len(items), cell_margin=(3, 3, 3, 3))
        hc = col.rows[0].cells[0]
        cell_style(hc, fill=[S[4]["deep"], S[4]["deep"], S[4]["panel"], S[4]["panel"]][n_])
        on = WHITE if n_ < 2 else INK
        cell_p(hc, dates, 6.8, on, FSB, track=20, lead=1.3, before=1)
        cell_p(hc, ttl, 10.5, on, F, bold=True, lead=1.25, after=2)
        for j, it in enumerate(items):
            c_ = col.rows[j + 1].cells[0]
            cell_style(c_, fill=S[4]["tint"], borders={"top": (2, WHITE)})
            cell_p(c_, it, 8.2, INK, F, lead=1.38, before=1, after=1)
    caption(156)
    h2(157)
    dt = table(doc, [14, 154], 3, cell_margin=(0, 2.4, 0, 2.4))
    for k, i in enumerate(range(158, 161)):
        r = blk(i)[2]
        n_ = r[0][0].split()[0]
        row_no_split(dt.rows[k])
        cell_p(dt.rows[k].cells[0], n_, 20, S[4]["fill"], FXB, lead=1.1)
        cpara(dt.rows[k].cells[1], r, 9.5, INK, bold_color=INK, lead=1.5, drop=len(n_) + 2)

    section_head(161)
    for i in range(162, 167):
        body(i)
    kt3 = cells_of(blk(167))[0][0][0]
    kb = table(doc, [168], 1, cell_margin=(7, 6, 7, 6))
    nosplit(kb)
    kc = kb.rows[0].cells[0]
    cell_style(kc, fill=S[4]["panel"])
    cell_p(kc, text_of(kt3[0]), 7.5, INK, FSB, track=40, lead=1.3, after=6)
    for pr in kt3[1:]:
        cpara(kc, pr, 10, INK, lead=1.5, after=3)

    # ================================================================ PART 5 (plum): data notes + annex
    CUR[0] = 5
    s5 = S[5]

    def band5(run):
        shape(run, 0, 0, 210, 112, fill=s5["panel"], behind=True, z=1)
        shape(run, 0, 112, 210, 3, fill=s5["fill"], behind=True, z=2)
        text_box(run, 20, 6, 170, 46, [T("DATA", 110, mix(s5["panel"], 0.38), FXB, lead=0.95)], z=20)
        text_box(run, 22, 50, 160, 8, [T(f"PART 5 · {s5['name'].upper()}", 7.5, WHITE, FSB, track=40)], z=21)
        text_box(run, 22, 57, 165, 30, [T(text_of(blk(168)[2]), 24, WHITE, FXB, lead=1.1)], z=21)
        text_box(run, 22, 86, 150, 24, [T(text_of(blk(170)[2]), 10.5, WHITE, F, lead=1.45)], z=21)
        kit.picture(run, kit.icon(s5["icon"], "FFFFFF", 18, fg="#" + s5["panel"]), 170, 18, 18, 18, behind=False, z=30)
    kit.page(top=28, header_shapes=[strip(5)], first_header_shapes=[band5])
    spacer(88)
    h2(169)
    rows = blk(171)[1]
    dn = table(doc, [40, 70, 58], len(rows), cell_margin=(2, 2.2, 2, 2.2))
    for r_i, (row, src) in enumerate(zip(dn.rows, rows)):
        row_no_split(row, header=r_i == 0)
        for c_i, (c_, (paras, _)) in enumerate(zip(row.cells, src)):
            txt = text_of(paras[0]) if paras else ""
            if r_i == 0:
                cell_style(c_, fill=s5["panel"])
                cell_p(c_, txt.upper(), 7, WHITE, F, bold=True, track=20, lead=1.3)
            else:
                cell_style(c_, fill=s5["tint"] if r_i % 2 == 0 else None, borders={"bottom": (0.5, RULE)})
                cell_p(c_, txt, 8, INK, FSB if c_i == 0 else F, lead=1.38)
    h2(172)
    for i in range(173, 189):
        r = blk(i)[2]
        t = text_of(r)
        if i in (173, 179, 187):
            kicker(t, before=8, after=4)
        else:
            m = re.match(r"^(\d+|—)\s{2}", t)
            lab = m.group(1) if m else ""
            row = table(doc, [10, 158], 1)
            cell_p(row.rows[0].cells[0], lab, 8.5, s5["deep"], FXB, lead=1.4)
            cpara(row.rows[0].cells[1], r, 8.2, INK, lead=1.45, after=3, drop=len(lab) + 2 if lab else 0)
    h2(189)
    rows = cells_of(blk(190))
    gl = table(doc, [26, 56, 4, 26, 56], len(rows), cell_margin=(1.6, 1.6, 1.6, 1.6))
    for r_i, (row, src) in enumerate(zip(gl.rows, blk(190)[1])):
        vals = [text_of(c_[0][0]) if c_[0] else "" for c_ in src]
        for c_i, v in zip((0, 1, 3, 4), (vals[0], vals[1], vals[3], vals[4])):
            c_ = row.cells[c_i]
            if v:
                cell_style(c_, borders={"bottom": (0.5, RULE)})
            cell_p(c_, v, 8.2, s5["deep"] if c_i in (0, 3) else INK, F, bold=c_i in (0, 3), lead=1.38)

    kit.page(top=28, header_shapes=[strip(5)])
    section_head(191, 192)
    photo_grid(193)
    spacer(2)
    callout(cells_of(blk(194)))

    # ---------------------------------------------------------------- back cover
    kit.page(folio=False, header_shapes=[lambda r: shape(r, 0, 0, 210, 297, fill=INK, behind=True, z=1)])
    a = P(doc, "")
    run = a.add_run()
    w5 = (168 - 4 * 1.2) / 5
    for i in range(5):
        shape(run, 21 + i * (w5 + 1.2), 150, w5, 6, fill=S[i + 1]["fill"], z=5)
    text_box(run, 21, 100, 168, 40, [T(text_of(blk(3)[2]), 26, WHITE, FXB, lead=1.2),
                                     T(text_of(blk(4)[2]), 12, mix(INK, 0.7), F, lead=1.4, before=6)])
    text_box(run, 21, 166, 168, 30, [T(text_of(blk(1)[2]), 8.5, WHITE, FSB, track=30, lead=1.5),
                                     T(text_of(blk(2)[2]), 8.5, mix(INK, 0.6), F, lead=1.5)])
    return kit.save(NAME + ".docx")


def render(docx):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(OUT), str(docx)], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return OUT / (docx.stem + ".pdf")


def find_pages(pdf):
    doc = pymupdf.open(pdf)
    texts = [" ".join(pg.get_text().split()).upper() for pg in doc]
    found = {}
    for i in range(9, 24):
        r = blk(i)[2]
        ttl = "".join(t for t, *_ in r[1:-1]).strip()
        key = " ".join(ttl.upper().split())
        for n, t in enumerate(texts[2:], 3):
            if key in t and "CONTENTS" not in texts[n - 1][:200]:
                found[ttl] = n
                break
    return found


if __name__ == "__main__":
    d = build({})
    pages = find_pages(render(d))
    d = build(pages)
    pdf = render(d)
    print("wrote", d, "and", pdf, "| contents pages:", pages)
