# Step 1: Make External Services Gracefully Optional

## Goal
The app hard-crashes on import if Mailchimp/Sendinblue/Slack/Firebase API keys are missing. For a portfolio deploy we don't need these services, but the app must boot without them.

## Status: NOT STARTED

---

## Changes

### 1a. `backend/core/config/settings.py` — Mailchimp

**Current (line 329-336, crashes if env vars missing):**
```python
from mailchimp_marketing import Client
mailchimp = Client()
mailchimp.set_config({
    "api_key": env.str("MAILCHIMP_API_KEY"),
    "server": env.str("MAILCHIMP_SERVER_PREFIX"),
})
```

**Change to:**
```python
mailchimp = None
_mailchimp_api_key = env.str("MAILCHIMP_API_KEY", default="")
_mailchimp_server = env.str("MAILCHIMP_SERVER_PREFIX", default="")
if _mailchimp_api_key and _mailchimp_server:
    from mailchimp_marketing import Client
    mailchimp = Client()
    mailchimp.set_config({"api_key": _mailchimp_api_key, "server": _mailchimp_server})
```

### 1b. `backend/core/config/settings.py` — Sendinblue (email)

**Current (line 74-81, crashes in production if key missing):**
```python
else:
    EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
    ANYMAIL = {"SENDINBLUE_API_KEY": env.str("SENDINBLUE_API_KEY")}
```

**Change to:**
```python
else:
    _sendinblue_key = env.str("SENDINBLUE_API_KEY", default="")
    if _sendinblue_key:
        EMAIL_BACKEND = "anymail.backends.sendinblue.EmailBackend"
        ANYMAIL = {"SENDINBLUE_API_KEY": _sendinblue_key}
    else:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
```

### 1c. `backend/core/config/settings.py` — Slack logger

**Current (line 339-341, hardcoded webhook URL):**
```python
SLACK_WEBHOOK_URL = (
    "https://hooks.slack.com/services/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"
)
```

**Change to:**
```python
SLACK_WEBHOOK_URL = env.str("SLACK_WEBHOOK_URL", default="")
```

**Also update logging root handlers (line 267):**
```python
# Current:
"handlers": ["console"] if DEBUG else ["sentry", "slack"],

# Change to:
_prod_handlers = ["sentry"]
if SLACK_WEBHOOK_URL:
    _prod_handlers.append("slack")

# Then in LOGGING dict:
"handlers": ["console"] if DEBUG else _prod_handlers,
```

### 1d. `backend/core/apps/email/mailchimp.py` — Guard all functions

Add `if mailchimp is None: return` at the top of:
- `create_mailchimp_user()`
- `set_mailchimp_user_as_premium()`
- `delete_mailchimp_user()`

### 1e. `backend/core/apps/firebase/authentication.py` — Guard initialization

**Current (line 18, crashes if env var missing):**
```python
"private_key": os.environ.get("FIREBASE_SA_PRIVATE_KEY").replace("\\n", "\n"),
```

**Change to:**
```python
"private_key": (os.environ.get("FIREBASE_SA_PRIVATE_KEY") or "").replace("\\n", "\n"),
```

### 1f. Stripe — No changes needed
Already has defaults of `""` for test keys.

---

## Files Modified
- `backend/core/config/settings.py`
- `backend/core/apps/email/mailchimp.py`
- `backend/core/apps/firebase/authentication.py`

---

## Testing Plan

### Test 1: Backend boots without ANY optional env vars
```bash
# Create a minimal .env with ONLY required vars (db + django basics)
cat > /tmp/test-minimal.env << 'EOF'
DEBUG=True
SECRET_KEY=test-secret-key-for-local-testing
DJANGO_HASHID_FIELD_SALT=test-salt-value
POSTGRES_DB=two-cents
POSTGRES_USER=postgresuser
POSTGRES_PASSWORD=mysecretpass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
STRIPE_TEST=true
FIREBASE_SA_PROJECT_ID=fake-project
FIREBASE_SA_PRIVATE_KEY_ID=fake-key-id
FIREBASE_SA_PRIVATE_KEY=fake-key
FIREBASE_SA_CLIENT_EMAIL=fake@fake.iam.gserviceaccount.com
FIREBASE_SA_CLIENT_ID=12345
EOF

# Try to import settings (should NOT crash)
cd backend && env $(cat /tmp/test-minimal.env | xargs) python -c "from core.config import settings; print('Settings loaded OK')"
```
**Expected:** Prints "Settings loaded OK" without crashing.

### Test 2: Mailchimp is None when keys missing
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) python -c "
from core.config.settings import mailchimp
assert mailchimp is None, 'mailchimp should be None without keys'
print('PASS: mailchimp is None')
"
```

### Test 3: Mailchimp functions no-op when disabled
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) python -c "
from core.apps.email.mailchimp import create_mailchimp_user, delete_mailchimp_user
# These should silently return None, not crash
create_mailchimp_user(None, None)
delete_mailchimp_user(None)
print('PASS: mailchimp functions no-op')
"
```

### Test 4: Email backend falls back to console in prod mode
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) DEBUG=False python -c "
from core.config.settings import EMAIL_BACKEND
assert EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend', f'Got {EMAIL_BACKEND}'
print('PASS: email falls back to console backend')
"
```

### Test 5: Slack handler excluded from logging when no webhook
```bash
cd backend && env $(cat /tmp/test-minimal.env | xargs) DEBUG=False python -c "
from core.config.settings import LOGGING
handlers = LOGGING['root']['handlers']
assert 'slack' not in handlers, f'slack should not be in handlers: {handlers}'
print(f'PASS: prod handlers = {handlers}')
"
```

### Test 6: docker-compose still works (existing dev flow not broken)
```bash
docker-compose up --build -d
# Wait for services to be healthy
sleep 15
curl -s http://localhost:8000/api/ | head -20
docker-compose down
```
**Expected:** Backend responds to API requests as before.
