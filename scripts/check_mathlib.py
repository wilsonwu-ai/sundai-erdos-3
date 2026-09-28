#!/usr/bin/env python3
"""Compile the local proof modules using the original AutoLab image's libraries.

Run inside the pinned image, normally through local_evaluator.py check-lean.
The result covers these modules only, never the full hill or a remote score.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from verify_lean import ALLOWED, VERSION, audit_output
from local_evaluator import IMAGE

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path("/opt/formal-conjectures")
MODULES = ("Erdos3SpecialCases", "Erdos3Bridge", "Erdos3Divergence", "Erdos3Reduction",
           "Erdos3Blocks", "Erdos3Dyadic", "Erdos3CrossScale",
           "Erdos3ThreeCase", "Erdos3RothBridge")
SCOPES = {
    "Erdos3SpecialCases": "elementary known special cases, using an explicit witness predicate",
    "Erdos3Bridge": "forward bridges to the hill definitions and special-case conclusions",
    "Erdos3Divergence": "elementary consequences of reciprocal non-summability",
    "Erdos3Reduction": "conditional implication; APFreeSummability remains an unproved parameter",
    "Erdos3Blocks": "finite logarithmic blocks and their reciprocal mass bounds",
    "Erdos3Dyadic": "analytic counting-to-summability transfer; APFreePowerEnvelope remains unproved",
    "Erdos3CrossScale": "equivalence of the hill with dyadic extremal summability for k>=4; neither side is proved",
    "Erdos3ThreeCase": "conditional: the Kelley-Meka or Bloom-Sisask bound implies erdos_3.variants.three; the bound is not proved",
    "Erdos3RothBridge": "maxCard 3 N = rothNumberNat N and transfers of Mathlib-native Roth-number bounds; no bound is proved",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write JSON here instead of stdout")
    args = parser.parse_args()
    version = subprocess.run(["lean", "--version"], text=True, capture_output=True,
                             check=True).stdout.strip()
    if f"version {VERSION}," not in version:
        raise SystemExit(f"Expected Lean {VERSION}, found {version}")
    lake = PROJECT / ".lake"
    libs = [lake / "build/lib/lean", *sorted((lake / "packages").glob("*/.lake/build/lib/lean"))]
    if not (PROJECT / "FormalConjecturesUtil/Answer.lean").is_file():
        raise SystemExit("Run this checker inside the pinned AutoLab image")
    records = []
    with tempfile.TemporaryDirectory(prefix="erdos3-proofs-") as directory:
        build = Path(directory)
        env = dict(os.environ)
        env["LEAN_PATH"] = ":".join([str(build), *(str(p) for p in libs if p.is_dir())])
        for module in MODULES:
            source = ROOT / "lean" / f"{module}.lean"
            source_bytes = source.read_bytes()
            source_text = source_bytes.decode()
            names = re.findall(r"^theorem\s+(\w+)", source_text, re.M)
            namespaces = re.findall(r"^namespace\s+(\w+)", source_text, re.M)
            if namespaces != [module] or not names or len(names) != len(set(names)):
                raise SystemExit(f"Unexpected theorem/namespace layout in {source.name}")
            expected = {f"{module}.{name}" for name in names}
            (build / source.name).write_bytes(source_bytes)
            result = subprocess.run(["lean", "-o", f"{module}.olean", source.name],
                                    cwd=build, env=env, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, timeout=300)
            print(result.stdout, end="", file=sys.stderr, flush=True)
            if result.returncode:
                raise SystemExit(f"Compilation failed for {source.name}: {result.returncode}")
            audits = audit_output(result.stdout, expected)
            records.append({"source": str(source.relative_to(ROOT)),
                            "scope": SCOPES[module],
                            "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
                            "theorems_checked": len(audits), "axioms": audits,
                            "stdout": result.stdout})
    record = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "status": "passed", "scope": "supporting results and analytic transfers in the pinned hill libraries",
              "original_conjecture_proved": False, "official_autolab_score": None,
              "compiler": version, "image": IMAGE,
              "answer_source_sha256": hashlib.sha256(
                  (PROJECT / "FormalConjecturesUtil/Answer.lean").read_bytes()).hexdigest(),
              "theorems_checked": sum(r["theorems_checked"] for r in records),
              "allowed_axioms": sorted(ALLOWED), "modules": records}
    payload = json.dumps(record, indent=2) + "\n"
    if args.output:
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(payload)
        print(f"PASS: {record['theorems_checked']} theorem audits. Report: {destination}")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
