# Independent adversarial review — full-proof graph

Review date: 27 September 2026. Read-only review of the proof modules and prior attempt, with this report as the sole owned output. New arguments below are ordinary mathematics, **not additional Lean-checked declarations**.

## Dependency audit

The current 30 supporting declarations do not close the fixed hill. The checked graph has these branches:

- Reciprocal divergence implies infinitude, unboundedness, and a two-term progression.
- Elementary positive-step progressions transfer to the exact Mathlib set predicate. Every length implies the exact frequent-at-top conclusion. Cofinite and affine-tail hypotheses discharge that conclusion for those special families.
- Finite logarithm blocks admit a reciprocal-mass upper bound. Summable normalized block counts imply reciprocal summability; a power envelope with exponent greater than one suffices for summable counts.
- `APFreeSummability` implies the hill; `APFreePowerEnvelope` implies `APFreeSummability` through the preceding analytic transfer.

The last two named propositions are explicit, unproved hypotheses. Neither the 30-declaration count nor an allowed-axiom audit removes theorem parameters. No declaration establishes a progression-free counting estimate. There is no completed unconditional proof path from the hill's reciprocal-divergence premise to its arbitrary-length conclusion.

The bridge is forward-only: `ContainsAP` implies existence of a subset satisfying `Set.IsAPOfLength`. It must not be reported as a checked equivalence of progression definitions.

## Weakest missing obligation for the present route

It suffices to prove, separately for every fixed k≥3 and every k-progression-free set A,

    Summable (fun a : A => 1 / (a : ℝ)).

For the existing dyadic transfer, the corresponding sufficient input is simply

    Summable (fun j => ((logBlock A j).ncard : ℝ) / (2 : ℝ)^j).

This input may be proved directly for each A. No common constant, decay exponent, uniform rate over A, or supremum over extremizers is required. The existing `APFreePowerEnvelope` is a stronger sufficient target, not a necessary hypothesis established by the current proof.

In ordinary mathematics the two pointwise summability conditions are equivalent: writing m_j for block reciprocal mass and c_j=|B_j|/2^j, the checked direction uses m_j≤c_j. For j≥1 the reverse bound c_j≤2m_j follows from a<2^(j+1). The zero block contributes only a finite exception; for example c_j≤2m_j+1_{j=0} covers zero's zero reciprocal. The repository does **not** currently contain this reverse-transfer theorem, so equivalence must not be labeled Lean-checked.

Similarly, the relationship between the full arbitrary-length statement and all fixed-k contrapositive statements uses the ordinary fact that a sufficiently long progression has a k-term prefix. The local elementary prefix lemma and forward bridge do not alone constitute a formal reverse equivalence for arbitrary Mathlib progression witnesses.

Taking a maximum over a different progression-free set at every scale is an additional step. Pointwise summability alone does not justify exchanging that maximum with an infinite sum. Candidate check 2 below supplies the required ordinary-mathematical construction for k≥4; it is not yet a Lean-checked equivalence. It does not supply a power-law envelope.

## Candidate check 1: a fixed difference carrying divergent mass

**Rejected.** The proposed implication that divergent reciprocal mass forces some fixed positive difference d with divergent reciprocal mass of progression starts is false even for length two.

For n≥1 define

    a_n = n(1 + floor(log₂ n)),     A = {a_n : n≥1}.

The sequence is strictly increasing. On the index block 2^j≤n<2^(j+1), it equals (j+1)n. There are 2^j terms, each less than (j+1)2^(j+1), so their reciprocal sum is at least 1/[2(j+1)]. Summing these disjoint index blocks gives a divergent reciprocal series over A.

Nevertheless,

    a_(n+1) − a_n ≥ 1 + floor(log₂ n) → ∞.

Fix d≥1. For n≥2^d the successive gap exceeds d, so no pair of terms starting at such an index differs by d. Only finitely many pairs in A have difference d. Thus the set of starts of fixed-d progressions has finite reciprocal sum, for every fixed d and every length at least two.

This example is compatible with Erdős 3: each index block supplies a progression of length 2^j and difference j+1. The difference may vary with the desired length. An argument that freezes the difference has imposed a false extra conclusion.

## Candidate check 2: independent factor-four blocks

**Accepted for k≥4.** Candidate supplied by the parallel mathematical research worker: choose any internally k-progression-free sets B_j⊆[4^j,2·4^j), and form their union. That union is k-progression-free.

For a purported crossing progression x_0<⋯<x_(k−1), take its largest occupied block [N,2N). Every older-block member is strictly below N/2. Let r be the number of progression terms in older blocks.

- If r≥2, two consecutive older terms show d<N/2. The first new term is the last older term plus d, hence is strictly below N: contradiction.
- If r=1, x_0<N/2 and x_1≥N. Since k≥4, x_3 exists and x_3=3x_1−2x_0>2N: contradiction.
- If r=0, the whole progression belongs to the largest block, contradicting its internal k-freeness.

The strict endpoints are correct for the half-open intervals. The same argument works for every k>4. It fails for k=3, concretely: {1}⊂[1,2) and {4,7}⊂[4,8) are internally three-progression-free but their union contains 1,4,7.

Consequently, for fixed k≥4, one may select an extremizer with r_k(4^j) elements in each translated length-4^j interval. The union is k-free and its j-th block reciprocal mass is at least r_k(4^j)/(2·4^j). Thus reciprocal summability of **every** k-free set forces summability of these normalized extremal counts. This is a real construction, not an interchange of supremum and summation.

To compare dyadic and factor-four series, splitting a length-2N interval into two length-N intervals gives r_k(2N)≤2r_k(N), hence the odd dyadic normalized term is at most the preceding even term. Therefore the two nonnegative series have the same summability behavior. These observations support an equivalence of the missing obligations for k≥4, but establish neither one's truth.

The accepted construction also undercuts an assumed universal extra restriction that prevents independently chosen, progression-free blocks from coexisting at separated scales. Any purported cross-scale mass recurrence must hold for these arbitrary choices. No specific nontrivial recurrence has been supplied or proved in this review.

## Current verdict

The conditional proofs and analytic transfer remain correctly scoped. The fixed-d shortcut is invalid. The separated-block construction is sound for k≥4 and clarifies the extremal-summability reduction, without proving its missing premise. A full proof still requires genuine new progress on the progression-free summability obligation; none is supplied by this review.

## Join review: start-set induction and digit cubes

Reviewed `length-induction.md` after it was written. Its start-mass inheritance argument is valid **conditional on H_k**: if the start set had finite reciprocal mass, its complement in a divergent A would remain divergent but contain no k-progression, contradicting H_k. The differing witnesses need not share a common step.

The finite counterexample A={1,2,3,6,9,10,15} is correct. Its four three-term progressions, listed in the report, would require respective fourth terms 4,14,12,21, all absent. Hence S₃(A)={1,2,3} but A has no four-term progression.

The stronger shifted base-five cubes also withstand the carry check. Set C₀={1} and C_m={1+Σ_(i<m)x_i5^i : x_i∈{0,1,2}}. Every member of C_(m−1) starts a three-term progression in C_m with positive step 5^(m−1). Monotonicity of S₃ and induction give 1∈S₃^m(C_m).

For a hypothetical four-term progression in C_m, subtracting each consecutive midpoint identity cancels the shift by one. Each resulting coefficient of 5^i lies in [-4,4]. Reduction modulo five forces the lowest coefficient to be zero, since zero is the only multiple of five in that interval. Division by five repeats this argument through all digits; no carry is hidden. Both midpoint identities therefore hold digitwise. A four-term integer progression inside {0,1,2} must have step zero, so every digit is constant and the four original numbers coincide, contradicting positive common difference. Thus C_m is four-progression-free for every finite m.

These finite examples disprove the qualitative extension and arbitrarily deep finite start-set iteration as sufficient structural criteria. They do not disprove any divergence-sensitive statement. Under H₃, the proposed extension with reciprocal divergence reattached is equivalent to H₄, rather than an independently established inductive step. All arguments in this section remain ordinary mathematics, not new Lean verification.

Editorial scope note: no argument here establishes that *every possible* successful proof must control witness differences quantitatively. The demonstrated conclusion is that this particular qualitative induction needs an additional ingredient.
