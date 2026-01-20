---
description: Port a CodeStitch HTML/LESS snippet into an Astro component
---

# CodeStitch Porting Workflow

Follow these steps to port a CodeStitch snippet (Stitch) into this Astro project.

## 1. Prerequisites
*   **User Must Be On CodeStitch**: The user should provide the **direct URL** to the Stitch in their dashboard (e.g., `https://codestitch.app/app/dashboard/stitches/2335`).
*   **Browser Session**: The `browser_subagent` shares the user's session, so it can access the code if the user is logged in.

## 2. Retrieve Code
Use the `browser_subagent` to visit the provided URL.
*   **HTML**: Extract the content of the HTML CodeMirror editor.
*   **CSS/LESS**:
    1.  Click the "LESS" radio button to ensure you get the LESS version.
    2.  Click the "CSS" tab if not active.
    3.  Extract the content of the CSS CodeMirror editor.
    4.  **Capture Core Styles**: Also look for any "Core Styles" or global variable definitions provided with the snippet.

## 3. Component Creation
1.  **Analyze**: Look at the HTML `id` attribute (e.g., `id="hero-2335"`) to determine the Category (Hero) and ID (2335).
2.  **File Path**: Create a new component at `src/components/[Category]/[Category][ID].astro` (e.g., `src/components/Hero/Hero2335.astro`).
3.  **Content format**:
    ```astro
    ---
    // Frontmatter (imports/props) if needed
    ---
    <!-- PASTE HTML HERE -->
    
    <style lang="less">
    /* PASTE LESS HERE */
    </style>
    ```

## 4. Integration (Choose One)

### Option A: Preview Only (Default)
If the user didn't specify where to put it:
1.  Create or overwrite `src/pages/stitch-preview.astro`.
2.  Import the new component and render it inside `<BaseLayout>`.
3.  Instruct user to visit `http://localhost:4321/stitch-preview`.

### Option B: Add to Page
If the user says "add to the about page":
1.  Open the target page (e.g., `src/pages/about.astro`).
2.  Import the new component.
3.  Add the component tag `<Hero2335 />` in the desired location within the HTML/Main.

### Option C: Replace Section
If the user says "replace the existing hero":
1.  Identify the page to modify (usually `index.astro` for Hero, or ask user).
2.  Find the import for the *old* component (e.g., `import Hero from "../components/Hero/Hero.astro"`).
3.  **Swap the Import**: Change it to `import Hero from "../components/Hero/Hero2335.astro"`.
4.  (Optional) Rename the local variable if needed, or alias it (e.g., `import Hero from "../components/Hero/Hero2335.astro"`). Keeping the tag `<Hero />` is easiest if you alias the import.

## 5. Global Styles Check (CRITICAL)
Before finalizing, you must verify the CSS variables.
1.  **Extract Variables**: List the variables used in the Stitch (e.g., `--primary`, `--headerColor`).
2.  **Check Project Defaults**: Read BOTH style files:
    *   `src/styles/root.less` - Core variables: `--primary`, `--primaryLight`, `--secondary`, `--headerColor`, `--bodyTextColor`, `--bodyTextColorWhite`, `--sectionPadding`, etc.
    *   `src/styles/dark.less` - Dark mode variables: `--dark`, `--medium`, `--accent`
3.  **Compare**:
    *   Do all variables used in the Stitch exist in `root.less` or `dark.less`?
    *   Are there naming conflicts (e.g., Stitch uses `--primaryColor` but project uses `--primary`)?
4.  **Action**:
    *   **If everything matches**: Proceed.
    *   **If DISCREPANCIES found**: **STOP execution and ASK the user**.
        *   List the missing or conflicting variables.
        *   Ask the user to choose:
            *   *Update Global*: Add variables to `root.less` or `dark.less`.
            *   *Map Variables*: Change the component code to use existing project variables.
            *   *Local Scope*: Define the variables inside the component's `<style>` block.

## 6. Update Tracking File
After successfully porting a stitch, update `stitch-urls.txt` to mark it as complete:
1.  Open `stitch-urls.txt` in the project root.
2.  Find the line with the stitch URL you just ported (e.g., `❌ https://codestitch.app/app/dashboard/stitches/342`).
3.  Change `❌` to `✅` and add the component filename in parentheses.
4.  Example: `✅ https://codestitch.app/app/dashboard/stitches/342 (Services342.astro)`

This helps track progress across all stitches in the Cleaning Company collection.

## 7. Verification
*   Run the dev server (`npm start`) and verify visual appearance.

---

## Quick Reference: Adding Existing Components to Pages

If a component has already been ported and you just need to add it to a page:

1.  **Import**: Add an import statement in the page's frontmatter:
    ```astro
    import ComponentName from "@components/Category/CategoryID.astro";
    ```
2.  **Place**: Add `<ComponentName />` in the desired location within the page's HTML.
3.  **Common placements**:
    *   After `<SideBySide />` for "About Us" related sections (e.g., Team components)
    *   After `<Services />` for service-related sections
    *   Before `<CTASimple />` for most content sections
