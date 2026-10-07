"""Read the supplied KP report so the redesign reuses its exact wording (no retyping).

blocks(): list of ("p", style, runs, images) and ("tbl", rows) in document order, where
runs = [(text, bold, italic, sup)] and sup marks a footnote reference (text = its number).
"""
from docx import Document
from docx.oxml.ns import qn

W = lambda t: qn("w:" + t)


def _on(rpr, tag):
    if rpr is None:
        return False
    el = rpr.find(W(tag))
    return el is not None and el.get(W("val")) not in ("0", "false")


def runs_of(p):
    out = []
    for r in p.iter(W("r")):
        rpr = r.find(W("rPr"))
        b, i = _on(rpr, "b"), _on(rpr, "i")
        for node in r:
            if node.tag == W("t"):
                out.append([node.text or "", b, i, False])
            elif node.tag == W("tab"):
                out.append(["\t", b, i, False])
            elif node.tag == W("br"):
                out.append(["\n", b, i, False])
            elif node.tag == W("footnoteReference"):
                out.append([node.get(W("id")), False, False, True])
    merged = []
    for t in out:                                   # merge neighbours with the same formatting
        if merged and merged[-1][1:] == t[1:] and not t[3]:
            merged[-1][0] += t[0]
        else:
            merged.append(t)
    return [tuple(m) for m in merged]


def text_of(runs):
    return "".join(t for t, b, i, s in runs if not s)


def blocks(path):
    d = Document(path)
    rels = {r.rId: r for r in d.part.rels.values()}

    def imgs(el):
        res = []
        for blip in el.iter(qn("a:blip")):
            rel = rels.get(blip.get(qn("r:embed")))
            if rel is not None:
                res.append((rel.target_ref.split("/")[-1], rel.target_part.blob))
        return res

    out = []
    for el in d.element.body:
        if el.tag == W("p"):
            ps = el.find(W("pPr"))
            st = ps.find(W("pStyle")).get(W("val")) if ps is not None and ps.find(W("pStyle")) is not None else ""
            r = runs_of(el)
            im = imgs(el)
            if text_of(r).strip() or im:
                out.append(("p", st, r, im))
        elif el.tag == W("tbl"):
            rows = []
            for tr in el.findall(W("tr")):
                cells = []
                for tc in tr.findall(W("tc")):
                    paras = [runs_of(p) for p in tc.findall(".//" + W("p"))]
                    cells.append(([p for p in paras if text_of(p).strip()], imgs(tc)))
                rows.append(cells)
            out.append(("tbl", rows))
    return out
