#!/usr/bin/env bash
# Regenerates Wavelength_Dating_App_FastAPI_Documentation.pdf from the markdown source.
#
# Requires: pandoc, weasyprint
#   sudo apt-get install -y pandoc weasyprint
#
# Usage: ./build_pdf.sh   (run from the docs/ directory, or via `bash docs/build_pdf.sh`)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SRC="dating-app-fastapi-documentation.md"
OUT_PDF="Wavelength_Dating_App_FastAPI_Documentation.pdf"
TMP_HTML="$(mktemp -d)/doc.html"

pandoc "$SRC" \
  --standalone \
  --toc --toc-depth=3 \
  --metadata title="Wavelength" \
  --metadata subtitle="Behavioral Compatibility Dating App — FastAPI Mobile Development Documentation" \
  --metadata author="Product & Engineering Documentation" \
  --metadata date="$(date '+%B %Y')" \
  --css="$SCRIPT_DIR/assets/pdf-style.css" \
  -o "$TMP_HTML"

# pandoc writes a relative --css path into the HTML; since TMP_HTML lives elsewhere,
# rewrite it to the absolute stylesheet path before rendering.
python3 - "$TMP_HTML" "$SCRIPT_DIR/assets/pdf-style.css" <<'PY'
import sys
html_path, css_path = sys.argv[1], sys.argv[2]
with open(html_path) as f:
    content = f.read()
content = content.replace('href="assets/pdf-style.css"', f'href="{css_path}"')
with open(html_path, "w") as f:
    f.write(content)
PY

weasyprint "$TMP_HTML" "$OUT_PDF"
echo "Wrote $SCRIPT_DIR/$OUT_PDF"
