# Step 7: Railway Project Setup

## Goal
Create the Railway project, add services, and configure environment variables.

## Status: NOT STARTED

**This step is entirely manual — done in Railway dashboard/CLI.**

---

## Procedure

### 7a. Create Railway project
1. Go to [railway.app](https://railway.app), sign up/login
2. Create a new project
3. Connect your GitHub repo
   - If the repo is only on GitLab, push it to GitHub first:
     ```bash
     git remote add github git@github.com:malfrine/two-cents.git
     git push github master
     ```

### 7b. Add PostgreSQL
1. In the project, click **"New"** → **"Database"** → **"PostgreSQL"**
2. Railway auto-provisions and exposes these variables:
   - `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`
3. You'll reference these with `${{Postgres.PGDATABASE}}` syntax in other services

### 7c. Add Backend service
1. Click **"New"** → **"GitHub Repo"** → select your repo
2. In service settings, set **Root Directory** to `backend`
3. Railway detects `railway.toml` → uses `Dockerfile.prod`
4. Add environment variables (see 7e below)

### 7d. Add Frontend service
1. Click **"New"** → **"GitHub Repo"** → same repo, second service
2. Set **Root Directory** to `frontend`
3. Add environment variables (see 7f below)
4. **Important:** Toggle "Available at build time" for all variables (Nuxt bakes them in at build time)

### 7e. Backend environment variables
```
DEBUG=False
SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_urlsafe(50))">
DJANGO_HASHID_FIELD_SALT=<generate another random string>
ALLOWED_HOSTS=2c.malfrine.com,.railway.app
DOMAIN=https://2c.malfrine.com
POSTGRES_DB=${{Postgres.PGDATABASE}}
POSTGRES_USER=${{Postgres.PGUSER}}
POSTGRES_PASSWORD=${{Postgres.PGPASSWORD}}
POSTGRES_HOST=${{Postgres.PGHOST}}
POSTGRES_PORT=${{Postgres.PGPORT}}
CORS_ALLOWED_ORIGINS=https://2c.malfrine.com
STRIPE_TEST=true
STRIPE_TEST_PUBLISHABLE_KEY=<your stripe test key or empty>
STRIPE_TEST_SECRET_KEY=<your stripe test secret or empty>
FIREBASE_SA_PROJECT_ID=<from firebase console>
FIREBASE_SA_PRIVATE_KEY_ID=<from service account json>
FIREBASE_SA_PRIVATE_KEY=<from service account json, keep \n as literal \n>
FIREBASE_SA_CLIENT_EMAIL=<from service account json>
FIREBASE_SA_CLIENT_ID=<from service account json>
FIREBASE_CLIENT_CERT_URL=<from service account json>
```

### 7f. Frontend environment variables (build-time)
```
NUXT_HOST=0.0.0.0
NUXT_PORT=8000
AXIOS_BASE_URL=https://<backend-railway-public-url>
DOMAIN=https://2c.malfrine.com
STRIPE_TEST=true
STRIPE_TEST_PUBLISHABLE_KEY=<your stripe test key or empty>
SENTRY_DSN=
STRIPE_ACCOUNT=
STRIPE_PROD_PUBLISHABLE_KEY=
```

---

## Testing Plan

### Test 1: Backend deploys and health check passes
After deploying, Railway shows deployment logs. Check:
1. `pip install` completes
2. `coinor-cbc` installs
3. `python manage.py migrate` runs
4. `gunicorn` starts on port 8000
5. Health check at `/api/health/` returns green in Railway dashboard

```bash
curl -s https://<backend-railway-url>/api/health/
```
**Expected:** `{"status": "ok"}`

### Test 2: Frontend deploys and serves pages
```bash
curl -s https://<frontend-railway-url>/ | head -30
```
**Expected:** HTML content with Vue/Nuxt app markup.

### Test 3: Database is connected
```bash
curl -s https://<backend-railway-url>/admin/
```
**Expected:** Django admin login page renders (proves DB connection works since admin needs sessions table).

### Test 4: Frontend can reach backend API
Open `https://<frontend-railway-url>/` in browser, open Network tab, check for successful API calls (even if they return auth errors, a response means connectivity works).

### Test 5: Railway logs show no crashes
Check Railway dashboard → each service → Logs:
- No Python tracebacks
- No Node.js unhandled exceptions
- Gunicorn workers are running
