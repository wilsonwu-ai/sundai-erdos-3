# What this Lean file proves

`Erdos3SpecialCases.lean` proves fourteen elementary results related to Erdős Problem 3. The full reciprocal-divergence conjecture remains open.

The predicate `ContainsAP A k` describes k terms `a + i*d` inside A, with a positive step d. Positivity guarantees distinct terms, which is checked separately. We use this dependency-free predicate to make the scope easy to inspect; a bridge to the hill's Mathlib predicate is not yet formalized.

The central verified cases are:

- A set containing every sufficiently large natural number contains progressions of every length.
- A set containing a tail of one infinite nonconstant progression contains progressions of every length.
- Multiples of any positive natural number contain progressions of every length.
- An unbounded natural-number set contains a two-term nonconstant progression.
- Powers of two are unbounded but contain no three-term nonconstant progression. Thus unboundedness alone cannot solve the conjecture.

The remaining theorems check strict increase, prefixes, supersets, the equivalence of unbounded and arbitrary lengths, and arithmetic facts used by the counterexample. These results are elementary known facts; no novelty claim is made.

Run with the pinned Lean 4.33.1 toolchain:

```sh
cd lean
lean Erdos3SpecialCases.lean
```

The file imports `Std` only and prints the axiom dependencies of every theorem. All dependencies are among `propext`, `Classical.choice`, and `Quot.sound`; some theorems use none. No proof uses `sorry` or `native_decide`.

This file is not an AutoLab `solution.lean`: AutoLab expects only a proof body for its fixed, much stronger theorem. Passing these checks does not mean the hill is solved.
