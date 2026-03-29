# Deployment Log — Instance 1

## Date: 2026-03-29

## Work Completed This Instance

### Step 1: Make external services optional
- Guarded Mailchimp init in settings.py (conditional import, `mailchimp = None` default)
- Sendinblue email falls back to console backend when key missing
- Slack webhook URL moved from hardcoded to env var
- Logging handlers conditionally include slack only when webhook is set
- Added `if mailchimp is None: return` guards to all 3 mailchimp.py functions
- Fixed Firebase authentication.py `os.environ.get().replace()` crash

### Step 2: Add CORS support
- Added `corsheaders` to THIRD_PARTY_APPS
- Added CorsMiddleware to MIDDLEWARE (before CommonMiddleware)
- Added CORS_ALLOWED_ORIGINS and CORS_ALLOW_CREDENTIALS settings

### Step 3: Fix Dockerfiles for Railway
- backend/Dockerfile.prod: `COPY ./backend /app` → `COPY . /app`
- frontend/Dockerfile.prod: `COPY ./frontend/...` → `COPY ...`

### Step 4: Frontend domain/stripe config
- Production domain now reads from `process.env.DOMAIN`
- STRIPE_TEST guarded against undefined with `|| 'true'`

### Step 5: Railway config + health check
- Created backend/railway.toml and frontend/railway.toml
- Added /api/health/ endpoint to urls.py

## Notes
- Did not run docker-compose integration tests (steps 1-5 testing plans include docker tests that require running containers)
- All changes are on the `mdas/deployment` branch
- Steps 6-8 are manual (DNS, Railway setup, smoke test) — left for the user

## Blockers Encountered
- Pre-existing `gevent==20.9.0` build failure — fixed by bumping to `21.12.0` (greenlet to `1.1.3`)
- Docker daemon was not initially running — user started it mid-session
- No local venv — all Python tests ran inside Docker containers

## For Next Instance
- Steps 1-5 are DONE and committed (`228552d`)
- Steps 6-8 are manual — guide the user interactively through Railway dashboard, DNS, and smoke testing
- The dev Dockerfile (`backend/Dockerfile`, not `.prod`) may also have the gevent issue but was NOT touched — it's for local dev only
