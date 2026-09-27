"""Positive import/check test inside the original hill image; not a hill proof."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

project = Path("/opt/formal-conjectures")
lake = project / ".lake"
libs = [lake / "build/lib/lean", *sorted((lake / "packages").glob("*/.lake/build/lib/lean"))]
env = dict(os.environ)
env["LEAN_PATH"] = ":".join(str(p) for p in libs if p.is_dir())
version = subprocess.run(["lean", "--version"], text=True, capture_output=True, check=True).stdout.strip()
assert "version 4.33.1," in version, version
source = """import FormalConjecturesUtil
theorem local_import_smoke : (answer(sorry) : Prop) ↔ True := by rfl
#print local_import_smoke
#print axioms local_import_smoke
"""
with tempfile.TemporaryDirectory(prefix="erdos3-smoke-") as directory:
    file = Path(directory) / "Smoke.lean"
    file.write_text(source)
    check = subprocess.run(["lean", str(file)], env=env, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=300)
    print(check.stdout, end="")
    assert check.returncode == 0, "Positive import smoke proof failed"
    assert "sorryAx" not in check.stdout and "declaration uses 'sorry'" not in check.stdout
    assert "'local_import_smoke' does not depend on any axioms" in check.stdout
    assert re.search(r"local_import_smoke\s*:\s*True ↔ True", check.stdout)
answer = project / "FormalConjecturesUtil/Answer.lean"
print(json.dumps({"status":"passed", "scope":"positive import smoke test, not full hill proof",
                  "compiler":version, "answer_source_sha256":hashlib.sha256(answer.read_bytes()).hexdigest(),
                  "toolchain":(project/"lean-toolchain").read_text().strip()},indent=2))
