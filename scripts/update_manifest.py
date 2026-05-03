#!/usr/bin/env python3
"""Update proof_manifest for a given claim (engine-compatible).

GROK_EPOCH_001.

- Loads alms/proof_manifest.json
- Locates claim by id in top-level `claims` array
- Syncs status from fixture (hash presence, replay hints)
- Recomputes claim_sets snapshot_hash for the claim's state
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "alms" / "proof_manifest.json"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(p: Path):
    return json.loads(p.read_text())


def save_json(p: Path, obj):
    p.write_text(json.dumps(obj, indent=2) + "\n")


def snapshot_hash(claims):
    rows = []
    for c in sorted(claims, key=lambda x: (x.get("claim_id", ""), x.get("path", ""))):
        rows.append("|".join([c.get("claim_id", ""), c.get("state", ""), c.get("path", "")]))
    return "sha256:" + sha256_hex("\n".join(rows).encode("utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--claim", required=True)
    args = ap.parse_args()

    if not MANIFEST.exists():
        print(json.dumps({"verdict": "FAIL", "reason": "manifest missing"}, indent=2))
        return 1

    m = load_json(MANIFEST)
    claims = m.get("claims", [])
    target = None
    for c in claims:
        if c.get("claim_id") == args.claim:
            target = c
            break

    if not target:
        print(json.dumps({"verdict": "FAIL", "reason": "claim not found in manifest"}, indent=2))
        return 1

    # Load fixture
    fixture_path = ROOT / target.get("path")
    if not fixture_path.exists():
        print(json.dumps({"verdict": "FAIL", "reason": "fixture missing", "path": str(fixture_path)}, indent=2))
        return 1

    fx = load_json(fixture_path)

    # Sync basic status from fixture
    has_hash = isinstance(fx.get("hash"), str) and fx.get("hash", "").startswith("sha256:")
    target["status"] = "INDETERMINATE" if not has_hash else target.get("status", "INDETERMINATE")
    target["layers_completed"] = list(set(target.get("layers_completed", []) + (["HASH"] if has_hash else [])))

    # Recompute claim_set for state
    state = target.get("state")
    by_state = [c for c in claims if c.get("state") == state]
    m.setdefault("claim_sets", {})
    m["claim_sets"].setdefault(state, {})
    m["claim_sets"][state]["total_claims"] = len(by_state)
    m["claim_sets"][state]["snapshot_hash"] = snapshot_hash(by_state)
    m["claim_sets"][state]["completeness"] = m["claim_sets"][state].get("completeness", "INCOMPLETE")

    save_json(MANIFEST, m)

    print(json.dumps({
        "verdict": "PASS",
        "claim_id": args.claim,
        "state": state,
        "snapshot_hash": m["claim_sets"][state]["snapshot_hash"]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
