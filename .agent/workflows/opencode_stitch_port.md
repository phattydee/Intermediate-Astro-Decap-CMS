---
description: Port CodeStitch snippets using OpenCode's built-in web scraper
---

# CodeStitch Porting Workflow (OpenCode Web Scraper)

This workflow uses **OpenCode's built-in web scraper** to extract code from CodeStitch snippets. 

⚠️ **Important Limitations:**
- CodeStitch requires authentication, so the scraper may not access the code editors directly
- Code editors are often loaded dynamically via JavaScript, which the scraper may not execute
- **Fallback**: If scraping fails, use the Chrome DevTools MCP workflow instead

## Prerequisites
- User must be logged into CodeStitch in their browser
- OpenCode CLI installed and configured
- The user provides a stitch URL from `stitch-urls.txt`

---

## Workflow Steps

### 1. Attempt to Scrape the Stitch Page

Use OpenCode's web scraper to fetch the page content:

```bash
# Example OpenCode command (adjust based on actual CLI syntax)
opencode scrape "https://codestitch.app/app/dashboard/stitches/342"
```

**What to look for in the scraped HTML:**
- Look for `<textarea>` or `<div>` elements containing the HTML/CSS code
- Search for CodeMirror instances: `class="CodeMirror"`
- Check for embedded `<script>` tags that might contain the code as JSON

### 2. Extract HTML Code

**Option A: Direct HTML in Page Source**
- Search the scraped content for the HTML code
- Look for patterns like `<section id="services-342">` or similar
- The code might be in a `<textarea>`, `<pre>`, or within a CodeMirror div

**Option B: JSON Embedded Data**
- Some sites embed code in JavaScript variables
- Search for patterns like: `var htmlCode = "..."` or `window.__INITIAL_STATE__`
- Parse the JSON to extract the HTML string

**Option C: API Endpoint (Advanced)**
- CodeStitch might have an API endpoint that returns the code
- Check network requests in browser DevTools to find the endpoint
- Example: `https://codestitch.app/api/stitches/342/code`
- Use OpenCode to fetch from this endpoint instead

### 3. Extract LESS/CSS Code

Follow the same approach as Step 2, but look for:
- CSS/LESS content in a separate editor
- Variables like `var cssCode = "..."` or `lessCode`
- The LESS content is usually in a second CodeMirror instance

### 4. Fallback: Use Chrome DevTools MCP

If the web scraper cannot access the code (likely scenario):

**Switch to the Chrome DevTools MCP workflow:**
1. Open the stitch URL in Chrome (user must be logged in)
2. Use OpenCode with Chrome DevTools MCP to:
   ```javascript
   // Get all CodeMirror editors
   const editors = document.querySelectorAll('.CodeMirror');
   const htmlContent = editors[0]?.CodeMirror?.getValue();
   const cssContent = editors[1]?.CodeMirror?.getValue();
   ```
3. Extract the code from the live browser session

**See the `/port_codestitch_opencode` workflow for full DevTools instructions.**

### 5. Identify Component Type and ID

From the extracted HTML:
1. Find the main container's `id` attribute (e.g., `id="services-342"`)
2. Parse the category and ID:
   - `services-342` → Category: "Services", ID: "342"
3. Map to component type:
   - `hero-*` → Hero
   - `services-*` → Services
   - `sbs-*` → SideBySide
   - `stats-*` → Stats
   - `contact-*` → Contact
   - `footer-*` → Footer
   - `cta-*` → CTA
   - `gallery-*` → Gallery

### 6. Create Astro Component

1. **File path**: `src/components/[Category]/[Category][ID].astro`
   - Example: `src/components/Services/Services342.astro`

2. **File structure**:
   ```astro
   ---
   // Props interface if needed
   interface Props {
     reverse?: boolean;
     // Add other props as needed
   }
   const { reverse = false } = Astro.props;
   ---
   
   <!-- PASTE EXTRACTED HTML HERE -->
   
   <style lang="less">
   /* PASTE EXTRACTED LESS HERE */
   </style>
   ```

3. **Insert the code**:
   - Paste the extracted HTML into the HTML section
   - Paste the extracted LESS into the `<style>` block
   - Clean up any escaped characters (e.g., `\n` → actual newlines)

### 7. Global Styles Check

**CRITICAL**: Verify CSS variables before finalizing.

1. **Extract variables**: Find all `var(--variableName)` in the LESS
2. **Check project files**:
   - `src/styles/root.less` - Core variables
   - `src/styles/dark.less` - Dark mode variables
3. **Compare**:
   - Are all variables defined in the project?
   - Any naming conflicts?
4. **Action**:
   - ✅ All match → Proceed
   - ⚠️ Discrepancies → **STOP and ask user**:
     - Update global styles?
     - Map to existing variables?
     - Define locally in component?

### 8. Update Tracking File

Mark the stitch as complete in `stitch-urls.txt`:

1. Open `stitch-urls.txt`
2. Find: `❌ https://codestitch.app/app/dashboard/stitches/342`
3. Change to: `✅ https://codestitch.app/app/dashboard/stitches/342 (Services342.astro)`

### 9. Add to Preview Page (Optional)

For testing:
1. Open `src/pages/stitch-preview.astro`
2. Add import: `import Services342 from "@components/Services/Services342.astro";`
3. Add tag: `<Services342 />`
4. Visit: `http://localhost:4321/stitch-preview`

### 10. Verification

- Run dev server: `npm run start`
- Check visual appearance matches original
- Test dark mode toggle
- Verify responsive behavior

---

## Scraping Strategies

### Strategy 1: Direct Page Scrape
```bash
# Fetch the page HTML
opencode scrape "https://codestitch.app/app/dashboard/stitches/342" > stitch-342.html

# Parse the HTML to find code
# Look for <textarea>, CodeMirror divs, or embedded JSON
```

### Strategy 2: API Endpoint (If Available)
```bash
# Try to find the API endpoint
# Example (may not exist):
opencode scrape "https://codestitch.app/api/stitches/342/code"
```

### Strategy 3: Authenticated Request
If OpenCode supports cookies/sessions:
```bash
# Use browser cookies for authentication
opencode scrape --cookies "session=YOUR_SESSION_COOKIE" "https://codestitch.app/app/dashboard/stitches/342"
```

### Strategy 4: Hybrid Approach
1. Use scraper to get the page structure
2. Identify where the code is loaded from (check `<script>` tags)
3. Make a second request to fetch the actual code

---

## Troubleshooting

### Problem: Scraper returns login page
**Solution**: CodeStitch requires authentication. Use Chrome DevTools MCP workflow instead.

### Problem: Code editors are empty in scraped HTML
**Solution**: The code is loaded via JavaScript. Use Chrome DevTools MCP to access the live DOM.

### Problem: Code is escaped/encoded
**Solution**: 
- Unescape HTML entities: `&lt;` → `<`, `&gt;` → `>`
- Parse JSON strings: `\"` → `"`
- Decode base64 if needed

### Problem: Cannot find the code in scraped content
**Solution**: 
1. Inspect the page in browser DevTools
2. Find where the code is actually stored (Network tab, Sources tab)
3. Adjust scraping strategy or switch to DevTools MCP workflow

---

## Batch Processing

To port multiple stitches:

1. **Read `stitch-urls.txt`**: Get all `❌` marked URLs
2. **Loop through each**:
   ```bash
   for url in $(grep "❌" stitch-urls.txt); do
     stitch_id=$(echo $url | grep -oP '\d+$')
     opencode scrape "$url" > "temp-$stitch_id.html"
     # Process the scraped content
     # Create Astro component
     # Update tracking file
   done
   ```
3. **Report progress** after each batch
4. **Handle failures**: Note which stitches need manual review

---

## Recommendation

**For most reliable results, use the Chrome DevTools MCP workflow** (`/port_codestitch_opencode`), as:
- CodeStitch requires authentication
- Code editors are dynamically loaded
- DevTools can access the live browser session

**Use this web scraper workflow only if:**
- You can authenticate the scraper with session cookies
- The code is available in the initial page HTML
- You're willing to parse complex JavaScript/JSON structures

---

## Quick Reference

| Step | Web Scraper | Chrome DevTools MCP |
|------|-------------|---------------------|
| **Access** | May fail (auth required) | ✅ Works (uses logged-in browser) |
| **Dynamic Content** | ❌ Cannot execute JS | ✅ Accesses live DOM |
| **Speed** | ⚡ Fast (if it works) | 🐢 Slower (browser automation) |
| **Reliability** | ⚠️ Low (for CodeStitch) | ✅ High |
| **Recommendation** | Fallback only | **Primary method** |
