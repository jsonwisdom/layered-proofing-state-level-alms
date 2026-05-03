# Layered Proofing by Jay Wisdom — State Level ALMS

Status: BOOTSTRAP
Epoch: GROK_EPOCH_001
Operator: Jay Wisdom
Public identity: jaywisdom.base
Research anchor: jaywisdom.eth

## Core doctrine

Layered Proofing separates civic claims into proof layers so no narrative can impersonate evidence.

```text
source_url explains origin.
frozen_artifact proves captured bytes.
hash proves byte identity.
receipt records verification state.
replay proves reproducibility.
root proves aggregate state.
```

## Rule

```text
source_url != frozen_artifact
```

HTTP-only evidence is not enough for verification. If the only available evidence is a mutable URL, the verdict is `INDETERMINATE`.

## State Level ALMS

Each state lane must maintain its own claims, receipts, replay outputs, and state root.

Initial lanes:

- AL — Alabama speed lane
- MN — Minnesota budget proof lane

## Verdicts

```json
["VERIFIED", "INDETERMINATE", "FAILED", "TAINTED"]
```

## Promotion rule

No claim may promote to `VERIFIED` unless all required layers exist and replay passes.
