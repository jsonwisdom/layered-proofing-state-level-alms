#!/usr/bin/env python3
"""Compute SHA-256 for a repo file and optionally update the claim hash.

GROK_EPOCH_001.

Default behavior:
- prints sha256:<64-hex>

Optional:
- --write updates the target JSON file's top-level `hash` field.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return "sha256:" + h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--write", action="store_true", help="write computed hash into JSON top-level hash field")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(json.dumps({"verdict": "FAIL", "reason": "file not found", "path": str(path)}, indent=2))
        return 1

    digest = sha256_file(path)
    report = {"verdict": "PASS", "path": str(path), "hash": digest}

    if args.write:
        data = json.loads(path.read_text())
        data["hash"] = digest
        path.write_text(json.dumps(data, indent=2) + "\n")
        report["write"] = "UPDATED_JSON_HASH_FIELD"

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
