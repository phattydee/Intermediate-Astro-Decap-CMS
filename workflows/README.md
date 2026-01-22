# Import Stitch Workflow

## Quick Start

### 1. Get cookies from browser

```bash
# Option A: Using the helper script (requires Playwright)
./workflows/get-cookies.sh

# Option B: Manual - Open browser DevTools → Application → Cookies → codestitch.app
# Copy all cookie values
```

### 2. Import a single stitch

```bash
./workflows/import-stitch.sh <stitch-number> "<cookies>"

# Example
./workflows/import-stitch.sh 376 "_ga=...; codestitch_session=..."
```

### 3. Import multiple stitches

```bash
# Interactive - prompts for each stitch
./workflows/import-stitches.sh 375 376 377 378

# Bulk import from stitch-urls.txt (skips already imported)
./workflows/import-all-stitches.sh
```

---

## Commands

| Command | Description |
|---------|-------------|
| `import-stitch.sh <num> "<cookies>"` | Import one stitch |
| `import-stitches.sh <nums...>` | Import multiple stitches |
| `import-all-stitches.sh` | Import all from stitch-urls.txt |
| `get-cookies.sh` | Get fresh cookies via browser |

---

## Cookie Setup

1. Navigate to https://codestitch.app/app/dashboard
2. Open DevTools (F12) → Application → Cookies → codestitch.app
3. Copy all cookie values (name=value; name=value; ...)
4. Use in import command

---

## Troubleshooting

**"Cannot find module" error:**
- The import was attempted with wrong component path
- Check `stitch-preview.astro` for duplicate/missing imports

**403 Forbidden:**
- Cookies expired
- Run `./workflows/get-cookies.sh` for fresh cookies

**Component not appearing:**
- Check `src/components/{Type}/` folder was created
- Verify import in `stitch-preview.astro`
- Run dev server: `npm run dev`

