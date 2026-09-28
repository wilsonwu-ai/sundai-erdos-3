import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Combinatorics.Additive.AP.Three.Defs

open Finset Real

/-- APAP's `int` statement (APAP/Integer.lean, rev 3b79412), copied verbatim as a
proposition, is false: take N = 2 and A = {0, 1} = range 2. -/
theorem apap_int_statement_false :
    ¬ (∀ {A : Finset ℕ} {N : ℕ} (_hAN : A ⊆ range N) (_hA : ThreeAPFree (α := ℕ) A),
      ∃ c > 0, #A ≤ N / exp (c * log N ^ (12⁻¹ : ℝ))) := by
  intro h
  have hfree : ThreeAPFree (α := ℕ) ((range 2 : Finset ℕ) : Set ℕ) := by
    intro a ha b hb c hc habc
    simp only [coe_range, Set.mem_Iio] at ha hb hc
    omega
  obtain ⟨c, hc, hle⟩ := h (A := range 2) (N := 2) subset_rfl hfree
  have hlog : 0 < log (2 : ℝ) := log_pos (by norm_num)
  have hpow : 0 < log (2 : ℝ) ^ (12⁻¹ : ℝ) := rpow_pos_of_pos hlog _
  have hexp : 1 < exp (c * log (2 : ℝ) ^ (12⁻¹ : ℝ)) := one_lt_exp_iff.mpr (mul_pos hc hpow)
  simp only [card_range, Nat.cast_ofNat] at hle
  rw [le_div_iff₀ (exp_pos _)] at hle
  nlinarith

#print axioms apap_int_statement_false
