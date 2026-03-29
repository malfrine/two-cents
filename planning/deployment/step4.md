# Step 4: Update Frontend for Configurable Domain

## Goal
The frontend hardcodes `https://two-cents.ca` as the production domain and crashes if `STRIPE_TEST` env var is undefined. Make both configurable/safe.

## Status: NOT STARTED

---

## Changes

### 4a. `frontend/nuxt.config.js` — Production domain from env

**Current (line 29):**
```javascript
domain = 'https://two-cents.ca'
```

**Change to:**
```javascript
domain = process.env.DOMAIN || 'https://two-cents.ca'
```

### 4b. `frontend/nuxt.config.js` — Guard STRIPE_TEST

**Current (line 31, crashes if STRIPE_TEST is undefined):**
```javascript
const isProdStripe = process.env.STRIPE_TEST.toLowerCase() === 'false'
```

**Change to:**
```javascript
const isProdStripe = (process.env.STRIPE_TEST || 'true').toLowerCase() === 'false'
```

---

## Files Modified
- `frontend/nuxt.config.js`

---

## Testing Plan

### Test 1: Nuxt config loads without STRIPE_TEST env var
```bash
cd /Users/malfrine/Documents/code/projects/two-cents/frontend
# Unset STRIPE_TEST and try to evaluate the config
node -e "
delete process.env.STRIPE_TEST;
process.env.NODE_ENV = 'production';
// Simulate the config logic
const isProdStripe = (process.env.STRIPE_TEST || 'true').toLowerCase() === 'false';
console.log('isProdStripe:', isProdStripe);
console.assert(isProdStripe === false, 'Should default to test stripe');
console.log('PASS: No crash without STRIPE_TEST');
"
```

### Test 2: DOMAIN env var is respected in production mode
```bash
cd /Users/malfrine/Documents/code/projects/two-cents/frontend
node -e "
process.env.NODE_ENV = 'production';
process.env.DOMAIN = 'https://2c.malfrine.com';
process.env.STRIPE_TEST = 'true';
const config = require('./nuxt.config.js');
const domain = config.default ? config.default.env.baseUrl : config.env.baseUrl;
console.log('domain:', domain);
console.assert(domain === 'https://2c.malfrine.com', 'Domain should be from env');
console.log('PASS: Domain from env var works');
"
```

### Test 3: Frontend builds successfully with new config
```bash
cd /Users/malfrine/Documents/code/projects/two-cents/frontend
STRIPE_TEST=true npm run build
```
**Expected:** Nuxt build completes without errors.

### Test 4: Frontend builds without STRIPE_TEST set
```bash
cd /Users/malfrine/Documents/code/projects/two-cents/frontend
unset STRIPE_TEST && npm run build
```
**Expected:** Build completes (no crash from `.toLowerCase()` on undefined).
