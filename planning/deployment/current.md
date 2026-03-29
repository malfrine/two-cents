# Current Step Tracker

## Active Step: NONE (not started yet)

## Progress Overview

| Step | Description | Status | Type |
|------|------------|--------|------|
| 1 | Make external services gracefully optional | NOT STARTED | Code changes |
| 2 | Add CORS support for split-origin deploy | NOT STARTED | Code changes |
| 3 | Update Dockerfiles for Railway build context | NOT STARTED | Code changes |
| 4 | Update frontend for configurable domain | NOT STARTED | Code changes |
| 5 | Add Railway config & health check endpoint | NOT STARTED | Code changes + new files |
| 6 | DNS configuration (2c.malfrine.com) | NOT STARTED | Manual (Vercel + Railway) |
| 7 | Railway project setup | NOT STARTED | Manual (Railway dashboard) |
| 8 | Post-deploy admin, seed data & smoke test | NOT STARTED | Manual |

**Steps 1-5** = code changes I make.
**Steps 6-8** = manual steps you do in Railway/Vercel dashboards.

---

## Current Working Notes

_This section gets updated as we work through each step._

### Blockers
- None yet

### Decisions Made
- Hosting platform: Railway (not Vercel, Render, or Fly.io)
- Domain: 2c.malfrine.com via CNAME from Vercel DNS to Railway
- Architecture: Frontend + Backend as separate Railway services + managed Postgres
- External services (Mailchimp, Sendinblue, Slack): make optional, don't need for portfolio

### Open Questions
- Do you have access to the Firebase project (two-cents-canada or two-cents-canada-dev)?
- Do you want to keep Stripe in test mode, or disable payments entirely?
- Do you want to push the repo to GitHub (currently seems to be on GitLab)?
