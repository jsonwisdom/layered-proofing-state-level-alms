#!/usr/bin/env python3
"""Compute national root for Layered Proofing.

GROK_EPOCH_001 / NATIONAL-STRUCT-001 fix.

Inputs:
- alms/national_manifest.json
- alms/roots/<STATE>-state-root.json
- docs/explanations/<STATE>-explanation.json

Hard rules:
- Every participating state must have explicit status.
- Every state root must bind to an explanation_hash.
- Missing state root or explanation blocks national root.
- National root includes state + status + root + explanation hash.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "alms" / "national_manifest.json"
ROOTS_DIR = ROOT / "alms" / "roots"
EXPLAIN_DIR = ROOT / "docs" / "explanations"


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def load_json(path: Path):
    return json.loads(path.read_text())


def merkle_root(leaves: list[str]) -> str:
    if not leaves:
        return "sha256:" + sha256_hex(b"")
    level = [leaf.replace("sha256:", "") for leaf in sorted(leaves)]
    while len(level) > 1:
        nxt = []
        for i in range(0, len(level), 2):
            left = level[i]
            right = level[i + 1] if i + 1 < len(level) else left
            nxt.append(sha256_hex(bytes.fromhex(left) + bytes.fromhex(right)))
        level = nxt
    return "sha256:" + level[0]


def main() -> int:
    if not MANIFEST.exists():
        print(json.dumps({"verdict": "FAIL", "reason": "missing national_manifest.json"}, indent=2))
        return 1

    manifest = load_json(MANIFEST)
    states = manifest.get("participating_states", [])
    if not states:
        print(json.dumps({"verdict": "FAIL", "reason": "no participating states declared"}, indent=2))
        return 1

    state_entries = []
    violations = []

    for state in states:
        code = state.get("state")
        declared_status = state.get("status")
        if not code or not declared_status:
            violations.append({"state": code or "UNKNOWN", "reason": "state/status missing in national manifest"})
            continue

        root_path = ROOTS_DIR / f"{code}-state-root.json"
        explain_path = EXPLAIN_DIR / f"{code}-explanation.json"

        if not root_path.exists():
            violations.append({"state": code, "reason": "missing state root"})
            continue
        if not explain_path.exists():
            violations.append({"state": code, "reason": "missing public explanation"})
            continue

        root_doc = load_json(root_path)
        explanation = load_json(explain_path)

        if root_doc.get("status") != declared_status:
            violations.append({"state": code, "reason": "declared status does not match state root status"})
        if root_doc.get("explanation_hash") != explanation.get("explanation_hash"):
            violations.append({"state": code, "reason": "explanation_hash mismatch"})
        if root_doc.get("state_root") != explanation.get("state_root_hash"):
            violations.append({"state": code, "reason": "state_root mismatch with explanation"})

        state_entries.append({
            "state": code,
            "status": root_doc.get("status"),
            "state_root": root_doc.get("state_root"),
            "explanation_hash": root_doc.get("explanation_hash")
        })

    leaves = []
    for entry in state_entries:
        leaves.append("sha256:" + sha256_hex(canonical_json(entry)))

    national_root = merkle_root(leaves)
    status = "FAILED" if violations else "VERIFIED"

    national_explanation = {
        "explanation_id": "US-NATIONAL-EXPLAIN-001",
        "epoch": "GROK_EPOCH_001",
        "national_root": national_root,
        "status": status,
        "participating_state_count": len(states),
        "state_entries": state_entries,
        "violations": violations,
        "generation_timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    }
    national_explanation_hash = "sha256:" + sha256_hex(canonical_json(national_explanation))
    national_explanation["explanation_hash"] = national_explanation_hash

    out = {
        "epoch": "GROK_EPOCH_001",
        "status": status,
        "national_root": national_root,
        "national_explanation_hash": national_explanation_hash,
        "participating_states": states,
        "state_entries": state_entries,
        "violations": violations
    }

    (ROOTS_DIR / "national-root.json").write_text(json.dumps(out, indent=2) + "\n")
    (EXPLAIN_DIR / "national-explanation.json").write_text(json.dumps(national_explanation, indent=2) + "\n")
    print(json.dumps({"root": out, "explanation": national_explanation}, indent=2))
    return 0 if status == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
