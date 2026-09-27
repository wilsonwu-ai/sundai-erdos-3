# Length induction: two candidate steps and their obstructions

2026-09-27. This round contains mathematical arguments and one exhaustive finite check. It does not contain a proof of Erdős 3 or a new Lean theorem.

Work with positive integers; removing zero from a subset of `ℕ` has no effect on the reciprocal series under the hill's convention. Write

$$
M(A)=\sum_{a\in A}\frac1a,\qquad D(A)\iff M(A)=\infty.
$$

For `k ≥ 1` and `d ≥ 1`, define

$$
P_{k,d}(A)=\{a\ge1:\forall i\in\{0,\ldots,k-1\},\ a+id\in A\},
\quad S_k(A)=\bigcup_{d\ge1}P_{k,d}(A).
$$

Thus `S_k(A)` is the set of starts of length-`k` progressions, with difference allowed to depend on the start. Let `AP_k(A)` mean `S_k(A) ≠ ∅`, and let

$$
H_k:\quad\forall A\subseteq\mathbb N_{>0},\ D(A)\Longrightarrow AP_k(A).
$$

The [known three-term theorem](https://arxiv.org/abs/2007.03528) supplies `H₃` mathematically. This report does not assume it has been formalized in this repository.

## Candidate 1: retain one difference throughout length induction

**REFUTED.** The proposed statement is

$$
\forall A,\quad D(A)\Longrightarrow
\exists d\ge1\ \forall k\ge1,\quad P_{k,d}(A)\ne\varnothing.
\tag{C1}
$$

This would suffice for every `H_k`, but improperly strengthens the required quantifier order: Erdős 3 allows a different difference for each length.

Take

$$
a_n=n(1+\lfloor\log_2 n\rfloor),\quad n\ge1,
\qquad A=\{a_n:n\ge1\}.
$$

The sequence is strictly increasing. For `2ʲ ≤ n < 2ʲ⁺¹`, its terms are `a_n=(j+1)n`. Consequently

$$
\sum_{n=2^j}^{2^{j+1}-1}\frac1{a_n}
\ge\frac{2^j}{(j+1)2^{j+1}}
=\frac1{2(j+1)}.
$$

Disjoint dyadic index blocks prove `D(A)`. This is an infinite-series argument, not an extrapolation from a finite computation.

Put `b_n=1+⌊log₂ n⌋`. Because `b_n` is nondecreasing,

$$
a_{n+1}-a_n=(n+1)b_{n+1}-nb_n\ge b_n\longrightarrow\infty.
$$

For any fixed `d`, choose `N` with `b_n>d` for `n≥N`. Distinct tail terms then differ by more than `d`. Any pair at distance `d` must have its smaller term among the finitely many `a_n` with `n<N`; each smaller term has at most one partner. Therefore `P₂,d(A)` is finite. A length-`k` progression of step `d` has `k-1` distinct starts of adjacent step-`d` pairs, so its length is bounded for that fixed `d`. This disproves `(C1)`.

It also refutes the commonly proposed resource lemma

$$
D(A)\Longrightarrow\exists d\ge1,\ M(P_{2,d}(A))=\infty,
$$

and the analogous assertion with any `k≥2`, since `P_k,d ⊆ P₂,d`. Countably many finite difference fibers can collectively have divergent reciprocal mass. Each dyadic index block of the example is itself a long progression of difference `j+1`; the example is not a counterexample to Erdős 3.

## A valid intermediate fact for variable differences

**PROVED mathematically, conditional on `H_k`:**

$$
H_k\Longrightarrow\forall A,\quad D(A)\Longrightarrow D(S_k(A)).
\tag{start-mass inheritance}
$$

Proof: suppose `M(S_k(A))<∞`. Since `S_k(A)⊆A` and all summands are nonnegative, the complement `B=A\S_k(A)` still has divergent reciprocal mass. By `H_k`, it contains a `k`-progression. Its start belongs to `B`, but the same progression lies in `A`, so its start belongs to `S_k(A)`, a contradiction. No fixed difference was extracted.

For `k=3`, this proves that `S₃(A)` is reciprocal-divergent whenever `A` is. Reapplying `H₃` gives a three-term progression of starts. The next step is where induction breaks.

## Candidate 2: turn a progression of starts into a longer progression

**REFUTED.** The proposed structural extension is

$$
\forall A\subseteq\mathbb N_{>0},\quad
AP_3(S_3(A))\Longrightarrow AP_4(A).
\tag{C2}
$$

If `(C2)` were true, start-mass inheritance and `H₃` would prove `H₄`: first `D(S₃(A))`, then `AP₃(S₃(A))`, then `AP₄(A)`.

An exact finite counterexample is

$$
A=\{1,2,3,6,9,10,15\}.
$$

All its nonconstant three-term progressions are:

| Start | Difference | Terms |
| --- | --- | --- |
| 1 | 1 | 1, 2, 3 |
| 2 | 4 | 2, 6, 10 |
| 3 | 3 | 3, 6, 9 |
| 3 | 6 | 3, 9, 15 |

Thus `S₃(A)={1,2,3}` contains a three-term progression. `A` contains no four-term progression. The finite check enumerated every `a∈A` and every integer `1≤d≤⌊(max(A)-a)/(k-1)⌋`, for `k=3,4`, and required membership of all `k` terms. The four-term list was empty; there is no sampling or floating-point arithmetic in this check.

The failed inference is precise: the starts have a shared spacing, but the progressions attached to those starts need not use that spacing or compatible spacings. Their union is not necessarily a longer progression.

For the general induction scheme `AP₃(S_k(A)) ⇒ AP_{k+1}(A)`, the same example already defeats the `k=3` step.

### Further iteration does not supply the missing synchronization

For any `m≥1`, the finite set

$$
C_m=\left\{1+\sum_{i=0}^{m-1}x_i5^i:x_i\in\{0,1,2\}\right\}
$$

with `C₀={1}`, has `C_{m-1}⊆S₃(C_m)`, by using difference `5^{m-1}`. Monotonicity of `S₃` gives `1∈S₃^m(C_m)`.

Nevertheless `C_m` is four-term-progression-free. In either consecutive midpoint identity of a hypothetical four-term progression, the coefficient of each power of five lies in `[-4,4]`. Reduction modulo five and induction on the digit position force each coefficient to vanish. Each digit therefore forms a four-term integer progression inside `{0,1,2}`, whose difference must be zero. All four original numbers would coincide. Thus no fixed number of nested start-set applications, by itself, forces a four-term progression.

This family is an obstruction to the qualitative structural inference, not to a divergence-sensitive theorem.

## Exact unproved assumption remaining

Adding the original hypothesis back into candidate 2 gives

$$
\forall A,\quad D(A)\land AP_3(S_3(A))\Longrightarrow AP_4(A).
\tag{missing divergence-sensitive step}
$$

**OPEN in this round.** Under the known `H₃` and the proved start-mass inheritance argument, this statement is equivalent to `H₄`: its extra start-set premise is already guaranteed for every divergent `A`. It must not be described as an established induction lemma or mathematical progress toward closing the four-term case.

What survives is a useful hereditary reciprocal-mass property. What fails is fixed-difference selection and a purely qualitative conversion from progressions of starts to a longer progression. To make this induction route work, an additional ingredient must link the divergence hypothesis to compatible progression witnesses; no such ingredient is supplied here.
