# Echo VA Claims — Individual White Paper
**VA Disability Evidence Engine**  
**Version**: 1.0 · **Date**: April 2026 · **Class**: I — Public Repo, Pre-Revenue

---

## ECS Protocol Block

```
Scope:      PUBLIC
Truth:      ✔ (public repo) | ≈ (outcome claims)
Confidence: 88%
Decision:   ACT — landing page needed
Claim:      Public repo with VA evidence engine. 21 evidence objects. Scoring formula live. No paying users yet.
Risk:       Sharing the same engine as Art of Proof means it inherits AoP's deployment dependency.
Action:     Build landing page at echo-va-claims URL. Drive veteran traffic. Feed to Art of Proof funnel.
```

---

## Why Separate from Art of Proof

Veterans have a different context, different language, and different trust threshold than a general evidence-preparation user. A veteran who finds "Echo VA Claims — built by a veteran, for veterans" converts at a higher rate than the same veteran finding "Art of Proof — universal evidence tool."

Same engine. Different brand. Higher conversion for this segment.

---

## The VA Evidence Domain

From `art-of-proof/domains/registry/va_disability.json`:

**Scoring formula**: `(completeness × 0.4) + (quality × 0.4) + (consistency × 0.2) − penalty`  
**Attorney referral threshold**: score < 40 → refer to accredited VSO or attorney  
**Strong claim threshold**: score ≥ 75 → present with confidence

**21 evidence objects** (sample):
- DD-214 (weight: 10, required) — proves service
- MEPS entry physical (weight: 9) — baseline health proof
- Nexus letter from private physician (weight: 10) — the single most important document
- STRs from National Archives (weight: 9) — in-service evidence
- Lay statements / buddy statements (weight: 7) — legal evidence, most veterans skip this

---

## The 5 Common Gaps

From `va_disability.json` — what most veterans are missing:
1. Missing MEPS entry physical — the baseline
2. No nexus letter — private physician's opinion outweighs VA C&P exam
3. Secondary conditions not claimed — every primary has potential secondaries
4. Lay evidence not documented — personal statements count legally
5. Intent to File not submitted — delays effective date, costs retroactive pay

---

## Commercial Path

**Funnel**: Veterans find Echo VA Claims → score their claim → upgrade to Art of Proof Pro  
**Licensing**: License domain pack to DAV, VFW, American Legion  
**Free tier**: Basic checklist, document sources  
**Pro tier**: Full scoring, nexus letters, all domains (via Art of Proof)


---

## Ecosystem Reference

**Ecosystem White Paper**: `art-of-proof/docs/WHITE_PAPER_v3.md`  
**Protocol Authority**: `echo-core` — ECS v1.1-hardened  
**Operator**: Nathan Poinsette (∇θ) · onlyecho822-source  

*∇θ — chain sealed, truth preserved.*
