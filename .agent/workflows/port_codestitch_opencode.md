---
description: Port CodeStitch snippets using OpenCode CLI with Chrome DevTools MCP
---

# CodeStitch Porting Workflow (OpenCode)

This workflow is designed for **OpenCode**, a CLI AI coding assistant that can use Chrome DevTools MCP to visit websites and extract code.

## Prerequisites
- User must be logged into CodeStitch in their Chrome browser
- OpenCode must have access to Chrome DevTools MCP
- The user provides a stitch URL from `stitch-urls.txt` (e.g., `https://codestitch.app/app/dashboard/stitches/342`)

## Workflow Steps

### 1. Navigate to Stitch Page
Use Chrome DevTools MCP to navigate to the provided CodeStitch URL.
- Wait for the page to fully load
- Verify you can see the stitch preview

### 2. Extract HTML Code
1. Locate the HTML code editor on the page (usually a CodeMirror instance)
2. Extract the full HTML content from the editor
3. Store this content temporarily

**DevTools approach:**
- Use `document.querySelector('.CodeMirror')` to find the editor
- Access `.CodeMirror.getValue()` to get the HTML content
- Alternative: Look for a "Copy HTML" button and click it, then read from clipboard

### 3. Extract LESS/CSS Code
1. Click the "LESS" radio button if present (to ensure LESS format, not compiled CSS)
2. Click the "CSS" tab if not already active
3. Locate the CSS/LESS code editor (another CodeMirror instance)
4. Extract the full LESS content

**DevTools approach:**
- Find all CodeMirror instances on the page
- The second one typically contains the CSS/LESS
- Use `.CodeMirror.getValue()` to extract content
- Alternative: Look for a "Copy CSS" or "Copy LESS" button

### 4. Identify Component Type and ID
From the extracted HTML:
1. Find the main container's `id` attribute (e.g., `id="services-342"`)
2. Parse the category (e.g., "services") and ID (e.g., "342")
3. Determine the component category:
   - `hero-*` → Hero
   - `services-*` → Services
   - `sbs-*` or `sidebyside-*` → SideBySide
   - `sbsr-*` → SideBySide (Reverse variant)
   - `stats-*` → Stats
   - `contact-*` → Contact
   - `footer-*` → Footer
   - `cta-*` → CTA
   - `gallery-*` → Gallery
   - `reviews-*` or `testimonials-*` → Reviews/Testimonials

### 5. Create Astro Component
1. **Determine file path**: `src/components/[Category]/[Category][ID].astro`
   - Example: `src/components/Services/Services342.astro`
2. **Create the file** with this structure:
   ```astro
   ---
   // Props interface if needed
   interface Props {
     reverse?: boolean;
     // Add other props as needed
   }
   const { reverse = false } = Astro.props;
   ---
   
   <!-- PASTE HTML HERE -->
   
   <style lang="less">
   /* PASTE LESS HERE */
   </style>
   ```
3. **Paste the extracted HTML** into the HTML section
4. **Paste the extracted LESS** into the `<style>` block

### 6. Check for Variations
Some stitches have multiple layout variations (e.g., standard/reverse, different card counts):
- If the HTML contains conditional logic or multiple layouts, consider adding props
- Common props: `reverse`, `imageType`, `cardCount`
- Example: Services might have 4-card vs 6-card variations

### 7. Global Styles Check
**CRITICAL**: Verify CSS variables before finalizing.

1. **Extract variables from the LESS**: Look for `var(--variableName)` usage
2. **Check project defaults**:
   - Read `src/styles/root.less` for core variables
   - Read `src/styles/dark.less` for dark mode variables
3. **Compare**:
   - Do all variables exist in the project?
   - Are there naming conflicts?
4. **Action**:
   - ✅ If all variables match: Proceed
   - ⚠️ If discrepancies found: **STOP and report to user**
     - List missing/conflicting variables
     - Ask user to choose:
       - Update global styles (`root.less` or `dark.less`)
       - Map to existing variables (modify component code)
       - Define locally (add to component's `<style>` block)

### 8. Update Tracking File
Update `stitch-urls.txt` to mark the stitch as complete:
1. Open `stitch-urls.txt`
2. Find the line: `❌ https://codestitch.app/app/dashboard/stitches/[ID]`
3. Change to: `✅ https://codestitch.app/app/dashboard/stitches/[ID] ([ComponentName].astro)`
4. Example: `✅ https://codestitch.app/app/dashboard/stitches/342 (Services342.astro)`

### 9. Add to Preview Page (Optional)
If testing is needed:
1. Open `src/pages/stitch-preview.astro`
2. Add import: `import Services342 from "@components/Services/Services342.astro";`
3. Add component tag in the desired location: `<Services342 />`
4. Save and verify at `http://localhost:4321/stitch-preview`

### 10. Verification
- Ensure dev server is running (`npm run start`)
- Visit the preview page or target page
- Verify:
  - Layout matches the original stitch
  - Colors are correct (using project variables)
  - Dark mode works (if applicable)
  - Responsive behavior is intact

---

## Tips for OpenCode

### Finding CodeMirror Editors
```javascript
// Get all CodeMirror instances
const editors = document.querySelectorAll('.CodeMirror');
const htmlEditor = editors[0];
const cssEditor = editors[1];

// Extract content
const htmlContent = htmlEditor.CodeMirror.getValue();
const cssContent = cssEditor.CodeMirror.getValue();
```

### Alternative: Button Click Method
```javascript
// Look for copy buttons
const copyHtmlBtn = document.querySelector('[aria-label*="Copy HTML"]');
const copyCssBtn = document.querySelector('[aria-label*="Copy CSS"]');

// Click and read from clipboard
copyHtmlBtn?.click();
// Read clipboard content
```

### Handling Dynamic Content
- Wait for CodeMirror to fully initialize before extracting
- Use `setTimeout` or `waitForSelector` if needed
- Verify content is not empty before proceeding

---

## Batch Processing

To port multiple stitches efficiently:

1. **Read `stitch-urls.txt`**: Get all lines marked with `❌`
2. **Loop through each URL**:
   - Extract stitch ID from URL
   - Follow steps 1-10 for each stitch
   - Update tracking file after each successful port
3. **Report progress**: After each batch of 5-10, report completion status
4. **Handle errors**: If extraction fails, skip and note the stitch ID for manual review

---

## Quick Reference

| Category | File Path Example | Common Props |
|----------|------------------|--------------|
| Hero | `src/components/Hero/Hero342.astro` | - |
| Services | `src/components/Services/Services342.astro` | `cardCount`, `imageType` |
| SideBySide | `src/components/SideBySide/SBS342.astro` | `reverse`, `imageType` |
| Stats | `src/components/Stats/Stats342.astro` | - |
| Contact | `src/components/Contact/Contact342.astro` | - |
| Footer | `src/components/Footer/Footer342.astro` | - |
| CTA | `src/components/CTA/CTA342.astro` | - |
| Gallery | `src/components/Gallery/Gallery342.astro` | `filterType` |
