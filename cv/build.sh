#!/usr/bin/env bash
# Genera los PDF del CV. OUT_DIR define el destino (por defecto, ./cv/dist).
set -euo pipefail
CV="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(dirname "$CV")"
OUT_DIR="${OUT_DIR:-$CV/dist}"
FONTS="$HOME/.local/share/fonts/cv-portfolio"
mkdir -p "$OUT_DIR"

if [ ! -d "$FONTS" ]; then
  uv run --quiet --with fonttools python "$CV/mkfonts.py" "$CV/fonts" "$FONTS"
  fc-cache -f "$FONTS" >/dev/null
fi

python3 -m http.server 8731 --bind 127.0.0.1 --directory "$ROOT" >/dev/null 2>&1 &
SRV=$!
trap 'kill $SRV 2>/dev/null || true' EXIT
until curl -sf -o /dev/null http://127.0.0.1:8731/cv/index.html; do :; done

render() {
  chromium --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --virtual-time-budget=6000 \
    --print-to-pdf="$OUT_DIR/$2" "http://127.0.0.1:8731/cv/index.html?$1" 2>/dev/null
  qpdf --linearize --replace-input "$OUT_DIR/$2"
}

render "lang=es&len=short" "CV_Andres_AlvarezDeCienfuegos_ES_1pag.pdf"
render "lang=es&len=long"  "CV_Andres_AlvarezDeCienfuegos_ES_2pag.pdf"
render "lang=en&len=short" "CV_Andres_AlvarezDeCienfuegos_EN_1pag.pdf"
render "lang=en&len=long"  "CV_Andres_AlvarezDeCienfuegos_EN_2pag.pdf"
