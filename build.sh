#!/usr/bin/env bash
# Regenera lo que no se edita a mano: la version inglesa y los PDF del CV.
# Lanzar despues de tocar index.html o cv/index.html.
set -euo pipefail
cd "$(dirname "$0")"
python3 build-en.py
bash cv/build.sh
echo "listo"
