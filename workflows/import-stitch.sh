#!/bin/bash

# Import a single CodeStitch component
# Usage: ./import-stitch.sh <stitch-number> "<cookies>"
# Example: ./import-stitch.sh 376 "_ga=...; codestitch_session=..."
#
# NOTE: Stitches marked as "REMOVED" in stitch-urls.txt may still be available.
# Always try importing them first before assuming they're gone.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -z "$1" ]; then
    echo "Usage: $0 <stitch-number> \"<cookies>\""
    echo ""
    echo "Example:"
    echo "  $0 376 \"_ga=GA1.1...; codestitch_session=...\""
    echo ""
    echo "To get cookies:"
    echo "  1. Open https://codestitch.app/app/dashboard/stitches/<number>"
    echo "  2. Open DevTools (F12) → Application → Cookies → codestitch.app"
    echo "  3. Copy all cookie values"
    exit 1
fi

STITCH_NUM="$1"
COOKIES="$2"

if [ -z "$COOKIES" ]; then
    echo "Error: Cookies required"
    echo "Usage: $0 <stitch-number> \"<cookies>\""
    exit 1
fi

echo "Importing stitch $STITCH_NUM..."

cd "$ROOT_DIR"
python import_stitch.py "https://codestitch.app/app/dashboard/stitches/$STITCH_NUM" "$COOKIES"

echo ""
echo "Done! Component created."
echo "Check the component and preview at: http://localhost:4321/stitch-preview"
