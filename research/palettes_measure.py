#!/usr/bin/env python3
"""Colour measurement + palette derivation for reference boards ref-A … ref-G.

Usage (numpy + Pillow only):
    .venv/bin/python research/palettes_measure.py measure  > measurements.md   # phase 1
    .venv/bin/python research/palettes_measure.py derive                         # phase 2, writes research/palettes.json

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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, ".claude/skills/report-design/references/images/ref-%s.jpeg")
OUT_JSON = os.path.join(ROOT, "research/palettes.json")

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
# Canonical measured colours, picked from phase-1 output (see palettes.md §2).
FAMILIES = {
    # id: refs, measured accent (brand fill), measured deep (or None), measured bright (or None),
    #     measured tint (or None), measured page grey
}

def find_L(H, C, target, against, lighter=False, lo=0.05, hi=0.99):
    """Highest (or lowest, if lighter) OKLCH lightness with contrast >= target vs `against`."""
    best = None
    for L in np.arange(hi, lo, -0.0025) if not lighter else np.arange(lo, hi, 0.0025):
        hx = oklch_hex(L, C, H)
        if contrast(hx, against) >= target: return L, hx
    return best

def derive(fam):
    paper, paper_alt = "FFFFFF", fam["paper_alt"]
    acc = fam["accent"]; La, Ca, Ha = oklch(acc)
    # accent_deep: measured deep if it reaches 7:1 on paper_alt, else darken in OKLCH
    deep = fam.get("deep")
    if not deep or contrast(deep, paper_alt) < 7:
        src = deep or acc
        Ls, Cs, Hs = oklch(src)
        Hs = Ha  # keep the brand hue
        L, deep = find_L(Hs, Cs, 7.0, paper_alt)
    bright = fam.get("bright") or acc
    tint = fam.get("tint")
    if not tint:
        tint = oklch_hex(0.955, min(0.035, Ca * 0.3), Ha)
    # chart ramp: 5 OKLCH steps, lightness from 0.86 to the deep shade, chroma bell-shaped
    Ld, Cd, _ = oklch(deep)
    Ls = np.linspace(0.86, Ld, 5)
    Cmax = max(Ca, Cd)
    ramp = [oklch_hex(l, Cmax * (0.45 + 0.55 * np.sin(np.pi * (0.25 + 0.75 * i / 4))), Ha) for i, l in enumerate(Ls)]
    ramp[-1] = deep
    color = {
        "ink": fam["ink"], "ink_soft": fam["ink_soft"], "paper": paper, "paper_alt": paper_alt,
        "rule": fam["rule"], "hairline": fam["hairline"],
        "accent_deep": deep, "accent": acc, "accent_bright": bright, "accent_tint": tint,
        "on_accent": "FFFFFF" if contrast("FFFFFF", acc) >= contrast(fam["ink"], acc) else fam["ink"],
        "signal": fam["signal"],
        # legacy keys used by scripts/reportkit.py
        "tint": paper_alt, "grey": fam["ink_soft"],
    }
    return color, ramp

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "measure"
    if mode == "measure":
        allres = {L: measure(L) for L in "ABCDEFG"}
        print(json.dumps(allres, indent=1))
