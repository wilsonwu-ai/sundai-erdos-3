# Erdős Problem 3: statement, status, and honest targets

Checked 27 September 2026. The target is **Problem 3**, not Problem 13 from the pasted example. The full problem remains **open** in the community database and DeepMind's formal-conjectures repository. This project must not describe an elementary special case or a finite search as a solution to the open conjecture.

## Exact mathematical target

For every set of natural numbers A whose reciprocal series diverges, must A contain arithmetic progressions of every finite length? A nontrivial progression has the form a, a+d, …, a+(k−1)d with d>0. The formal statement asks for unboundedly many possible lengths, which is equivalent to every finite length by taking prefixes.

The [DeepMind source](https://github.com/google-deepmind/formal-conjectures/blob/a24e30f9c7767245a5030e210f40c28487dae5c5/FormalConjectures/ErdosProblems/3.lean) expresses this as:

```lean
theorem erdos_3 : answer(sorry) ↔ ∀ A : Set ℕ,
    (¬ Summable fun a : A ↦ 1 / (a : ℝ)) →
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k := by
  sorry
```

This is an upstream **unproved statement**, archived in [math/formal-conjectures-3.lean](math/formal-conjectures-3.lean); neither its `sorry` nor its `answer(sorry)` is a proof. Natural numbers include 0 and Lean defines division by zero as 0, so including 0 contributes no reciprocal mass.

The exact AutoLab hill has now been recovered locally. Its `statement.lean` matches the main conjecture above, naming it `hill`; its evaluator declares Lean 4.33.1. The original Problem 13 screenshot was not used to establish this.

## Verified research status

The [community database at commit c011744](https://github.com/teorth/erdosproblems/blob/c011744b4fa23ab83e066193c0d738e347bd8f8c/data/problems.yaml) records #3 as open with a $5,000 prize, a formalized statement, and no formalized solution. The relevant record is archived in [math/status-3.yaml](math/status-3.yaml). This is evidence of the catalog's status, not a guarantee that no unindexed claim exists.

Bloom and Sisask proved the three-term case in 2020. Their quantitative theorem bounds any three-term-progression-free subset of {1,…,N} by C·N/(log N)^(1+c), for c>0. [Primary paper](https://arxiv.org/abs/2007.03528).

Kelley and Meka subsequently obtained a stronger three-term bound N·exp(−c(log N)^β), for positive constants c and β. This still concerns length three. [Primary paper](https://arxiv.org/abs/2302.05537).

For k≥5, Leng, Sah, and Sawhney give bounds N·exp(−(log log N)^cₖ). The displayed bound does not by itself establish the reciprocal-divergence conjecture for all lengths. [Primary paper](https://arxiv.org/abs/2402.17995).

The DeepMind file gained known-result variants on 27 September 2026, but every variant still contains `by sorry`. Its `research solved` label describes the mathematical literature, not a completed Lean proof. The [APAP formalization project](https://github.com/YaelDillies/apap) is a potential source of reusable machinery; its README describes the integer theorem as a future goal, so completion must be audited before reuse.

## Three useful local theorem targets

1. **Cofinite case:** if all n≥N belong to A, then A contains a k-term progression for every k. Witness a=N and d=1. This verifies a substantial family of inputs and the progression interface, but the assumption is much stronger than reciprocal divergence.
2. **Unbounded-set, two-term case:** an unbounded A contains two distinct elements, hence a nonconstant progression of length two. The new `Erdos3Divergence.lean` proves the preceding implication from the exact reciprocal non-summability hypothesis using the image's imported summability library.
3. **Affine-tail family:** if A contains a+(N+i)d for all i≥0 and d>0, then A contains progressions of every finite length. This includes multiples and residue classes and demonstrates reusable proof composition.

These are known special cases, not novel mathematical results. All three are now implemented and checked in [Erdos3SpecialCases.lean](../lean/Erdos3SpecialCases.lean). The file also checks progression-prefix and superset lemmas, equivalence of unbounded lengths with all lengths, and an explicit obstruction to an invalid shortcut: powers of two are unbounded but contain no nonconstant three-term progression.

At the first bridge checkpoint, the original fourteen proofs and nine additional declarations compiled with Lean **4.33.1** inside the pinned image. All printed axiom dependencies are subsets of `propext`, `Classical.choice`, and `Quot.sound`. `Erdos3Bridge.lean` supplies a forward conversion from the elementary `ContainsAP` predicate to the exact `Set.IsAPOfLength` and filter conclusion; a full equivalence is not asserted. `Erdos3Divergence.lean` connects reciprocal divergence with infinitude, unboundedness, and a two-term progression. `Erdos3Reduction.lean` proves a conditional route with an explicit unproved assumption. None proves the unrestricted conjecture. [Source and scope](../lean/README.md) · [Executed audits](../artifacts/mathlib-verification.json).

## Audit of the answer placeholder

It would be incorrect to conclude from the literal text `answer(sorry)` alone that this hill necessarily uses an untrusted axiom. In the [current upstream answer elaborator](https://github.com/google-deepmind/formal-conjectures/blob/c252a41054125b5fd9c8356e2137cd9b55337657/FormalConjecturesUtil/Answer.lean), default mode is `always_true`: when `answer(sorry)` is expected to be a proposition, the elaborator returns `True` directly. That makes this wrapper an affirmative conjecture, `True ↔ P`.

[AnswerDefaultRepro.lean](math/AnswerDefaultRepro.lean) reproduces this relevant branch with core Lean and compiles on 4.33.1. The later [container smoke check](../scripts/container_smoke.py) imported `FormalConjecturesUtil` from the exact pinned image and also printed `True ↔ True` with no axiom dependencies. Its actual `Answer.lean` hash matches the preserved historical source. [Executed environment evidence](../artifacts/local-evaluator-verification.json).

## A meaningful research bridge

Let Bⱼ = A∩[2ʲ,2ʲ⁺¹). Every member of Bⱼ contributes at most 2⁻ʲ to the reciprocal sum. Consequently,

    reciprocal mass in Bⱼ ≤ |Bⱼ| / 2ʲ.

If the right-hand bounds sum to a finite value, the reciprocal series converges. Thus, for a fixed k, an upper bound C·N/(log N)^(1+ε) for every k-progression-free set would imply the k-term case by contradiction and dyadic decomposition. The exponent must exceed 1 for this argument. This explains why the Bloom–Sisask bound solves k=3 and why merely positive-density results do not solve the full conjecture.

This paragraph is our elementary derivation, not a newly claimed theorem from the cited sources. The dyadic transfer is now formalized in [Erdos3Blocks.lean](../lean/Erdos3Blocks.lean) and [Erdos3Dyadic.lean](../lean/Erdos3Dyadic.lean). Supplying the required extremal bound for every k remains the unresolved mathematical obstacle.

The checked [conditional reduction](../lean/Erdos3Reduction.lean) now isolates that obstacle as `APFreeSummability`: for each `k ≥ 3`, every set avoiding a `k`-term progression has summable reciprocals. Given this assumption, the proof establishes the exact hill conclusion by choosing `k = max n 3` above each requested threshold. The assumption is an explicit theorem parameter, not an axiom or an established result.

The implemented proof partitions the subtype `A` by `Nat.log 2 a`; `summable_partition` reduces summability to the fiber sums. `Nat.lt_pow_succ_log_self` bounds each fiber and `Nat.pow_log_le_self` bounds its nonzero members' reciprocals. `Summable.of_nonneg_of_le` compares the fiber sums to the cardinality envelope. `Real.summable_one_div_nat_rpow` handles an envelope proportional to `1/(j+1)^p` for `p > 1`. All seven new declarations compile in the actual image, giving 30 checked supporting declarations overall. [Full-proof attempt, current source check, and failed routes](proof-attempt-2026-09-27.md).

The `Nat.log` bucket at zero also contains the number zero, whose reciprocal contributes zero. Handle that case explicitly. Direct Cauchy condensation on a set's reciprocal indicator is invalid in general because that indicator need not be antitone.

## Blockers and claim boundaries

- The requested full solution would settle a major open conjecture; no valid proof was found in this focused source check.
- Finite exhaustive searches cannot certify the universal claim about arbitrary infinite sets.
- Known special cases require accurate labels: “Lean-verified special cases; full Erdős #3 remains open.”
- The full hill's pinned image now runs locally. Its positive import check passed and its original admitted baseline was rejected; neither check solves the mathematical target.
- A successful fixed-hill submission requires the exact fixed statement, compilation without `sorry`, and the allowed-axiom audit; all three must be checked independently.

Seven primary source files or projects were used for the substantive report: the DeepMind conjecture, the community database, Bloom–Sisask, Kelley–Meka, Leng–Sah–Sawhney, APAP, and the answer elaborator. The canonical erdosproblems.com/3 page was inaccessible through the browser tool, so the live community repository supplies the recorded status.
