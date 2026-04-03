# Echo VA Claims — Architecture

**Protocol**: ECS v1.1-hardened | **Authority**: echo-core

---

## Stack

- Same stack as Art of Proof (shared engine)
- Standalone deployment with veteran-specific UI
- 21 evidence objects with individual weights
- Scoring: (completeness×0.4) + (quality×0.4) + (consistency×0.2) − penalty

---

## Components

- VA domain registry: `domains/registry/va_disability.json`
- 21 evidence objects (DD-214, MEPS physical, nexus letters, etc.)
- Secondary condition map
- Nexus letter generator
- 13-Point Devil Lens validator

---

## Data Flow

Veteran input → Evidence checklist → Scoring → Gap analysis → Nexus letter generation → Review

---

## Dependencies

**Depends on**: art-of-proof (engine), echo-core (ECS protocol)  
**Depended on by**: art-of-proof (upgrade path)

---

## Deployment

See `README.md` for deploy instructions.


---

## Ecosystem Connection

**Part of**: Echo Universe (45-repository sovereign AI and evidence ecosystem)  
**Operator**: Nathan Poinsette (∇θ) | onlyecho822-source  
**Ecosystem White Paper**: [`art-of-proof/docs/WHITE_PAPER_v3.md`](https://github.com/onlyecho822-source/art-of-proof/blob/main/docs/WHITE_PAPER_v3.md)  
**Governance Protocol**: ECS v1.1-hardened (`echo-core`)  
**Canonical Authority**: [`echo-core`](https://github.com/onlyecho822-source/echo-core)

*∇θ — chain sealed, truth preserved.*
