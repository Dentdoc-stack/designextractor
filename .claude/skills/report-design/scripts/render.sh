#!/usr/bin/env bash
# usage: render.sh report.docx [outdir]  -> PDF, one PNG per page, and a contact sheet
set -euo pipefail
DOCX="$1"; OUT="${2:-$(dirname "$DOCX")/render}"
mkdir -p "$OUT"; rm -f "$OUT"/page-*.png
soffice --headless --convert-to pdf --outdir "$OUT" "$DOCX" >/dev/null 2>&1
PDF="$OUT/$(basename "${DOCX%.*}").pdf"
pdftoppm -r 80 -png "$PDF" "$OUT/page"
echo "pdf: $PDF"; ls "$OUT"/page-*.png | wc -l | xargs echo "pages:"
pdffonts "$PDF" | tail -n +3 | awk '{print "font:", $1, "emb=" $(NF-4)}'
