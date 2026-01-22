import subprocess
import re
import os
import sys
from pathlib import Path

def run_curl(url, cookies):
    """Fetch HTML content using curl with cookies."""
    cmd = [
        "curl", "-s", "-L",
        "-H", "Cookie: " + cookies,
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def parse_stitch_html(html_content):
    """Extract the stitch section HTML from the textarea in CodeStitch dashboard."""
    # CodeStitch uses <textarea class="CODE-TEXTAREA" data-cmtype="application/xml">
    pattern = r'<textarea[^>]*class="CODE-TEXTAREA"[^>]*data-cmtype="application/xml"[^>]*>(.*?)</textarea>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        # Code is HTML-encoded, need to decode
        import html
        encoded_html = match.group(1)
        decoded_html = html.unescape(encoded_html)
        # Clean up whitespace
        lines = decoded_html.strip().split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return '\n'.join(cleaned_lines)
    return None

def parse_stitch_styles(html_content):
    """Extract CSS/LESS styles from the textarea in CodeStitch dashboard."""
    pattern = r'<textarea[^>]*class="CODE-TEXTAREA"[^>]*data-cmtype="css"[^>]*>(.*?)</textarea>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    if not matches:
        return None
    
    import html
    candidates = []
    
    for encoded_css in matches:
        decoded_css = html.unescape(encoded_css).strip()
        # LESS syntax indicators: (1280/16rem), (630/16rem), nested @keyframes
        has_less_values = '(1280/16rem)' in decoded_css or '(630/16rem)' in decoded_css
        has_nested_rules = decoded_css.count('{') > 20 and '@keyframes' in decoded_css
        
        if has_less_values or has_nested_rules:
            candidates.append((len(decoded_css), decoded_css))
    
    # Return the longest LESS candidate (there are CSS, LESS, SCSS versions)
    if candidates:
        candidates.sort(reverse=True)
        return candidates[0][1]
    
    # Fallback to first CSS
    return html.unescape(matches[0]).strip()

def parse_dark_mode(html_content):
    """Extract dark mode styles - these are typically included in the LESS/CSS."""
    # Dark mode is usually already in the LESS/CSS code, no separate extraction needed
    return None

def parse_stitch_scripts(html_content):
    """Extract JavaScript from the textarea in CodeStitch dashboard."""
    pattern = r'<textarea[^>]*class="CODE-TEXTAREA"[^>]*data-cmtype="javascript"[^>]*>(.*?)</textarea>'
    match = re.search(pattern, html_content, re.DOTALL)
    if match:
        import html
        encoded_js = match.group(1)
        decoded_js = html.unescape(encoded_js).strip()
        return decoded_js
    return None

def extract_name_from_url(url):
    """Extract component name from URL if pattern matches."""
    # Try to extract from URL like /dashboard/stitches/374
    match = re.search(r'/stitches/(\d+)', url)
    if match:
        number = match.group(1)
        return number
    return None

def guess_component_name(html_content, url):
    """Try to guess the component name from the HTML."""
    # First try from URL
    number = extract_name_from_url(url)
    if number:
        # Try to find ID in the content to determine type
        id_pattern = r'id="([^"]*)"'
        match = re.search(id_pattern, html_content)
        if match:
            section_id = match.group(1)
            # Guess component type from ID prefix
            if 'hero' in section_id.lower():
                return f"Hero{number}"
            elif 'sbsr' in section_id.lower():
                return f"SBSR{number}"
            elif 'sbs' in section_id.lower():
                return f"SBS{number}"
            elif 'stats' in section_id.lower():
                return f"Stats{number}"
            elif 'services' in section_id.lower():
                return f"Services{number}"
            elif 'faq' in section_id.lower():
                return f"FAQ{number}"
            elif 'reviews' in section_id.lower():
                return f"Reviews{number}"
            elif 'pricing' in section_id.lower():
                return f"Pricing{number}"
            elif 'gallery' in section_id.lower():
                return f"Gallery{number}"
            elif 'meet' in section_id.lower():
                return f"MeetUs{number}"
            elif 'contact' in section_id.lower():
                return f"Contact{number}"
            elif 'footer' in section_id.lower():
                return f"Footer{number}"
            elif 'why-choose' in section_id.lower():
                return f"WhyChooseUs{number}"
            elif 'cta' in section_id.lower() or 'call to action' in section_id.lower():
                return f"CTA{number}"
            elif 'steps' in section_id.lower():
                return f"Steps{number}"
            elif 'events' in section_id.lower():
                return f"Events{number}"
            elif 'blog' in section_id.lower() or 'posts' in section_id.lower():
                return f"Blog{number}"
            elif 'content' in section_id.lower():
                return f"Content{number}"
            elif 'locations' in section_id.lower():
                return f"Locations{number}"
            else:
                # Just use number as generic Component
                return f"Component{number}"

    # Try to find ID in the HTML
    id_pattern = r'id="([^"]*)"'
    match = re.search(id_pattern, html_content)
    if match:
        section_id = match.group(1)
        numbers = re.findall(r'\d+', section_id)
        if numbers:
            number = numbers[0]
            if 'hero' in section_id.lower():
                return f"Hero{number}"
            elif 'sbsr' in section_id.lower():
                return f"SBSR{number}"
            elif 'sbs' in section_id.lower():
                return f"SBS{number}"
            elif 'stats' in section_id.lower():
                return f"Stats{number}"
            elif 'services' in section_id.lower():
                return f"Services{number}"
            elif 'faq' in section_id.lower():
                return f"FAQ{number}"
            elif 'reviews' in section_id.lower():
                return f"Reviews{number}"
            elif 'pricing' in section_id.lower():
                return f"Pricing{number}"
            elif 'gallery' in section_id.lower():
                return f"Gallery{number}"
            elif 'meet' in section_id.lower():
                return f"MeetUs{number}"
            elif 'contact' in section_id.lower():
                return f"Contact{number}"
            elif 'footer' in section_id.lower():
                return f"Footer{number}"
            elif 'why-choose' in section_id.lower():
                return f"WhyChooseUs{number}"
            elif 'cta' in section_id.lower():
                return f"CTA{number}"
            elif 'steps' in section_id.lower():
                return f"Steps{number}"
            elif 'events' in section_id.lower():
                return f"Events{number}"
            elif 'blog' in section_id.lower() or 'posts' in section_id.lower():
                return f"Blog{number}"
            else:
                return f"Component{number}"

    return None

def guess_component_folder(component_name):
    """Guess the folder based on component name prefix."""
    prefixes = {
        'Hero': 'Hero',
        'SBSR': 'SideBySideReverse',
        'SBS': 'SideBySide',
        'Stats': 'Stats',
        'Services': 'Services',
        'FAQ': 'FAQ',
        'Reviews': 'Reviews',
        'Pricing': 'Pricing',
        'Gallery': 'Gallery',
        'MeetUs': 'MeetOurTeam',
        'Contact': 'Contact',
        'Footer': 'Footer',
        'WhyChooseUs': 'WhyChooseUs',
        'CTA': 'CTA',
        'Steps': 'Steps',
        'Events': 'Events',
        'Blog': 'Blog',
        'Content': 'Content',
        'Locations': 'Locations',
    }

    for prefix, folder in prefixes.items():
        if component_name.startswith(prefix):
            return folder

    return 'Hero'

def create_astro_component(component_name, html_content, styles, scripts):
    """Create the Astro component file."""
    folder = guess_component_folder(component_name)

    # Create folder if it doesn't exist
    folder_path = Path(f"src/components/{folder}")
    folder_path.mkdir(parents=True, exist_ok=True)

    # Build the component content
    component_content = f"""---

---

<!-- ============================================ --><!--            {component_name}              --><!-- ============================================ -->
{html_content}
"""

    if scripts:
        component_content += f"""

<script>
    {scripts}
</script>
"""

    if styles:
        component_content += f"""

<style lang="less">
    {styles}
</style>
"""

    # Write the component file
    file_path = folder_path / f"{component_name}.astro"
    file_path.write_text(component_content)

    return str(file_path)

def update_stitch_preview(component_name, folder):
    """Update the stitch-preview.astro file with the new component."""
    preview_file = Path("src/pages/stitch-preview.astro")
    content = preview_file.read_text()

    # Add import if not already present
    import_line = f'import {component_name} from "@components/{folder}/{component_name}.astro";'
    if import_line not in content:
        # Find the last import and add after it
        lines = content.split('\n')
        last_import_idx = -1
        for i, line in enumerate(lines):
            if line.strip().startswith('import '):
                last_import_idx = i

        if last_import_idx >= 0:
            lines.insert(last_import_idx + 1, import_line)
            content = '\n'.join(lines)

    # Add usage section if not already present
    usage_section = f"""            <h3 style="text-align: center; padding: 10px; margin-top: 100px;">
                {component_name}
            </h3>
            <{component_name} />
"""
    if usage_section not in content:
        # Add before the closing tags
        content = content.replace('        </section>\n    </div>\n</BaseLayout>', usage_section + '        </section>\n    </div>\n</BaseLayout>')

    preview_file.write_text(content)

def main():
    if len(sys.argv) < 3:
        print("Usage: python import_stitch.py <url> <cookies>")
        print("Example: python import_stitch.py https://codestitch.app/intermediate/hero-362/ \"session=abc123; token=xyz789\"")
        sys.exit(1)

    url = sys.argv[1]
    cookies = sys.argv[2]

    print(f"Fetching stitch from: {url}")

    # Fetch the HTML
    html = run_curl(url, cookies)

    if not html:
        print("Error: Failed to fetch HTML content")
        sys.exit(1)

    # Parse the content
    html_content = parse_stitch_html(html)
    styles = parse_stitch_styles(html)
    scripts = parse_stitch_scripts(html)
    # dark_mode is now included in styles (LESS/CSS)

    if not html_content:
        print("Error: Could not extract stitch content from HTML")
        sys.exit(1)

    # Guess component name
    component_name = guess_component_name(html_content, url)

    if not component_name:
        print("Error: Could not determine component name from HTML")
        sys.exit(1)

    print(f"Component name: {component_name}")

    # Create the component
    file_path = create_astro_component(component_name, html_content, styles, scripts)
    print(f"Created component: {file_path}")

    # Update preview file
    folder = guess_component_folder(component_name)
    update_stitch_preview(component_name, folder)
    print(f"Updated stitch-preview.astro with {component_name}")

    print("\nDone! Component has been created and added to the preview page.")

if __name__ == "__main__":
    main()
