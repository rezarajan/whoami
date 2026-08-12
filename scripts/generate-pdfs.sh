#!/usr/bin/env bash
# Pre-render resume.pdf and cv.pdf into hugo/static/ so the local dev site
# serves the same download links the CI pipeline publishes. The files are
# gitignored; CI generates its own copies into the deployed site.
#
# Usage: scripts/generate-pdfs.sh [base_url]
#   base_url defaults to the deployed site so PDF links resolve there.
set -euo pipefail
cd "$(dirname "$0")/.."

BASE_URL="${1:-https://rezarajan.github.io/whoami/}"
BASE_PATH=$(basename "$BASE_URL")
PORT=8929

for browser in google-chrome chromium chromium-browser; do
	if command -v "$browser" >/dev/null 2>&1; then
		BROWSER="$browser"
		break
	fi
done
: "${BROWSER:?no chrome/chromium found}"

TMP=$(mktemp -d)
trap 'kill "$SERVER_PID" 2>/dev/null || true; rm -rf "$TMP"' EXIT

(cd hugo && hugo --gc --minify --baseURL "$BASE_URL" -d "$TMP/$BASE_PATH" >/dev/null)
python3 -m http.server "$PORT" --directory "$TMP" >/dev/null 2>&1 &
SERVER_PID=$!
sleep 1

"$BROWSER" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 \
	--print-to-pdf=hugo/static/cv.pdf "http://localhost:$PORT/$BASE_PATH/"
"$BROWSER" --headless --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 \
	--print-to-pdf=hugo/static/resume.pdf "http://localhost:$PORT/$BASE_PATH/resume/"

echo "Wrote hugo/static/resume.pdf and hugo/static/cv.pdf"
