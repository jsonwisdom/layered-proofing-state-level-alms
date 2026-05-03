#!/usr/bin/env python3
"""Layered Proofing validator stub.

GROK_EPOCH_001 / CORE-STRUCT-002 fix.
Loads the proof manifest, schemas, and an input claim fixture.
Enforces the first runtime rule:

  source_url != frozen_artifact.reference

This is intentionally small. It makes the repo executable before roots/replay exist.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "alms" / "proof_manifest.json"

REQUIRED_LAYERS = [
    "CLAIM",
    "SOURCE",
    "FROZEN_ARTIFACT",
    "HASH",
    "RECEIPT",
    "REPLAY",
    "STATE_ROOT",
    "NATIONAL_ROOT",
    "PUBLIC_EXPLANATION",
]


def load_json(path: Path):
    return json.loads(path.read_text())


def verdict(status: str, reason: str, path: str | None = None) -> int:
    report = {
        "epoch": "GROK_EPOCH_001",
        "verdict": status,
        "reason": reason,
        "path": path,
    }
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


def main() -> int:
    if len(sys.argv) != 2:
        return verdict("FAIL", "usage: scripts/validate_claim.py <claim.json>")

    claim_path = ROOT / sys.argv[1]
    if not claim_path.exists():
        return verdict("FAIL", "claim file missing", str(claim_path))

    manifest = load_json(MANIFEST)
    claim = load_json(claim_path)

    lanes = manifest.get("lanes", [])
    if not lanes:
        return verdict("FAIL", "manifest has no lanes")

    for lane in lanes:
        layers = lane.get("layers", [])
        if layers != REQUIRED_LAYERS:
            return verdict("FAIL", f"lane layer order mismatch: {lane.get('lane_id')}")

    if claim.get("layer") != "CLAIM":
        return verdict("FAIL", "top-level claim layer must be CLAIM", str(claim_path))

    source_url = claim.get("source_url")
    frozen = claim.get("frozen_artifact")

    if frozen is None:
        return verdict("INDETERMINATE", "missing frozen_artifact", str(claim_path))

    frozen_reference = frozen.get("reference")
    frozen_mode = frozen.get("mode")
    allowed_modes = manifest.get("validation_rules", {}).get("frozen_modes", [])

    if frozen_mode not in allowed_modes:
        return verdict("FAIL", f"invalid frozen_artifact mode: {frozen_mode}", str(claim_path))

    if source_url and frozen_reference and source_url == frozen_reference:
        return verdict("FAIL", "source_url equals frozen_artifact.reference", str(claim_path))

    if source_url and source_url.startswith("http") and frozen_mode == "repo":
        return verdict("PASS", "source and frozen artifact separated", str(claim_path))

    return verdict("INDETERMINATE", "claim structurally valid but evidence/replay incomplete", str(claim_path))


if __name__ == "__main__":
    raise SystemExit(main())
