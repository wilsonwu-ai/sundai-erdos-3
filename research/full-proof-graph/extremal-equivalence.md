# Lean-checked: the hill is equivalent to extremal summability

**Erdős 3 is still not proved.** This round turned the ordinary-mathematics equivalence in [cross-scale.md](cross-scale.md) into 22 kernel-checked declarations in the pinned hill image. The exact hill is now proved *equivalent* to a classical statement about the extremal function for progression-free sets. Neither side is proved. [Lean module](../../lean/Erdos3CrossScale.lean) · [axiom audit](../../artifacts/mathlib-verification.json).

## The checked statement

Write rₖ(N) for the largest size of a k-progression-free subset of {1,…,N}. The Lean statement uses the imported library's own definition, `Set.IsAPOfLengthFree.maxCard k N`, not a definition written for this project.

```lean
theorem hill_statement_iff_extremal :
    (answer(sorry) ↔ ∀ A : Set ℕ,
      (¬ Summable fun a : A ↦ 1 / (a : ℝ)) →
      ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k) ↔
    ∀ k : ℕ, 4 ≤ k → Summable fun j : ℕ ↦
      (Set.IsAPOfLengthFree.maxCard k (2 ^ j) : ℝ) / 2 ^ j
```

The left side is the frozen hill proposition, copied verbatim, including `answer(sorry)`. Lean accepts `hill_iff_extremal` as its proof, so the two statements agree definitionally. Every declaration's axioms are within `{propext, Classical.choice, Quot.sound}`.

In words: a passing AutoLab proof exists **if and only if** the series ∑ⱼ rₖ(2ʲ)/2ʲ converges for every k ≥ 4. The case k = 3 is implied, because a 3-free set is also 4-free.

Green and Tao state the same equivalence (with k ≥ 3) in the introduction of their r₄ paper: *"the famous conjecture of Erdős asserting that every set of natural numbers whose sum of reciprocals is divergent is equivalent to the claim that ∑ rₖ(2ⁿ)/2ⁿ < ∞ for all k ⩾ 3"* ([arXiv:1705.01703](https://arxiv.org/abs/1705.01703)). No novelty is claimed for the mathematics. What this round adds is a kernel check against the exact hill statement, environment and axiom policy.

## What the 22 declarations prove

| Group | Declarations | Content |
| --- | --- | --- |
| Progression algebra | `free_mono`, `free_image_add`, `free_preimage_add`, `free_mono_length` | Progression-freeness passes to subsets, both shifts, and longer lengths |
| Separated blocks | `sepBlock_union_free` and three `a_` helpers | For k ≥ 4, arbitrary k-free subsets of the blocks [4ʲ, 2·4ʲ) have a k-free union |
| Extremal function | `r_attained`, `card_le_r`, `r_two_mul_le` | `maxCard` is attained, bounds every free subset, and satisfies r(2n) ≤ 2r(n) |
| Upper transfer | `logBlock_ncard_le_r`, `freeSummable_of_dyadic`, `dyadic_of_quart` | If ∑ rₖ(2ʲ)/2ʲ converges, every k-free set has summable reciprocals |
| Lower construction | `quart_of_freeSummable` and three `e_` helpers | Translated extremizers placed in separated blocks force ∑ rₖ(4ʲ)/4ʲ < ∞ |
| Equivalences | `freeSummable_iff_quart`, `freeSummable_iff_dyadic`, `hill_iff_extremal`, `hill_statement_iff_extremal` | The fixed-k and full-hill equivalences |

The lower construction is the step that needs k ≥ 4. For k = 3, {1} ⊂ [1,2) and {4,7} ⊂ [4,8) are each 3-free, but their union contains 1, 4, 7.

## The exact remaining obstacle

For a fixed k, the series term is rₖ(2ʲ)/2ʲ. A bound rₖ(N) ≪ N/(log N)ᶜ makes the j-th term ≪ j⁻ᶜ, which is summable exactly when c > 1. So length k needs an upper bound that beats N/log N by a logarithmic power greater than one. Erdős conjectured rₖ(N) ≪_C N/(log N)^C for every C > 0; [erdosproblems.com/3](https://www.erdosproblems.com/3) records this as known only for k = 3.

| Length | Best published upper bound (checked 27 Sep 2026) | Known to make the series converge? |
| --- | --- | --- |
| k = 3 | N·exp(−c(log N)^(1/9)) ([Bloom–Sisask 2023](https://arxiv.org/abs/2309.02353), improving [Kelley–Meka 2023](https://arxiv.org/abs/2302.05537)). The k = 3 case of Erdős 3 was first proved with N/(log N)^(1+c) ([Bloom–Sisask 2020](https://arxiv.org/abs/2007.03528)). | **Yes.** The hill still needs every k. |
| k = 4 | N(log N)^(−c) for an unspecified absolute c > 0 ([Green–Tao 2017](https://arxiv.org/abs/1705.01703)), which the authors say "appears to be the limit of our methods". | **No.** It would need c > 1; erdosproblems.com calls c "some small constant". |
| k ≥ 5 | N·exp(−(log log N)^(cₖ)) for some cₖ > 0 ([Leng–Sah–Sawhney 2024](https://arxiv.org/abs/2402.17995)) | **No.** No source reports convergence. |

A read-only search covered erdosproblems.com/3, its forum thread, ProofAtlas, and targeted arXiv and web searches through 27 September 2026. It found no result proving convergence for any k ≥ 4, and no claimed resolution of Erdős 3. The problem is listed as open with a $5,000 prize. An independent skeptic re-fetched every source and confirmed all 13 claims. One claim needed a wording fix: an editorial paraphrase of the erdosproblems.com page had been presented as a verbatim quote. [Claims, quotes, verdicts and search log](../../artifacts/literature-check.json).

## How this was produced

```text
▸ GRAPH SPEC
GOAL:     Kernel-check the cross-scale equivalence in the exact hill image.
FAN OUT:  6 Lean lanes over 15 frozen statements (algebra, separated blocks,
          extremal function, upper transfer, lower construction, equivalences).
          Each lane proved its own lemmas against sorry stubs of the others.
ANCHOR:   The Lean 4.33.1 kernel in the pinned image; a verbatim copy of the hill.
VERIFY:   Deterministic lane checker: compile, no sorry in owned blocks, owned
          statements identical to the skeleton, other regions untouched,
          forbidden-token scan. Skeleton and checker read-only and hash-verified
          before merge.
REDUCE:   Mechanical block merge, then scripts/check_mathlib.py on all modules.
HUMAN GATE: No AutoLab submission is reachable from any node; research agents
          had no shell or network write access.
FROZEN:   The hill statement, the pinned image, the axiom whitelist, all 15 statements.
```

All six lanes passed the checker on their first attempt. The merged module compiled on its first build, and `check-lean` audited 52 declarations in total: the earlier 30 plus these 22.

## What this means for a submission

`solution.lean` is appended to the fixed statement and can import only that statement's context, not this repository's modules. A future proof of the right-hand side would therefore still need these declarations inlined into one proof body. That step is mechanical because every piece is already checked. Until the extremal series is shown to converge for every k ≥ 4, no submission can pass, and the current attempt is still rejected as expected.

That inlining has now been done for the equivalence itself. [`submissions/equivalence/solution.lean`](../../submissions/equivalence/solution.lean) is a single 579-line proof body, regenerated byte-for-byte by [`scripts/inline_solution.py`](../../scripts/inline_solution.py) from the checked modules. It proves the equivalence as the fixed statement of a separate public hill, [`wilsonwu-ai/erdos-3-extremal-equivalence`](https://app.autolab.ai/hills/wilsonwu-ai/erdos-3-extremal-equivalence). That hill was forked from `ottogin/erdos-3`, with its evaluator, tests, baseline and lock files byte-identical. Only the statement, README and name differ.

- **Local evaluation:** the unchanged evaluator, run in the pinned image against the committed tree `615c66dd`, returned `passed: true` and `proved = 1`. The axioms were `propext`, `Classical.choice` and `Quot.sound`, and the report signature verified. The `by sorry` baseline was rejected as a negative control.
- **Submission:** the signed report was submitted to that hill's leaderboard and ranks #1.
- **Scope:** this is a leaderboard entry for the equivalence theorem, not for Erdős 3. [Publication record and file hashes](../../artifacts/equivalence-hill-publication.json).
