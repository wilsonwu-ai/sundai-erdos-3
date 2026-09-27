import FormalConjecturesUtil
import Erdos3SpecialCases

/-!
Connect the elementary positive-step definition to the exact set/cardinality
and filter predicates used by the frozen Erdős 3 hill. These are bridges and
special cases; they do not prove the reciprocal-divergence conjecture.
-/

namespace Erdos3Bridge

/-- Every elementary finite progression gives a set of exactly that cardinality.
The `Fin k` range construction also handles the empty progression when `k = 0`. -/
theorem containsAP_to_setAP {A : Set ℕ} {k : ℕ}
    (h : Erdos3SpecialCases.ContainsAP (fun n => n ∈ A) k) :
    ∃ S ⊆ A, S.IsAPOfLength k := by
  classical
  obtain ⟨a, d, hd, hterms⟩ := h
  let f : Fin k → ℕ := fun i => a + i.val * d
  have hmono : StrictMono f := by
    intro i j hij
    exact Erdos3SpecialCases.ap_terms_strictly_increase a d i.val j.val hd hij
  have hf : Function.Injective f := hmono.injective
  let : Fintype (Set.range f) := Fintype.ofFinite _
  refine ⟨Set.range f, ?_, a, d, ?_⟩
  · rintro x ⟨i, rfl⟩
    exact hterms i.val i.isLt
  · constructor
    · simp only [ENat.card_eq_coe_fintype_card, Set.card_range_of_injective hf,
        Fintype.card_fin]
    · ext x
      constructor
      · rintro ⟨i, rfl⟩
        refine ⟨i.val, ?_, ?_⟩
        · exact_mod_cast i.isLt
        · simp [f]
      · rintro ⟨n, hn, rfl⟩
        have hn' : n < k := by exact_mod_cast hn
        refine ⟨⟨n, hn'⟩, ?_⟩
        simp [f]

/-- Every finite length implies the exact frequent-at-top conclusion of the hill. -/
theorem all_lengths_to_frequently {A : Set ℕ}
    (h : ∀ k : ℕ, ∃ S ⊆ A, S.IsAPOfLength k) :
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k := by
  apply Filter.frequently_atTop.mpr
  intro n
  exact ⟨n, le_rfl, h n⟩

/-- Transfer elementary arbitrarily long progressions into the frozen hill's conclusion. -/
theorem elementary_all_lengths_to_frequently {A : Set ℕ}
    (h : Erdos3SpecialCases.ArbitrarilyLongAPs (fun n => n ∈ A)) :
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k := by
  apply all_lengths_to_frequently
  intro k
  exact containsAP_to_setAP (h k)

/-- A set containing every natural above a threshold satisfies the exact conclusion. -/
theorem cofinite_hill_conclusion {A : Set ℕ} (N : ℕ)
    (hA : ∀ n, N ≤ n → n ∈ A) :
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k := by
  exact elementary_all_lengths_to_frequently
    (Erdos3SpecialCases.cofinite_contains_all_lengths N hA)

/-- Containing a tail of any infinite positive-step progression is also sufficient. -/
theorem affine_tail_hill_conclusion {A : Set ℕ} (a d N : ℕ)
    (hd : 0 < d) (hA : ∀ n, N ≤ n → a + n * d ∈ A) :
    ∃ᶠ (k : ℕ) in Filter.atTop, ∃ S ⊆ A, S.IsAPOfLength k := by
  exact elementary_all_lengths_to_frequently
    (Erdos3SpecialCases.affine_tail_contains_all_lengths a d N hd hA)

#print axioms containsAP_to_setAP
#print axioms all_lengths_to_frequently
#print axioms elementary_all_lengths_to_frequently
#print axioms cofinite_hill_conclusion
#print axioms affine_tail_hill_conclusion

end Erdos3Bridge
