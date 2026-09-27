#!/usr/bin/env python3
"""Negative controls exercise Lean and the audit's refusal to accept bad proofs."""
import subprocess
import tempfile
from pathlib import Path
from verify_lean import audit_output, compiler


def main():
    cases = [
        ("valid", "theorem sample : True := by trivial", True),
        ("admitted", "theorem sample : False := by sorry", False),
        ("extra_axiom", "axiom invented : False\ntheorem sample : False := invented", False),
        ("false_proof", "theorem sample : False := by trivial", False),
        ("missing_audit", "theorem sample : True := by trivial", False),
    ]
    with tempfile.TemporaryDirectory(prefix="erdos3-negative-") as folder:
        for name, source, want in cases:
            path = Path(folder) / "Control.lean"
            path.write_text(source + ("\n#print axioms sample\n" if name != "missing_audit" else "\n"))
            run = subprocess.run([compiler(), str(path)], text=True, stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT, timeout=30)
            accepted = False
            if run.returncode == 0:
                try:
                    audit_output(run.stdout, {"sample"})
                    accepted = True
                except ValueError:
                    pass
            assert accepted == want, (name, run.stdout)
            print(f"PASS {name}: {'accepted' if accepted else 'rejected'}")


if __name__ == "__main__":
    main()
