#!/usr/bin/env python3
"""Compute deterministic state root for Layered Proofing with public explanation binding.

GROK_EPOCH_001 / AUDIT-STRUCT-001 fix.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "alms" / "proof_manifest.json"
ROOTS_DIR = ROOT / "alms" / "roots"
EXPLAIN_DIR = ROOT / "docs" / "explanations"


def load_json(path: Path):
    return json.loads(path.read_text())


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


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


def claim_set_snapshot_hash(claims: list[dict]) -> str:
    rows = []
    for claim in sorted(claims, key=lambda c: (c.get("claim_id", ""), c.get("path", ""))):
        rows.append("|".join([claim.get("claim_id", ""), claim.get("state", ""), claim.get("path", "")]))
    return "sha256:" + sha256_hex("\n".join(rows).encode("utf-8"))


def replay_claim(claim_path: str) -> dict:
    cmd = [sys.executable, "scripts/validate_claim.py", "--replay", claim_path]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    try:
        report = json.loads(proc.stdout)
    except Exception:
        report = {"verdict": "FAIL", "reason": "validator produced non-json", "stdout": proc.stdout, "stderr": proc.stderr}
    report["exit_code"] = proc.returncode
    return report


def build_explanation(state, root_hash, snapshot_hash, status, reports):
    violations = [r for r in reports if r.get("verdict") != "PASS"]
    explanation = {
        "explanation_id": f"{state}-EXPLAIN-001",
        "state": state,
        "state_root_hash": root_hash,
        "snapshot_hash": snapshot_hash,
        "verdict_summary": status,
        "violation_details": violations,
        "claim_count": len(reports),
        "passing_claim_count": len([r for r in reports if r.get("verdict") == "PASS"]),
        "generation_timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }
    explanation_bytes = canonical_json(explanation)
    explanation_hash = "sha256:" + sha256_hex(explanation_bytes)
    explanation["explanation_hash"] = explanation_hash
    return explanation


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"verdict": "FAIL", "reason": "usage: scripts/compute_state_root.py <STATE>"}, indent=2))
        return 1

    state = sys.argv[1].upper()
    manifest = load_json(MANIFEST)
    claims = [c for c in manifest.get("claims", []) if c.get("state") == state]

    reports = []
    passing_hashes = []
    for claim in claims:
        claim_path = claim.get("path")
        report = replay_claim(claim_path)
        report["claim_path"] = claim_path
        reports.append(report)
        if report.get("verdict") == "PASS" and report.get("actual_hash"):
            passing_hashes.append(report["actual_hash"])

    snapshot_hash = claim_set_snapshot_hash(claims)

    if not claims:
        status = "INDETERMINATE"
    elif any(r.get("verdict") != "PASS" for r in reports):
        status = "FAILED"
    else:
        status = "VERIFIED"

    root = merkle_root(passing_hashes)

    explanation = build_explanation(state, root, snapshot_hash, status, reports)

    EXPLAIN_DIR.mkdir(parents=True, exist_ok=True)
    explain_path = EXPLAIN_DIR / f"{state}-explanation.json"
    explain_path.write_text(json.dumps(explanation, indent=2) + "\n")

    out = {
        "state": state,
        "state_root": root,
        "status": status,
        "explanation_hash": explanation.get("explanation_hash")
    }

    ROOTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ROOTS_DIR / f"{state}-state-root.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")

    print(json.dumps({"root": out, "explanation": explanation}, indent=2))
    return 0 if status == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
