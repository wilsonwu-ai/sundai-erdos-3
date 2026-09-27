import FormalConjecturesUtil

/-!
# Elementary consequences of the exact reciprocal-divergence hypothesis

These known facts reach length two only. Infinitude and unboundedness do not
suffice for longer progressions, as the powers-of-two example demonstrates.
-/

namespace Erdos3Divergence

theorem not_summable_implies_infinite {A : Set ℕ}
    (hdiv : ¬ Summable fun a : A ↦ 1 / (a : ℝ)) : A.Infinite := by
  intro hfinite
  exact hdiv (hfinite.summable (fun n : ℕ ↦ 1 / (n : ℝ)))

theorem not_summable_implies_unbounded {A : Set ℕ}
    (hdiv : ¬ Summable fun a : A ↦ 1 / (a : ℝ)) :
    ∀ N : ℕ, ∃ n, N ≤ n ∧ n ∈ A := by
  intro N
  obtain ⟨n, hn, hN⟩ := (not_summable_implies_infinite hdiv).exists_gt N
  exact ⟨n, le_of_lt hN, hn⟩

theorem not_summable_implies_two_term_ap {A : Set ℕ}
    (hdiv : ¬ Summable fun a : A ↦ 1 / (a : ℝ)) :
    ∃ S ⊆ A, S.IsAPOfLength 2 := by
  have hInfinite := not_summable_implies_infinite hdiv
  obtain ⟨a, ha, _⟩ := hInfinite.exists_gt 0
  obtain ⟨b, hb, hab⟩ := hInfinite.exists_gt a
  exact ⟨{a, b}, Set.pair_subset ha hb, Nat.isAPOfLength_pair hab⟩

#print axioms not_summable_implies_infinite
#print axioms not_summable_implies_unbounded
#print axioms not_summable_implies_two_term_ap

end Erdos3Divergence
