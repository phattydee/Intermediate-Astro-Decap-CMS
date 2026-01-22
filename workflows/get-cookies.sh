#!/bin/bash

# Get cookies from codestitch.app using Playwright
# Usage: ./get-cookies.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COOKIES_FILE="$SCRIPT_DIR/cookies.txt"

echo "Opening browser to get cookies..."
echo "1. Navigate to https://codestitch.app/app/dashboard"
echo "2. Make sure you're logged in"
echo "3. The script will extract cookies automatically"
echo ""

# Use node with playwright to get cookies
node -e "
const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    
    await page.goto('https://codestitch.app/app/dashboard');
    
    // Wait for login
    console.log('Please log in if needed...');
    await page.waitForURL('**/app/dashboard**', { timeout: 60000 });
    
    // Get cookies
    const cookies = await page.context().cookies();
    
    // Format as cookie string
    const cookieStr = cookies.map(c => c.name + '=' + c.value).join('; ');
    
    console.log('');
    console.log('Cookies extracted:');
    console.log('');
    console.log(cookieStr);
    console.log('');
    console.log('Saved to: $COOKIES_FILE');
    
    // Save to file
    require('fs').writeFileSync('$COOKIES_FILE', cookieStr);
    
    await browser.close();
})();
"
