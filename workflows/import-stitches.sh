#!/bin/bash

# Import multiple CodeStitch components
# Usage: ./import-stitches.sh <stitch-number> [<stitch-number> ...]
# Example: ./import-stitches.sh 375 376 377 378

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -z "$1" ]; then
    echo "Usage: $0 <stitch-number> [<stitch-number> ...]"
    echo ""
    echo "Examples:"
    echo "  $0 376                         # Single stitch"
    echo "  $0 375 376 377 378            # Multiple stitches"
    echo ""
    echo "Note: You'll be prompted for cookies after each stitch"
    exit 1
fi

cd "$ROOT_DIR"

for STITCH_NUM in "$@"; do
    echo ""
    echo "========================================"
    echo "Importing stitch $STITCH_NUM..."
    echo "========================================"
    echo ""
    echo "Getting cookies from codestitch.app..."
    echo "Open browser DevTools → Application → Cookies → codestitch.app"
    echo "Paste cookies below (press Enter when done):"
    echo ""
    read -r COOKIES

    if [ -z "$COOKIES" ]; then
        echo "Skipping stitch $STITCH_NUM (no cookies provided)"
        continue
    fi

    python import_stitch.py "https://codestitch.app/app/dashboard/stitches/$STITCH_NUM" "$COOKIES"

    echo ""
    echo "Stitch $STITCH_NUM imported!"
    echo ""
done

echo ""
echo "========================================"
echo "All stitches imported!"
echo "========================================"
