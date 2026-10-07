#!/usr/bin/env python3
"""Pick a report design family (A-G) for a brief, and say which layouts, colours and fonts to use.

usage:
  pick_design.py brief.json                      # markdown recommendation
  pick_design.py brief.json --json               # machine-readable result
  pick_design.py brief.json --tokens-out t.json  # also write a report-design compatible tokens.json
  pick_design.py --check-plan "COV TOC SUM ..."  [--brochure]
  pick_design.py --list                          # the seven families in one table
  pick_design.py --examples                      # regression: worked examples of selection-framework.md

The scoring, hard rules and rhythm checks implement references/selection-framework.md (sections 3-7).
Palettes come from assets/palettes.json; per-family build specs live in references/families/.
Pure Python 3, no dependencies.
"""
import colorsys
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
FAMILIES = "ABCDEFG"
TIEBREAK = "AGCEFDB"  # most to least robust in DOCX, used last

# formality, density tolerance, photo dependency, ink coverage, residual a11y risk, DOCX robustness, accent hue.
# Robustness of B and D raised from 1 to 2: full-page header shapes and rounded DrawingML panels render
# correctly in LibreOffice (references/docx-techniques.md); Word is untested, so they stay below A and G.
FAM = {
    "A": dict(form=5, dens=3, photo=2, ink=4, risk=1, robust=3, hue=223),
    "B": dict(form=2, dens=1, photo=5, ink=5, risk=4, robust=2, hue=178),
    "C": dict(form=3, dens=2, photo=3, ink=2, risk=2, robust=2, hue=112),
    "D": dict(form=2, dens=1, photo=4, ink=3, risk=3, robust=2, hue=168),
    "E": dict(form=3, dens=2, photo=4, ink=2, risk=3, robust=2, hue=184),
    "F": dict(form=3, dens=2, photo=5, ink=4, risk=2, robust=2, hue=221),
    "G": dict(form=4, dens=3, photo=3, ink=2, risk=2, robust=3, hue=177),
}

INFO = {
    "A": dict(name="Navy Annual", board="Rapport annuel 2025", palette="navy", spec="A-navy-annual.md",
              heading="Figtree", body="Figtree", alt_body="Inter",
              motif="full-navy cover and 1/3 navy split panels, bold caps titles, KPI row with navy icon discs, one-hue data",
              corners="square", photos="natural colour", mood="calm, institutional, trustworthy"),
    "B": dict(name="Forest Breakslide", board="Breakslide", palette="forest", spec="B-forest-breakslide.md",
              heading="Montserrat", body="Inter", alt_body=None,
              motif="dark green cover/break pages, stepped vertical slabs, three-dot marker, cut-corner photos",
              corners="cut (one 45 degree chamfer)", photos="green-graded colour", mood="premium, calm, eco-modern"),
    "C": dict(name="Leaf & Black", board="Business Plan Presentation", palette="green", spec="C-green-business-plan.md",
              heading="Roboto", body="Roboto", alt_body="Inter",
              motif="45 degree diamond photo crops bleeding off the edge, giant green numerals, green/black alternation",
              corners="cut / diagonal", photos="black and white", mood="confident, numbers-forward, start-up"),
    "D": dict(name="Prism Rounded", board="Prism", palette="teal", palette_variant="D", spec="D-teal-prism.md",
              heading="IBM Plex Sans", body="IBM Plex Sans", alt_body=None,
              motif="rounded slabs and pills holding text, caps titles with a raised teal dot, full-colour break pages",
              corners="rounded", photos="natural colour, rounded crops", mood="friendly, modern, approachable"),
    "E": dict(name="Clinicare Aqua", board="Clinicare", palette="aqua", spec="E-aqua-clinicare.md",
              heading="Nunito Sans", body="Nunito Sans", alt_body="Inter",
              motif="pale aqua tint panels, circle photos with a white ring across a white/aqua edge, offset aqua blocks",
              corners="round (circles only)", photos="natural colour, circle crops", mood="calm, clinical, reassuring"),
    "F": dict(name="Docoro Royal Block", board="Docoro", palette="royal", spec="F-royal-docoro.md",
              heading="Poppins", body="Inter", alt_body=None,
              motif="hard royal-blue blocks bleeding off the edge that photos and stat cards straddle, big numerals",
              corners="square", photos="natural colour", mood="bold, confident, service-led"),
    "G": dict(name="Market Frame", board="Market", palette="teal", spec="G-teal-market.md",
              heading="Montserrat", body="Inter", alt_body=None,
              motif="hairline frame 10 mm in, hanging tag, rotated pill tab, teal panels crossing the frame",
              corners="square + pill tabs", photos="natural colour", mood="composed, clean, corporate"),
}

# Layout ID -> recipe heading in each family spec (section 5). Missing IDs: use the closest recipe,
# re-skinned with the family's tokens (selection-framework.md section 8).
RECIPES = {
    "A": dict(COV="5.1", END="5.2 / 5.11", TOC="5.3", OPN="5.4", BRK="5.4", SUM="5.5", KPI="5.5", TXT="5.6", TX2="5.6",
              CHT="5.7", DNT="5.7", MAP="5.7", TAB="5.8", APX="5.8", ORG="5.9", STP="5.10", TML="5.10", FWD="5.12", QTE="5.12"),
    "B": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              TEAM="R8", CMP="R9", REC="R9", STP="R9", END="R10", APX="R11"),
    "C": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              APX="R7", MTX="R8", TML="R9", STP="R9", TEAM="R10", END="R11", CMP="R12"),
    "D": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              TML="R8", CMP="R9", REC="R9", STP="R9", CAS="R10", PHS="R10", TEAM="R11", END="R12", APX="R13"),
    "E": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              TEAM="R8", CMP="R9", STP="R9", REC="R9", END="R10", APX="R11"),
    "F": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              CMP="R7", QTE="R8", TEAM="R9", END="R10", REC="R11", APX="R12"),
    "G": dict(COV="R1", TOC="R2", OPN="R3", BRK="R3", SUM="R4", KPI="R4", TXT="R5", TX2="R5", CHT="R6", TAB="R7",
              APX="R7", CMP="R8", TEAM="R9", QTE="R10", END="R11"),
}

LAYOUT_NAMES = dict(
    COV="Cover", TOC="Contents", FWD="Foreword / letter", SUM="Executive summary", OPN="Section opener",
    BRK="Break page (one sentence)", KPI="Highlights (big numbers)", CHT="Chart page", DNT="Part-to-whole (donut)",
    MAP="Geography (map + stats)", TXT="Reading page", TX2="Two-column reading", PHS="Photo split", TAB="Table page",
    STP="Steps / process", ORG="Org chart", TML="Timeline", TEAM="Team", QTE="Quote / testimonials",
    MTX="2x2 matrix / SWOT", CMP="Comparison columns", REC="Recommendations", CAS="Case study",
    APX="Appendix / references", END="Closing / back cover")

#                   A  B  C  D  E  F  G
DOCTYPE = {
    "annual_report":   [3, 1, 1, 1, 1, 1, 2],
    "esg_report":      [3, 2, 1, 1, 1, 0, 2],
    "consulting":      [2, 0, 2, 1, 0, 1, 3],
    "business_plan":   [1, 1, 3, 2, 0, 1, 2],
    "investor_update": [2, 0, 3, 1, 0, 1, 2],
    "clinical_report": [2, 0, 0, 0, 3, 2, 1],
    "patient_info":    [1, 0, 0, 1, 3, 2, 1],
    "health_brochure": [0, 0, 0, 1, 2, 3, 1],
    "white_paper":     [2, 0, 1, 1, 1, 0, 3],
    "ops_review":      [2, 0, 3, 1, 1, 1, 2],
    "grant_public":    [3, 0, 1, 0, 1, 1, 2],
    "proposal":        [2, 1, 2, 1, 0, 1, 3],
    "marketing":       [0, 3, 2, 3, 1, 2, 2],
    "company_profile": [2, 2, 2, 2, 1, 2, 3],
    "portfolio":       [0, 3, 1, 3, 0, 2, 1],
}
INDUSTRY = {
    "finance":      [3, 0, 1, 0, 0, 2, 2],
    "healthcare":   [1, 0, 0, 1, 3, 3, 1],
    "tech":         [1, 1, 3, 3, 1, 2, 2],
    "environment":  [2, 3, 2, 2, 1, 0, 2],
    "industrial":   [2, 1, 2, 1, 0, 1, 3],
    "public":       [3, 0, 1, 2, 2, 1, 2],
    "creative":     [0, 3, 1, 3, 1, 2, 1],
    "professional": [2, 0, 2, 1, 0, 1, 3],
    "general":      [2, 1, 2, 2, 1, 1, 2],
}
AUDIENCE_FORMALITY = {"regulator": 5, "board": 5, "shareholders": 5, "investors": 4, "clients": 4, "management": 3,
                      "staff": 3, "public": 3, "patients": 3, "customers": 2, "creative": 2}

# selection-framework.md 3.3: first matching keyword set wins
DOCTYPE_KEYWORDS = [
    ("annual_report", ["annual report", "rapport annuel", "year in review"]),
    ("esg_report", ["sustainability", "esg", "csr", "rse", "impact report", "gri"]),
    ("business_plan", ["business plan", "pitch", "funding"]),
    ("investor_update", ["investor update", "quarterly update", "shareholder letter"]),
    ("clinical_report", ["quality account", "patient safety", "clinical audit", "outcomes", "quality report"]),
    ("patient_info", ["patient information", "leaflet", "your procedure"]),
    ("health_brochure", ["clinic", "our doctors"]),
    ("white_paper", ["white paper", "whitepaper", "research", "study", "insight"]),
    ("ops_review", ["operations review", "monthly review", "performance review"]),
    ("grant_public", ["grant", "evaluation", "programme report", "program report", "public consultation"]),
    ("proposal", ["proposal", "tender", "rfp", "bid"]),
    ("marketing", ["brochure", "product", "catalogue", "catalog"]),
    ("company_profile", ["company profile", "capabilities", "capability statement", "about us"]),
    ("portfolio", ["portfolio", "showcase"]),
]
# selection-framework.md 3.4
DOCTYPE_DEFAULTS = {
    "annual_report": dict(audience=["shareholders"], pages=24, photos="few"),
    "esg_report": dict(audience=["investors", "public"], industry="environment"),
    "consulting": dict(audience=["clients"], industry="professional", photos="none"),
    "business_plan": dict(audience=["investors"], industry="tech"),
    "investor_update": dict(audience=["investors"], pages=6, photos="none"),
    "clinical_report": dict(audience=["board"], industry="healthcare", output="office_print"),
    "patient_info": dict(audience=["patients"], industry="healthcare", a11y="strict"),
    "health_brochure": dict(audience=["customers"], industry="healthcare", photos="plenty"),
    "white_paper": dict(audience=["clients"], industry="professional", photos="none", text_share=0.7),
    "ops_review": dict(audience=["management"], output="office_print", photos="none"),
    "grant_public": dict(audience=["regulator", "public"], industry="public", output="office_print", a11y="strict"),
    "proposal": dict(audience=["clients"], industry="professional"),
    "marketing": dict(audience=["customers"], photos="plenty"),
    "company_profile": dict(audience=["clients"], photos="plenty"),
    "portfolio": dict(audience=["creative"], industry="creative", photos="plenty"),
}
BASE_DEFAULTS = dict(audience=["clients"], industry="general", pages=12, words_per_page=300, tables=0,
                     text_share=0.5, photos="none", output="screen", a11y="standard", editable=True)
DECISION_DOCS = {"consulting", "clinical_report", "ops_review", "white_paper", "grant_public", "proposal",
                 "esg_report", "annual_report", "investor_update", "business_plan"}


# ----------------------------------------------------------------------------- colour helpers
def _hex(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _to_hex(rgb):
    return "".join("%02X" % round(max(0, min(1, c)) * 255) for c in rgb)


def luminance(h):
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (f(c) for c in _hex(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b="FFFFFF"):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def hexinfo(h):
    hh, l, s = colorsys.rgb_to_hls(*_hex(h))
    return round(hh * 360), s, contrast(h)


def _with_lightness(h, light, sat=None):
    hh, _, s = colorsys.rgb_to_hls(*_hex(h))
    return _to_hex(colorsys.hls_to_rgb(hh, light, s if sat is None else sat))


def shade_to_contrast(h, target, darker=True):
    """Lightest HSL lightness (searching darker or lighter from h) whose contrast with white is still >= target."""
    _, l, _ = colorsys.rgb_to_hls(*_hex(h))
    lo, hi = (0.0, l) if darker else (l, 1.0)
    for _ in range(40):
        mid = (lo + hi) / 2
        if contrast(_with_lightness(h, mid)) >= target:
            lo = mid
        else:
            hi = mid
    return _with_lightness(h, lo)


def hue_dist(a, b):
    d = abs(a - b) % 360
    return min(d, 360 - d)


# ----------------------------------------------------------------------------- brief
def infer_doctype(text):
    t = (text or "").lower()
    for dt, words in DOCTYPE_KEYWORDS:
        if any(w in t for w in words):
            return dt
    return "consulting"


def normalise(brief):
    b = dict(brief)
    applied = []
    if not b.get("doctype"):
        b["doctype"] = infer_doctype(" ".join([b.get("title", ""), b.get("description", "")]))
        applied.append("doctype inferred as %s" % b["doctype"])
    if b["doctype"] not in DOCTYPE:
        raise SystemExit("unknown doctype %r; use one of: %s" % (b["doctype"], ", ".join(DOCTYPE)))
    for k, v in {**BASE_DEFAULTS, **DOCTYPE_DEFAULTS.get(b["doctype"], {})}.items():
        if k not in b or b[k] in (None, ""):
            b[k] = v
            applied.append("%s = %s (default)" % (k, v))
    if isinstance(b["audience"], str):
        b["audience"] = [b["audience"]]
    for a in b["audience"]:
        if a not in AUDIENCE_FORMALITY:
            raise SystemExit("unknown audience %r; use: %s" % (a, ", ".join(AUDIENCE_FORMALITY)))
    if b["industry"] not in INDUSTRY:
        raise SystemExit("unknown industry %r; use: %s" % (b["industry"], ", ".join(INDUSTRY)))
    if b.get("family"):
        b["family"] = b["family"].upper()
    return b, applied


# ----------------------------------------------------------------------------- scoring (selection-framework 4)
def score(B):
    excl, notes = {}, []
    if B.get("family"):
        notes.append("H0 you named family %s" % B["family"])
    if B["a11y"] == "strict":
        excl["B"] = "H1 strict accessibility"
    if B["output"] == "office_print":
        excl.setdefault("B", "H2 office printing of dark pages")
    if B["photos"] == "none":
        for f in "BF":
            excl.setdefault(f, "H3 photo-dependent and no photos")
    if B["pages"] > 40 or B["text_share"] > 0.6:
        for f in "BD":
            excl.setdefault(f, "H4 long or text-heavy")
    if B.get("brand_hex") and contrast(B["brand_hex"]) < 4.5:
        excl.setdefault("B", "H8 brand colour too light for a dark-mode family")
    W = dict(doctype=5, formality=3, density=3, photos=3, industry=2, output=2,
             a11y=3 if B["a11y"] == "strict" else 2, robust=3 if B["editable"] else 1, length=2, hue=1)
    req_form = max(AUDIENCE_FORMALITY[a] for a in B["audience"])
    req_form = min(5, max(1, req_form + {"conservative": 1, "expressive": -1}.get(B.get("tone"), 0)))
    need_dens = 1 if B["words_per_page"] < 250 else (2 if B["words_per_page"] <= 450 else 3)
    if B.get("tables", 0) >= 4:
        need_dens = 3
    rows = {}
    for i, f in enumerate(FAMILIES):
        p, s = FAM[f], {}
        s["doctype"] = DOCTYPE[B["doctype"]][i]
        s["formality"] = max(0, 3 - abs(p["form"] - req_form))
        gap = need_dens - p["dens"]
        s["density"] = 3 if gap <= 0 else (1 if gap == 1 else 0)
        dep = p["photo"]
        s["photos"] = max(0, {"plenty": 3, "few": 3 - max(0, dep - 3), "none": 3 - max(0, dep - 2)}[B["photos"]])
        s["industry"] = INDUSTRY[B["industry"]][i]
        s["output"] = max(0, {"screen": 3, "pro_print": 3 - max(0, p["ink"] - 3),
                              "office_print": 3 - max(0, p["ink"] - 2)}[B["output"]])
        s["a11y"] = max(0, 3 - max(0, p["risk"] - (1 if B["a11y"] == "strict" else 2)))
        s["robust"] = p["robust"]
        pg = B["pages"]
        s["length"] = 3 if pg <= 4 else (min(3, p["dens"] + 1) if pg <= 20 else p["dens"])
        if B.get("brand_hex") and hexinfo(B["brand_hex"])[1] < 0.15:
            s["hue"] = 3 if f == "C" else 1
        elif B.get("brand_hex"):
            d = hue_dist(hexinfo(B["brand_hex"])[0], p["hue"])
            s["hue"] = 3 if d <= 30 else 2 if d <= 60 else 1 if d <= 90 else 0
        else:
            s["hue"] = 0
        rows[f] = (sum(W[k] * s[k] for k in W), s)
    cand = [f for f in FAMILIES if f not in excl]
    key = lambda f: (-rows[f][0], -rows[f][1]["doctype"], FAM[f]["ink"], FAM[f]["photo"], TIEBREAK.index(f))
    ranked = sorted(cand, key=key)
    primary = None
    if B.get("family"):
        primary = B["family"]
        if primary in excl:
            notes.append("warning: rule %s would have excluded %s" % (excl[primary], primary))
    elif B.get("dark") and "B" in cand:
        primary = "B"; notes.append("H9 dark mode requested -> B")
    elif B["doctype"] == "annual_report" and "A" in cand:
        primary = "A"; notes.append("H5 annual report -> A")
    elif B["industry"] == "healthcare":
        hc = [f for f in ranked if f in "EF"]
        if hc:
            primary = hc[0]; notes.append("H6 healthcare -> best of E/F")
    primary = primary or ranked[0]
    rest = [f for f in ranked if f != primary]
    if B["industry"] == "healthcare" and primary not in "EF":
        hc = [f for f in rest if f in "EF"]
        rest = hc + [f for f in rest if f not in hc]
    return dict(primary=primary, alternate=rest[0] if rest else None, ranked=[(f, rows[f][0]) for f in ranked],
                excluded=excl, maxpts=3 * sum(W.values()), weights=W, detail={f: rows[f][1] for f in FAMILIES},
                req_form=req_form, need_dens=need_dens, notes=notes)


def variants(B, fam):
    v = []
    if B["photos"] == "none":
        v.append(("no_photo", "photo slots become accent blocks, motif panels, charts or KPI tiles; team pages use initials; never stock photos"))
    elif B["photos"] == "few":
        v.append(("few_photo", "photos only on cover, foreword and at most 1 page in 4; the rest uses the no-photo fallbacks"))
    if B["output"] == "office_print":
        v.append(("print_light", "full-colour pages <= 15%; openers become tint panel + deep-accent title; white back cover"))
    if B["a11y"] == "strict":
        v.append(("accessible", "accent_deep for all accent text; body 11 pt (12 pt patient-facing); no text on photos; rotated tab text repeated in body"))
    if fam in "CEF" and (B["words_per_page"] > 450 or B.get("tables", 0) >= 4):
        v.append(("dense", "tables full width on tint panels; two-column reading pages allowed; at most one KPI page per section"))
    if B.get("brand_hex"):
        v.append(("brand", "accent roles rebuilt from %s (structure, motif and neutrals unchanged)" % B["brand_hex"]))
    return v


# ----------------------------------------------------------------------------- tokens
def load_palettes():
    return json.loads((SKILL / "assets" / "palettes.json").read_text())


def tokens_for(fam, brand_hex=None):
    info = INFO[fam]
    pal = json.loads(json.dumps(load_palettes()[info["palette"]]))
    color, ramp = pal["color"], list(pal["chart_series"])
    if info.get("palette_variant") and pal.get("variants", {}).get(info["palette_variant"]):
        color["accent"] = color["accent_bright"] = pal["variants"][info["palette_variant"]]
    if brand_hex:  # selection-framework 4.6
        b = brand_hex.lstrip("#").upper()
        c = contrast(b)
        if c >= 7:
            deep, bright = b, shade_to_contrast(b, 3.2, darker=False)
        else:
            deep, bright = shade_to_contrast(b, 7.0), b
        hh, _, s = colorsys.rgb_to_hls(*_hex(b))
        color.update(accent_deep=deep, accent=bright if c < 4.5 else b, accent_bright=bright,
                     accent_tint=_to_hex(colorsys.hls_to_rgb(hh, 0.94, min(s, 0.45))),
                     on_accent="FFFFFF" if contrast(bright if c < 4.5 else b) >= 4.5 else color["ink"])
        d = _hex(deep)  # tints of the deep shade, mixed toward white (keeps the hue, avoids neon steps)
        ramp = [_to_hex([c + (1 - c) * t for c in d]) for t in (0.72, 0.54, 0.36, 0.18, 0)]
    return color, ramp


def engine_tokens(fam, color, ramp):
    """tokens.json for the report-design engine: text-safe accent, deep-first chart series, family fonts."""
    base = json.loads((SKILL.parent / "report-design" / "assets" / "tokens.json").read_text())
    info = INFO[fam]
    base["name"] = "%s (%s)" % (info["name"], fam)
    base["color"] = {"ink": color["ink"], "paper": color["paper"], "accent": color["accent_deep"],
                     "accent_tint": color["accent_tint"], "tint": color.get("tint", color["paper_alt"]),
                     "signal": color["signal"], "grey": color.get("grey", color["ink_soft"]),
                     "rule": color["rule"], "hairline": color["hairline"],
                     "accent_fill": color["accent"], "accent_bright": color["accent_bright"],
                     "on_accent": color["on_accent"]}
    base["chart_series"] = list(reversed(ramp))[:4]
    base["font"] = {"serif": info["heading"], "sans": info["body"], "fallback_serif": "Arial", "fallback_sans": "Arial"}
    return base


# ----------------------------------------------------------------------------- content -> layout (selection-framework 6.2)
def layout_for(it):
    t, n = it.get("type"), it.get("count", 0)
    if t == "figures":
        return ("KPI", "%d figures: KPI page in two rows" % n) if 5 <= n <= 8 else \
               ("TAB", "more than 8 figures: use a table") if n > 8 else ("KPI", "KPI strip (on SUM or a KPI page)")
    if t == "timeseries":
        s, pts = it.get("series", 1), it.get("points", 6)
        if s >= 4:
            return "TAB", "4+ series: small multiples or a table"
        return "CHT", ("column chart, latest bar in accent_deep" if pts <= 12 and s == 1 else "line chart")
    if t == "comparison":
        items, attrs = it.get("items", 2), it.get("attributes", 2)
        if it.get("precise") or (items >= 3 and attrs >= 3):
            return "TAB", "comparison with precise values or 3+ attributes: table"
        return "CMP", "comparison columns, recommended option in accent"
    if t == "parts":
        return ("DNT", "donut / 100% bar (parts must sum to 100%)") if n <= 5 else ("CHT", "ranked horizontal bars")
    if t == "ranked":
        return ("TAB", "long ranked list: table") if n > 15 else ("CHT", "sorted horizontal bar") if it.get("values", True) \
            else ("TXT", "numbered list with big numerals")
    if t == "steps":
        return ("STP", "row of numbered tiles, <= 25 words each") if n <= 5 else \
               ("TXT", "two-column numbered list") if n <= 8 else ("TAB", "more than 8 steps: table or split into phases")
    if t == "org":
        return ("ORG", "org chart") if it.get("levels", 2) <= 3 and it.get("children", 4) <= 6 else ("TAB", "table of units")
    if t == "quote":
        return ("QTE", "quote page") if it.get("words", 30) > 40 or it.get("portrait") or n >= 2 else \
               ("TXT", "pull quote in the margin of a reading page")
    if t == "text":
        w = it.get("words", 400)
        return ("TX2", "two-column reading") if w > 1500 and it.get("no_figures") else \
               ("TXT", "reading page") if w > 600 else ("TXT", "short text: share the page with the next item")
    if t == "table":
        cols, rows = it.get("columns", 5), it.get("rows", 10)
        if rows > 30 or it.get("reference"):
            return "APX", "reference data: appendix table"
        return "TAB", ("landscape table" if 8 <= cols <= 12 else "split into two tables" if cols > 12 else "portrait table")
    if t == "swot":
        return ("MTX", "SWOT matrix, big S W O T letters") if it.get("max_bullets", 4) <= 5 else ("TAB", "4-row table")
    if t == "timeline":
        return ("TML", "horizontal timeline" if n <= 6 else "vertical timeline") if n <= 12 else ("TAB", "table of events")
    if t == "team":
        return ("TEAM", "row" if n <= 4 else "grid") if n <= 12 else ("TAB", "table of names and roles")
    if t == "recommendations":
        return "REC", ("numbered cards with priority/owner/timing" if n <= 6 else "top 6 as cards + table for the rest")
    if t == "risks":
        return ("MTX", "likelihood x impact matrix") if n <= 10 else ("TAB", "risk table")
    if t == "case":
        return "CAS", "case study, one per page, <= 250 words"
    if t == "map":
        return ("MAP", "map + stat column") if it.get("image") else ("TAB", "table of locations + KPI strip")
    if t == "pricing":
        return "CMP", "pricing tiers, recommended tier in accent"
    if t == "photo":
        return "PHS", "photo split page"
    if t == "summary":
        return "SUM", "answer first, 3-5 points, KPI strip"
    if t == "foreword":
        return "FWD", "letter + portrait or pull quote"
    if t == "appendix":
        return "APX", "appendix / references"
    return "TXT", "unknown content type %r: treated as text" % t


def item_pages(it, lay):
    if lay in ("TXT", "TX2") and it.get("type") == "text":
        w = it.get("words", 400)
        return 0 if w <= 600 else max(1, math.ceil(w / (650 if lay == "TX2" else 450)))
    if lay in ("TAB", "APX") and it.get("type") == "table":
        return max(1, math.ceil(it.get("rows", 10) / 25))
    return 1


def build_plan(B):
    secs = B.get("sections") or []
    body, carry = [], []
    for si, s in enumerate(secs):
        pages = []
        for it in s.get("items", []):
            lay, why = layout_for(it)
            k = item_pages(it, lay)
            if k == 0:
                carry.append(it.get("title", "short text"))
                continue
            for j in range(k):
                pages.append((lay, "%s%s" % (it.get("title") or why, " (cont.)" if j else "")))
        if carry and not pages:
            pages.append(("TXT", "; ".join(carry)))
        carry = []
        body.append((s.get("title", "Section %d" % (si + 1)), pages))
    n_body = sum(len(p) for _, p in body)
    total = n_body + 2
    plan = []
    if total > 4:
        plan.append(("COV", B.get("title", "Cover")))
    if total + 1 >= 8 and B["doctype"] not in ("marketing", "health_brochure", "portfolio"):
        plan.append(("TOC", "Contents"))
    has_sum = any(l == "SUM" for _, ps in body for l, _ in ps)
    if B["doctype"] in DECISION_DOCS and not has_sum and n_body >= 3:
        plan.append(("SUM", "Executive summary (add it: decision documents answer first)"))
    openers = {i for i, (_, pages) in enumerate(body) if total >= 9 and len(pages) >= 3}
    print_light = B.get("output") == "office_print"
    while True:  # drop the opener of the shortest section until the colour budget (R3) holds
        n = len(plan) + n_body + len(openers) + 1
        colour = sum(1 for l, _ in plan if l == "COV") + (0 if print_light else len(openers) + 1)
        if not openers or colour / n <= (0.15 if print_light else 0.25):
            break
        openers.discard(min(openers, key=lambda i: (len(body[i][1]), -i)))
    for i, (title, pages) in enumerate(body):
        if i in openers:
            plan.append(("OPN", title))
        plan.extend(pages)
    plan.append(("END", "Closing / contact"))
    return plan


DENS = dict(COV="a", TOC="m", FWD="m", SUM="m", OPN="a", BRK="a", KPI="a", CHT="m", DNT="m", MAP="m", TXT="d", TX2="d",
            PHS="m", TAB="d", STP="a", ORG="m", TML="m", TEAM="a", QTE="a", MTX="m", CMP="m", REC="d", CAS="m", APX="d",
            END="a")
COLOUR = {"COV", "OPN", "BRK", "END"}


def check_rhythm(plan, brochure=False, print_light=False):
    errs, n = [], len(plan)
    for i in range(2, n):
        if plan[i] == plan[i - 1] == plan[i - 2] and plan[i] not in ("TXT", "TAB", "APX"):
            errs.append("R1 three %s pages in a row ending p%d" % (plan[i], i + 1))
        if i >= 3 and plan[i] == plan[i - 1] == plan[i - 2] == plan[i - 3]:
            errs.append("R1 four %s pages in a row ending p%d" % (plan[i], i + 1))
    run = 0
    for i, l in enumerate(plan):
        if l == "APX" and all(x in ("APX", "END") for x in plan[i:]):
            run = 0
            continue
        run = run + 1 if DENS.get(l) == "d" else 0
        if run > 3:
            errs.append("R2 more than 3 dense pages in a row ending p%d (insert a KPI, chart, quote or steps page)" % (i + 1))
    # print_light turns openers into tint pages and the back cover white, so only COV/BRK are solid colour
    c = sum(1 for l in plan if l in ({"COV", "BRK"} if print_light else COLOUR))
    limit = 0.15 if print_light else 0.25
    if n and c / n > limit:
        errs.append("R3 colour pages %d/%d exceed %d%%" % (c, n, limit * 100))
    idx = [i for i, l in enumerate(plan) if l in ("OPN", "BRK")]
    for a, b in zip(idx, idx[1:]):
        if b - a < 3:
            errs.append("R4 opener/break pages too close (p%d and p%d)" % (a + 1, b + 1))
    if plan.count("BRK") > n // 8:
        errs.append("R5 too many break pages")
    if n >= 8 and not brochure and "TOC" not in plan:
        errs.append("R6 contents page missing")
    for i, l in enumerate(plan):
        if l == "OPN" and (i + 2 >= n or plan[i + 1] in COLOUR or plan[i + 2] in COLOUR):
            errs.append("R7 opener on p%d is not followed by 2 content pages" % (i + 1))
    return errs or ["ok"]


# ----------------------------------------------------------------------------- output
def recommend(brief):
    B, applied = normalise(brief)
    plan = build_plan(B) if B.get("sections") else None
    if plan and "pages" not in brief:
        B["pages"] = len(plan)
        applied = [a for a in applied if not a.startswith("pages =")] + ["pages = %d (from the page plan)" % len(plan)]
    r = score(B)
    fam = r["primary"]
    color, ramp = tokens_for(fam, B.get("brand_hex"))
    var = variants(B, fam)
    out = dict(brief=B, defaults_applied=applied, primary=fam, alternate=r["alternate"], ranked=r["ranked"],
               excluded=r["excluded"], notes=r["notes"], maxpts=r["maxpts"], detail=r["detail"], weights=r["weights"],
               variants=var, family=INFO[fam], spec="references/families/" + INFO[fam]["spec"],
               tokens=dict(color=color, chart_series_light_to_deep=ramp), recipes=RECIPES[fam])
    if plan:
        ids = [l for l, _ in plan]
        out["plan"] = plan
        out["plan_check"] = check_rhythm(ids, brochure=B["doctype"] in ("marketing", "health_brochure"),
                                         print_light=any(v[0] == "print_light" for v in var))
    return out


def why_lines(r):
    p, a = r["primary"], r["alternate"]
    if not a:
        return []
    W, dp, da = r["weights"], r["detail"][p], r["detail"][a]
    diffs = sorted(((W[k] * (dp[k] - da[k]), k) for k in W), reverse=True)
    lines = ["beats %s on %s" % (a, ", ".join("%s (+%d)" % (k, d) for d, k in diffs if d > 0)[:200] or "the hard rules")]
    worse = [("%s (%d)" % (k, d)) for d, k in diffs if d < 0]
    if worse:
        lines.append("%s is stronger on %s" % (a, ", ".join(worse)))
    return lines


def to_markdown(r):
    p, a, f = r["primary"], r["alternate"], r["family"]
    pts = {f: sum(r["weights"][k] * r["detail"][f][k] for k in r["weights"]) for f in FAMILIES}
    L = ["# Design recommendation", "",
         "**Use %s %s** (%s board) - %s/%d points. Alternate: **%s %s** - %s points." % (
             p, f["name"], f["board"], pts.get(p, "-"), r["maxpts"], a, INFO[a]["name"] if a else "-", pts.get(a, "-")), ""]
    for n in r["notes"]:
        L.append("- Rule: %s" % n)
    for w in why_lines(r):
        L.append("- %s" % w)
    if r["excluded"]:
        L.append("- Excluded: " + "; ".join("%s (%s)" % kv for kv in r["excluded"].items()))
    if r["defaults_applied"]:
        L.append("- Defaults applied (say so in the delivery note): " + "; ".join(r["defaults_applied"]))
    L += ["", "## Ranking", "", "| Family | Name | Points |", "|---|---|---|"]
    L += ["| %s | %s | %s |" % (k, INFO[k]["name"], v) for k, v in r["ranked"]]
    L += ["", "## Design kit", "",
          "- Spec to follow: `%s` (sections 5-6 for layouts and components, 7 for photo fallbacks, 10 for DOCX build)" % r["spec"],
          "- Mood: %s" % f["mood"],
          "- Signature motif (use only this one): %s" % f["motif"],
          "- Corners: %s. Photo treatment: %s" % (f["corners"], f["photos"]),
          "- Type: headings **%s**, body **%s**%s (TTFs in `assets/fonts/`)" % (
              f["heading"], f["body"], " (alt body %s)" % f["alt_body"] if f.get("alt_body") else ""), ""]
    c = r["tokens"]["color"]
    L += ["| Role | Hex | On white | Use |", "|---|---|---|---|"]
    use = dict(ink="body text", ink_soft="captions, secondary text", accent_deep="ALL accent text, panels with small white text",
               accent="brand fills, slabs, panels", accent_bright="large fills, numerals >= 24 pt only if < 4.5:1",
               accent_tint="tint panels", paper_alt="grey bands", rule="rules", hairline="table rows",
               on_accent="text placed on accent fills", signal="negative values only")
    for k in ("ink", "ink_soft", "accent_deep", "accent", "accent_bright", "accent_tint", "paper_alt", "rule", "on_accent", "signal"):
        if k in c:
            L.append("| %s | #%s | %.2f:1 | %s |" % (k, c[k], contrast(c[k]), use.get(k, "")))
    L += ["", "Chart ramp (light to deep, highlight the series that carries the argument in the deepest step): " +
          " ".join("#" + x for x in r["tokens"]["chart_series_light_to_deep"]), ""]
    if r["variants"]:
        L += ["## Variants to apply", ""] + ["- **%s**: %s" % v for v in r["variants"]] + [""]
    if r.get("plan"):
        L += ["## Page plan", "", "| Page | Layout | Content | Recipe in spec |", "|---|---|---|---|"]
        for i, (lay, what) in enumerate(r["plan"], 1):
            L.append("| %d | %s %s | %s | %s |" % (i, lay, LAYOUT_NAMES[lay], what, r["recipes"].get(lay, "closest recipe, re-skinned")))
        L += ["", "Rhythm check: " + "; ".join(r["plan_check"]), ""]
    else:
        L += ["## Layout recipes", "", "| Layout | Recipe in spec |", "|---|---|"]
        L += ["| %s %s | %s |" % (k, LAYOUT_NAMES[k], v) for k, v in r["recipes"].items()]
        L += ["", "Add `sections` to the brief to get a page-by-page plan.", ""]
    return "\n".join(L)


def list_families():
    pal = load_palettes()
    L = ["| Family | Name | Mood | Accent | Type | Corners | Photo dependency | Best for |", "|---|---|---|---|---|---|---|---|"]
    best = dict(A="annual, ESG, grant/public, board reports", B="dark-mode portfolios, agency or eco profiles (screen only)",
                C="business plans, pitch documents, investor/ops updates", D="marketing, company profiles, portfolios",
                E="clinical, patient and public health reports", F="healthcare services brochures, KPI-led reviews",
                G="consulting, white papers, proposals, ops reviews")
    for k in FAMILIES:
        i = INFO[k]
        acc = pal[i["palette"]]["color"]["accent"] if not i.get("palette_variant") else pal["teal"]["variants"]["D"]
        L.append("| %s | %s | %s | #%s | %s / %s | %s | %d/5 | %s |" % (
            k, i["name"], i["mood"], acc, i["heading"], i["body"], i["corners"], FAM[k]["photo"], best[k]))
    return "\n".join(L)


EXAMPLES = {
    "annual report insurer": (dict(doctype="annual_report", audience=["shareholders", "board"], industry="finance",
        pages=32, words_per_page=380, tables=6, text_share=0.45, photos="few", output="pro_print", a11y="standard",
        editable=False, brand_hex="#00205B"), ("A", "G")),
    "hospital quality report": (dict(doctype="clinical_report", audience=["board", "regulator"], industry="healthcare",
        pages=20, words_per_page=420, tables=7, text_share=0.5, photos="few", output="office_print", a11y="strict",
        editable=True), ("E", "A")),
    "seed business plan": (dict(doctype="business_plan", audience=["investors"], industry="tech", pages=16,
        words_per_page=220, tables=2, text_share=0.4, photos="few", output="screen", a11y="standard", editable=False,
        brand_hex="#6C2BD9"), ("C", "G")),
    "consulting ops review": (dict(doctype="consulting", audience=["management", "clients"], industry="industrial",
        pages=42, words_per_page=520, tables=9, text_share=0.65, photos="none", output="office_print",
        a11y="standard", editable=True), ("G", "A")),
    "clinic services brochure": (dict(doctype="health_brochure", audience=["patients", "customers"],
        industry="healthcare", pages=8, words_per_page=180, tables=0, text_share=0.35, photos="plenty",
        output="pro_print", a11y="standard", editable=False), ("F", "E")),
    "ESG report": (dict(doctype="esg_report", audience=["investors", "public"], industry="environment", pages=28,
        words_per_page=400, tables=5, text_share=0.5, photos="plenty", output="screen", a11y="standard",
        editable=False, brand_hex="#2E7D32"), ("A", "G")),
    "agency portfolio": (dict(doctype="portfolio", audience=["creative"], industry="creative", pages=10,
        words_per_page=150, tables=0, text_share=0.3, photos="plenty", output="screen", a11y="standard",
        editable=False), ("D", "B")),
}


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    if argv[0] == "--list":
        print(list_families())
        return 0
    if argv[0] == "--check-plan":
        ids = argv[1].split()
        bad = [x for x in ids if x not in DENS]
        if bad:
            print("unknown layout IDs:", bad, "known:", " ".join(DENS))
            return 2
        print("\n".join(check_rhythm(ids, brochure="--brochure" in argv, print_light="--print-light" in argv)))
        return 0
    if argv[0] == "--examples":
        fails = 0
        for name, (b, want) in EXAMPLES.items():
            r = score(normalise(b)[0])
            got = (r["primary"], r["alternate"])
            fails += got != want
            print("%-26s -> %s alt %s %s | %s" % (name, got[0], got[1], "ok" if got == want else "EXPECTED %s alt %s" % want,
                                                  r["ranked"]))
        return 1 if fails else 0
    r = recommend(json.loads(Path(argv[0]).read_text()))
    if "--tokens-out" in argv:
        path = Path(argv[argv.index("--tokens-out") + 1])
        path.write_text(json.dumps(engine_tokens(r["primary"], r["tokens"]["color"], r["tokens"]["chart_series_light_to_deep"]), indent=2))
        print("wrote", path, file=sys.stderr)
    if "--json" in argv:
        print(json.dumps(r, indent=2, default=list))
    else:
        print(to_markdown(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
