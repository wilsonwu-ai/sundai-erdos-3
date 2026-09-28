# Roadmap: how we would attack Erdős 3

**Erdős 3 is open, and nobody currently knows how to prove it.** This page records the plan chosen on 27 September 2026. It does not set out to "find the proof". It attacks the one bound that every proof must contain, in the order specialists would, with Lean refereeing every step. Its goals pay off even if the final one is never reached.

## What any proof must contain

[`hill_statement_iff_extremal`](../lean/Erdos3CrossScale.lean) is Lean-checked in both directions. So **any** proof of Erdős 3 must show, for every k ≥ 4, that

$$\sum_{j\ge0}\frac{r_k(2^j)}{2^j}<\infty,$$

where rₖ(N) is the largest subset of {1,…,N} with no k-term progression. No structural shortcut avoids this. A bound rₖ(N) ≪ N/(log N)^(1+c) is enough. That means breaking the *logarithmic barrier*, which for k = 3 took from Roth's 1953 theorem until [Bloom–Sisask 2020](https://arxiv.org/abs/2007.03528). [Details and current bounds](full-proof-graph/extremal-equivalence.md).

## Why current methods stop

The mechanism descriptions below are our reading of the cited papers, not quotations. The bounds themselves are verified in [literature-check.json](../artifacts/literature-check.json).

- **The standard tool is a density-increment loop.** If A has few k-term progressions, it is denser on some structured subset (a Bohr set, or a level set of a nilsequence), so you restrict to that subset and repeat. Each round, the subset shrinks and the density rises only additively, by about δ^C. The number of rounds times the loss per round caps the final bound.
- **k = 3 was broken open.** [Kelley–Meka 2023](https://arxiv.org/abs/2302.05537) obtain a *multiplicative* density increment, using physical-space arguments (sifting plus almost-periodicity) instead of large Fourier coefficients. That needs only about log(1/δ) rounds, which gives a quasi-polynomial bound. [Bloom–Sisask](https://arxiv.org/abs/2309.02353) sharpen the exponent to 1/9.
- **k = 4 is stuck.** [Green–Tao 2017](https://arxiv.org/abs/1705.01703) run the loop with quadratic Fourier analysis and reach N(log N)⁻ᶜ for an unspecified small c. They describe this as "the limit of our methods".
- **k ≥ 5 is further behind.** [Leng–Sah–Sawhney 2024](https://arxiv.org/abs/2402.17995) combine quasi-polynomial inverse theorems for Gowers norms with the density increment, and reach N·exp(−(log log N)^(cₖ)).

**The hinge, as we read it:** a Kelley–Meka-style *multiplicative* density increment for four-term progressions, meaning a higher-order analogue of their sifting argument. Everything after that is follow-through, though k ≥ 5 would need the same idea at every degree.

## How to run the attack

1. **Finite fields first (F₅ⁿ).** This is the standard testing ground: subspaces replace Bohr sets, and small cases can be computed. We still need to verify whether four-term progressions in F₅ⁿ are also stuck near the logarithmic barrier. The polynomial method that settled cap sets does not reach four-term progressions.
2. **Pass every candidate lemma through the loop this repository already uses:**
   - write a precise statement;
   - try to falsify it computationally on small groups;
   - write a proof;
   - have an independent skeptic attack it;
   - only then formalize it in Lean.

   The graph fans out over *lemmas*, not over the theorem.
3. **Climb in order:**
   - make the constant c in Green–Tao's k = 4 bound explicit;
   - get a multiplicative increment in F₅ⁿ;
   - beat the logarithmic barrier in F₅ⁿ;
   - only then work over the integers.

## What AI can and cannot do here

- **Can:** synthesize the literature, falsify candidate inequalities quickly by computation, formalize known results, and keep the bookkeeping honest.
- **Cannot:** we have no evidence that an agent fleet can supply the missing idea. A fleet aimed at this problem will produce convincing-looking wrong proofs. Lean is what keeps them out of this repository, and every claim here passes through it.

## Goals that pay off along the way

| Goal | What it is | Scope |
| --- | --- | --- |
| **A** | A Lean proof of the k = 3 case, in Formal Conjectures' exact statement `erdos_3.variants.three` | The mathematics is known. This is formalization and bridging work. **Started; status below.** |
| **B** | Better bounds for four-term progressions in F_pⁿ | A research long shot, and a real result on its own |
| **C** | k = 4 over the integers, then every k | The moonshot. Even k = 4 alone does not settle the hill, which needs every k |

## Goal A status (27 September 2026)

Goal A splits into two parts. The first is done; the second is the real work.

**A1: bound ⇒ the three-term case. Done and Lean-checked.** [`Erdos3ThreeCase.lean`](../lean/Erdos3ThreeCase.lean) contains five declarations. `check-lean` then audited 57 in total, all using only `propext`, `Classical.choice` and `Quot.sound`.

- `three_of_kelleyMeka` proves that Formal Conjectures' `erdos_3.variants.kelley_meka` implies `erdos_3.variants.three`. Both statements, and the `r` abbreviation, are copied verbatim from upstream; a whitespace-normalized text comparison confirmed the match.
- `three_of_logBarrier` shows that the weaker Bloom–Sisask (2020) form, rₖ(N) ≪ N/(log N)^(1+c), already suffices.
- The route reuses `freeSummable_of_dyadic`, which holds for every k, including 3.

**A2: the Kelley–Meka bound itself. Not formalized anywhere we could find.** A read-only audit of [APAP](https://github.com/YaelDillies/APAP) at commit `3b79412` found the following. An independent skeptic re-opened every cited line and confirmed all 12 key claims.

- **Finite-field case: complete.** Theorem `ff` has no `sorry`, and the blueprint marks it proved.
- **Integer case: not started beyond its statement.** `int` in `APAP/Integer.lean` is a bare `sorry` that imports nothing from the rest of the project. Bohr-set regularity (`BohrSet.regularity`) is also `sorry`, and the blueprint's integer chapter reads "To do." throughout.
- **The `int` statement, as written, is false.** Its `∃ c > 0` comes after `A` and `N`, and at N = 2 with A = {0, 1} no c works. [A Lean proof of the negation](apap/IntStatementCounterexample.lean) compiles in the pinned image with standard axioms. The intended theorem presumably fixes c before A and N and handles small N, for example with a constant factor or a threshold N ≥ N₀. This does not affect APAP's finite-field result.
- **Toolchain gap.** APAP runs Lean 4.35.0-rc2 with a newer Mathlib; Formal Conjectures and the hill image run Lean 4.33.1.

**The definition bridge also has to be built.** Formal Conjectures measures r₃ with `Set.IsAPOfLengthFree.maxCard 3 N`, over subsets of {1,…,N}. Mathlib and APAP use `ThreeAPFree` and `rothNumberNat`. No lemma connects them in either copy of `FormalConjecturesForMathlib`. The audit estimates three pieces:

- `IsAPOfLengthFree 3 ↔ ThreeAPFree` (medium);
- an `sSup` characterization of `addRothNumber` (low to medium);
- `maxCard 3 N = rothNumberNat N`, via `addRothNumber_Ico` (low once the other two exist).

**Upstream path.** Formal Conjectures does not merge proofs longer than about 25–50 lines. It links to externally hosted proofs with an attribute. Its attribute source documents a conditional form for exactly this case:

```lean
@[category research solved, AMS 11,
  conditional formal_proof using lean4 at "<link to Erdos3ThreeCase.lean>"
    assuming erdos_3.variants.kelley_meka]
theorem erdos_3.variants.three : ...
```

A1 qualifies for that tag now. When A2 lands, it becomes an unconditional `formal_proof` link. Submitting requires Google's CLA and a PR from your GitHub account, so it has not been done.

### Progress since (27 September 2026, later)

**The definition bridge is done and Lean-checked.** [`Erdos3RothBridge.lean`](../lean/Erdos3RothBridge.lean) adds seven declarations, so `check-lean` now audits 64 across nine modules:

- `isAPOfLengthFree_three_iff`: Formal Conjectures' `IsAPOfLengthFree 3` is Mathlib's `ThreeAPFree`.
- `maxCard_three_eq_rothNumberNat`: `maxCard 3 N = rothNumberNat N`.
- `kelleyMeka_iff_rothNumberNat`: the `kelley_meka` variant, restated in Mathlib's terms.
- `three_of_uniform_finset_bound`: a bound of the shape a *corrected* APAP `int` theorem would have implies `erdos_3.variants.three`.

So once an integer Kelley–Meka theorem exists in Mathlib's vocabulary, only `Erdos3ThreeCase` and this bridge stand between it and the Formal Conjectures statement. Both are already checked. The image's Mathlib is the same revision as current upstream Formal Conjectures (`0df444a`), and all nine packages match.

**The integer case is mapped.** [integer-case-map.json](../artifacts/integer-case-map.json) maps the argument of Bloom–Sisask's exposition (arXiv:2302.07211v3) onto APAP, in 18 steps. The skeptic confirmed all 12 claims it checked.

- **Effort: major.** The map rates 1 step major, 3 substantial, 10 moderate and 4 routine. Nine steps have a finite-field analogue already proved in APAP. Eight are Bohr-set work with no finite-field counterpart.
- **Critical path:**
  1. Bohr-set API and a fix to the regularity definition;
  2. the size bound |B_ρ| ≥ (ρ/4)^d |B|;
  3. Bohr-set regularity, currently `sorry` in APAP;
  4. **almost-periodicity relative to Bohr sets** (paper Theorem 17), the one major step. Neither source proves it: the paper defers to Schoen–Sisask [Theorem 5.4];
  5. the density-increment iteration over regular Bohr sets;
  6. the structural theorem;
  7. the three-term count in ℤ/(2N+1)ℤ;
  8. the final bound.
- **What transfers:** APAP's general-group layer (unbalancing, dependent random choice and sifting, almost-periodicity in L^∞, Chang's lemma, weighted L^p norms) carries over as stated.
- **What does not:** the finite-field proof's key simplification. It makes each subspace the new ambient group, and Bohr sets are not groups.
- **A second APAP statement looks wrong.** `BohrSet.IsRegular` (`APAP/Prereqs/Bohr/Regular.lean:16`) bounds κ by `B.rank / 100`, whereas the paper's Definition 24 and APAP's own blueprint (`bohr.tex:49`) use 1/(100·rank). The skeptic confirmed the mismatch verbatim. The mapper's further reading, not yet checked in Lean, is that the regularity lemma then becomes too strong to hold for high-rank Bohr sets.
- **A corrected `int` statement**, matching `three_of_uniform_finset_bound`:
  `∃ C > 0, ∃ c > 0, ∀ N, ∀ A ⊆ range N, ThreeAPFree A → #A ≤ C · N / exp(c · (log N)^(1/12))`.

**Upstream contributions: prepared, not posted.** Formal Conjectures follows [Mathlib's AI conventions](https://leanprover-community.github.io/contribute/index.html). They require disclosing AI use and state that "Using an LLM when writing comments on GitHub or Zulip is not allowed: use your own words." So issue and PR text must be written by the author, not generated. The code is ready:

- **Formal Conjectures:** branch [`erdos3-three-conditional-proof`](https://github.com/wilsonwu-ai/formal-conjectures/tree/erdos3-three-conditional-proof) on the fork contains the one-file change: the `conditional formal_proof … assuming erdos_3.variants.kelley_meka` tag, with `three` moved below `kelley_meka`.
  - Without the move, Lean reports `Unknown constant erdos_3.variants.kelley_meka`, because `assuming` resolves the declaration after type-checking.
  - The tagged declarations compile against Formal Conjectures' byte-identical attribute implementation.
  - Remaining, by the author: sign Google's CLA, open an issue, then the PR.
- **APAP:** the counterexample to `int` ([Lean file](apap/IntStatementCounterexample.lean)) and the `IsRegular` mismatch are ready to report in an issue, in the author's own words.

### Next steps for A

1. **Post the two upstream items** (author): the Formal Conjectures issue and PR, and the APAP issue.
2. **Pick the first Bohr-set target.** The size bound |B_ρ| ≥ (ρ/4)^d |B| is self-contained, sits on the critical path, and has a blueprint sketch (with an inconsistency in its cell count). It is the natural first lane, and it would be contributed to APAP rather than kept here.
3. **Decide whether to commit to A2.** It is a major project, and the almost-periodicity step alone is research-grade formalization. A1 and the bridge already give a checked conditional result and a ready plug-in point.
