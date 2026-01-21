---
description: Port a CodeStitch HTML/LESS snippet into an Astro component
tags: [opencode, authentication, batch-processing, codestitch]
---

## OpenCode Integration

This workflow is designed to work with opencode tools and commands. Key integration points:

- **Authentication**: Use `curl` commands with proper cookie headers
- **File Operations**: Use `read`, `write`, `edit` tools for component creation
- **Progress Tracking**: Update `stitch-urls.txt` using `edit` tool
- **Batch Processing**: Loop through URLs using bash commands
- **Error Handling**: Check HTTP response codes and handle failures

## Quick Start for OpenCode

1. **Authentication Setup**: Get cookies using browser console method
2. **Test Connection**: Use provided curl command to verify access
3. **Process Batch**: Run automation script or process individual URLs
4. **Create Components**: Follow component creation and integration steps
5. **Update Tracking**: Mark completed items in `stitch-urls.txt`

# CodeStitch Porting Workflow

Follow these steps to port a CodeStitch snippet (Stitch) into this Astro project.

## 1. Authentication Setup

### 1.1 Get Authentication Cookies
Instruct the user to:
1. **Log into CodeStitch**: Open browser and log into `https://codestitch.app`
2. **Get Authentication Cookies**:
   - Press F12 → Console tab
   - Run: `console.log(document.cookie)`
   - Copy the full cookie string (includes: `_ga`, `_gcl_au`, `XSRF-TOKEN`, `codestitch_session`, `_rdt_uuid`, `_ga_K8992C75LX`)
3. **CRITICAL**: The `codestitch_session` cookie is **required** for authenticated access
4. **Store Cookies**: Save cookies in environment variable or temporary file for curl commands

### 1.2 Required Cookie Format & Validation
The curl command requires these cookies in this specific format:
```bash
Cookie: _ga=GA1.1.948162789.1768921038; _gcl_au=1.1.1781687127.1768921038; XSRF-TOKEN=[TOKEN]; codestitch_session=[SESSION]; _rdt_uuid=[UUID]; _ga_K8992C75LX=[VALUE]
```

**IMPORTANT**: 
- If `codestitch_session` is missing, most stitches will return **403 Forbidden**
- Always validate cookies contain session before proceeding
- Use curl with HTTP response code checking to detect access issues

## 2. Authentication & Error Handling

### 2.1 Session Cookie Validation
**CRITICAL**: The `codestitch_session` cookie is **required** for accessing most stitches. Without it:
- Most stitches return **403 Forbidden**
- Some may load but show "Forbidden" content
- No code extraction is possible

### 2.2 403 Error Recovery Process
When a 403 error occurs, the workflow will:
1. **Stop processing** the current stitch
2. **Display detailed error message** with authentication steps
3. **Prompt for new cookies** (if running interactively)
4. **Update tracking file** with `(403 Forbidden)` status
5. **Continue to next stitch** (or retry with new cookies)

### 2.3 Interactive Cookie Update
If running in a terminal (TTY detected), you can:
- **Paste new cookie string** when prompted
- **Continue without update** (may result in more errors)
- **Retry failed stitches** with fresh authentication

### 2.4 Manual Cookie Update Steps
When 403 errors occur:
1. Open browser → https://codestitch.app
2. Log in with your credentials
3. Press F12 → Console tab
4. Run: `console.log(document.cookie)`
5. Copy the complete cookie string
6. Update your script's COOKIES variable
7. Restart the porting process

## 3. Batch Processing Workflow

### 2.1 URL List Processing
1. **Read Stitch URLs**: Load list of stitch URLs from `stitch-urls.txt`
2. **For Each URL**: 
   - Extract stitch ID from URL pattern: `https://codestitch.app/app/dashboard/stitches/[ID]`
   - Skip lines marked with `✅` (completed)
   - Process lines marked with `❌` (pending)

### 2.2 Download Complete Stitch Content
For each unprocessed stitch URL:

```bash
# Set authentication cookies
COOKIES="_ga=GA1.1.948162789.1768921038; _gcl_au=1.1.1781687127.1768921038; XSRF-TOKEN=[TOKEN]; codestitch_session=[SESSION]; _rdt_uuid=[UUID]; _ga_K8992C75LX=[VALUE]"

# Check if cookies contain session (required for authenticated access)
if [[ "$COOKIES" != *"codestitch_session"* ]]; then
    echo "WARNING: No codestitch_session cookie found. Limited access may occur."
    echo "Proceeding anyway - some stitches may return 403 Forbidden."
fi

# Download HTML page with stitch and check response
HTTP_CODE=$(curl -s -o "temp-stitch-$ID.html" -w "%{http_code}" \
     -H "Cookie: $COOKIES" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "https://codestitch.app/app/dashboard/stitches/$ID")

# Check if download was successful
if [ "$HTTP_CODE" -eq "403" ]; then
    echo "ERROR: Stitch $ID returned 403 Forbidden"
    echo "AUTHENTICATION REQUIRED: Your session cookie may be expired or missing."
    echo ""
    echo "Please follow these steps to update authentication:"
    echo "1. Open browser and log into https://codestitch.app"
    echo "2. Press F12 → Console tab"
    echo "3. Run: console.log(document.cookie)"
    echo "4. Copy the FULL cookie string (including codestitch_session)"
    echo "5. Update your COOKIES variable and retry"
    echo ""
    echo "The cookie string should include: _ga, _gcl_au, XSRF-TOKEN, codestitch_session, _rdt_uuid, _ga_K8992C75LX"
    echo ""
    # Update tracking file with forbidden status
    sed -i "s|❌ https://codestitch.app/app/dashboard/stitches/$ID|❌ https://codestitch.app/app/dashboard/stitches/$ID (403 Forbidden)|g" stitch-urls.txt
    
    # Ask for fresh cookies interactively if supported
    if [ -t 0 ]; then  # Check if running in terminal
        echo "Press Enter to continue without updating cookies, or"
        read -p "Paste new cookie string here (or press Enter to skip): " NEW_COOKIES
        if [ ! -z "$NEW_COOKIES" ]; then
            COOKIES="$NEW_COOKIES"
            echo "Updated cookies - will retry authentication with new session"
        else
            echo "Continuing with current cookies (may result in more 403 errors)"
        fi
    fi
    
    continue
elif [ "$HTTP_CODE" -ne "200" ]; then
    echo "ERROR: Stitch $ID returned HTTP $HTTP_CODE - skipping"
    continue
fi

# Download required CSS files (only if HTML download succeeded)
curl -H "Cookie: $COOKIES" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "https://codestitch.app/site/css/core-styles.css?v=4" >> "temp-stitch-$ID.html"
curl -H "Cookie: $COOKIES" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "https://codestitch.app/site/css/user-dash.css" >> "temp-stitch-$ID.html"
curl -H "Cookie: $COOKIES" \
     -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
     "https://codestitch.app/site/css/main.css" >> "temp-stitch-$ID.html"
```

### 2.3 Extract Code Blocks
From downloaded `temp-stitch-$ID.html`:
1. **HTML**: Parse and extract the stitch HTML content from the page
2. **CSS/LESS**: Extract embedded styles and CSS variables
3. **JavaScript**: Extract any JavaScript code blocks
4. **Core Styles**: Parse global style definitions and dependencies

## 3. Component Creation

### 3.1 Analyze Stitch
1. **Extract Metadata**: Parse HTML to identify:
   - Stitch ID from page content or URL
   - Category (Hero, Services, SBS, etc.) from page title or navigation
   - Component type and structure

### 3.2 Create Astro Component File
1. **File Path**: `src/components/[Category]/[Category][ID].astro`
   - Example: `src/components/Hero/Hero345.astro`
2. **Component Structure**:
   ```astro
   ---
   // Component imports and props if needed
   ---
   <!-- Extracted HTML content -->
   
   <style lang="less">
   /* Extracted CSS/LESS styles */
   </style>
   ```

### 3.3 Process Extracted Content
1. **HTML**: Clean and format extracted HTML for Astro component
2. **CSS/LESS**: Convert LESS to CSS if needed, include dark mode styles
3. **JavaScript**: Extract any required JavaScript and include in component
4. **Dependencies**: Note any external libraries or imports required

## 4. Component Creation
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

## 4. Integration Options

### Option A: Preview Only (Default)
1.  Create or overwrite `src/pages/stitch-preview.astro`
2.  Import the new component and render it inside `<BaseLayout>`
3.  Instruct the user to visit `http://localhost:4321/stitch-preview`

### Option B: Add to Specific Page
1.  Open the target page (e.g., `src/pages/about.astro`)
2.  Import the new component: `import ComponentName from "../components/Category/CategoryID.astro"`
3.  Add the component tag `<ComponentName />` in the desired location

### Option C: Replace Existing Section
1.  Identify the page to modify (usually `index.astro` for Hero sections)
2.  Find the existing component import
3.  **Swap the Import**: Change to the new component file
4.  Keep the existing tag name for easier integration

## 6. Global Styles Check (CRITICAL)
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

## 5. Update Tracking File
After successfully porting a stitch, update `stitch-urls.txt` to mark it as complete:
1.  Open `stitch-urls.txt` in the project root
2.  Find the line with the stitch URL you just ported (e.g., `❌ https://codestitch.app/app/dashboard/stitches/342`)
3.  Change `❌` to `✅` and add the component filename in parentheses
4.  Example: `✅ https://codestitch.app/app/dashboard/stitches/342 (Services342.astro)`

This helps track progress across all stitches in the collection.

## 6. Batch Processing Script

### 6.1 Complete Automation Script
```bash
#!/bin/bash
# Set your authentication cookies (get from browser console)
COOKIES="_ga=GA1.1.948162789.1768921038; _gcl_au=1.1.1781687127.1768921038; XSRF-TOKEN=[USER_TOKEN]; codestitch_session=[USER_SESSION]; _rdt_uuid=[USER_UUID]; _ga_K8992C75LX=[USER_GA]"

# Check if cookies contain session (required for authenticated access)
if [[ "$COOKIES" != *"codestitch_session"* ]]; then
    echo "WARNING: No codestitch_session cookie found. Limited access may occur."
    echo "Proceeding anyway - some stitches may return 403 Forbidden."
fi

while IFS= read -r url; do
    # Skip completed items
    if [[ $url == ✅* ]] || [[ $url == "✅ ("* ]]; then
        continue
    fi
    
    # Extract stitch ID from various URL formats
    ID=$(echo $url | grep -o 'stitches/[0-9]\+' | grep -o '[0-9]\+')
    
    if [ -z "$ID" ]; then
        echo "No ID found in line: $url"
        continue
    fi
    
    echo "Processing stitch $ID..."
    
    # Download HTML page and check response
    HTTP_CODE=$(curl -s -o "temp-stitch-$ID.html" -w "%{http_code}" \
         -H "Cookie: $COOKIES" \
         -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
         "https://codestitch.app/app/dashboard/stitches/$ID")

    # Check if download was successful
    if [ "$HTTP_CODE" -eq "403" ]; then
        echo "ERROR: Stitch $ID returned 403 Forbidden"
        echo "AUTHENTICATION REQUIRED: Your session cookie may be expired or missing."
        echo ""
        echo "Please follow these steps to update authentication:"
        echo "1. Open browser and log into https://codestitch.app"
        echo "2. Press F12 → Console tab"
        echo "3. Run: console.log(document.cookie)"
        echo "4. Copy the FULL cookie string (including codestitch_session)"
        echo "5. Update your COOKIES variable and retry"
        echo ""
        echo "The cookie string should include: _ga, _gcl_au, XSRF-TOKEN, codestitch_session, _rdt_uuid, _ga_K8992C75LX"
        echo ""
        # Update tracking file with forbidden status
        sed -i "s|❌ https://codestitch.app/app/dashboard/stitches/$ID|❌ https://codestitch.app/app/dashboard/stitches/$ID (403 Forbidden)|g" stitch-urls.txt
        
        # Ask for fresh cookies interactively if supported
        if [ -t 0 ]; then  # Check if running in terminal
            echo "Press Enter to continue without updating cookies, or"
            read -p "Paste new cookie string here (or press Enter to skip): " NEW_COOKIES
            if [ ! -z "$NEW_COOKIES" ]; then
                COOKIES="$NEW_COOKIES"
                echo "Updated cookies - will retry authentication with new session"
            else
                echo "Continuing with current cookies (may result in more 403 errors)"
            fi
        fi
        
        continue
    elif [ "$HTTP_CODE" -ne "200" ]; then
        echo "ERROR: Stitch $ID returned HTTP $HTTP_CODE - skipping"
        continue
    fi
    
    # Download required CSS files (only if HTML download succeeded)
    curl -H "Cookie: $COOKIES" \
         -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
         "https://codestitch.app/site/css/core-styles.css?v=4" >> "temp-stitch-$ID.html"
    curl -H "Cookie: $COOKIES" \
         -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
         "https://codestitch.app/site/css/user-dash.css" >> "temp-stitch-$ID.html"
    curl -H "Cookie: $COOKIES" \
         -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
         "https://codestitch.app/site/css/main.css" >> "temp-stitch-$ID.html"
    
    # Extract HTML, CSS, JS, and create component
    # [Your parsing and component creation logic here]
    
    # Cleanup temp files
    rm "temp-stitch-$ID.html"
    
    # Update tracking file with success
    sed -i "s|❌ $url|✅ $url (Category$ID.astro)|g" stitch-urls.txt
    
done < stitch-urls.txt
```

## 7. Global Styles Check (CRITICAL)
Before finalizing, you must verify CSS variables:
1.  **Extract Variables**: List variables used in the Stitch (e.g., `--primary`, `--headerColor`)
2.  **Check Project Defaults**: Read BOTH style files:
    *   `src/styles/root.less` - Core variables: `--primary`, `--primaryLight`, `--secondary`, `--headerColor`, `--bodyTextColor`, `--bodyTextColorWhite`, `--sectionPadding`, etc.
    *   `src/styles/dark.less` - Dark mode variables: `--dark`, `--medium`, `--accent`
3.  **Compare**:
    *   Do all variables used in the Stitch exist in `root.less` or `dark.less`?
    *   Are there naming conflicts (e.g., Stitch uses `--primaryColor` but project uses `--primary`)?
4.  **Action**:
    *   **If everything matches**: Proceed
    *   **If DISCREPANCIES found**: **STOP execution and ASK the user**
        *   List missing or conflicting variables
        *   Ask the user to choose:
            *   *Update Global*: Add variables to `root.less` or `dark.less`
            *   *Map Variables*: Change component code to use existing project variables
            *   *Local Scope*: Define variables inside the component's `<style>` block

## 8. Verification
*   Run the dev server (`npm start`) and verify the visual appearance
*   Check dark mode functionality by toggling theme
*   Verify responsive behavior across different screen sizes

---

## Complete Workflow Summary

1. **Authentication** → Get cookies from browser console
2. **Batch Process** → Loop through `stitch-urls.txt` with curl  
3. **Extract Code** → Parse HTML, CSS/LESS, JavaScript from downloads
4. **Create Components** → Generate `.astro` files with proper structure
5. **Integrate** → Add components to pages or preview
6. **Check Variables** → Verify CSS variable compatibility
7. **Track Progress** → Update completion status in `stitch-urls.txt`
8. **Verify** → Test components in dev server

## 8. Verification
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
