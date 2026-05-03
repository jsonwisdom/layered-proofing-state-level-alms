# Public Explanation Template

Status: TEMPLATE
Epoch: GROK_EPOCH_001

## Required fields

```json
{
  "explanation_id": "string",
  "state": "MN | AL | ...",
  "state_root_hash": "sha256:<64-hex>",
  "snapshot_hash": "sha256:<64-hex>",
  "verdict_summary": "VERIFIED | FAILED | INDETERMINATE | TAINTED",
  "violation_details": [],
  "claim_count": 0,
  "passing_claim_count": 0,
  "generation_timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "explanation_hash": "sha256:<64-hex> | COMPUTED_AFTER_CANONICALIZATION"
}
```

## Rule

The public explanation is Layer 9.

It must not soften or hide internal failure states.

```text
public narrative must bind to state_root + snapshot_hash + violations
```

If the state root is FAILED, the public explanation must say FAILED.

If the explanation is missing, national root generation must remain blocked.
