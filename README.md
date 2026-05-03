# layered-proofing-state-level-alms

**Layered Proofing by Jay Wisdom — State Level ALMS**

Operator: Jay Wisdom  
Public identity: `jaywisdom.base`  
Research anchor: `jaywisdom.eth`  
Epoch: `GROK_EPOCH_001`

## Mission

Create an adversarial proving ground for state-level civic claims and American citizen recursive protection from AI-generated authority.

Every claim must survive nine distinct layers. No layer may impersonate another.

AI may assist. AI may not become the authority.

## Citizen recursive protection

American citizens should not be governed, denied, labeled, scored, charged, or publicly described by an AI-generated claim that cannot be traced, challenged, replayed, or corrected.

Core protections:

```json
{
  "citizen_rights": [
    "human_readable_explanation",
    "machine_readable_receipt",
    "source_traceability",
    "version_history",
    "appeal_path",
    "correction_path",
    "independent_replay_when_feasible"
  ]
}
```

Core rule:

```text
citizen rights > model confidence
receipts > narrative
appeal > automation
public evidence > black-box authority
```

Doctrine file:

```text
docs/AMERICAN_CITIZEN_RECURSIVE_PROTECTION.md
```

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

## AI model failure doctrine

External AI systems are stress nodes, not authorities.

Doctrine file:

```text
docs/RECURSIVE_PRACTICES_AND_MODEL_FAILURES.md
```

Rules:

- AI may propose.
- Repo must verify.
- Hashes must come from bytes.
- Replay must test stored artifacts.
- Model confidence is not proof.
- Model outages become audit evidence.
- No external model may promote a claim to `VERIFIED`.

## Hard rules

- No fake verification.
- No invented hashes.
- No invented sources.
- Missing evidence means `INDETERMINATE`.
- State roots require replayable receipts.
- National roots require explicit state status labels.
- Public explanations must not soften failed or indeterminate verdicts.
- Civic AI claims require appeal, traceability, and correction paths.
- Humor is allowed; fake verification is forbidden.

## Next recommended upgrades

1. Freeze full official MMB artifact bytes: PDF, HTML dump, or extracted official table.
2. Finish second MN claim hash + replay to test multi-claim state roots.
3. Generate or verify national root only after explicit state statuses exist.
4. Add citizen verification interface for public claim checking.
5. Add Base / ENS / EAS anchor only after wallet or chain receipt exists.

## Status

Bootstrap phase. Stress-test relentlessly.

```text
Do not praise. Do not invent. Break it.
```
