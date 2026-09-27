# Full-proof attempt: dyadic counting and the unresolved bound

**Outcome: no full proof of Erdős 3 was obtained.** The primary [problem database](https://www.erdosproblems.com/3) still lists the conjecture as open. The new Lean work proves an analytic transfer and an explicitly conditional route to the hill. It does not establish the progression-free estimate required by that route.

## The part now checked by Lean

Divide a set A into blocks Bⱼ according to the integer part of log₂(a). Apart from the harmless zero convention, these are A∩[2ʲ,2ʲ⁺¹). Every block is finite. Its reciprocal mass is at most |Bⱼ|/2ʲ. Consequently:

\[
\sum_{j\ge0}\frac{|B_j|}{2^j}<\infty
\quad\Longrightarrow\quad
\sum_{a\in A}\frac1a<\infty.
\]

The formal proof partitions the subtype A, bounds each finite block, and applies the nonnegative series comparison theorem. It also checks that a bound |Bⱼ|/2ʲ ≤ C/(j+1)ᵖ with p>1 suffices. Lean's block zero includes the number zero if it belongs to A; its reciprocal contribution is zero, and the proof treats it explicitly.

[Erdos3Blocks.lean](../lean/Erdos3Blocks.lean) contains four block lemmas. [Erdos3Dyadic.lean](../lean/Erdos3Dyadic.lean) contains the two analytic transfers and the conditional full-hill implication. All seven declarations compiled in the pinned image and passed the standard-axiom audit, alongside the original 23. [Executed evidence](../artifacts/mathlib-verification.json).

The missing assumption in the final theorem is named `APFreePowerEnvelope`. For each fixed k≥3 it requires constants C and p>1 working for **every** k-progression-free set and **every** block. The constants may depend on k. The theorem takes this assumption as a parameter; no proof of it is supplied. This power envelope is sufficient and may be stronger than the conjecture. The code does not assert equivalence.

## Attempt 1: sum known extremal bounds

Let rₖ(N) be the largest size of a k-progression-free subset of {1,…,N}. Green–Tao identify the conjecture with summability of rₖ(2ʲ)/2ʲ for every fixed k≥3; this literature equivalence is not itself formalized here. Their four-term bound supplies a positive logarithmic exponent, without the exponent exceeding one that this comparison needs. [Green–Tao, introduction and Theorem 1.1](https://arxiv.org/html/1705.01703v3).

Bloom–Sisask's bound for k=3 has the required exponent 1+ε, with ε>0. It supplies the known three-term result in ordinary mathematics; this repository has not formalized their proof. [Bloom–Sisask](https://arxiv.org/abs/2007.03528).

For k≥5, Leng–Sah–Sawhney give a bound with normalized decay exp(−(log log N)ᶜ), where 0<c<1. On dyadic scales this yields a nonsummable envelope comparable to exp(−(log j)ᶜ). [Theorem 1.1](https://arxiv.org/html/2402.17995v2).

The scalar profile δⱼ=1/(j log j), for j≥2, has a divergent sum while lying below both j⁻ᶜ for 0<c≤1 and exp(−(log j)ᶜ) for 0<c<1, eventually. This elementary comparison explains why those envelopes alone do not produce a contradiction. It is **not** a construction of a progression-free counterexample to Erdős 3.

## Attempt 2: use relative density

Relative Szemerédi theorems need a fixed positive relative density and a majorant satisfying a specified linear-forms condition. Reciprocal divergence alone supplies neither hypothesis. Normalizing an arbitrary sparse indicator to have mean one does not prove that condition. [Conlon–Fox–Zhao, Theorem 2.4](https://arxiv.org/html/1305.5440).

No construction meeting these conditions from the original hill hypothesis was obtained. Applying the theorem without them would leave a gap.

## Attempt 3: amplify a density estimate

The known higher-order density-increment argument can stop when N is at most exp(exp((log(1/δ))ᶜ)). A divergent sequence of block densities does not force that stopping alternative to fail. Repeating the argument therefore does not establish the missing summability estimate. [Leng–Sah–Sawhney, Lemma 3.7](https://arxiv.org/html/2402.17995v2).

A proposed shortcut rₖ(mn) ≤ rₖ(m)rₖ(n) is false. For k=3, r₃(3)=2, whereas r₃(9)=5: {1,2,4,8,9} has no three-term progression. Thus 5>2·2 contradicts the proposed bound. The [exhaustive integer check](check_amplification.py) examines every subset and every three-element combination for these two finite universes; its [recorded output](../artifacts/amplification-counterexample.json) is separate from Lean verification and from the infinite conjecture.

## Remaining obligation

The fixed-hill submission still stops at reciprocal summability for a progression-free set. The new analytic theorem checks how a sufficiently strong counting bound would discharge that goal. None of the examined routes proves such a bound for all progression lengths. No passing full-hill submission or official AutoLab score is claimed.
