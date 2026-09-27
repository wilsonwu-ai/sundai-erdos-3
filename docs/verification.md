# Verification record

## Current pinned-image proof checkpoint

`python3 scripts/local_evaluator.py check-lean` compiled four modules in the actual frozen hill image and audited all **23** theorem declarations: fourteen original elementary results, five definition/filter bridges, three divergence consequences, and one conditional reduction. The source hashes are computed from the exact copied compilation inputs. Every axiom set is a subset of `propext`, `Classical.choice`, and `Quot.sound`. [Machine-readable evidence](../artifacts/mathlib-verification.json).

Independent review checked cardinality, the empty progression, positive common difference, preservation of hypotheses, and the conditional reduction's scope. The latter's `APFreeSummability` parameter is explicitly printed and remains unproved. The image compiler also passed the valid control and rejected the four invalid controls.

The updated exact-hill attempt reached the new goal of reciprocal summability for a progression-free set, then failed at the deliberate unproved step. Its rejection and local signature verification are recorded in [reduction-attempt.json](../artifacts/reduction-attempt.json). That expected rejection is separate from the passing supporting-module checks.

The Pages workflow now requires both the original host-compiler job and a new pinned-image Mathlib job before publication. The historical verification record below remains the provenance of the first checkpoint.

## Formal artifact

The coordinator executed `python3 scripts/verify_lean.py` on the actual proof file using Lean 4.33.1. All 14 theorem declarations compiled and every printed axiom set was a subset of `propext`, `Classical.choice`, and `Quot.sound`. The machine-readable result, source hash, compiler identity, and stdout are in [artifacts/lean-verification.json](../artifacts/lean-verification.json).

`python3 scripts/test_verifier.py` accepted a valid control and rejected four negative controls: an admitted proof, a custom axiom, a false proof, and a missing axiom printout. These are tests of our local workflow. They do not certify AutoLab's evaluator or prove the mathematical conjecture.

An independent worker reran the compiler and reviewed statements, positivity of the common difference, distinctness, quantifiers, the powers-of-two argument, and the missing connections to the exact hill. [Independent review](independent-review.md).

In the initial pass, the answer-marker behavior was reproduced in core Lean and supported by historical source, without executing the exact image. The subsequent [local-container setup](local-evaluator.md) pulled that image and measured its actual `Answer.lean`: its hash matches the historical source. The local setup guide records the follow-up environment checks separately from the original 14-theorem artifact.

## Deployment and interface

The GitHub Actions workflow requires compiler and finite-explorer checks before Pages deployment. A successful website build is not a proof of Erdős 3.

- `node --test tests/explorer.test.mjs`: four suites pass. An independent combinations-based oracle checks all 1,024 subsets of `{1,…,10}` at seven progression lengths (7,168 cases). A separate closed-form count checks all integers through 300. Input boundaries and primality are also checked.
- [Local browser report](../artifacts/browser-qa.json): 19 checks pass in Chrome, including prime patterns, next-pattern interaction, powers of two, custom-set validation and deduplication, 300-number/8-term limits, 16-term construction, disclosure, keyboard button activation, four evidence labels, and visible open-conjecture status. No page errors or failed requests remain.
- Desktop 1440 px and mobile 390/320 px widths have no horizontal overflow. The coordinator inspected desktop and mobile screenshots for type hierarchy, diagram legibility, color/contrast, wrapping, spacing, control placement, and the status label.
- The exact README Mermaid source rendered with `mmdc`; the coordinator inspected its raster preview for clipped labels and confusing arrows. The two smaller graph-plan diagrams also rendered successfully. GitHub's Markdown API rendered the surrounding README and recognized its Mermaid fence.

Browser reproduction uses `scripts/browser_qa.mjs`, with optional `SITE_URL`, `PUPPETEER_MODULE`, and `CHROME` environment variables. Screenshots are local QA artifacts ignored by Git. The site itself has no runtime dependencies or external assets.

The [first hosted verification and deployment run](https://github.com/wilsonwu-ai/sundai-erdos-3/actions/runs/36335702610) passed on Ubuntu. This independently reran the 14 local proofs with the pinned Linux compiler, negative controls, finite-explorer tests, and answer-marker reproduction before deploying Pages. The [live site](https://wilsonwu-ai.github.io/sundai-erdos-3/) returned HTTP 200. [Production browser QA](../artifacts/production-browser-qa.json) then passed the same 19 interaction, evidence, responsiveness, and error checks on the published URL.

## Local evaluator follow-up

The follow-up installed Colima 0.10.3, Lima 2.2.0, Docker CLI 29.8.1, and Docker Buildx 0.37.1. A dedicated `erdos3` VM uses Apple virtualization and existing Rosetta support, with 8 CPUs, 16 GiB RAM, and a 60 GiB sparse data disk. The Docker server is 29.5.2. Only this project is shared into the VM, and the default Docker context remains unchanged.

The original AMD64 image was pulled by digest. `hills==0.11.0` checked the contract and froze the original public hill; the resulting tree exactly matches `0149383772ad4a7c7cc45a434de11be51678a524`. A separate proof importing the actual image's `FormalConjecturesUtil` compiled on its Lean 4.33.1 binary, printed `True ↔ True`, and required no axioms. The original `by sorry` baseline was rejected by the unchanged evaluator with `passed: false` and `the proof uses sorry`; `hills verify` confirmed its local report signature. This is local environment verification, not a successful proof or a remote score.

The helper in [local-evaluator.md](local-evaluator.md) preserves the fixed target hashes, scopes the runtime environment, stores signing keys and reports in ignored directories, and returns a distinct rejection status for failed proofs. An independent code review found a manifest completeness gap before use; the helper now requires all five frozen file records, rejects duplicates, and checks the exact origin hash before comparing file hashes.

The editable starter also ran through the actual evaluator, reached the intended divergence-to-progressions proof obligation, and returned the expected wrapper exit `2`. Its full local report signature verified. The [sanitized machine-readable record](../artifacts/local-evaluator-verification.json) preserves these results without publishing the signing key or claiming a remote score.

## Graph retrospective

```text
RUN RETRO — sundai-erdos-3 · 2026-09-27
VERIFIER KILL RATE   0/14 submitted theorem declarations rejected; 4/4 negative controls rejected
FAN-OUT EFFICIENCY   3/3 delegated workers returned useful artifacts (100%)
COMPRESSION RATIO    source/probe corpus → 3 scoped worker reports + 14 checked declarations; raw item count not instrumented
RETURNED VS SENT     4/4 assignments returned (3 initial tasks + independent-review follow-up)
COST                 ~24k delegated-token planning allowance → actual usage unavailable; no paid external model calls
```

Recommendation: leave the graph width unchanged. Future work should target a precise missing lemma and its dependencies before allocating more proof-search workers.
