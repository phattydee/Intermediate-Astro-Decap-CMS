---
description: Authenticate with CodeStitch for automated code extraction
---

# CodeStitch Authentication Workflow

This workflow explains how to authenticate with CodeStitch when using automated tools like OpenCode, web scrapers, or API clients.

## Authentication Methods

CodeStitch uses session-based authentication. Here are the available methods:

---

## Method 1: Browser Session (Recommended for OpenCode)

**Best for**: OpenCode with Chrome DevTools MCP

### Steps:
1. **Log in manually** to CodeStitch in your Chrome browser
2. **Keep the browser open** and logged in
3. **Use Chrome DevTools MCP** to access the authenticated session
   - OpenCode can connect to your existing Chrome instance
   - The session cookies are automatically available

### Verification:
```javascript
// In Chrome DevTools Console (or via OpenCode)
document.cookie.includes('session') // Should return true if logged in
```

**Advantages**:
- ✅ No need to handle credentials programmatically
- ✅ Session persists as long as browser is open
- ✅ Works with 2FA/MFA if enabled

**Workflow to use**: `/port_codestitch_opencode`

---

## Method 2: Session Cookie Export

**Best for**: Web scrapers, API clients, headless automation

### Steps:

#### A. Export Cookies from Browser

**Option 1: Using Browser DevTools**
1. Log in to CodeStitch in your browser
2. Open DevTools (F12)
3. Go to **Application** tab → **Cookies** → `https://codestitch.app`
4. Find the session cookie (usually named `session`, `auth_token`, or similar)
5. Copy the **Name** and **Value**

**Option 2: Using Browser Extension**
1. Install a cookie export extension (e.g., "EditThisCookie", "Cookie-Editor")
2. Log in to CodeStitch
3. Click the extension icon
4. Export cookies as JSON or copy the session cookie value

#### B. Use Cookie in Requests

**For OpenCode Web Scraper**:
```bash
# If OpenCode supports cookie headers
opencode scrape --cookie "session=YOUR_SESSION_VALUE" "https://codestitch.app/app/dashboard/stitches/342"
```

**For curl/wget**:
```bash
# Using curl
curl -H "Cookie: session=YOUR_SESSION_VALUE" "https://codestitch.app/app/dashboard/stitches/342"

# Using wget
wget --header="Cookie: session=YOUR_SESSION_VALUE" "https://codestitch.app/app/dashboard/stitches/342"
```

**For Python (requests library)**:
```python
import requests

cookies = {
    'session': 'YOUR_SESSION_VALUE'
}

response = requests.get(
    'https://codestitch.app/app/dashboard/stitches/342',
    cookies=cookies
)
```

#### C. Cookie Expiration
- Session cookies typically expire after 24 hours or when you log out
- You'll need to re-export the cookie when it expires
- Check for 401/403 responses indicating expired session

---

## Method 3: Programmatic Login (Advanced)

**Best for**: Fully automated workflows, CI/CD pipelines

### Steps:

#### A. Inspect Login Flow
1. Open CodeStitch login page in browser with DevTools open
2. Go to **Network** tab
3. Log in and observe the requests
4. Note:
   - Login endpoint URL (e.g., `/api/auth/login`)
   - Request method (POST)
   - Required fields (email, password, CSRF token, etc.)
   - Response cookies/tokens

#### B. Implement Login Script

**Example (Python)**:
```python
import requests

# Step 1: Get CSRF token (if required)
session = requests.Session()
login_page = session.get('https://codestitch.app/login')
# Parse CSRF token from HTML if needed

# Step 2: Send login request
login_data = {
    'email': 'your-email@example.com',
    'password': 'your-password',
    # 'csrf_token': csrf_token  # If required
}

response = session.post(
    'https://codestitch.app/api/auth/login',  # Adjust URL
    data=login_data
)

# Step 3: Session object now has authenticated cookies
# Use it for subsequent requests
stitch_response = session.get(
    'https://codestitch.app/app/dashboard/stitches/342'
)
```

#### C. Handle 2FA/MFA
If CodeStitch uses two-factor authentication:
- You'll need to handle the 2FA code input
- Consider using TOTP libraries if using authenticator apps
- Or prompt user for 2FA code during script execution

---

## Method 4: API Key/Token (If Available)

**Best for**: Official API access (if CodeStitch provides it)

### Steps:
1. Check if CodeStitch offers API keys in account settings
2. Generate an API key
3. Use the key in request headers:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" "https://codestitch.app/api/stitches/342"
   ```

**Note**: As of this writing, CodeStitch may not offer public API access. Check their documentation.

---

## Troubleshooting

### Problem: "401 Unauthorized" or "403 Forbidden"
**Solutions**:
- ✅ Verify you're logged in to CodeStitch in your browser
- ✅ Check if session cookie has expired (re-export if needed)
- ✅ Ensure cookie is being sent with the request
- ✅ Try logging out and back in to get a fresh session

### Problem: "CSRF token mismatch"
**Solutions**:
- ✅ Include CSRF token in POST requests
- ✅ Extract token from login page HTML or cookies
- ✅ Ensure you're using the same session for token retrieval and request

### Problem: "Rate limited" or "Too many requests"
**Solutions**:
- ✅ Add delays between requests (e.g., 1-2 seconds)
- ✅ Reduce batch size
- ✅ Contact CodeStitch support for rate limit increase

### Problem: Login page redirects or captcha
**Solutions**:
- ✅ Use Method 1 (Browser Session) instead
- ✅ Complete captcha manually in browser, then export cookies
- ✅ Consider using browser automation (Puppeteer, Playwright)

---

## Security Best Practices

1. **Never commit credentials** to version control
   - Use environment variables: `process.env.CODESTITCH_EMAIL`
   - Use `.env` files (add to `.gitignore`)

2. **Rotate session cookies regularly**
   - Don't reuse old cookies
   - Log out when done

3. **Use read-only access** when possible
   - Don't automate account changes or purchases

4. **Respect rate limits**
   - Add delays between requests
   - Don't overwhelm the server

5. **Check Terms of Service**
   - Ensure automated access is permitted
   - Contact CodeStitch if unsure

---

## Recommended Workflow

**For most users**:
1. ✅ Use **Method 1** (Browser Session with Chrome DevTools MCP)
2. ✅ Follow the `/port_codestitch_opencode` workflow
3. ✅ Keep your browser logged in while extracting code

**For advanced automation**:
1. Use **Method 2** (Session Cookie Export)
2. Re-export cookies when they expire
3. Follow the `/opencode_stitch_port` workflow

**Avoid**:
- ❌ Method 3 (Programmatic Login) unless absolutely necessary
- ❌ Storing credentials in scripts or config files

---

## Quick Reference

| Method | Difficulty | Reliability | Security | Best For |
|--------|-----------|-------------|----------|----------|
| Browser Session | ⭐ Easy | ⭐⭐⭐ High | ⭐⭐⭐ High | OpenCode + DevTools |
| Cookie Export | ⭐⭐ Medium | ⭐⭐ Medium | ⭐⭐ Medium | Web scrapers |
| Programmatic Login | ⭐⭐⭐ Hard | ⭐ Low | ⭐ Low | CI/CD (if permitted) |
| API Key | ⭐ Easy | ⭐⭐⭐ High | ⭐⭐⭐ High | If available |

---

## Next Steps

After authenticating:
- Follow `/port_codestitch_opencode` for Chrome DevTools MCP approach
- Follow `/opencode_stitch_port` for web scraper approach
- Update `stitch-urls.txt` after each successful port