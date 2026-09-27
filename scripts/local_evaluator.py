#!/usr/bin/env python3
"""Run the unchanged Erdős 3 AutoLab evaluator in its pinned local image."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".local-evaluator"
HILL = ROOT / ".autolab/hills/erdos-3"
IMAGE = "ghcr.io/ottogin/lean-mathlib@sha256:964547ad81e109c78545512867bae70b710c55d833078674878faad7de0ebb85"
ORIGIN = "0149383772ad4a7c7cc45a434de11be51678a524"
CONTEXT = "colima-erdos3"
HILLS = ["uv", "tool", "run", "--from", "hills==0.11.0", "hills"]


def environment():
    for name in ("tmp", "reports", "hills-home"):
        (STATE / name).mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update(DOCKER_CONTEXT=CONTEXT, DOCKER_DEFAULT_PLATFORM="linux/amd64",
               HILLS_RUNTIME="docker", HILLS_HOME=str(STATE / "hills-home"),
               TMPDIR=str(STATE / "tmp"))
    return env


def run(args, *, capture=False, check=True):
    print("+ " + shlex.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), cwd=ROOT, env=environment(),
                          text=True, capture_output=capture, check=check)


def verify_target():
    manifest = json.loads((ROOT / "research/autolab/public-files-manifest.json").read_text())
    frozen = {"statement.lean", "eval.py", "hill.yaml", "pyproject.toml", "tests/test_hill.py"}
    records = {entry["path"]: entry for entry in manifest["files"]}
    if manifest.get("tree_hash") != ORIGIN or len(records) != len(manifest["files"]) or not frozen <= records.keys():
        raise SystemExit("The provenance manifest is incomplete, duplicated, or refers to a different hill version")
    for name in sorted(frozen):
        file = HILL / name
        if not file.is_file() or hashlib.sha256(file.read_bytes()).hexdigest() != records[name]["sha256"]:
            raise SystemExit(f"Fixed target differs from the preserved upstream snapshot: {file}")


def start():
    for tool in ("colima", "docker", "uv"):
        if not shutil.which(tool):
            raise SystemExit(f"Missing {tool}. See docs/local-evaluator.md for installation.")
    run(["colima", "--profile", "erdos3", "start", "--vm-type", "vz", "--vz-rosetta",
         "--cpu", "8", "--memory", "16", "--disk", "60",
         "--mount", f"{ROOT}:w", "--ssh-config=false", "--activate=false"])
    for _ in range(60):
        ready = subprocess.run(["docker", "info", "--format", "{{.ServerVersion}}"],
                               env=environment(), text=True, capture_output=True, timeout=10)
        if ready.returncode == 0:
            print(f"Docker ready: {ready.stdout.strip()}")
            return
        time.sleep(1)
    raise SystemExit("Colima started but its Docker context did not become ready")


def setup():
    start()
    run(["docker", "pull", "--platform", "linux/amd64", IMAGE])
    if not HILL.exists():
        run(["autolab", "hills", "pull", "ottogin/erdos-3", "--version", ORIGIN])
    verify_target()
    committed = run(["git", "--git-dir", HILL / ".vc", "rev-parse", "--verify", "HEAD"],
                    capture=True, check=False)
    if committed.returncode:
        run([*HILLS, "commit", HILL, "-m", "Local reproduction of pinned ottogin/erdos-3"])
    print("Local environment ready. Run: python3 scripts/local_evaluator.py smoke")


def evaluate(submission, output=None):
    verify_target()
    submission = Path(submission).resolve()
    if not (submission / "solution.lean").is_file():
        raise SystemExit("Submission must be a directory containing solution.lean")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    report = Path(output).resolve() if output else STATE / "reports" / f"attempt-{stamp}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    run([*HILLS, "eval", submission, "-H", HILL, "--runtime", "docker", "-v", "-o", report])
    data = json.loads(report.read_text())
    run([*HILLS, "verify", report])
    print(f"Report: {report}")
    print(json.dumps({k: data.get(k) for k in ("passed", "metrics", "details")}, indent=2, ensure_ascii=False))
    print("This is a local evaluation, not an official AutoLab leaderboard score.")
    return data


def smoke():
    verify_target()
    run(["docker", "run", "--rm", "--init", "--platform", "linux/amd64",
         "--user", f"{os.getuid()}:{os.getgid()}", "--mount", f"type=bind,src={ROOT},dst=/workspace,readonly",
         "--network", "none", IMAGE, "python", "/workspace/scripts/container_smoke.py"])
    data = evaluate(HILL / "examples/baseline", STATE / "reports/baseline.json")
    if data.get("passed") is not False or data.get("details", {}).get("error") != "the proof uses sorry":
        raise SystemExit("Unexpected baseline outcome; inspect the report before continuing.")
    print("SMOKE PASS: imported-library proof accepted; original admitted baseline rejected.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("setup", "start", "stop", "status", "smoke", "shell"):
        sub.add_parser(name)
    evaluate_parser = sub.add_parser("eval")
    evaluate_parser.add_argument("submission")
    evaluate_parser.add_argument("--output")
    args = parser.parse_args()
    if args.command == "setup": setup()
    elif args.command == "start": start()
    elif args.command == "stop": run(["colima", "--profile", "erdos3", "stop"])
    elif args.command == "status":
        run(["colima", "--profile", "erdos3", "status"])
        run(["docker", "image", "inspect", IMAGE, "--format", "{{json .RepoDigests}}"])
        run([*HILLS, "describe", HILL])
    elif args.command == "smoke": smoke()
    elif args.command == "eval":
        result = evaluate(args.submission, args.output)
        raise SystemExit(0 if result.get("passed") else 2)
    elif args.command == "shell":
        run(["docker", "run", "--rm", "-it", "--platform", "linux/amd64",
             "--user", f"{os.getuid()}:{os.getgid()}", "--mount", f"type=bind,src={ROOT},dst=/workspace",
             "-w", "/opt/formal-conjectures", IMAGE, "bash"])


if __name__ == "__main__":
    main()
