#!/usr/bin/env python3
"""Compute deterministic state root for Layered Proofing.

GROK_EPOCH_001 / ROOT-STRUCT-001 fix.

Rule:
- Input manifest: alms/proof_manifest.json
- State argument: MN, AL, etc.
- Select claims for that state from manifest.claims
- Replay each claim through scripts/validate_claim.py --replay
- Build Merkle root from sorted claim hashes
- Write alms/roots/<STATE>-state-root.json
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

    state = sys.argv[1].upper()
    manifest = load_json(MANIFEST)
    claims = [c for c in manifest.get("claims", []) if c.get("state") == state]

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

    if not claims:
        status = "INDETERMINATE"
        reason = "no claims for state"
    elif len(passing_hashes) != len(claims):
        status = "FAILED"
        reason = "one or more claims failed replay"
    else:
        status = "VERIFIED"
        reason = "all claims replayed"

    root = merkle_root(passing_hashes)
    out = {
        "epoch": "GROK_EPOCH_001",
        "state": state,
        "status": status,
        "reason": reason,
        "claim_count": len(claims),
        "passing_claim_count": len(passing_hashes),
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
