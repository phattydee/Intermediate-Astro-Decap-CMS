#!/bin/bash

# Import all stitches from stitch-urls.txt
# Usage: ./import-all-stitches.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
URLS_FILE="$ROOT_DIR/stitch-urls.txt"

if [ ! -f "$URLS_FILE" ]; then
    echo "Error: $URLS_FILE not found"
    exit 1
fi

cd "$ROOT_DIR"

echo "Importing all stitches from $URLS_FILE..."
echo ""
echo "Getting cookies from codestitch.app..."
echo "Open browser DevTools → Application → Cookies → codestitch.app"
echo "Paste ALL cookies below (they'll be used for all stitches):"
echo ""
read -r COOKIES

if [ -z "$COOKIES" ]; then
    echo "Error: Cookies required"
    exit 1
fi

# Extract stitch numbers from URLs (format: https://codestitch.app/.../stitches/NUMBER)
# Skip lines that start with ❌ (already have issues) and ✅ (already imported)
grep -E 'stitches/[0-9]+' "$URLS_FILE" | \
    grep -v '❌' | \
    grep -v '✅' | \
    sed -E 's/.*stitches\/([0-9]+).*/\1/' | \
    sort -u | \
    while read -r STITCH_NUM; do
        if [ -n "$STITCH_NUM" ]; then
            echo ""
            echo "========================================"
            echo "Importing stitch $STITCH_NUM..."
            echo "========================================"

            if python import_stitch.py "https://codestitch.app/app/dashboard/stitches/$STITCH_NUM" "$COOKIES" 2>&1; then
                echo "✓ Stitch $STITCH_NUM imported successfully"
            else
                echo "✗ Stitch $STITCH_NUM failed (cookies may have expired)"
                echo "  Getting fresh cookies..."
                echo "  Open https://codestitch.app/app/dashboard/stitches/$STITCH_NUM"
                echo "  DevTools → Application → Cookies → codestitch.app"
                echo "  Paste new cookies:"
                read -r NEW_COOKIES

                if [ -n "$NEW_COOKIES" ]; then
                    if python import_stitch.py "https://codestitch.app/app/dashboard/stitches/$STITCH_NUM" "$NEW_COOKIES" 2>&1; then
                        echo "✓ Stitch $STITCH_NUM imported successfully"
                        COOKIES="$NEW_COOKIES"
                    else
                        echo "✗ Stitch $STITCH_NUM failed again, skipping..."
                    fi
                else
                    echo "  Skipping stitch $STITCH_NUM"
                fi
            fi
        fi
    done

echo ""
echo "========================================"
echo "Import complete!"
echo "========================================"
