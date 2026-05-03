#!/usr/bin/env python3
"""Layered Proofing validator.

GROK_EPOCH_001.
Enforces layer separation and provides a bootstrap replay check.
"""

from __future__ import annotations

import hashlib
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


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def verdict(status: str, reason: str, path: str | None = None, extra: dict | None = None) -> int:
    report = {
        "epoch": "GROK_EPOCH_001",
        "verdict": status,
        "reason": reason,
        "path": path,
    }
    if extra:
        report.update(extra)
    print(json.dumps(report, indent=2))
    return 0 if status == "PASS" else 1


def validate_structure(claim: dict, claim_path: Path) -> tuple[str, str]:
    manifest = load_json(MANIFEST)
    lanes = manifest.get("lanes", [])
    if not lanes:
        return "FAIL", "manifest has no lanes"

    for lane in lanes:
        layers = lane.get("layers", [])
        if layers != REQUIRED_LAYERS:
            return "FAIL", f"lane layer order mismatch: {lane.get('lane_id')}"

    if claim.get("layer") != "CLAIM":
        return "FAIL", "top-level claim layer must be CLAIM"

    frozen = claim.get("frozen_artifact")
    if frozen is None:
        return "INDETERMINATE", "missing frozen_artifact"

    frozen_mode = frozen.get("mode")
    allowed_modes = manifest.get("validation_rules", {}).get("frozen_modes", [])
    if frozen_mode not in allowed_modes:
        return "FAIL", f"invalid frozen_artifact mode: {frozen_mode}"

    source_url = claim.get("source_url")
    frozen_reference = frozen.get("reference")
    if source_url and frozen_reference and source_url == frozen_reference:
        return "FAIL", "source_url equals frozen_artifact.reference"

    return "PASS", "structure valid"


def replay_claim(claim: dict, claim_path: Path) -> tuple[str, str, dict]:
    status, reason = validate_structure(claim, claim_path)
    if status != "PASS":
        return status, reason, {}

    frozen = claim["frozen_artifact"]
    frozen_mode = frozen.get("mode")
    frozen_reference = frozen.get("reference")
    expected_hash = claim.get("hash")

    if not expected_hash:
        return "INDETERMINATE", "missing expected hash", {}

    if frozen_mode != "repo":
        return "INDETERMINATE", f"replay not implemented for frozen mode: {frozen_mode}", {}

    artifact_path = ROOT / frozen_reference
    if not artifact_path.exists():
        return "INDETERMINATE", "frozen artifact path missing", {"frozen_artifact_path": str(artifact_path)}

    actual_hash = sha256_file(artifact_path)
    extra = {
        "expected_hash": expected_hash,
        "actual_hash": actual_hash,
        "frozen_artifact_path": str(artifact_path.relative_to(ROOT)),
    }

    if actual_hash != expected_hash:
        return "FAIL", "replay hash mismatch", extra

    return "PASS", "replay hash matched", extra


def main() -> int:
    replay = False
    args = sys.argv[1:]
    if args and args[0] == "--replay":
        replay = True
        args = args[1:]

    if len(args) != 1:
        return verdict("FAIL", "usage: scripts/validate_claim.py [--replay] <claim.json>")

    claim_path = ROOT / args[0]
    if not claim_path.exists():
        return verdict("FAIL", "claim file missing", str(claim_path))

    claim = load_json(claim_path)

    if replay:
        status, reason, extra = replay_claim(claim, claim_path)
        return verdict(status, reason, str(claim_path.relative_to(ROOT)), extra)

    status, reason = validate_structure(claim, claim_path)
    if status == "PASS":
        return verdict("PASS", "source and frozen artifact separated", str(claim_path.relative_to(ROOT)))
    return verdict(status, reason, str(claim_path.relative_to(ROOT)))


if __name__ == "__main__":
    raise SystemExit(main())
