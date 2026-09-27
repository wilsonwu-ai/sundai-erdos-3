# AutoLab Erdős 3: exact task and reproducibility notes

Inspected 2026-09-27. No hosted climb, remote evaluation, score submission, rental, or paid model request was started.

**Local-container follow-up:** the dedicated Colima/Docker environment has now been installed and the pinned image pulled. The recovered hill froze locally with the exact published tree hash. The image's actual `FormalConjecturesUtil/Answer.lean` hashes to `c8b3b31e9bb25c511e577b1812159a210e9346720f19ec6c6b30905a0802db7a`, identical to the historical source below. See [local setup and commands](../docs/local-evaluator.md) for the active environment; the initial investigation and its former runtime blocker are preserved below.

## The immutable target

- [AutoLab hill](https://app.autolab.ai/hills/ottogin/erdos-3): `ottogin/erdos-3`, version `0.1.0`.
- Official tree hash: `0149383772ad4a7c7cc45a434de11be51678a524`.
- Official commit: `eadb2b1ce37869284d2d0d0343161b94fc96a9e2`.
- Toolchain declared by the evaluator: Lean `v4.33.1`.
- Image: `ghcr.io/ottogin/lean-mathlib@sha256:964547ad81e109c78545512867bae70b710c55d833078674878faad7de0ebb85`.
- Image platform: Linux `amd64`; built 2026-09-09. Its formal-conjectures source/cache layer is about 3.33 GB compressed.

Public source copies are in [autolab/erdos-3](autolab/erdos-3/). [public-files-manifest.json](autolab/public-files-manifest.json) records every copied file's SHA-256, byte length, origin tree, and commit. [hill-metadata.json](autolab/hill-metadata.json) preserves selected task-level API metadata. The `.autolab/` working state is ignored by Git.

The exact fixed statement is:

```lean
import FormalConjecturesUtil

namespace Erdos3

theorem hill : answer(sorry) ↔ ∀ A : Set ℕ,
    (¬ Summable fun a : A ↦ 1 / (a : ℝ)) →
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k :=
```

The user-provided paste mentions Erdős **13**, but the requested URL and recovered task are Erdős **3**. They are different hills.

The [organizer's live openmath list](https://app.autolab.ai/lists/alejandrozu/openmath) now identifies **seven** runnable hills and says Erdős 3 was added after the original six-problem selection. Its task-level metadata and opening description are preserved in [openmath-list.json](autolab/openmath-list.json); user-specific fields and the unrelated 100-entry research catalog are omitted. The list itself distinguishes a hill's score from mathematical and competition review.

## What a passing submission would mean

The hill asks for a directory containing only the proof term or `by` block in `solution.lean`. The evaluator appends it to the fixed statement, appends `#print axioms hill`, and invokes Lean in the pinned environment. Compilation must succeed, the combined output must not report `sorry`/`sorryAx`, and the printed axiom set must be a subset of `propext`, `Classical.choice`, and `Quot.sound`. The metric is binary: `proved = 1` only on acceptance. There is no partial-credit metric.

The raw `answer(sorry)` is a formal-conjectures answer marker. It is **not sufficient evidence that the task is broken**. The upstream answer elaborator current before the image build defaults this marker to `True` when the expected type is `Prop`. See [Answer-at-image-date.lean](autolab/Answer-at-image-date.lean), especially lines 66–69 and 136–139, from [upstream commit c252a410](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjecturesUtil/Answer.lean).

Initially that source version was identified using the last commit affecting the file before the image's build time. The later local-container setup directly measured the file inside the pinned image and confirmed its byte hash matches. This confirms that file; it does not reconstruct the Git revision of the entire source checkout. [image-config.json](autolab/image-config.json) shows that the image cloned the default branch without a commit argument and deleted `.git`; [image-manifest.json](autolab/image-manifest.json) preserves its layer digests.

Under the default elaborator, this is `True ↔` the full Erdős arithmetic-progression conjecture. A proof of a finite experiment or a special case is useful progress but does not complete this hill.

## Initial local workflow and the former blocker

The installed CLI successfully downloaded the public files with:

```sh
cd research/autolab
autolab hills pull ottogin/erdos-3 --version 0149383772ad4a7c7cc45a434de11be51678a524
```

It put them at `.autolab/hills/erdos-3` beneath `research/autolab`. That initial local commit stopped at the dependency check because Docker, Podman, Apptainer, and Singularity were absent. The files were still downloaded. No proof evaluation ran during that operation. The follow-up setup installed Colima/Docker, downloaded the active working hill under the repository root's `.autolab/hills/erdos-3`, and successfully froze its unchanged public files.

With the required container runtime and a registered/committed local hill, the official OSS tool's documented evaluation commands are:

```sh
hills describe erdos-3
hills eval /absolute/path/to/submission -H erdos-3 -o report.json
hills verify report.json
```

The CLI says a non-owner receives public files and locally generated scores are unofficial; the original owner can pull the exact bundle. The task's empty `private.lock` can be inspected directly, but that does not convert this public download into an official scored run. See [AutoLab local workflow](https://docs.autolab.ai/concepts/) and the [hills command reference](https://github.com/autolab-ai/hills#reference).

A direct native Lean check can help develop a proof if its toolchain and dependencies match, but it must be labeled separately from an AutoLab image run and official score. Do not rewrite the fixed statement, weaken the requested theorem, or treat an altered evaluator as the same hill.

## Hosted climb workflow and cost boundary

The [AutoLab climb guide](https://docs.autolab.ai/guides/projects/) documents `autolab init --hill ottogin/erdos-3` as creating a paused climb, and `autolab start` as starting it. The web menu also offers an entirely-local mode and a hosted mode driven by one's own coding agent. Hosted mode still uses AutoLab's selected model for analysis and needs attached or rented compute. The [experiment guide](https://docs.autolab.ai/guides/experiments/) documents `autolab submit` as committing, uploading, and queuing an experiment.

No documented, guaranteed-free hosted evaluation route was found. No hosted action was taken. Local proof development and public artifact preparation can proceed without starting one.

## Retrieval notes

Anonymous HTTP access to the exact hill URL returned `404`; its trailing-slash route redirected to sign-in. The installed AutoLab CLI's existing authentication could read the **public** hill through its documented client API. Credential values were neither printed nor saved in this project. The read-only helper [fetch_public_metadata.py](autolab/fetch_public_metadata.py) saves only selected hill metadata and public OCI metadata.
