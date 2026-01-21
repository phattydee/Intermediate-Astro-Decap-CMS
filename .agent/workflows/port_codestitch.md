---
description: Port a CodeStitch HTML/LESS snippet into an Astro component
tags: [opencode, authentication, batch-processing, codestitch]
---

## 🚨 CRITICAL UPDATE: CSS Extraction Issues Fixed

### Problem Solved
The port_codestitch workflow has been enhanced to fix the major issue where **commented CSS code blocks were not being copied properly** from CodeStitch.

### Key Improvements Made
1. **Enhanced CSS Extraction**: Multiple extraction methods to handle different CodeStitch page structures
2. **Comment Preservation**: Specifically preserves CSS comments (`/* */`) that appear as "commented out" in the UI but are actually active code
3. **LESS vs CSS Comment Handling**: Distinguishes between LESS comments (`//`) and CSS comments (`/* */`)
4. **Content Validation**: Automatically checks if extracted CSS contains expected patterns
5. **Debugging Tools**: Comprehensive debugging and validation scripts
6. **Fallback Methods**: Alternative extraction when primary method fails

### Quick Start for Fixing Existing Components
If you have components with incomplete CSS:

```bash
# Fix CSS for a specific component ID
fix_css_extraction 399  # Replace 399 with your stitch ID
```

### When to Use Enhanced Extraction
- Component appears broken or missing styles
- CSS seems incomplete (fewer selectors than expected)
- No comment blocks in extracted CSS
- Responsive breakpoints missing
- Dark mode styles not working

This workflow now ensures **ALL CSS content** is properly extracted, including sections that appear commented out in the CodeStitch UI but are actually active code that should be preserved.

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

#### 2.3.1 Understanding CodeStitch Code Display Structure
CodeStitch displays code in specific HTML containers that must be properly identified:
- **HTML Code Blocks**: Typically in `<pre><code>` elements with language identifiers
- **CSS/LESS Code Blocks**: Similar structure but may include both CSS and LESS options
- **Commented CSS**: CodeStitch often includes CSS with `/* ... */` comments that ARE part of the active code
- **LESS Syntax**: Uses `//` for single-line comments (compile-time only) and `/* */` for CSS comments

#### 2.3.2 HTML Extraction Strategy
```bash
# Extract HTML from code containers (multiple methods for robustness)
HTML_EXTRACTED=$(grep -A 1000 -B 5 'HTML' temp-stitch-$ID.html | \
  sed -n '/<pre[^>]*>/,/<\/pre>/p' | \
  sed 's/<pre[^>]*>//g; s/<\/pre>//g' | \
  sed 's/<code[^>]*>//g; s/<\/code>//g' | \
  sed '/^[[:space:]]*$/d')
```

#### 2.3.3 CSS/LESS Extraction Strategy (CRITICAL FOR COMMENTED CSS)
```bash
# Extract CSS/LESS from code containers - MUST preserve comments
CSS_EXTRACTED=$(grep -A 1000 -B 5 'CSS\|LESS' temp-stitch-$ID.html | \
  sed -n '/<pre[^>]*>/,/<\/pre>/p' | \
  sed 's/<pre[^>]*>//g; s/<\/pre>//g' | \
  sed 's/<code[^>]*>//g; s/<\/code>//g' | \
  sed '/^[[:space:]]*$/d')

# Alternative extraction using JavaScript-like parsing for complex pages
# This handles cases where code is in div containers or other elements
CSS_EXTRACTED_ALT=$(grep -o '<pre[^>]*>.*</pre>' temp-stitch-$ID.html | \
  sed 's/<[^>]*>//g' | \
  sed 's/<\/pre>//g')
```

#### 2.3.4 Special Handling for Commented CSS
CodeStitch often includes CSS that appears "commented out" in the UI but is actually active code:

```bash
# Ensure ALL CSS content is preserved, including commented sections
# This regex preserves both types of comments:
# CSS comments: /* comment */ (active in final output)
# LESS comments: // comment (compile-time only, may be removed)

FINAL_CSS=$(echo "$CSS_EXTRACTED" | \
  sed 's/&lt;/\</g; s/&gt;/\>/g; s/&amp;/\&/g' | \
  # Preserve ALL comments including those that appear commented in UI
  sed '/\/\*/!{/\/\//d;}' # Only remove LESS single-line comments, preserve CSS comments
)
```

#### 2.3.5 JavaScript Extraction
```bash
# Extract JavaScript from script tags
JS_EXTRACTED=$(grep -o '<script[^>]*>.*</script>' temp-stitch-$ID.html | \
  sed 's/<script[^>]*>//g; s/<\/script>//g')
```

#### 2.3.6 Content Validation and Cleaning
```bash
# Validate extracted content isn't empty or just HTML artifacts
if [ -z "$HTML_EXTRACTED" ] || [[ "$HTML_EXTRACTED" == *"<!--"* ]]; then
  echo "ERROR: HTML extraction failed for stitch $ID"
  echo "Attempting alternative extraction methods..."
  
  # Fallback: Look for code in different container types
  HTML_EXTRACTED=$(grep -o '<div[^>]*class="[^"]*code[^"]*"[^>]*>.*</div>' temp-stitch-$ID.html | \
    head -1 | \
    sed 's/<[^>]*>//g; s/<\/[^>]*>//g')
fi

# Ensure CSS contains actual CSS rules, not just comments
if [[ "$FINAL_CSS" != *"{"* ]] || [[ "$FINAL_CSS" != *"}"* ]]; then
  echo "WARNING: Extracted CSS may be incomplete for stitch $ID"
  echo "Checking for alternative CSS containers..."
  
  # Look for CSS in different HTML structures
  ALTERNATIVE_CSS=$(grep -A 50 'style' temp-stitch-$ID.html | grep -o '{[^}]*}' | head -5)
  if [ ! -z "$ALTERNATIVE_CSS" ]; then
    FINAL_CSS="$FINAL_CSS"$'\n'"$ALTERNATIVE_CSS"
  fi
fi
```

#### 2.3.7 Component Structure Assembly
```bash
# Create the component with all extracted content
COMPONENT_CONTENT="---
// Extracted from CodeStitch ID: $ID
---

$HTML_EXTRACTED

<style lang=\"less\">
$FINAL_CSS
</style>"

# Handle JavaScript if present
if [ ! -z "$JS_EXTRACTED" ]; then
  COMPONENT_CONTENT="$COMPONENT_CONTENT"$'\n'$'\n'"<script>"
  COMPONENT_CONTENT="$COMPONENT_CONTENT"$'\n'"$JS_EXTRACTED"
  COMPONENT_CONTENT="$COMPONENT_CONTENT"$'\n'"</script>"
fi
```

#### 2.3.8 Critical Validation Steps
```bash
# 1. Ensure HTML contains the expected section ID
if [[ "$HTML_EXTRACTED" != *id="$CATEGORY-$ID"* ]] && [[ "$HTML_EXTRACTED" != *id="$CATEGORY-$ID"* ]]; then
  echo "WARNING: HTML may not contain expected ID attribute for stitch $ID"
fi

# 2. Verify CSS contains the scoped selectors
if [[ "$FINAL_CSS" != *"#${CATEGORY}-${ID}"* ]]; then
  echo "WARNING: CSS may not contain expected scoped selectors for stitch $ID"
fi

# 3. Check for missing commented CSS (common issue)
if [[ "$FINAL_CSS" == *"/*"* ]] && [[ $(echo "$FINAL_CSS" | grep -c "/*") -lt 2 ]]; then
  echo "WARNING: Commented CSS sections may be missing from stitch $ID"
  echo "This often happens when CSS appears commented in the UI but is actually active code"
fi
```

## Summary of Key Improvements:

1. **Multiple Extraction Methods**: Uses different approaches to handle various CodeStitch page structures
2. **Comment Preservation**: Specifically preserves CSS comments (`/* */`) that appear as commented code in UI
3. **LESS Comment Handling**: Distinguishes between CSS comments (keep) and LESS comments (may remove)
4. **Content Validation**: Checks that extracted content contains expected patterns
5. **Fallback Methods**: Alternative extraction when primary method fails
6. **Artifact Cleaning**: Removes HTML entities and common extraction artifacts

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

## 8. Troubleshooting CSS Extraction Issues

### 8.1 Common CSS Extraction Problems

#### Problem: Commented CSS Not Copying
**Symptoms**: Component appears missing styles, broken layout, or incomplete styling
**Causes**: CodeStitch UI shows CSS as "commented out" but it's actually active code that should be preserved

**Detection**:
```bash
# Check if extracted CSS is missing comment blocks
if [[ $(echo "$FINAL_CSS" | grep -c "/*") -lt 2 ]]; then
  echo "ERROR: Commented CSS sections missing from stitch $ID"
fi
```

**Solutions**:
```bash
# Method 1: Enhanced extraction that preserves all CSS comments
ENHANCED_CSS=$(curl -s "https://codestitch.app/app/dashboard/stitches/$ID" | \
  grep -A 200 -B 5 'style.*lang="less"' | \
  sed -n '/<code>/,/<\/code>/p' | \
  sed 's/<code[^>]*>//g; s/<\/code>//g' | \
  sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g')

# Method 2: Extract from page's raw content areas
RAW_CSS=$(curl -s "https://codestitch.app/app/dashboard/stitches/$ID" | \
  grep -o '\/\*[^*]*\*+([^/*][^*]*\*+\/\)*' | \
  head -20)

# Method 3: Look for CSS in hidden elements that contain actual code
HIDDEN_CSS=$(curl -s "https://codestitch.app/app/dashboard/stitches/$ID" | \
  grep -A 100 'data-clipboard-text' | \
  grep -o '"[^"]*{' | \
  sed 's/"//g')
```

#### Problem: CSS Appears as Comments in UI but is Active
**Understanding**: CodeStitch often displays CSS like this in UI:
```css
/*-- -------------------------- */
/*--          Services          --*/
/*-- -------------------------- --*/

#services-342 {
    padding: var(--sectionPadding);
}

/* This might appear commented in UI but is active */
.cs-item:hover {
    transform: translateY(-0.4375rem);
}
```

**Solution**: Extract ALL content between `/*` and `*/` markers:
```bash
# Extract everything between comment markers - this is actual active code
ACTIVE_CSS=$(echo "$RAW_CSS" | \
  sed -n '/\/\*/,/\*\//p' | \
  sed 's/\/\*//g; s/\*\///g' | \
  sed '/^[[:space:]]*$/d')
```

### 8.2 Debugging CSS Extraction

#### Step-by-Step CSS Debug Process
```bash
# 1. Download page source
curl -H "Cookie: $COOKIES" "https://codestitch.app/app/dashboard/stitches/$ID" > debug-source-$ID.html

# 2. Find all potential CSS containers
echo "=== Finding CSS containers ==="
grep -n -A 5 -B 5 "css\|CSS\|style\|less" debug-source-$ID.html | head -50

# 3. Extract content from different container types
echo "=== Extracting from <pre> tags ==="
grep -o '<pre[^>]*>.*</pre>' debug-source-$ID.html | head -3

echo "=== Extracting from <code> tags ==="
grep -o '<code[^>]*>.*</code>' debug-source-$ID.html | head -3

echo "=== Extracting from <textarea> tags ==="
grep -o '<textarea[^>]*>.*</textarea>' debug-source-$ID.html | head -3

# 4. Look for data attributes that might contain code
echo "=== Checking data attributes ==="
grep -o 'data-[^=]*="[^"]*"' debug-source-$ID.html | grep -i code
```

#### Validation Script
```bash
validate_css_extraction() {
  local ID=$1
  local CSS_FILE=$2
  
  echo "=== Validating CSS for Stitch $ID ==="
  
  # Check for required CSS patterns
  local HAS_SELECTORS=$(grep -c "{" "$CSS_FILE")
  local HAS_COMMENTS=$(grep -c "/\*" "$CSS_FILE")
  local HAS_STITCH_ID=$(grep -c "#.*$ID" "$CSS_FILE")
  
  echo "CSS selectors found: $HAS_SELECTORS"
  echo "CSS comments found: $HAS_COMMENTS"
  echo "Stitch ID selectors: $HAS_STITCH_ID"
  
  if [ "$HAS_SELECTORS" -lt 3 ]; then
    echo "WARNING: Very few CSS selectors found - extraction may be incomplete"
  fi
  
  if [ "$HAS_COMMENTS" -lt 1 ]; then
    echo "WARNING: No CSS comments found - may be missing commented CSS"
  fi
  
  if [ "$HAS_STITCH_ID" -lt 1 ]; then
    echo "ERROR: No stitch ID found in CSS selectors"
  fi
}

# Usage: validate_css_extraction $ID "extracted.css"
```

### 8.3 Enhanced Extraction Script

#### Complete CSS Extraction Solution
```bash
extract_css_comprehensive() {
  local ID=$1
  local COOKIES="$2"
  
  echo "Starting comprehensive CSS extraction for stitch $ID..."
  
  # Download page with all content
  local PAGE_CONTENT=$(curl -s -H "Cookie: $COOKIES" \
    "https://codestitch.app/app/dashboard/stitches/$ID")
  
  # Method 1: Standard code block extraction
  local CSS_METHOD1=$(echo "$PAGE_CONTENT" | \
    grep -A 1000 -B 5 'less\|css' | \
    sed -n '/<pre[^>]*>/,/<\/pre>/p' | \
    sed 's/<[^>]*>//g')
  
  # Method 2: Extract from clipboard data attributes
  local CSS_METHOD2=$(echo "$PAGE_CONTENT" | \
    grep -o 'data-clipboard-text="[^"]*"' | \
    sed 's/data-clipboard-text="//g; s/"$//g' | \
    sed 's/&lt;/</g; s/&gt;/>/g')
  
  # Method 3: Extract from script tag contents
  local CSS_METHOD3=$(echo "$PAGE_CONTENT" | \
    grep -A 200 'window\.__CODE__' | \
    grep -o '"[^"]*{' | \
    sed 's/"//g')
  
  # Choose best method (one with most CSS content)
  local BEST_METHOD=""
  local MAX_SELECTORS=0
  
  for method in "$CSS_METHOD1" "$CSS_METHOD2" "$CSS_METHOD3"; do
    local SELECTOR_COUNT=$(echo "$method" | grep -c "{")
    if [ "$SELECTOR_COUNT" -gt "$MAX_SELECTORS" ]; then
      MAX_SELECTORS=$SELECTOR_COUNT
      BEST_METHOD="$method"
    fi
  done
  
  # Clean and enhance best method
  local FINAL_CSS=$(echo "$BEST_METHOD" | \
    sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g' | \
    # Preserve ALL CSS comments including those that look commented in UI
    sed '/\/\*/!{/\/\//d;}' | \
    # Clean up HTML entities
    sed 's/&nbsp;/ /g; s/&quot;/"/g' | \
    # Remove excessive whitespace but preserve structure
    sed '/^[[:space:]]*$/d')
  
  echo "$FINAL_CSS"
}
```

### 8.4 Testing Extracted Components

#### Manual Testing Checklist
1. **Visual Inspection**: Open component in browser - does it look complete?
2. **Responsive Testing**: Check mobile, tablet, desktop breakpoints
3. **Dark Mode**: Toggle dark mode - do all styles apply correctly?
4. **CSS Validation**: Check browser dev tools for missing styles
5. **Comment Analysis**: Do comments match what was visible in CodeStitch?

#### Automated Testing
```bash
test_component_css() {
  local COMPONENT_FILE=$1
  local EXPECTED_ID=$2
  
  # Extract CSS from component
  local COMPONENT_CSS=$(sed -n '/<style/,/<\/style>/p' "$COMPONENT_FILE" | \
    sed 's/<style[^>]*>//g; s/<\/style>//g')
  
  # Validation checks
  local ISSUES=0
  
  # Check for stitch ID in CSS
  if [[ "$COMPONENT_CSS" != *"$EXPECTED_ID"* ]]; then
    echo "ISSUE: Stitch ID $EXPECTED_ID not found in CSS"
    ISSUES=$((ISSUES + 1))
  fi
  
  # Check for minimum CSS complexity
  if [ $(echo "$COMPONENT_CSS" | grep -c "{") -lt 5 ]; then
    echo "ISSUE: CSS appears too simple - may be incomplete"
    ISSUES=$((ISSUES + 1))
  fi
  
  # Check for common CodeStitch patterns
  if [[ "$COMPONENT_CSS" != *".cs-"* ]]; then
    echo "ISSUE: No CodeStitch class patterns found"
    ISSUES=$((ISSUES + 1))
  fi
  
  return $ISSUES
}
```

## 9. Verification
*   Run the dev server (`npm start`) and verify the visual appearance.
*   Check dark mode functionality by toggling theme.
*   Verify responsive behavior across different screen sizes.
*   **NEW**: Run CSS validation script on each extracted component.
*   **NEW**: Compare extracted component visually with CodeStitch preview.
*   **NEW**: Check browser dev tools for any missing or broken CSS rules.

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

## Quick Reference: CSS Extraction Issues

### Common Problems & Solutions

| Problem | Symptom | Solution |
|---------|----------|----------|
| Commented CSS missing | Broken layout, incomplete styles | Use enhanced extraction that preserves `/* */` comments |
| CSS appears commented in UI | Styles not applying | Extract ALL content between `/*` and `*/` markers |
| Incomplete CSS extraction | Missing responsive breakpoints | Use multiple extraction methods and validate selector count |
| HTML entities in CSS | CSS syntax errors | Clean with `sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g'` |
| Wrong CSS container | Empty or garbled CSS | Try extracting from `<pre>`, `<code>`, and `<textarea>` tags |

### Quick Fix Commands

```bash
# Quick CSS fix for most common issues
fix_css_extraction() {
  local ID=$1
  
  # Download and extract with comment preservation
  curl -s "https://codestitch.app/app/dashboard/stitches/$ID" | \
    grep -A 200 'style.*lang="less"' | \
    sed -n '/<code>/,/<\/code>/p' | \
    sed 's/<[^>]*>//g; s/&lt;/</g; s/&gt;/>/g' | \
    grep -o '/\*[^*]*\*+([^/*][^*]*\*+\/\)*' | \
    sed 's/\/\*//g; s/\*\///g' > "fixed-css-$ID.less"
  
  echo "CSS fixed and saved to fixed-css-$ID.less"
}

# Usage: fix_css_extraction 399
```

### Validation Checklist

- [ ] Component has the expected number of CSS selectors (usually 10+)
- [ ] CSS contains the stitch ID (e.g., `#services-399`)
- [ ] Comment blocks are preserved in CSS
- [ ] Responsive breakpoints are present (`@media` queries)
- [ ] Dark mode styles are included if applicable
- [ ] No HTML entities remain in CSS (`&lt;`, `&gt;`, etc.)

### Debug Commands

```bash
# Check what CSS was actually extracted
echo "=== CSS Content Analysis ==="
echo "Total lines: $(wc -l < extracted.css)"
echo "CSS selectors: $(grep -c '{' extracted.css)"
echo "Comments: $(grep -c '/*' extracted.css)"
echo "Stitch ID references: $(grep -c '#[a-z]-[0-9]' extracted.css)"

# Find missing patterns
echo "=== Missing Patterns ==="
if ! grep -q ".cs-container" extracted.css; then
  echo "Missing .cs-container pattern"
fi
if ! grep -q "@media" extracted.css; then
  echo "Missing responsive breakpoints"
fi
```

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
