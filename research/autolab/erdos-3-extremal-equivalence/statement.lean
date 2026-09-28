import FormalConjecturesUtil

/-!
# Erdős Problem 3 is equivalent to extremal summability

This hill does NOT ask for a proof of Erdős Problem 3, which is open. It asks
for a proof that the exact Erdős 3 statement of `ottogin/erdos-3` (copied
verbatim, including `answer(sorry)`, which elaborates to `True`) is equivalent
to convergence of the dyadic extremal series for every progression length at
least four. `Set.IsAPOfLengthFree.maxCard k N` is the largest size of a subset
of `{1, …, N}` with no non-trivial `k`-term arithmetic progression.
-/

namespace Erdos3Equivalence

/-- Erdős 3 holds if and only if `∑ⱼ maxCard k (2^j) / 2^j` converges for every `k ≥ 4`. -/
theorem hill :
    (answer(sorry) ↔ ∀ A : Set ℕ,
      (¬ Summable fun a : A ↦ 1 / (a : ℝ)) →
      ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k) ↔
    ∀ k : ℕ, 4 ≤ k → Summable fun j : ℕ ↦
      (Set.IsAPOfLengthFree.maxCard k (2 ^ j) : ℝ) / 2 ^ j :=
