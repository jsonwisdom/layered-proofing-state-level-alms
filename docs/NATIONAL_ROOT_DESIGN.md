# National Root Aggregation Design

Status: DESIGN_LOCKED_NOT_DEPLOYED
Epoch: GROK_EPOCH_001
Operator: Jay Wisdom

## Purpose

Define how state roots roll up into a national root without hiding weak or incomplete states.

## Core rule

```text
ANY state not PASS means national status is not PASS.
```

No exceptions.

## Input shape

```json
{
  "version": "US_SNAPSHOT_2026-05-03",
  "states": [
    {
      "state": "MN",
      "root": "sha256:<state-root>",
      "status": "PASS",
      "version": "MN_SNAPSHOT_2026-05-03"
    },
    {
      "state": "AL",
      "root": null,
      "status": "INDETERMINATE",
      "version": "AL_BOOTSTRAP_2026-05-03"
    }
  ]
}
```

## Verdict rules

```json
{
  "all_states_PASS": "PASS",
  "any_state_INDETERMINATE": "INDETERMINATE",
  "any_state_FAIL": "FAIL",
  "missing_state": "FAIL",
  "missing_root_with_PASS": "FAIL"
}
```

## Leaf rule

Each state leaf must bind state code, state root, status, and version.

```text
leaf_material = state + "|" + root + "|" + status + "|" + version
leaf_hash = sha256(leaf_material)
```

## National root

```text
national_root = merkle(sorted(state_leaf_hashes))
```

## Hard boundary

A national root with one PASS state and one INDETERMINATE state may still compute a hash, but its verdict must remain INDETERMINATE.

The hash commits to the mixed state. It does not launder the mixed state into success.

## Current state

```json
{
  "MN": "READY_FOR_BROWSER_ROOT_CHECK",
  "AL": "BOOTSTRAP_ONLY",
  "US": "DESIGN_LOCKED_NOT_DEPLOYED"
}
```
