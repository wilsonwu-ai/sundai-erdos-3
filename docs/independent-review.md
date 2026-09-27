# Independent proof and scope review

The latest [full-proof graph review](../research/full-proof-graph/review.md) audits the remaining mathematical obligation and independently checks the new counterexamples and separated-block construction. These are written mathematical arguments, not additional Lean certificates. The full hill remains unproved.

## Latest Lean review: dyadic analytic transfer

An independent reader reviewed `Erdos3Blocks.lean` and `Erdos3Dyadic.lean`: finite fibers, the explicit zero case, positive dyadic denominators, exact finite cardinality, unique partition, nonnegative comparison, and the shifted p-series with p>1. No logical defect was found. The coordinator corrected one elaboration failure involving function composition, then all 30 supporting declarations passed the pinned-image compiler and axiom audit.

`APFreePowerEnvelope` remains an unproved parameter. Its constants depend on the progression length and must work uniformly over all relevant sets and blocks. This is a sufficient quantitative hypothesis, not a proved estimate or a claimed equivalence to Erdős 3. The full proof was not obtained. [Detailed research attempt](../research/proof-attempt-2026-09-27.md).

## Continuation review: exact hill bridges

The continuation added `Erdos3Bridge.lean` (five declarations), `Erdos3Divergence.lean` (three), and `Erdos3Reduction.lean` (one). Independent read-only review confirmed the forward bridge uses positive-step injectivity to obtain **exactly** `k` elements, handles `k=0`, and produces the hill's precise filter conclusion for its stated special cases. It does not claim a reverse equivalence.

The divergence module retains the exact non-summability hypothesis and establishes only infinitude, unboundedness, and length two. The conditional reduction retains `APFreeSummability` as an unproved theorem parameter. Its standard axiom list is not evidence that the parameter has been established.

The coordinator ran the final four-module checker inside the pinned image: all 23 declarations compiled and passed their axiom audits. The reviewer also identified a source-hash race in the new checker; it now hashes the immutable bytes actually copied for compilation. The compiler selector was corrected so a mounted Mac executable cannot be selected inside Linux. Positive and negative controls passed using the image compiler. [Executed module record](../artifacts/mathlib-verification.json).

The earlier review below records the initial fourteen-result scope. Its missing bridges are superseded by the continuation above; its warning about the unchanged external evaluator remains relevant.

## Initial checkpoint

Reviewed 2026-09-27 by a separate agent that did not author the proof. **PASS for the 14 stated elementary theorems. The full Erdős 3 hill is not solved by these files.**

## Reproduction

Both commands completed with exit code `0`:

```sh
.tools/lean-4.33.1-darwin_aarch64/bin/lean lean/Erdos3SpecialCases.lean
.tools/lean-4.33.1-darwin_aarch64/bin/lean research/math/AnswerDefaultRepro.lean
```

The checked executable reported Lean `4.33.1`, `arm64-apple-darwin24.6.0`, release commit `819816b2e0a3bf405af45ae5c7af2491d8f5bee6`. This was a native macOS run, not a run inside AutoLab's Linux AMD64 image.

Reviewed file hashes:

| File | SHA-256 |
| --- | --- |
| `lean/Erdos3SpecialCases.lean` | `83f4ca47095bda82b1ddb1020d569607a925d45945522f03b84f8972f7248383` |
| `research/math/AnswerDefaultRepro.lean` | `820a8a3972e08f6cc6450c52ac7a6cfe3d84415b0d02f91a49c9b082d642fa2d` |
| `research/autolab/erdos-3/eval.py` | `8a0ac14c62863b6d738b91d311e63f5caa0be608849b761ee238711d9dcdc215` |

## Theorem review

`ContainsAP A k` requires a natural start, a **strictly positive** natural step, and membership of all `k` indexed terms. The positive-step requirement excludes repeating one point as an apparent long progression. `ap_terms_strictly_increase` establishes strict increase for every pair of increasing indices, so all indexed terms are distinct. Length zero is intentionally vacuous; the results quantify over every finite length and therefore cannot be discharged using length zero alone.

| Checked declarations | Assessment |
| --- | --- |
| `ap_terms_strictly_increase` | Strict monotonicity follows from a positive step. Valid distinctness guarantee. |
| `containsAP_mono`, `arbitrarilyLongAPs_mono` | Membership and progression properties pass to supersets. |
| `containsAP_prefix` | The first `l` terms of a length-`k` progression work when `l ≤ k`. |
| `unbounded_lengths_iff_all_lengths` | Prefix closure converts unbounded available lengths into every finite length; the reverse implication chooses the requested length itself. |
| `cofinite_contains_all_lengths` | Its explicit hypothesis is that every number at or above `N` belongs to the set. Starting at `N` with step one works. |
| `affine_tail_contains_all_lengths` | A set containing the specified tail of a nonconstant arithmetic progression contains every finite length. The hypothesis explicitly requires positive step. |
| `multiples_contain_all_lengths` | Every multiple set for `d > 0` contains the progression starting at zero with step `d`. Zero is allowed because the underlying type is `Nat`. |
| `unbounded_contains_two` | Unboundedness gives `a` and a second element `b ≥ a+1`; the constructed difference `b-a` is positive. |
| `powers_two_no_midpoint` | If the final exponent exceeds the middle exponent, the last power is already at least twice the middle power; adding the first positive power rules out the midpoint equation. |
| `powers_two_no_three` | Positive step forces increasing middle and last powers, hence increasing exponents. The midpoint lemma then rules out a three-term progression. |
| `nat_lt_two_pow`, `powers_two_unbounded` | Induction proves the elementary exponential bound and supplies an explicit power of two beyond each threshold. |
| `unbounded_does_not_imply_all_lengths` | Instantiates the purported universal implication with powers of two, contradicting their lack of a three-term progression. |

All 14 declarations had axiom output. Five use no axioms; the others use subsets of `propext`, `Classical.choice`, and `Quot.sound`. The actual proof file contains no `sorry`, `admit`, `native_decide`, `unsafe`, or custom axiom declaration. Ordinary `decide` is used for small decidable arithmetic facts and produces Lean-checkable proof terms. The source contains no commands designed to impersonate axiom output.

No mathematical defect was found in these statements or proofs. They prove elementary facts already known mathematically; they do not establish new general progress on the conjecture.

## Scope that must remain explicit

The local development imports `Std` and uses its own `ContainsAP` predicate. It does **not** prove an equivalence with Mathlib's `Set.IsAPOfLength`, nor translate its `∀ k` formulation into the exact hill's `Filter.Frequently` formulation. The relationship is mathematically natural, but a checked bridge is absent.

There are no real reciprocal sums in this file. In particular, it does not prove that reciprocal divergence implies unboundedness, that the displayed positive families satisfy the original divergence premise, or that powers of two have a convergent reciprocal sum. Its powers-of-two result refutes the weaker claim that **unboundedness alone** guarantees arbitrary progressions; it is not a counterexample to Erdős 3.

The cofinite theorem's explicit threshold hypothesis is checked. Equivalence of that hypothesis with an abstract finite-complement predicate is not formalized here. Similarly, the powers-of-two theorem proves unboundedness directly; a separate abstract set-infinitude equivalence is not needed by its stated conclusion and is not included.

Calling these results “14 checked elementary theorems related to Erdős 3” is supported. Calling them an accepted AutoLab proof, a solution of the full divergent-sum conjecture, or a disproof via powers of two is unsupported.

## Answer-marker reproduction

`AnswerDefaultRepro.lean` contains a small, explicit replacement elaborator modeling one branch of upstream behavior. Lean printed:

```text
theorem proposition_placeholder : True ↔ True :=
Iff.rfl
'proposition_placeholder' does not depend on any axioms
'proposition_placeholder_is_true' does not depend on any axioms
```

Thus the modeled `Prop` placeholder becomes `True` without introducing `sorryAx`. This is a valid minimal reproduction of the branch, **not an import or execution of the exact AutoLab image's `FormalConjecturesUtil`**. The file's header correctly states this limit. Its two demonstration theorems are separate from the 14 elementary theorems.

## Static observation about the upstream evaluator

An external checker weakness was found by reading the downloaded evaluator; no adversarial submission was created or run. In `_axioms`, the presence of `does not depend on any axioms` anywhere in combined process output immediately returns the empty set. Otherwise the first matching `depends on axioms: [...]` is used. The parser does not bind that text to the fully qualified target declaration `Erdos3.hill`.

Because the evaluator concatenates submitted source and subsequently parses textual process output, this is an insufficient trust boundary for arbitrary hostile submissions. It is a reason to independently inspect the actual target declaration and its dependency graph before treating a leaderboard result as mathematical evidence. The inspection establishes a parser weakness; it does not claim a demonstrated end-to-end attack. The upstream evaluator was left unchanged, and no official score is claimed in this project.

This issue does not invalidate the local verification above: the reviewed source and all 14 named axiom reports were checked together, and the source has no injected output or extraneous untrusted code.
