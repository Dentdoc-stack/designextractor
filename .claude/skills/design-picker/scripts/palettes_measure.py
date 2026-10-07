#!/usr/bin/env python3
"""Colour measurement + palette derivation for reference boards ref-A … ref-G.

Usage (numpy + Pillow only):
    .venv/bin/python .claude/skills/design-picker/scripts/palettes_measure.py measure  > measurements.md   # phase 1
    .venv/bin/python .claude/skills/design-picker/scripts/palettes_measure.py derive                         # phase 2, writes .claude/skills/design-picker/assets/palettes.json

Phase 1 (measure)
  1. Segment each board into thumbnails (page content) and drop the Pinterest
     background: recursive XY-cut on a per-board "background-like" mask (A, B, C) or
     hand-fixed grids verified by overlay (D, E, F, G). Every box is inset 3-6 px to
     drop shadows / mock-up frames.
  2. "Flat" pixels = local 5x5 std (max over RGB) < 4. Flat pixels are graphic fills
     (slabs, panels, page ground); non-flat pixels are photos, text and edges.
  3. Flat chromatic pixels (CIELAB C* > 12) -> k-means (k=7, k-means++ seeded,
     Lab space) -> clusters within dE76 < 7 merged. Hex = per-channel median of members.
  4. Flat neutrals (C* < 5) binned by L*; modes reported as paper / page grey / mid grey.
  5. Ink: darkest 2 % of all near-neutral pixels inside the boxes (text cores).
     Small text is anti-aliased at this resolution -> tagged [uncertain].
Phase 2 (derive)
  Token sets in OKLCH: hue fixed to the measured accent, lightness moved, chroma
  clipped to the sRGB gamut by bisection (never mixed with black).
"""
import json, sys, os
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../.."))
IMG = os.path.join(ROOT, ".claude/skills/report-design/references/images/ref-%s.jpeg")
OUT_JSON = os.path.join(ROOT, ".claude/skills/design-picker/assets/palettes.json")

# ----------------------------------------------------------------------------- colour math
def srgb_to_lin(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)

def lin_to_srgb(l):
    l = np.clip(np.asarray(l, float), 0, 1)
    return np.where(l <= 0.0031308, 12.92 * l, 1.055 * l ** (1 / 2.4) - 0.055) * 255.0

M_XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
WHITE = np.array([0.95047, 1.0, 1.08883])

def rgb_to_lab(rgb):
    xyz = srgb_to_lin(rgb) @ M_XYZ.T / WHITE
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], -1)

def lin_to_oklab(lin):
    M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929],
                   [0.2119034982, 0.6806995451, 0.1073969566],
                   [0.0883024619, 0.2817188376, 0.6299787005]])
    M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468],
                   [1.9779984951, -2.4285922050, 0.4505937099],
                   [0.0259040371, 0.7827717662, -0.8086757660]])
    return np.cbrt(lin @ M1.T) @ M2.T

def oklab_to_lin(lab):
    M2i = np.array([[1.0, 0.3963377774, 0.2158037573],
                    [1.0, -0.1055613458, -0.0638541728],
                    [1.0, -0.0894841775, -1.2914855480]])
    M1i = np.array([[4.0767416621, -3.3077115913, 0.2309699292],
                    [-1.2684380046, 2.6097574011, -0.3413193965],
                    [-0.0041960863, -0.7034186147, 1.7076147010]])
    return ((np.asarray(lab) @ M2i.T) ** 3) @ M1i.T

def hex2rgb(h):
    h = h.lstrip("#"); return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], float)

def rgb2hex(rgb):
    return "".join("%02X" % int(round(min(255, max(0, v)))) for v in rgb)

def oklch(h):
    L, a, b = lin_to_oklab(srgb_to_lin(hex2rgb(h)))
    return L, float(np.hypot(a, b)), float(np.degrees(np.arctan2(b, a)) % 360)

def in_gamut(L, C, H, eps=1e-6):
    lin = oklab_to_lin([L, C * np.cos(np.radians(H)), C * np.sin(np.radians(H))])
    return np.all(lin >= -eps) and np.all(lin <= 1 + eps)

def oklch_hex(L, C, H):
    """OKLCH -> hex, chroma reduced by bisection until in sRGB gamut (hue/lightness kept)."""
    if not in_gamut(L, C, H):
        lo, hi = 0.0, C
        for _ in range(40):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if in_gamut(L, mid, H) else (lo, mid)
        C = lo
    lin = oklab_to_lin([L, C * np.cos(np.radians(H)), C * np.sin(np.radians(H))])
    return rgb2hex(lin_to_srgb(lin))

def rel_lum(h):
    return float(srgb_to_lin(hex2rgb(h)) @ np.array([0.2126, 0.7152, 0.0722]))

def contrast(h1, h2):
    a, b = sorted([rel_lum(h1), rel_lum(h2)], reverse=True)
    return (a + 0.05) / (b + 0.05)

def de2000(h1, h2):
    L1, a1, b1 = rgb_to_lab(hex2rgb(h1)); L2, a2, b2 = rgb_to_lab(hex2rgb(h2))
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2); Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360; h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    if C1p * C2p == 0: dh = 0
    elif dh > 180: dh -= 360
    elif dh < -180: dh += 360
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    if C1p * C2p == 0: hbp = h1p + h2p
    elif abs(h1p - h2p) <= 180: hbp = (h1p + h2p) / 2
    elif h1p + h2p < 360: hbp = (h1p + h2p + 360) / 2
    else: hbp = (h1p + h2p - 360) / 2
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dtheta = 30 * np.exp(-((hbp - 275) / 25) ** 2)
    Rc = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp; Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dtheta)) * Rc
    return float(np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh)))

# Machado et al. 2009, severity 1.0, applied in linear RGB
CVD = {"deutan": np.array([[0.367322, 0.860646, -0.227968], [0.280085, 0.672501, 0.047413], [-0.011820, 0.042940, 0.968881]]),
       "protan": np.array([[0.152286, 1.052583, -0.204868], [0.114503, 0.786281, 0.099216], [-0.003882, -0.048116, 1.051998]])}

def simulate(h, kind):
    return rgb2hex(lin_to_srgb(CVD[kind] @ srgb_to_lin(hex2rgb(h))))

def naive_cmyk(h):
    """Device-naive RGB->CMYK (full GCR). Real ICC conversions (e.g. FOGRA39) put more C/M/Y
    under dark colours, so total ink is a LOWER bound here."""
    r, g, b = hex2rgb(h) / 255
    k = 1 - max(r, g, b)
    if k >= 1: return (0, 0, 0, 100)
    c, m, y = [(1 - v - k) / (1 - k) for v in (r, g, b)]
    return tuple(round(100 * v) for v in (c, m, y, k))

# ----------------------------------------------------------------------------- segmentation
def bglike(L, a):
    mx, mn = a.max(2), a.min(2); ch = mx - mn; lum = a.mean(2)
    if L == "A": return (ch < 10) & (lum < 228) & (lum > 120)
    if L == "B": return (np.abs(a - np.array([2, 63, 58])).max(2) < 22) | ((lum < 45) & (a[..., 1] > a[..., 0]))
    if L == "C": return (ch < 8) & (lum < 226) & (lum > 120)

def _runs(g):
    r, i, n = [], 0, len(g)
    while i < n:
        if g[i]:
            j = i
            while j < n and g[j]: j += 1
            r.append((i, j)); i = j
        else: i += 1
    return r

def xycut(m, x0, y0, x1, y1, out, minrun=3, thr=0.96, minsize=40):
    sub = m[y0:y1, x0:x1]
    for axis in (0, 1):
        g = sub.mean(1 if axis == 0 else 0) >= thr; n = len(g); runs = _runs(g)
        lo = runs[0][1] if runs and runs[0][0] == 0 else 0
        hi = runs[-1][0] if runs and runs[-1][1] == n else n
        inner = [r for r in runs if r[0] != 0 and r[1] != n and r[1] - r[0] >= minrun]
        if lo > 0 or hi < n or inner:
            cuts = [lo] + [c for r in inner for c in r] + [hi]
            for k in range(0, len(cuts), 2):
                p0, p1 = cuts[k], cuts[k + 1]
                if p1 - p0 < minsize: continue
                if axis == 0: xycut(m, x0, y0 + p0, x1, y0 + p1, out, minrun, thr, minsize)
                else: xycut(m, x0 + p0, y0, x0 + p1, y1, out, minrun, thr, minsize)
            return out
    out.append((x0, y0, x1, y1)); return out

def _grid(cols, rows):
    return [(x0, y0, x1, y1) for (y0, y1) in rows for (x0, x1) in cols]

def thumb_boxes(L, a):
    if L in "ABC":
        bx = xycut(bglike(L, a), 0, 0, a.shape[1], a.shape[0], [])
        bx = [b for b in bx if (b[2] - b[0]) * (b[3] - b[1]) > 2500]
    elif L == "D":
        bx = _grid([(8, 224), (232, 449), (456, 672)], [(int(20 + 128.9 * k), int(20 + 128.9 * k) + 122) for k in range(9)])
    elif L == "E":
        bx = [(18, 18, 305, 186), (321, 18, 457, 97), (321, 108, 457, 186)] + _grid(
            [(18, 154), (167, 305), (321, 457)],
            [(202, 279), (294, 370), (386, 462), (476, 554), (568, 648), (662, 739), (754, 830)])
    elif L == "F":
        bx = _grid([(28, 237), (243, 450), (453, 665)],
                   [(21, 140), (144, 266), (270, 388), (396, 515), (520, 640), (645, 764), (769, 888), (891, 1012), (1019, 1140), (1144, 1263)])
    elif L == "G":
        bx = _grid([(49, 357), (376, 687)], [(66, 238), (257, 431), (449, 624), (640, 813), (833, 1005), (1023, 1200)])
    i = {"A": 3, "B": 3, "C": 3, "D": 4, "E": 3, "F": 6, "G": 4}[L]
    return [(x0 + i, y0 + i, x1 - i, y1 - i) for x0, y0, x1, y1 in bx]

def local_std(a, r=2):
    a = a.astype(float); k = 2 * r + 1; H, W = a.shape[:2]; out = []
    for c in range(3):
        p = np.pad(a[..., c], r, mode="edge")
        res = []
        for q in (p, p * p):
            cs = np.pad(q.cumsum(0).cumsum(1), ((1, 0), (1, 0)))
            res.append(cs[k:k + H, k:k + W] - cs[0:H, k:k + W] - cs[k:k + H, 0:W] + cs[0:H, 0:W])
        out.append(np.sqrt(np.maximum(res[1] / k / k - (res[0] / k / k) ** 2, 0)))
    return np.max(out, 0)

def kmeans(X, k, seed=0, iters=40):
    rng = np.random.default_rng(seed)
    C = [X[rng.integers(len(X))]]
    for _ in range(k - 1):
        d = np.min(((X[:, None, :] - np.array(C)[None]) ** 2).sum(-1), 1)
        C.append(X[rng.choice(len(X), p=d / d.sum())])
    C = np.array(C)
    for _ in range(iters):
        lab = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), 1)
        newC = np.array([X[lab == j].mean(0) if (lab == j).any() else C[j] for j in range(k)])
        if np.allclose(newC, C): break
        C = newC
    return C, lab

def measure(L):
    a = np.asarray(Image.open(IMG % L).convert("RGB"))
    m = np.zeros(a.shape[:2], bool)
    boxes = thumb_boxes(L, a)
    for x0, y0, x1, y1 in boxes: m[y0:y1, x0:x1] = True
    flat = local_std(a) < 4
    rgb = a[m].astype(float); lab = rgb_to_lab(rgb); fl = flat[m]
    chroma = np.hypot(lab[:, 1], lab[:, 2]); N = len(rgb)
    res = {"board": L, "thumbnails": len(boxes), "pixels": int(N), "flat_share": float(fl.mean())}
    # chromatic flat clusters
    sel = fl & (chroma > 12)
    X = lab[sel]; R = rgb[sel]
    sub = np.random.default_rng(1).choice(len(X), min(len(X), 20000), replace=False)
    C, _ = kmeans(X[sub], 7)
    labs = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), 1)
    groups = [[j] for j in range(len(C))]
    merged = True
    while merged:  # merge clusters closer than dE76 7
        merged = False
        cents = [X[np.isin(labs, g)].mean(0) for g in groups]
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if np.linalg.norm(cents[i] - cents[j]) < 7:
                    groups[i] += groups.pop(j); merged = True; break
            if merged: break
    cl = []
    for g in groups:
        mm = np.isin(labs, g)
        if mm.sum() == 0: continue
        hx = rgb2hex(np.median(R[mm], 0))
        Lk, Ck, Hk = oklch(hx)
        cl.append({"hex": hx, "share_all": float(mm.sum() / N), "share_chromatic": float(mm.mean()),
                   "oklch": [round(Lk, 3), round(Ck, 3), round(Hk, 1)]})
    res["chromatic_flat_share"] = float(sel.mean())
    res["clusters"] = sorted(cl, key=lambda c: -c["share_all"])
    # neutrals
    neu = fl & (chroma < 5)
    Ln = lab[neu, 0]; Rn = rgb[neu]
    bands = {"paper (L*>=97.5)": (97.5, 101), "page grey (L* 90-97.5)": (90, 97.5),
             "light grey (L* 75-90)": (75, 90), "mid grey (L* 40-75)": (40, 75), "dark (L*<40)": (-1, 40)}
    nb = {}
    for name, (lo, hi) in bands.items():
        mm = (Ln >= lo) & (Ln < hi)
        if mm.sum() < 50: nb[name] = None; continue
        q = (Rn[mm] // 2 * 2).astype(int)  # mode of 2-level quantised colours
        keys, cnt = np.unique(q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2], return_counts=True)
        top = keys[np.argmax(cnt)]
        mode = np.array([top // 65536, top // 256 % 256, top % 256]) + 1
        nb[name] = {"mode_hex": rgb2hex(mode), "median_hex": rgb2hex(np.median(Rn[mm], 0)), "share_all": float(mm.sum() / N)}
    res["neutrals"] = nb
    # light accent tints: flat, L*>88, 3<=C*<=20, Lab hue within 25 deg of the main cluster
    main = rgb_to_lab(hex2rgb(res["clusters"][0]["hex"]))
    hmain = np.degrees(np.arctan2(main[2], main[1]))
    hue = np.degrees(np.arctan2(lab[:, 2], lab[:, 1]))
    dh = np.abs((hue - hmain + 180) % 360 - 180)
    tm = fl & (lab[:, 0] > 88) & (chroma >= 3) & (chroma <= 20) & (dh < 25)
    res["tint"] = ({"hex": rgb2hex(np.median(rgb[tm], 0)), "share_all": float(tm.mean())}
                   if tm.sum() > 200 else None)
    res["neutral_flat_share"] = float(neu.mean())
    # ink: darkest 2 % of near-neutral pixels (any flatness)
    nn = chroma < 8
    Lall = lab[nn, 0]; thr = np.percentile(Lall, 2)
    res["ink_estimate"] = {"hex": rgb2hex(np.median(rgb[nn][Lall <= thr], 0)), "L*_p2": float(thr)}
    res["photo_text_share"] = float(1 - fl.mean())
    return res

# ----------------------------------------------------------------------------- derivation
# Canonical measured colours, picked from phase-1 output (see palettes.md section 2).
# Every hex below is a measured cluster median unless marked "derived".
FAMILIES = {
    "navy": {"refs": ["A"], "accent": "1C2E60",       # A cover/panel fill (k-means cluster 172A5C; flat cover sample 1C2E60)
             "bright": "5398BA",                       # A "2025" numerals on navy cover
             "page_grey": "F2F3F4",                    # A ground measured E6E5E6 is mock-up lighting; DESIGN-user value used
             "ramp_seen": ["778FB4", "4A6E9F", "2A447E", "1B2E5A"]},  # A bar chart, light->deep
    "royal": {"refs": ["F"], "accent": "0339A6", "page_grey": "F2F2F2"},
    "teal": {"refs": ["G", "D"], "accent": "01A19A",   # G fill; D 379A86 is dE2000 5.9 away -> same family
             "mid_seen": "018780", "variants": {"D": "379A86"}, "page_grey": "EEEEEE"},
    "forest": {"refs": ["B"], "accent": "005A58",      # B dark-mode ground / slabs
               "bright": "118A6B",                     # B secondary green bars (gradient towards 22B380)
               "page_grey": "F2F3F4", "dark_ground": "005A58"},
    "aqua": {"refs": ["E"], "accent": "4CC0CB", "tint": "E0FEFE", "page_grey": "EDEFEF"},
    "green": {"refs": ["C"], "accent": "57B848", "page_grey": "F5F5F5", "ink": "141414"},
}
NEUTRALS = {"ink": "1F1F1F", "ink_soft": "5C5C5C", "rule": "BFBFBF", "hairline": "D9D9D9"}
MIN_INK_NEUTRAL = 6.0   # % — a page band lighter than this risks vanishing on office lasers
MIN_INK_TINT = 7.0      # % on the strongest channel for chromatic panel tints

def max_ink(h): return max(naive_cmyk(h))

def darken_until(h, pct):
    L, C, H = oklch(h)
    while max_ink(h) < pct and L > 0.5:
        L -= 0.002; h = oklch_hex(L, C, H)
    return h

def find_L(H, C, target, against_list, lo=0.05, hi=0.99):
    """Highest OKLCH lightness (hue fixed, chroma gamut-clipped) reaching `target` vs every colour in against_list."""
    for L in np.arange(hi, lo, -0.0025):
        hx = oklch_hex(L, C, H)
        if all(contrast(hx, a) >= target for a in against_list): return float(L), hx
    raise ValueError

def pick_signal(refs_hex, backgrounds):
    best = None
    for H in list(range(345, 360)) + list(range(0, 61)):
        L, hx = find_L(H, 0.20, 4.5, backgrounds)
        score = min(min(de2000(hx, r), de2000(simulate(hx, "deutan"), simulate(r, "deutan")),
                        de2000(simulate(hx, "protan"), simulate(r, "protan"))) for r in refs_hex)
        score -= 0.3 * abs(((H - 30 + 180) % 360) - 180)    # preference for a true red-orange (OKLCH h 30)
        if best is None or score > best[0]: best = (score, hx, H)
    return best[1]

def ramp_for(accent, deep, H, L_light=0.87):
    """5 single-hue OKLCH steps light->deep. The brand accent is pinned to the interior step
    (1..3) that maximises the smallest adjacent dE2000; lightness is linear on each side of it."""
    La, Ca, _ = oklch(accent); Ld, Cd, _ = oklch(deep)
    Cs = np.interp(range(5), [0, 2, 4], [0.55 * Ca, Ca, max(Cd, 0.6 * Ca)])
    cands = []
    for k in (1, 2, 3):
        if not (L_light > La > Ld): break
        Ls = np.empty(5)
        Ls[:k + 1] = np.linspace(L_light, La, k + 1); Ls[k:] = np.linspace(La, Ld, 5 - k)
        out = [oklch_hex(l, c, H) for l, c in zip(Ls, Cs)]
        out[k] = accent; out[-1] = deep
        cands.append(out)
    if not cands:   # accent is the darkest step (navy, royal, forest)
        out = [oklch_hex(l, c, H) for l, c in zip(np.linspace(L_light, Ld, 5), Cs)]
        out[-1] = deep
        cands.append(out)
    return max(cands, key=lambda o: min(de2000(o[i], o[i + 1]) for i in range(4)))

def derive(fid, fam):
    ink = fam.get("ink", NEUTRALS["ink"])
    paper = "FFFFFF"
    paper_alt = darken_until(fam["page_grey"], MIN_INK_NEUTRAL)
    acc = fam["accent"]; La, Ca, Ha = oklch(acc)
    if contrast(acc, paper_alt) >= 7: deep = acc
    else: _, deep = find_L(Ha, Ca, 7.0, [paper, paper_alt])
    bright = fam.get("bright", acc)
    tint = fam.get("tint") or oklch_hex(0.955, min(0.04, 0.35 * Ca), Ha)
    tint = darken_until(tint, MIN_INK_TINT)
    w = contrast("FFFFFF", acc)
    on_acc = "FFFFFF" if w >= 3.0 else ink
    sig = pick_signal([acc, deep, bright], [paper, paper_alt, tint])
    color = {"ink": ink, "ink_soft": NEUTRALS["ink_soft"], "paper": paper, "paper_alt": paper_alt,
             "rule": NEUTRALS["rule"], "hairline": NEUTRALS["hairline"],
             "accent_deep": deep, "accent": acc, "accent_bright": bright, "accent_tint": tint,
             "on_accent": on_acc, "signal": sig,
             "tint": paper_alt, "grey": NEUTRALS["ink_soft"]}   # legacy keys read by scripts/reportkit.py
    if "dark_ground" in fam: color["dark_ground"] = fam["dark_ground"]
    ramp = ramp_for(acc, deep, Ha)
    return color, ramp

def flags(c):
    return "AAA" if c >= 7 else "AA" if c >= 4.5 else "large/graphics" if c >= 3 else "FAIL"

def tables(meas):
    out = []
    for L, r in meas.items():
        pg = (r["neutrals"].get("page grey (L* 90-97.5)") or {}).get("median_hex", "F2F3F4")
        out.append(f"\n#### ref-{L} — {r['thumbnails']} thumbnails, {r['pixels']:,} px; flat {r['flat_share']:.0%}, "
                   f"photo/text/edges {r['photo_text_share']:.0%}; page grey used for contrast: #{pg}\n")
        out.append("| role | hex | area % (all) | % of chromatic flat | OKLCH L C h | on white (= white text on it) | on page grey | ink 1F1F1F on it | naive C/M/Y/K % |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        rows = []
        for c in r["clusters"]:
            if c["share_chromatic"] < 0.02 and c["share_all"] < 0.005: continue
            rows.append(("chromatic cluster", c["hex"], c["share_all"], c["share_chromatic"], c["oklch"]))
        if r["tint"]: rows.append(("accent tint", r["tint"]["hex"], r["tint"]["share_all"], None, None))
        for k, v in r["neutrals"].items():
            if v and v["share_all"] >= 0.001: rows.append(("neutral " + k, v["median_hex"], v["share_all"], None, None))
        rows.append(("ink estimate [uncertain]", r["ink_estimate"]["hex"], None, None, None))
        for role, hx, sa, sc, ok in rows:
            ok = ok or [round(v, 3) for v in oklch(hx)]
            cw, cg, wo = contrast(hx, "FFFFFF"), contrast(hx, pg), contrast("1F1F1F", hx)
            out.append(f"| {role} | `{hx}` | {'' if sa is None else f'{100*sa:.1f}'} | {'' if sc is None else f'{100*sc:.0f}'} | "
                       f"{ok[0]:.3f} {ok[1]:.3f} {ok[2]:.0f} | {cw:.2f} {flags(cw)} | {cg:.2f} {flags(cg)} | {wo:.2f} {flags(wo)} | "
                       f"{'/'.join(map(str, naive_cmyk(hx)))} |")
    return "\n".join(out)

def derived_tables(pal):
    out = []
    for fid, p in pal.items():
        c = p["color"]
        out.append(f"\n#### {fid} (refs {', '.join(p['source_refs'])})\n")
        out.append("| token | hex | on white | on paper_alt | on accent_tint | ink on it | naive C/M/Y/K % (TAC) | dE2000 vs white |")
        out.append("|---|---|---|---|---|---|---|---|")
        for k in ["ink", "ink_soft", "paper", "paper_alt", "rule", "hairline", "accent_deep", "accent", "accent_bright",
                  "accent_tint", "on_accent", "signal", "dark_ground"]:
            if k not in c: continue
            hx = c[k]
            out.append(f"| {k} | `{hx}` | {contrast(hx,'FFFFFF'):.2f} | {contrast(hx,c['paper_alt']):.2f} | "
                       f"{contrast(hx,c['accent_tint']):.2f} | {contrast(c['ink'],hx):.2f} | {'/'.join(map(str, naive_cmyk(hx)))} ({sum(naive_cmyk(hx))}) | {de2000(hx,'FFFFFF'):.1f} |")
        r = p["chart_series"]
        steps = " → ".join(f"`{h}`" for h in r)
        des = ", ".join(f"{de2000(r[i], r[i+1]):.1f}" for i in range(4))
        dsim = ", ".join(f"{de2000(simulate(r[i],'deutan'), simulate(r[i+1],'deutan')):.1f}" for i in range(4))
        cw = ", ".join(f"{contrast(h,'FFFFFF'):.2f}" for h in r)
        out.append(f"\nchart ramp light→deep: {steps}  \nadjacent ΔE2000: {des} (deuteranope-simulated: {dsim})  \n"
                   f"contrast of each step on white: {cw}  \n"
                   f"signal vs accent ΔE2000 normal/deutan/protan: {de2000(c['signal'],c['accent']):.1f} / "
                   f"{de2000(simulate(c['signal'],'deutan'),simulate(c['accent'],'deutan')):.1f} / "
                   f"{de2000(simulate(c['signal'],'protan'),simulate(c['accent'],'protan')):.1f}; "
                   f"signal vs accent_deep: {de2000(c['signal'],c['accent_deep']):.1f} / "
                   f"{de2000(simulate(c['signal'],'deutan'),simulate(c['accent_deep'],'deutan')):.1f} / "
                   f"{de2000(simulate(c['signal'],'protan'),simulate(c['accent_deep'],'protan')):.1f}")
        if "ramp_seen" in FAMILIES[fid]:
            out.append(f"  \nmeasured chart shades on the board: {', '.join('`'+h+'`' for h in FAMILIES[fid]['ramp_seen'])}")
    return "\n".join(out)

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "measure"
    if mode == "measure":
        print(json.dumps({L: measure(L) for L in "ABCDEFG"}, indent=1))
    elif mode == "tables":
        print(tables({L: measure(L) for L in "ABCDEFG"}))
    elif mode == "derive":
        pal = {}
        for fid, fam in FAMILIES.items():
            color, ramp = derive(fid, fam)
            entry = {"source_refs": ["ref-" + r for r in fam["refs"]], "canonical_measured": fam["accent"],
                     "color": color, "chart_series": ramp}
            if "variants" in fam: entry["variants"] = fam["variants"]
            pal[fid] = entry
        with open(OUT_JSON, "w") as f: json.dump(pal, f, indent=2)
        print(derived_tables(pal))
