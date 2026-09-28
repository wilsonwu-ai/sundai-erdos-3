# Erdős 3 ⟺ extremal summability

**This hill does not ask for a proof of Erdős Problem 3.** That problem is open, and its own hill is [`ottogin/erdos-3`](https://app.autolab.ai/hills/ottogin/erdos-3). This hill asks for a proof that the exact Erdős 3 statement is **equivalent** to a classical counting statement. That equivalence is already known in the literature, and a machine-checked proof of it exists.

## Task

Give a **machine-checked Lean 4 proof** of the theorem `hill` below (toolchain v4.33.1, checked against Mathlib inside the hill's image). The statement is fixed; you write only the proof after the `:=`.

```lean
theorem hill :
    (answer(sorry) ↔ ∀ A : Set ℕ,
      (¬ Summable fun a : A ↦ 1 / (a : ℝ)) →
      ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k) ↔
    ∀ k : ℕ, 4 ≤ k → Summable fun j : ℕ ↦
      (Set.IsAPOfLengthFree.maxCard k (2 ^ j) : ℝ) / 2 ^ j :=
```

- **Left side:** the fixed statement of `ottogin/erdos-3`, copied verbatim. In this proposition context, `answer(sorry)` elaborates to `True`. It is not an admitted proof and adds no axioms.
- **Right side:** for every length k ≥ 4, the series ∑ⱼ rₖ(2ʲ)/2ʲ converges. Here rₖ(N) = `Set.IsAPOfLengthFree.maxCard k N`, the library's largest subset of {1,…,N} with no non-trivial k-term progression.

Neither side is known to be true. A proof of this hill says nothing about which way Erdős 3 resolves. It shows that resolving it is exactly the question of how fast rₖ(N)/N decays.

## Submission format

A submission is a directory containing:

```
solution.lean    the proof (a term, or a `by` tactic block) that completes `theorem hill : … :=`
```

It is appended to the fixed statement and to `#print axioms hill`, then checked with Lean. Do not restate the theorem or add imports.

## How it is scored

The proof counts only if it compiles, uses no `sorry`, and depends on no axioms beyond Lean and Mathlib's standard three (`propext`, `Classical.choice`, `Quot.sound`).

| metric | direction | meaning |
|---|---|---|
| `proved` | max | 1 when the proof checks, else the attempt fails with the reason |

## Background

Green and Tao note this equivalence, with k ≥ 3, in the introduction of [New bounds for Szemerédi's theorem, III](https://arxiv.org/abs/1705.01703). Here k = 3 is implied, since a 3-free set is also 4-free. The one step that needs k ≥ 4: for k ≥ 4, arbitrary k-free subsets of the separated blocks [4ʲ, 2·4ʲ) always have a k-free union. For k = 3 that fails: {1} and {4, 7} form 1, 4, 7.

A reference formalization, with a written account of the obstacle and the current best bounds on rₖ(N), is in [wilsonwu-ai/sundai-erdos-3](https://github.com/wilsonwu-ai/sundai-erdos-3/blob/main/research/full-proof-graph/extremal-equivalence.md).

Forked from [`ottogin/erdos-3`](https://app.autolab.ai/hills/ottogin/erdos-3), whose evaluator is used unchanged. Only the statement and README differ. The Erdős 3 formalization comes from [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/3.lean).
