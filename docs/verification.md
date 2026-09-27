# Verification record

## Formal artifact

The coordinator executed `python3 scripts/verify_lean.py` on the actual proof file using Lean 4.33.1. All 14 theorem declarations compiled and every printed axiom set was a subset of `propext`, `Classical.choice`, and `Quot.sound`. The machine-readable result, source hash, compiler identity, and stdout are in [artifacts/lean-verification.json](../artifacts/lean-verification.json).

`python3 scripts/test_verifier.py` accepted a valid control and rejected four negative controls: an admitted proof, a custom axiom, a false proof, and a missing axiom printout. These are tests of our local workflow. They do not certify AutoLab's evaluator or prove the mathematical conjecture.

An independent worker reran the compiler and reviewed statements, positivity of the common difference, distinctness, quantifiers, the powers-of-two argument, and the missing connections to the exact hill. [Independent review](independent-review.md).

The upstream answer-marker behavior was reproduced in core Lean. Historical upstream source supports the default `True` behavior, but the exact container was not executed. Its bundled source version is inferred from image construction history and upstream timestamps, not established by a byte-for-byte extraction.

## Deployment and interface

The GitHub Actions workflow requires compiler and finite-explorer checks before Pages deployment. A successful website build is not a proof of Erdős 3.

- `node --test tests/explorer.test.mjs`: four suites pass. An independent combinations-based oracle checks all 1,024 subsets of `{1,…,10}` at seven progression lengths (7,168 cases). A separate closed-form count checks all integers through 300. Input boundaries and primality are also checked.
- [Local browser report](../artifacts/browser-qa.json): 19 checks pass in Chrome, including prime patterns, next-pattern interaction, powers of two, custom-set validation and deduplication, 300-number/8-term limits, 16-term construction, disclosure, keyboard button activation, four evidence labels, and visible open-conjecture status. No page errors or failed requests remain.
- Desktop 1440 px and mobile 390/320 px widths have no horizontal overflow. The coordinator inspected desktop and mobile screenshots for type hierarchy, diagram legibility, color/contrast, wrapping, spacing, control placement, and the status label.
- The exact README Mermaid source rendered with `mmdc`; the coordinator inspected its raster preview for clipped labels and confusing arrows. The two smaller graph-plan diagrams also rendered successfully. GitHub's Markdown API rendered the surrounding README and recognized its Mermaid fence.

Browser reproduction uses `scripts/browser_qa.mjs`, with optional `SITE_URL`, `PUPPETEER_MODULE`, and `CHROME` environment variables. Screenshots are local QA artifacts ignored by Git. The site itself has no runtime dependencies or external assets.

The [first hosted verification and deployment run](https://github.com/wilsonwu-ai/sundai-erdos-3/actions/runs/36335702610) passed on Ubuntu. This independently reran the 14 local proofs with the pinned Linux compiler, negative controls, finite-explorer tests, and answer-marker reproduction before deploying Pages. The [live site](https://wilsonwu-ai.github.io/sundai-erdos-3/) returned HTTP 200. [Production browser QA](../artifacts/production-browser-qa.json) then passed the same 19 interaction, evidence, responsiveness, and error checks on the published URL.

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
