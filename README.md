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

## Hard rules

- No fake verification.
- No invented hashes.
- No invented sources.
- Missing evidence means `INDETERMINATE`.
- State roots require replayable receipts.
- National roots require explicit state status labels.
- Humor is allowed; fake verification is forbidden.

## Status

Bootstrap phase. Stress-test relentlessly.

```text
Do not praise. Do not invent. Break it.
```
