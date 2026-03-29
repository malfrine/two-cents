# Step 5: Add Railway Configuration & Health Check

## Goal
Add Railway config files so it knows how to build/deploy each service, and add a health check endpoint to the backend.

## Status: NOT STARTED

---

## Changes

### 5a. Create `backend/railway.toml` (NEW FILE)

```toml
[build]
dockerfilePath = "Dockerfile.prod"

[deploy]
healthcheckPath = "/api/health/"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### 5b. Create `frontend/railway.toml` (NEW FILE)

```toml
[build]
dockerfilePath = "Dockerfile.prod"

[deploy]
healthcheckPath = "/"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3
```

### 5c. Add health check endpoint — `backend/core/config/urls.py`

Add a simple `/api/health/` endpoint:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path("api/health/", health_check),
    # ... existing paths ...
]
```

---

## Files Modified
- `backend/core/config/urls.py`

## Files Created
- `backend/railway.toml`
- `frontend/railway.toml`

---

## Testing Plan

### Test 1: railway.toml files are valid TOML
```bash
python3 -c "
import tomllib
with open('backend/railway.toml', 'rb') as f:
    d = tomllib.load(f)
    assert d['build']['dockerfilePath'] == 'Dockerfile.prod'
    assert d['deploy']['healthcheckPath'] == '/api/health/'
    print(f'backend/railway.toml: {d}')
with open('frontend/railway.toml', 'rb') as f:
    d = tomllib.load(f)
    assert d['build']['dockerfilePath'] == 'Dockerfile.prod'
    assert d['deploy']['healthcheckPath'] == '/'
    print(f'frontend/railway.toml: {d}')
print('PASS: Both TOML files are valid')
"
```

### Test 2: Health check endpoint responds
```bash
# With docker-compose running:
docker-compose up -d
sleep 15
curl -s http://localhost:8000/api/health/
```
**Expected:** `{"status": "ok"}`

### Test 3: Health check does NOT require authentication
```bash
# No auth header — should still return 200
curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/health/
```
**Expected:** `200`

### Test 4: Validate railway.toml references existing Dockerfiles
```bash
# Ensure the referenced Dockerfiles actually exist
test -f backend/Dockerfile.prod && echo "PASS: backend Dockerfile.prod exists" || echo "FAIL"
test -f frontend/Dockerfile.prod && echo "PASS: frontend Dockerfile.prod exists" || echo "FAIL"
```
