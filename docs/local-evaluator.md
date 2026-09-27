# Local AutoLab evaluator for Erdős 3

The helper runs the unchanged `ottogin/erdos-3` evaluator in its exact pinned Linux image. It uses a dedicated Colima VM on this Apple Silicon Mac. This prepares proof development; it does not solve the conjecture or create a hosted climb.

**Verified September 27, 2026:** the positive imported-library proof passed; the original baseline was rejected specifically for `sorry`; its signed local report verified. The local tree hash exactly matches the published origin, with local commit `b5b9326b6d40f958c044743a2389333c7442cefd`. The actual image's `Answer.lean` hash matches the preserved historical source. The VM is left running for development.

[Recorded environment evidence](../artifacts/local-evaluator-verification.json) includes the compiler, image digest, tree, positive check, baseline rejection, starter proof state, and signature-verification results. It excludes the local signing key.

## Daily commands

From the repository root:

```sh
python3 scripts/local_evaluator.py status
python3 scripts/local_evaluator.py start
python3 scripts/local_evaluator.py check-lean
python3 scripts/local_evaluator.py eval submissions/current
```

`check-lean` compiles the supporting modules under `lean/` using the image's actual libraries, builds their dependencies in a temporary container directory, and audits every declared theorem. It saves [mathlib-verification.json](../artifacts/mathlib-verification.json). This is the command for a passing supporting-results check; it does not submit those modules as a solution of the full hill.

Edit [`submissions/current/solution.lean`](../submissions/current/solution.lean), which contains only the proof body after the fixed statement's `:=`. The current attempt reduces the target to reciprocal summability for a set avoiding a fixed progression length, then deliberately fails at that unproved assertion. Replace the failure with an actual proof. The helper exits `0` for a passing proof and `2` for a rejected proof; infrastructure failures are also nonzero. It prints the exact path of the signed local JSON report.

The attempt was checked in the real container and now stops at `⊢ Summable fun a : A ↦ 1 / (a : ℝ)`, with reciprocal divergence and progression-freeness in scope. [Recorded remaining goal](../artifacts/reduction-attempt.json). Lean's recovery from an unfinished tactic can introduce `sorryAx` internally, even though this attempt uses an explicit `fail` rather than a written `sorry`. The upstream evaluator then gives the generic `the proof uses sorry` reason. Read `details.output` for the actual error and proof state.

To rerun the environment checks:

```sh
python3 scripts/local_evaluator.py smoke
```

This first compiles a tiny, separate proof using `FormalConjecturesUtil` in the pinned image, checks Lean 4.33.1 and its axiom output, and confirms the actual image's proposition answer-marker behavior. It then submits the hill's original `by sorry` baseline to the unchanged evaluator and requires the specific rejection `the proof uses sorry`. An expected rejection confirms the evaluator is working; it is not a solved hill.

To inspect the image interactively or free the VM's CPU/RAM allocation:

```sh
python3 scripts/local_evaluator.py shell
python3 scripts/local_evaluator.py stop
```

The shell starts in `/opt/formal-conjectures`; the repository is at `/workspace`. Use the image's own Lean and libraries. Stopping preserves the image cache and local reports; `start` resumes the VM. No login-start service is installed.

## Reproduce setup on an Apple Silicon Mac

Prerequisites: macOS virtualization support, installed Rosetta, Homebrew, `uv`, and an authenticated AutoLab CLI able to read the public hill. The machine used here already had Rosetta, `uv`, and AutoLab.

```sh
brew install colima docker docker-buildx
python3 scripts/local_evaluator.py setup
python3 scripts/local_evaluator.py smoke
```

Docker Buildx is optional for this prebuilt-image evaluator. If desired, follow Homebrew's plugin-path instructions. This session installed a plugin symlink in `~/.docker/cli-plugins/`.

The helper uses:

| Setting | Value |
| --- | --- |
| Colima profile | `erdos3` |
| Docker context | `colima-erdos3`, scoped to each helper subprocess |
| VM | ARM64, Apple Virtualization Framework, Rosetta for AMD64 |
| Resources | 8 CPUs, 16 GiB RAM, 60 GiB sparse data disk |
| Host share | This repository only |
| Container platform | `linux/amd64` |
| Host AutoLab runner | `hills==0.11.0`, matching the installed client pin |
| Lean | `4.33.1`, supplied by the pinned image |
| Official origin tree | `0149383772ad4a7c7cc45a434de11be51678a524` |
| Image | `ghcr.io/ottogin/lean-mathlib@sha256:964547ad81e109c78545512867bae70b710c55d833078674878faad7de0ebb85` |

`setup` downloads the original public hill to `.autolab/hills/erdos-3`, checks the preserved hashes for the statement, evaluator, manifest, dependency declaration, and hill test, then creates its local frozen version if needed. It does not overwrite an existing hill or weaken the statement. It leaves the image's bundled dependencies unchanged.

The helper scopes `HILLS_HOME` and Python's `TMPDIR` inside `.local-evaluator/`, so all AutoLab bind mounts fit within the repository share. `.local-evaluator/` and `.autolab/` are Git-ignored. Local signing keys, working copies, caches, and full reports stay there. Nothing changes the user's default Docker context.

## Local versus official

AutoLab provides non-owners the public hill files. A locally frozen tree and locally valid signature do not establish an official score for the upstream owner's hill. The raw tool's `official` field refers to its local committed-tree policy; this project reports upstream acceptance separately. No remote score submission, hosted climb, compute rental, or remote execution-node service is started by this helper.

The mathematical target remains exactly the original one. The separate positive smoke theorem and the repository's supporting modules are not substituted for it. A genuine candidate must pass compilation and the original axiom policy in this image, followed by independent review of the claim and proof.

The [CLI investigation](local-evaluator-cli-notes.md) explains the source-checked flags, mount behavior, and why a failed-proof report cannot be identified solely by the official CLI's exit status. [Colima installation](https://github.com/abiosoft/colima/blob/main/docs/INSTALL.md), [Colima runtime configuration](https://github.com/abiosoft/colima/blob/main/docs/FAQ.md), and [AutoLab concepts](https://docs.autolab.ai/concepts/) are the upstream references.
