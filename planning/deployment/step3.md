# Step 3: Update Dockerfiles for Railway Build Context

## Goal
Railway builds each service from its own root directory. The current `Dockerfile.prod` files assume being built from the repo root. Fix the COPY paths.

## Status: NOT STARTED

---

## Changes

### 3a. `backend/Dockerfile.prod`

**Full replacement:**
```dockerfile
FROM python:3.8

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH="${PYTHONPATH}:/app/core/apps/pennies:/app/core"

RUN mkdir -p /app && mkdir -p /app/staticfiles
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install -y coinor-cbc

RUN pip install -r requirements.txt

EXPOSE 8000

RUN chmod +x ./scripts/gunicorn.sh

CMD ["./scripts/gunicorn.sh"]
```

**Key changes from original:**
- `COPY ./backend /app` → `COPY . /app` (Railway builds from `backend/` root)
- Removed `entrypoint.sh` reference (Railway Postgres is immediately available, no need to poll)
- CMD uses `gunicorn.sh` which already runs `collectstatic` + `migrate` + `gunicorn`

### 3b. `frontend/Dockerfile.prod`

**Key changes:**
```dockerfile
# Before:
COPY ./frontend/package.json ./frontend/package-lock.json /app/
COPY ./frontend/ /app/

# After:
COPY package.json package-lock.json /app/
COPY . /app/
```

Everything else stays the same (ARGs, ENVs, build, CMD).

---

## Files Modified
- `backend/Dockerfile.prod`
- `frontend/Dockerfile.prod`

---

## Testing Plan

### Test 1: Backend Docker image builds from backend/ directory
```bash
cd /Users/malfrine/Documents/code/projects/two-cents
docker build -t two-cents-backend-test -f backend/Dockerfile.prod ./backend
```
**Expected:** Image builds successfully. The `coinor-cbc` binary is installed and `pip install` completes.

### Test 2: Backend container starts and runs gunicorn
```bash
# Start postgres first for the backend to connect to
docker run -d --name tc-test-postgres \
  -e POSTGRES_DB=two-cents \
  -e POSTGRES_USER=postgresuser \
  -e POSTGRES_PASSWORD=mysecretpass \
  -p 5433:5432 \
  postgres:10-alpine

sleep 5

# Run backend container
docker run -d --name tc-test-backend \
  -e DEBUG=True \
  -e SECRET_KEY=test-key \
  -e DJANGO_HASHID_FIELD_SALT=test-salt \
  -e POSTGRES_DB=two-cents \
  -e POSTGRES_USER=postgresuser \
  -e POSTGRES_PASSWORD=mysecretpass \
  -e POSTGRES_HOST=host.docker.internal \
  -e POSTGRES_PORT=5433 \
  -e STRIPE_TEST=true \
  -e FIREBASE_SA_PROJECT_ID=fake \
  -e FIREBASE_SA_PRIVATE_KEY_ID=fake \
  -e FIREBASE_SA_PRIVATE_KEY=fake \
  -e FIREBASE_SA_CLIENT_EMAIL=fake@fake.iam.gserviceaccount.com \
  -e FIREBASE_SA_CLIENT_ID=12345 \
  -p 8001:8000 \
  two-cents-backend-test

sleep 10
docker logs tc-test-backend 2>&1 | tail -20
curl -s http://localhost:8001/api/health/
```
**Expected:** Gunicorn starts, migrations run, health check returns `{"status": "ok"}`.

### Test 3: Frontend Docker image builds from frontend/ directory
```bash
cd /Users/malfrine/Documents/code/projects/two-cents
docker build -t two-cents-frontend-test \
  --build-arg NUXT_HOST=0.0.0.0 \
  --build-arg NUXT_PORT=8000 \
  --build-arg AXIOS_BASE_URL=http://localhost:8001 \
  --build-arg DOMAIN=http://localhost:8000 \
  --build-arg STRIPE_TEST=true \
  --build-arg STRIPE_TEST_PUBLISHABLE_KEY="" \
  --build-arg SENTRY_DSN="" \
  --build-arg STRIPE_ACCOUNT="" \
  --build-arg STRIPE_PROD_PUBLISHABLE_KEY="" \
  -f frontend/Dockerfile.prod ./frontend
```
**Expected:** `npm install` and `npm run build` (Nuxt build) succeed.

### Test 4: Frontend container starts and serves pages
```bash
docker run -d --name tc-test-frontend -p 8002:8000 two-cents-frontend-test
sleep 5
curl -s http://localhost:8002/ | head -20
```
**Expected:** Returns HTML content (the Nuxt app's index page).

### Test 5: Cleanup
```bash
docker stop tc-test-backend tc-test-frontend tc-test-postgres 2>/dev/null
docker rm tc-test-backend tc-test-frontend tc-test-postgres 2>/dev/null
```

### Test 6: Original docker-compose still works
The dev `Dockerfile` (not `.prod`) and `docker-compose.yml` should be unaffected.
```bash
docker-compose up --build -d
sleep 15
curl -s http://localhost:8000/api/
docker-compose down
```
**Expected:** Dev environment works exactly as before.
