# Deployment Plan — Two Cents to Railway at 2c.malfrine.com

## For Claude: How to Navigate This

You are deploying a failed startup called "Two Cents" (DIY financial planning with a MILP solver) as a portfolio project on Railway.

### Quick Context
- **Stack:** Django 3.1 backend + Nuxt 2 (Vue) frontend + PostgreSQL + Pyomo/CBC solver
- **Target:** Host at `2c.malfrine.com` on Railway (~$5/mo)
- **Why not Vercel:** Backend is Django with a system binary (`coinor-cbc`). Vercel can't do this.
- **Branch:** `mdas/deployment`

### File Structure
```
planning/deployment/
  README.md        ← You are here. Start here every session.
  current.md       ← Track which step is active, blockers, and working notes. UPDATE THIS.
  step1.md         ← Make external services optional (Mailchimp, Sendinblue, Slack, Firebase)
  step2.md         ← Add CORS support (django-cors-headers)
  step3.md         ← Fix Dockerfiles for Railway build context
  step4.md         ← Make frontend domain/stripe configurable
  step5.md         ← Railway config files + health check endpoint
  step6.md         ← DNS setup (manual — user does this)
  step7.md         ← Railway project creation (manual — user does this)
  step8.md         ← Post-deploy smoke test (manual — user does this)
  logs/            ← Working logs from each Claude instance
    log1.md        ← Instance 1 log
    log2.md        ← Instance 2 log (and so on)
```

### Instance Logging
Each Claude instance should create a log file in `planning/deployment/logs/`:
- Check for existing log files and create the next one: `log{N+1}.md`
- Record: what you worked on, decisions made, blockers, and anything the next instance needs to know
- Update this log at the end of your session before committing

### How to Work

1. **Read `current.md` first** to see where we left off.
2. **Read the step file** for the current step (e.g., `step1.md`).
3. **Break work into testable chunks.** Do ONE step at a time. After making the code changes for a step, run the tests from that step's testing plan BEFORE moving to the next step. Write tests if needed. Do NOT batch all steps and test at the end.
4. **Run the tests** from the step's testing plan after making changes. If tests can't run locally (e.g. Docker not running, no venv), note this as a blocker and ask the user how to proceed.
5. **Update `current.md`** — mark the step as DONE only after tests pass, note any issues, move to next step.
6. **Do NOT commit automatically.** At the end of your session, present a summary of all changes to the user and wait for their explicit approval before committing. Commit with a message like: `step 1: make external services optional`

### Steps 1-5 are code changes. Steps 6-8 are manual (the user does them).

### Key Files You'll Be Editing
- `backend/core/config/settings.py` — Steps 1, 2
- `backend/core/apps/email/mailchimp.py` — Step 1
- `backend/core/apps/firebase/authentication.py` — Step 1
- `backend/Dockerfile.prod` — Step 3
- `frontend/Dockerfile.prod` — Step 3
- `frontend/nuxt.config.js` — Step 4
- `backend/core/config/urls.py` — Step 5
- `backend/railway.toml` — Step 5 (new file)
- `frontend/railway.toml` — Step 5 (new file)

### Important Codebase Notes
- Backend uses `django-environ` for env vars: `env.str("KEY", default="fallback")`
- The `mailchimp` object is imported from settings by `backend/core/apps/email/mailchimp.py` and used in `onboarding/views.py` and `users/utilities.py`
- Firebase auth module (`backend/core/apps/firebase/authentication.py`) initializes at import time — will crash if env vars are None
- The Nuxt config evaluates `process.env.STRIPE_TEST.toLowerCase()` at module load — crashes if undefined
- `gunicorn.sh` already runs `collectstatic` + `migrate` before starting gunicorn
- The dev `Dockerfile` (no `.prod` suffix) and `docker-compose.yml` are for local dev — don't touch these
