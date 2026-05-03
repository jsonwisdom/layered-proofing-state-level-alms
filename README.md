# layered-proofing-state-level-alms

**Layered Proofing by Jay Wisdom — State Level ALMS**

Operator: Jay Wisdom  
Public identity: `jaywisdom.base`  
Research anchor: `jaywisdom.eth`  
Epoch: `GROK_EPOCH_001`

## Mission

Create an adversarial proving ground for state-level civic claims.

Every claim must survive nine distinct layers. No layer may impersonate another.

## The 9 layers

1. Claim — what is being asserted
2. Source — where it came from, explanatory only
3. Frozen artifact — immutable capture of bytes
4. Hash — cryptographic digest of frozen artifact
5. Receipt — verification record
6. Replay — deterministic reproduction proof
7. State root — per-state Merkle or aggregate root
8. National root — cross-state consolidation
9. Public explanation — human-readable audit card

## Core rule

```text
source_url != frozen_artifact
```

Source URL explains origin.  
Frozen artifact proves captured bytes.

HTTP-only links are allowed as source references only. If the only evidence is an HTTP URL, verdict must be `INDETERMINATE`.

## Bootstrap frozen artifact modes

```json
{
  "allowed_modes": ["repo", "github_commit", "sha256"]
}
```

Later upgrade modes may include IPFS CID, Arweave ID, transaction hash, EAS UID, or signed wallet proof.

## State lanes

- `AL` — Alabama speed lane
- `MN` — Minnesota budget proof lane
- Later: 50 states + DC

## Current MN reality bridge

Claim:

```text
MN-BUDGET-2026-01
```

Current state:

```json
{
  "replay": "PASS",
  "state_root": "COMPUTED",
  "status": "INDETERMINATE",
  "reason": "snapshot-level source proof only; not full raw MMB source completeness"
}
```

Frozen source snapshot:

```text
fixtures/mn/sources/mmb_budget_snapshot_2026-05-03.txt
```

Claim wrapper:

```text
fixtures/mn/mn_budget_2026_claim.json
```

Boundary:

```text
This proves integrity of the captured source snapshot.
It does not yet prove the complete Minnesota budget fact against full official MMB raw source bytes.
```

## Hard rules

- No fake verification.
- No invented hashes.
- No invented sources.
- Missing evidence means `INDETERMINATE`.
- State roots require replayable receipts.
- National roots require explicit state status labels.
- Public explanations must not soften failed or indeterminate verdicts.
- Humor is allowed; fake verification is forbidden.

## Next recommended upgrades

1. Freeze full official MMB artifact bytes: PDF, HTML dump, or extracted official table.
2. Add a second MN claim to test multi-claim state roots.
3. Generate or verify national root only after explicit state statuses exist.
4. Add Base / ENS / EAS anchor only after wallet or chain receipt exists.

## Status

Bootstrap phase. Stress-test relentlessly.

```text
Do not praise. Do not invent. Break it.
```
