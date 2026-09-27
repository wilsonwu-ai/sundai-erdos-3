# Local evaluator CLI notes

Inspected the installed AutoLab client and its cached official `hills` package on 2026-09-27. These are source-verified setup notes; actual runtime acceptance results belong in the local evaluator report.

## Tool version and invocation

The installed AutoLab client pins **`hills==0.11.0`** in `autolab.execnode.hills.DEFAULT_HILLS_VERSION`. Its `autolab hills` wrapper launches:

```sh
uv tool run --from hills==0.11.0 hills
```

The image happens to contain `hills==0.5.0`; that is its own dependency and should not be silently upgraded. Host `hills` runs a standard-library shim in the image, so the host package is not injected into the container. Running `hills` from AutoLab's Python virtual environment directly is unnecessary: AutoLab itself uses the `uv tool run` command above.

The CLI resolves either a local hill name under `.autolab/hills` or a direct path ending in a directory containing `hill.yaml`. There is no separate global hill-registration command required for an existing downloaded hill. The previous public pull already created `.vc`; its initial commit failed only because a runtime was absent.

## Scoped environment

For the named Colima VM selected for this project, use these variables only in the task shell/script:

```sh
export DOCKER_CONTEXT=colima-erdos3
export DOCKER_DEFAULT_PLATFORM=linux/amd64
export HILLS_RUNTIME=docker
export HILLS_HOME=/Applications/sundai-erdos-3/.local-evaluator/hills-home
export TMPDIR=/Applications/sundai-erdos-3/.local-evaluator/tmp
```

Create the last directory before launching Python. Do not repurpose `HOME`. `HILLS_HOME` contains the local signing key and must remain Git-ignored. The key need not be printed or copied into reports.

The runtime builds `docker run` without a `--platform` flag. Docker inherits the caller's environment, so the scoped `DOCKER_DEFAULT_PLATFORM` selects AMD64 for both pull and run. `DOCKER_CONTEXT` similarly selects the task VM without changing the user's globally selected context. A client executable alone is insufficient: the package tests `docker info` before declaring Docker usable.

## Required shares and mounts

`hills eval` mounts:

1. Its run directory under `HILLS_HOME/runs/…`, read/write. This contains the proof snapshot, materialized hill, shim, invocation, logs, and result.
2. The original hill directory, read-only, for references back to any locked files. In `--current` mode the working hill is mounted read/write instead.

`hills check` also creates a host temporary directory with prefix `hills-check-` and mounts that directory read-only. A project-local `TMPDIR` keeps this mount within the project share. With the paths above, sharing **`/Applications/sundai-erdos-3`** into the VM covers the evaluator's host bind mounts; broad home and macOS temporary-directory shares are unnecessary for this CLI path. Docker's own storage remains in its VM.

The package preserves absolute host paths inside the container. It passes the invoking UID/GID to Docker, neutralizes the image entrypoint, and keeps the image's own `PATH`. It only explicitly forwards `HILLS_RUN_DIR` and `HILLS_HILL_ROOT` during evaluation. A host `LEAN_PROJECT` override is therefore not automatically forwarded and is unnecessary: the fixed evaluator defaults to `/opt/formal-conjectures` in the image.

## Recommended first checks

From the repository root, the active downloaded hill is:

```sh
ERDOS3_HILL="$PWD/.autolab/hills/erdos-3"
```

The following is the manual bootstrap sequence for an uncommitted download. The helper in [local-evaluator.md](local-evaluator.md) automates setup and uses the committed hill once ready. `--current` is explicit in this bootstrap example:

```sh
uv tool run --from hills==0.11.0 hills check "$ERDOS3_HILL" --runtime docker
uv tool run --from hills==0.11.0 hills eval \
  "$ERDOS3_HILL/examples/baseline" \
  -H "$ERDOS3_HILL" --current --runtime docker -v \
  -o .local-evaluator/baseline-report.json
```

After successful runtime checks, a local freeze may be made with the same unchanged downloaded files:

```sh
uv tool run --from hills==0.11.0 hills commit "$ERDOS3_HILL" \
  -m "Freeze downloaded Erdős 3 evaluator for local checks"
```

Future evaluation can omit `--current`. The commit operation reruns the hill's checks and regenerates lock files. Record the resulting local tree hash separately from the published origin hash; a local freeze or valid local signature does not by itself mean that AutoLab accepted a remote score.

A baseline containing `sorry` should produce a report with `passed: false` and the error `the proof uses sorry`. **A valid failed-proof report still produces CLI exit status zero** in `hills 0.11.0`; inspect the JSON, not only the shell status. Runtime/infrastructure failure and intended proof rejection are different outcomes.

`hills check` uses pytest if present in the image; otherwise it directly executes test files. The downloaded test defines a pytest-style function, so merely executing that file would not invoke the assertion. Consequently a green contract check is not enough: independently run the rejected baseline and inspect its reason.

The image is prepared before the timed evaluation. The hill's outer watchdog is 1,800 seconds; its inner Lean timeout is 1,500 seconds. Download time is not charged to that watchdog.

## Positive smoke test boundary

A separate small theorem should compile **inside the pinned image**, importing `FormalConjecturesUtil` and using the same library paths as `eval.py`. This confirms the required Lean binary and compiled library are available, complementing the rejected baseline. For example, a separate smoke file can prove natural addition by zero and print its axioms. Such a theorem is only an environment check: do not substitute it for the fixed hill's statement or present it as a hill submission.

`--runtime host` means the caller is already inside the declared image, or deliberately uses a configured image launcher. It is not the correct shortcut for running this Linux image hill directly with native macOS Lean.

No hosted climb, remote submission, AutoLab execution-node service, or compute rental is needed for this local workflow.

## Code inspected

- Installed AutoLab: `autolab/cli.py`, `_hills_argv`, and `autolab/execnode/hills.py`.
- Official `hills 0.11.0`: `runtime.py` (`detect`, `build_command`, `ensure_image`), `runner.py` (`evaluate`, `_run_evaluator`), `check.py`, `hill.py` (`Hill.resolve`), `paths.py`, and `cli.py` (`cmd_eval`, `cmd_commit`).
- Frozen public task: [`research/autolab/erdos-3/eval.py`](../research/autolab/erdos-3/eval.py) and [`hill.yaml`](../research/autolab/erdos-3/hill.yaml).
