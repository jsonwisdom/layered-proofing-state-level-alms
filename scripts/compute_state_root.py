#!/usr/bin/env python3
"""Compute deterministic state root for Layered Proofing.

GROK_EPOCH_001 / INTEGRITY-STRUCT-001 fix.

Hard rules:
- Any failed claim makes the state root FAILED.
- Claim set must match declared completeness metadata when present.
- Snapshot hash commits to sorted claim ids + states + paths.
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


def load_json(path: Path):
    return json.loads(path.read_text())


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


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


def main() -> int:
    if len(sys.argv) != 2:
        print(json.dumps({"verdict": "FAIL", "reason": "usage: scripts/compute_state_root.py <STATE>"}, indent=2))
        return 1

    state = sys.argv[1].upper().replace("--LANE", "")
    manifest = load_json(MANIFEST)
    claims = [c for c in manifest.get("claims", []) if c.get("state") == state]
    declared_sets = manifest.get("claim_sets", {})
    declared = declared_sets.get(state, {})

    snapshot_hash = claim_set_snapshot_hash(claims)
    set_violations = []

    if declared:
        if declared.get("completeness") != "DECLARED_EXHAUSTIVE":
            set_violations.append("claim set completeness not DECLARED_EXHAUSTIVE")
        if declared.get("total_claims") != len(claims):
            set_violations.append(f"total_claims mismatch declared={declared.get('total_claims')} actual={len(claims)}")
        if declared.get("snapshot_hash") and declared.get("snapshot_hash") != snapshot_hash:
            set_violations.append("snapshot_hash mismatch")
    else:
        set_violations.append("missing claim_set declaration")

    reports = []
    passing_hashes = []
    for claim in claims:
        claim_path = claim.get("path")
        if not claim_path:
            reports.append({"verdict": "FAIL", "reason": "claim missing path", "claim": claim})
            continue
        report = replay_claim(claim_path)
        report["claim_path"] = claim_path
        reports.append(report)
        if report.get("verdict") == "PASS" and report.get("actual_hash"):
            passing_hashes.append(report["actual_hash"])

    failed_claims = [r for r in reports if r.get("verdict") != "PASS"]

    if not claims:
        status = "INDETERMINATE"
        reason = "no claims for state"
    elif set_violations:
        status = "FAILED"
        reason = "claim set integrity failed"
    elif failed_claims:
        status = "FAILED"
        reason = "one or more claims failed replay"
    else:
        status = "VERIFIED"
        reason = "all claims replayed and claim set integrity held"

    root = merkle_root(passing_hashes)
    out = {
        "epoch": "GROK_EPOCH_001",
        "state": state,
        "status": status,
        "reason": reason,
        "claim_count": len(claims),
        "passing_claim_count": len(passing_hashes),
        "claim_set": {
            "total_claims": len(claims),
            "snapshot_hash": snapshot_hash,
            "completeness": declared.get("completeness", "UNDECLARED"),
            "violations": set_violations
        },
        "state_root": root,
        "leaf_hashes": sorted(passing_hashes),
        "replay_reports": reports,
        "timestamp_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }

    ROOTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = ROOTS_DIR / f"{state}-state-root.json"
    out_path.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return 0 if status == "VERIFIED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
