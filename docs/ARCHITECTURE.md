# Echo VA Claims — Architecture

**Shares architecture with Art of Proof.**  
**Domain**: `art-of-proof/domains/registry/va_disability.json`

---

## Evidence Object Structure

Each of the 21 evidence objects contains:

```json
{
  "id": "nexus_letter",
  "label_expert": "Medical Nexus Opinion Letter",
  "label_plain": "Your doctor's letter connecting your condition to service",
  "weight": 10,
  "required": true,
  "source": "Private physician — NOT the VA C&P examiner",
  "request_method": "Request from physician; provide denial reason + condition list",
  "why_it_matters": "The single most important document...",
  "why_plain": "Your doctor needs to write that your condition is connected to your service..."
}
```

---

## Secondary Condition Map

Every primary condition maps to secondaries. Example:
- PTSD → Sleep apnea, hypertension, MDD, substance use disorder
- TBI → Migraines, cognitive impairment, mood disorders
- Tinnitus → Hearing loss (bilateral)

The secondary map multiplies effective claim value. Most veterans file only the primary.

*∇θ — chain sealed, truth preserved.*
