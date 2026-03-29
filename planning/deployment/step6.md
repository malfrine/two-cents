# Step 6: DNS Configuration

## Goal
Point `2c.malfrine.com` to the Railway frontend service.

## Status: NOT STARTED

**This step is entirely manual — no code changes.**

---

## Procedure

### 6a. Get Railway's CNAME target
1. In Railway dashboard, go to the **frontend** service
2. Settings → Networking → Custom Domain
3. Add `2c.malfrine.com`
4. Railway will display a CNAME target (e.g., `something.up.railway.app`)
5. Copy this value

### 6b. Add DNS record in Vercel
1. Go to Vercel Dashboard → `malfrine.com` project → Settings → Domains
2. Add a new DNS record:
   - **Type:** CNAME
   - **Name:** `2c`
   - **Value:** `<railway-cname-target>` (from step 6a)
3. Save

### 6c. Wait for propagation
- DNS propagation typically takes 1-10 minutes
- Railway auto-provisions SSL via Let's Encrypt once DNS resolves

### 6d. Backend URL
- The backend does NOT need a custom domain
- Railway gives it a URL like `two-cents-backend-production.up.railway.app`
- This URL goes into the frontend's `AXIOS_BASE_URL` env var

---

## Testing Plan

### Test 1: DNS resolves correctly
```bash
# After setting up DNS, verify the CNAME
dig 2c.malfrine.com CNAME +short
```
**Expected:** Returns the Railway CNAME target.

### Test 2: HTTPS works
```bash
curl -s -o /dev/null -w "%{http_code}" https://2c.malfrine.com/
```
**Expected:** `200` (or `302` redirect to login, depending on the app's root behavior).

### Test 3: SSL certificate is valid
```bash
echo | openssl s_client -servername 2c.malfrine.com -connect 2c.malfrine.com:443 2>/dev/null | openssl x509 -noout -dates
```
**Expected:** Shows valid certificate dates from Let's Encrypt.

### Test 4: API requests work cross-origin
Open browser dev tools at `https://2c.malfrine.com`, check Network tab:
- API calls to the backend Railway URL should succeed
- No CORS errors in console
- `Access-Control-Allow-Origin` header present on responses
