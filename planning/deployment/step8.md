# Step 8: Post-Deploy — Admin, Seed Data & Smoke Test

## Goal
Create a superuser, optionally seed data, and do a full end-to-end smoke test of the live site.

## Status: NOT STARTED

---

## Procedure

### 8a. Migrations (automatic)
The `gunicorn.sh` script runs `python manage.py migrate` on every container start.
Migrations should have already run during Step 7 deploy. Verify in Railway logs.

### 8b. Create superuser
Using Railway CLI:
```bash
railway link  # link to your project
railway run -s backend -- python manage.py createsuperuser
```
Or use Railway's web terminal (Service → Shell tab).

### 8c. (Optional) Seed published plans
Navigate to `https://<backend-railway-url>/admin/`:
1. Login with superuser credentials
2. Go to Published Plans → Add
3. Create 1-2 sample template plans so the landing page has content

### 8d. (Optional) Create a demo user
Either through the admin panel or the onboarding flow on the frontend.

---

## Testing Plan — Full End-to-End Smoke Test

### Test 1: Landing page loads
```bash
curl -s -o /dev/null -w "%{http_code}" https://2c.malfrine.com/
```
**Expected:** `200`

### Test 2: Static assets load (CSS, JS)
Open `https://2c.malfrine.com/` in browser:
- Page is styled (Vuetify dark theme, green primary color)
- No 404s in Network tab for CSS/JS files
- No console errors related to missing assets

### Test 3: Django admin works
```bash
curl -s -o /dev/null -w "%{http_code}" https://<backend-url>/admin/login/
```
**Expected:** `200` (login page renders)

### Test 4: Firebase auth flow
1. Go to `https://2c.malfrine.com/login`
2. Page renders login form
3. Firebase JS SDK loads (check Network tab for `firebase` requests)

### Test 5: API connectivity from frontend
1. Open browser dev tools → Network tab
2. Navigate through the app
3. Check that XHR requests to the backend URL return responses (not CORS errors)

### Test 6: Published plans display (if seeded)
1. Navigate to the published plans page
2. Template plans should render with financial data

### Test 7: Solver works (if user data exists)
1. Login with a test account
2. Fill in financial profile data
3. Request a financial plan
4. Backend logs should show Pyomo/CBC solver running
5. Plan results should display on the dashboard

### Test 8: SSL & security headers
```bash
# Check security headers
curl -s -I https://2c.malfrine.com/ | grep -iE "strict-transport|x-frame|x-content-type|content-security"
```
**Expected:** Basic security headers present (nuxt-helmet module adds these).

### Test 9: Performance baseline
```bash
# Simple response time check
curl -s -o /dev/null -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" https://2c.malfrine.com/
```
**Expected:** TTFB under 3 seconds (SSR page load on Railway).
