#!/usr/bin/env python3
"""Compile the scoped local artifact and audit every declared theorem.

This is a local check, not the AutoLab evaluator or an official hill score.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
VERSION = "4.33.1"


def compiler():
    local = ROOT / ".tools/lean-4.33.1-darwin_aarch64/bin/lean"
    return os.environ.get("LEAN") or (str(local) if local.exists() else shutil.which("lean"))


def audit_output(output, expected):
    if "sorryAx" in output or "declaration uses 'sorry'" in output:
        raise ValueError("Lean reported an admitted proof")
    audits = {}
    pattern = r"'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])"
    for match in re.finditer(pattern, output, re.S):
        name = match[1]
        axioms = {x.strip() for x in (match[2] or "").split(",") if x.strip()}
        if axioms - ALLOWED:
            raise ValueError(f"{name}: nonstandard axioms {sorted(axioms - ALLOWED)}")
        if name in audits:
            raise ValueError(f"Duplicate audit for {name}")
        audits[name] = sorted(axioms)
    if set(audits) != set(expected):
        raise ValueError(f"Axiom audit mismatch: expected {sorted(expected)}, got {sorted(audits)}")
    return audits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="artifacts/lean-verification.json")
    args = parser.parse_args()
    lean = compiler()
    if not lean:
        raise SystemExit("Lean is missing. Install Lean 4.33.1 or set LEAN to its executable.")
    version = subprocess.run([lean, "--version"], text=True, capture_output=True, check=True).stdout.strip()
    if f"version {VERSION}," not in version:
        raise SystemExit(f"Expected Lean {VERSION}; found {version}")
    source = ROOT / "lean/Erdos3SpecialCases.lean"
    source_text = source.read_text()
    names = re.findall(r"^theorem\s+(\w+)", source_text, re.M)
    if not names or len(names) != len(set(names)):
        raise SystemExit("Missing or duplicate theorem declarations")
    expected = {"Erdos3SpecialCases." + name for name in names}
    result = subprocess.run([lean, str(source)], cwd=ROOT, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    print(result.stdout, end="")
    if result.returncode:
        raise SystemExit(f"Lean compilation failed: {result.returncode}")
    audits = audit_output(result.stdout, expected)
    record = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "passed", "scope": "elementary special cases; not the AutoLab hill",
        "original_conjecture_proved": False, "official_autolab_score": None,
        "compiler": version, "source": str(source.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "theorems_checked": len(audits), "allowed_axioms": sorted(ALLOWED),
        "axioms": audits, "stdout": result.stdout,
    }
    destination = ROOT / args.output
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(record, indent=2) + "\n")
    print(f"PASS: {len(audits)} theorem axiom audits. Scope: local special cases only.")


if __name__ == "__main__":
    main()
