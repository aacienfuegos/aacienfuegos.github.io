#!/usr/bin/env bash
# Regenera la version inglesa. Lanzar despues de tocar index.html.
# Los PDF del CV van aparte porque tardan lo suyo y casi nunca cambian:
# bash cv/build.sh, que ademas publica en assets los que sirve la web.
set -euo pipefail
cd "$(dirname "$0")"
python3 build-en.py
echo "listo"
