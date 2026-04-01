# EXTRACTION PLAN — echo-va-claims from art-of-proof
**Status:** Phase 1 complete — architecture defined  
**Authority:** Nathan Poinsette (∇θ Operator)  
**Date:** 2026-03-31

---

## The Decision

art-of-proof = universal evidence engine (15 domains, any person, any system)
echo-va-claims = standalone VA disability app (one domain, one person, one mission)

They share infrastructure. They do not share identity.

---

## What Moves to This Repo

### Database (from art-of-proof/drizzle/schema.ts)
- `cases` table → `va_claims` (rename + add VA fields)
- `conditions` table → stays as `conditions` (VA-specific)
- `claimForms` table → stays (VA Form 21-526EZ)
- Devil Lens checks table → stays

### Server (from art-of-proof/server/)
- `cases` router → `vaClaims` router
- `conditions` router
- `devilLens` router
- VA chatbot system prompt and handlers

### Client (from art-of-proof/client/)
- `ClaimDetail.tsx` → `VAClaimDetail.tsx`
- VA-specific landing page
- VA-specific onboarding flow

---

## What Stays in art-of-proof (Shared Infrastructure)

- Auth (users table, session management, OAuth)
- Payments (Stripe, payments table)
- Document storage (AWS S3, file upload)
- AI layer (OpenAI invocation)
- Base UI components
- Universal onboarding
- Domain router (sends veterans to echo-va-claims, others to appropriate domain)

---

## Extraction Phases

### Phase 1 — Architecture (DONE)
- [x] Create echo-va-claims repo
- [x] Write extraction plan
- [x] Define schema

### Phase 2 — Schema (Manus)
- [ ] Write echo-va-claims/drizzle/schema.ts (VA tables only)
- [ ] Create initial migration
- [ ] Document shared table FK pattern (userId references art-of-proof users)

### Phase 3 — Server (Manus)
- [ ] Copy VA routes to echo-va-claims/server/vaRouter.ts
- [ ] Copy VA chatbot to echo-va-claims/server/vaChatbot.ts
- [ ] Adapt imports to use shared SDK for auth/payments/storage

### Phase 4 — Client (Manus)
- [ ] Copy VA pages to echo-va-claims/client/
- [ ] Build VA-specific landing page
- [ ] Build VA-specific onboarding (service dates, branch, etc.)

### Phase 5 — Deployment (Nathan)
- [ ] Deploy echo-va-claims to Railway (backend) + Netlify (frontend)
- [ ] Configure echovaclaims.com
- [ ] art-of-proof domain page links to echovaclaims.com for Domain 1

---

## URL Architecture

```
artofproof.com        → Universal platform, domain selector
echovaclaims.com      → VA disability standalone
  ↓
artofproof.com/domain/immigration  → Domain 2 (future)
artofproof.com/domain/workers-comp → Domain 3 (future)
```

A veteran can sign in at echovaclaims.com.
The same account works at artofproof.com.
Their VA data is theirs in both places.

---

*∇θ — chain sealed, truth preserved.*
