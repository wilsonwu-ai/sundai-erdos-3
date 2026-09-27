by
  constructor
  · intro _ A hdiv
    -- Reduce the exact unbounded-length goal to a fixed progression length.
    apply Filter.frequently_atTop.2
    intro n
    refine ⟨max n 3, le_max_left n 3, ?_⟩
    by_contra hNo
    apply hdiv
    have hfree : A.IsAPOfLengthFree (max n 3) := by
      intro S hSA hAP
      exact False.elim (hNo ⟨S, hSA, hAP⟩)
    -- The logical reduction is checked separately in Erdos3Reduction.lean.
    -- This remaining assertion is the research obstacle, not an axiom.
    fail "Unproved: show the reciprocal series is summable for this progression-free set."
  · intro _
    trivial
