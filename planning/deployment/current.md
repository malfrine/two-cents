# Current Step Tracker

## Active Step: ALL CODE STEPS DONE (Steps 1-5 complete, pending commit)

## Progress Overview

| Step | Description | Status | Type |
|------|------------|--------|------|
| 1 | Make external services gracefully optional | DONE | Code changes |
| 2 | Add CORS support for split-origin deploy | DONE | Code changes |
| 3 | Update Dockerfiles for Railway build context | DONE | Code changes |
| 4 | Update frontend for configurable domain | DONE | Code changes |
| 5 | Add Railway config & health check endpoint | DONE | Code changes + new files |
| 6 | DNS configuration (2c.malfrine.com) | NOT STARTED | Manual (Vercel + Railway) |
| 7 | Railway project setup | NOT STARTED | Manual (Railway dashboard) |
| 8 | Post-deploy admin, seed data & smoke test | NOT STARTED | Manual |

**Steps 1-5** = code changes (DONE).
**Steps 6-8** = manual steps you do in Railway/Vercel dashboards.

---

## Current Working Notes

### Blockers
- None

### Decisions Made
- Hosting platform: Railway (not Vercel, Render, or Fly.io)
- Domain: 2c.malfrine.com via CNAME from Vercel DNS to Railway
- Architecture: Frontend + Backend as separate Railway services + managed Postgres
- External services (Mailchimp, Sendinblue, Slack): made optional, don't need for portfolio
- Slack webhook URL no longer hardcoded — removed leaked webhook from source

### Open Questions
- Do you have access to the Firebase project (two-cents-canada or two-cents-canada-dev)?
- Do you want to keep Stripe in test mode, or disable payments entirely?
- Do you want to push the repo to GitHub (currently seems to be on GitLab)?
