# Step 2: Add CORS Support for Split-Origin Deploy

## Goal
Frontend and backend will be on different Railway URLs. The frontend makes XHR requests to the backend, so CORS headers are required. `django-cors-headers` is already in `requirements.txt` but not configured.

## Status: NOT STARTED

---

## Changes

### 2a. `backend/core/config/settings.py` — Add to INSTALLED_APPS

```python
THIRD_PARTY_APPS = [
    "rest_framework",
    "django_extensions",
    "whitenoise",
    "anymail",
    "corsheaders",  # <-- add
]
```

### 2b. `backend/core/config/settings.py` — Add to MIDDLEWARE

Must be placed **after** SecurityMiddleware and SessionMiddleware, **before** CommonMiddleware:

```python
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",        # <-- add here
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
```

### 2c. `backend/core/config/settings.py` — Add CORS settings

```python
# CORS
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[
    "http://localhost:8000",
    "http://localhost:3000",
])
CORS_ALLOW_CREDENTIALS = True
```

In production env vars: `CORS_ALLOWED_ORIGINS=https://2c.malfrine.com`

---

## Files Modified
- `backend/core/config/settings.py`

---

## Testing Plan

### Test 1: CORS middleware is active
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) python -c "
from core.config.settings import MIDDLEWARE, INSTALLED_APPS
assert 'corsheaders' in INSTALLED_APPS, 'corsheaders not in INSTALLED_APPS'
assert 'corsheaders.middleware.CorsMiddleware' in MIDDLEWARE, 'CorsMiddleware not in MIDDLEWARE'
# Check ordering: CorsMiddleware must come before CommonMiddleware
cors_idx = MIDDLEWARE.index('corsheaders.middleware.CorsMiddleware')
common_idx = MIDDLEWARE.index('django.middleware.common.CommonMiddleware')
assert cors_idx < common_idx, f'CorsMiddleware ({cors_idx}) must be before CommonMiddleware ({common_idx})'
print('PASS: CORS middleware correctly configured')
"
```

### Test 2: Default CORS allows localhost
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) python -c "
from core.config.settings import CORS_ALLOWED_ORIGINS
assert 'http://localhost:8000' in CORS_ALLOWED_ORIGINS
print(f'PASS: CORS_ALLOWED_ORIGINS = {CORS_ALLOWED_ORIGINS}')
"
```

### Test 3: CORS env var override works
```bash
cd backend && CORS_ALLOWED_ORIGINS=https://2c.malfrine.com env $(cat /tmp/test-minimal.env | xargs) python -c "
from core.config.settings import CORS_ALLOWED_ORIGINS
assert 'https://2c.malfrine.com' in CORS_ALLOWED_ORIGINS
print(f'PASS: CORS override works = {CORS_ALLOWED_ORIGINS}')
"
```

### Test 4: Preflight request returns CORS headers (with docker-compose)
```bash
docker-compose up -d
sleep 10
# Send OPTIONS preflight request
curl -s -I -X OPTIONS \
  -H "Origin: http://localhost:8000" \
  -H "Access-Control-Request-Method: GET" \
  http://localhost:8000/api/ \
  | grep -i "access-control"
docker-compose down
```
**Expected:** Response includes `Access-Control-Allow-Origin` header.
