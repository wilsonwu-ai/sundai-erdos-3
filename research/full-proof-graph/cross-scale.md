# Cross-scale attack: separated blocks remove the proposed interaction

This round produced a rigorous obstruction to a packing proof based on interactions between scales. It did not prove Erdős 3. The arguments below are ordinary mathematical proofs, not new Lean-checked declarations, and no novelty is claimed.

Write `k-AP-free` for a set containing no progression of k distinct integers. Define

$$
I_j=[4^j,2\cdot4^j)\cap\mathbb N,\qquad
r_k(n)=\max\{|E|:E\subseteq\{1,\ldots,n\},\ E\text{ is }k\text{-AP-free}\}.
$$

## Candidate 1: independent assembly of separated blocks — PROVED

**Exact statement.** For every integer k≥4 and every sequence of sets B_j⊆I_j, if every B_j is k-AP-free, then their union is k-AP-free. The sequence may be finite or infinite. There is no compatibility condition between the choices of B_j.

**Proof of the geometric fact.** No four-term progression can meet two or more of the intervals I_j. Suppose y_0<y_1<y_2<y_3 is such a progression, with common difference d>0. Let [N,2N) be its largest occupied block. Every term in an older block is strictly below N/2: the preceding block ends at N/2 and is half-open. The terms in the largest block form a nonempty final segment.

- If at least two terms are older, then y_0,y_1<N/2, so d=y_1−y_0<N/2. The first term in the new block equals its predecessor plus d, hence is less than N/2+N/2=N, a contradiction.
- If exactly one term is older, then y_0<N/2 and y_1≥N. Therefore y_3=3y_1−2y_0>2N, again a contradiction.

A k-term progression, k≥4, crossing a block boundary contains four consecutive terms crossing that boundary. To see this explicitly, if the first term in the largest block has index r, choose the four-term window starting at min(r−1,k−4). Thus every k-term progression in the union would lie in one block and contradict that block's hypothesis. ∎

The strict endpoints matter. The lemma is false for k=3: the progression {1,4,7} meets I_0 and I_1. It also does not say that an entire interval I_j is AP-free; it says that different such intervals cannot participate together in a four-term progression.

**Implication for the attempted attack.** An argument that charges accumulated reciprocal mass to unavoidable cross-block progressions has no interactions to charge on this family. There can be arbitrarily many occupied blocks, independently chosen and even containing shorter progressions: {16,17,18}∪{64,65,66} has two three-term progressions and no four-term progression. This does not refute Erdős 3, because sufficiently large normalized sizes of those independent blocks are exactly what remains unknown.

## Candidate 2: a uniform packing budget — OPEN

**Exact proposed inequality.** For each fixed k≥4, is there a finite constant C_k such that, for every m≥0 and every choice of internally k-AP-free B_j⊆I_j, 0≤j≤m,

$$
\sum_{j=0}^{m}\frac{|B_j|}{4^j}\le C_k?
\tag{P}
$$

This inequality would suffice. However, the preceding lemma shows why it cannot be obtained merely from forbidden interactions between the blocks: all the choices in (P) are compatible already. The exact gap is controlling their single-block extremal sizes across infinitely many scales.

Here is a complete justification that (P) is equivalent to the fixed-k reciprocal statement. This also justifies a uniform bound without illegitimately swapping `for every A, there exists a bound` with `there exists a bound for every A`.

**Step 1: translate finite maximizers.** For each j choose a maximizer E_j⊆{1,…,4^j}, with |E_j|=r_k(4^j). Such a maximizer exists because the underlying interval is finite. Set

$$
B_j=\{4^j-1+e:e\in E_j\}.
$$

Translation preserves arithmetic progressions and cardinality, so B_j⊆I_j is k-AP-free and has exactly r_k(4^j) elements. Consequently (P) is equivalent to

$$
\sum_{j\ge0}\frac{r_k(4^j)}{4^j}<\infty.
\tag{E4}
$$

**Step 2: base four and dyadic scales are interchangeable here.** Splitting {1,…,2n} into two consecutive length-n intervals gives

$$
r_k(2n)\le2r_k(n).
$$

Indeed, each intersection of a k-AP-free set with a half remains k-AP-free, and translating the second half preserves that property. Therefore

$$
\frac{r_k(2\cdot4^j)}{2\cdot4^j}
\le\frac{r_k(4^j)}{4^j},
\qquad
\sum_{\ell\ge0}\frac{r_k(2^\ell)}{2^\ell}
\le2\sum_{j\ge0}\frac{r_k(4^j)}{4^j}.
$$

The reverse implication for convergence is immediate by taking the even-indexed subseries.

**Step 3: (E4) implies reciprocal summability.** For any k-AP-free A⊆ℕ, its intersection with [2^ℓ,2^(ℓ+1)) translates into a k-AP-free subset of an interval of length 2^ℓ. Thus

$$
\sum_{a\in A,\ 2^\ell\le a<2^{\ell+1}}\frac1a
\le\frac{r_k(2^\ell)}{2^\ell}.
$$

Summing the nonnegative terms and applying Step 2 proves convergence. This even gives the uniform bound 2∑_j r_k(4^j)/4^j for every such A. The value 0 is omitted from the classical reciprocal sum; Lean's convention contributes zero there.

**Step 4: reciprocal summability implies (E4).** Assemble the maximizing B_j from Step 1 into B=⋃_j B_j. Candidate 1 proves B is k-AP-free. Each b∈B_j is below 2·4^j, hence

$$
\sum_{b\in B_j}\frac1b\ge\frac{r_k(4^j)}{2\cdot4^j}.
$$

If every k-AP-free set has summable reciprocals, this particular B does. Its disjoint blocks therefore force (E4). If (E4) diverged, the same construction would produce an actual divergent-reciprocal k-AP-free set. ∎

**Status distinction.** The equivalence is proved above. Neither (P) nor (E4) has been established here for k≥4. The existence of finite maximizers does not imply that their normalized sizes form a summable sequence. No assumption about a logarithmic exponent greater than one was introduced.

This agrees with the extremal-series equivalence stated in the introduction of [Green–Tao, New bounds for Szemerédi's theorem III](https://arxiv.org/html/1705.01703v3), which cites Tao–Vu, Exercise 10.0.6. The separated-block argument here specifically uses k≥4.

## Finite test predicates for the graph

1. **AP-free check:** for finite S, reject if there exist a≥1 and d≥1 with a+i·d∈S for all 0≤i<k.
2. **Cross-block check:** label each n by its I_j. Enumerate four-term progressions in the union of the full test intervals and reject the separation lemma if any progression has more than one label. This tests the geometry even though each whole interval contains internal progressions.
3. **Packing ratio:** for a proposed explicit C_k and selected AP-free blocks, compute ∑|B_j|/4^j exactly as a rational. A value greater than C_k refutes that particular numerical constant, not the existential claim that some C_k exists.
4. **Extremal consistency:** exact small r_k(n) values must satisfy r_k(2n)≤2r_k(n). They must not be assumed multiplicative in n.

Executed read-only finite checks in this round:

```text
Cross-block 4-APs in full factor-four blocks j=1,2,3: []
4-APs in {16,17,18,64,65,66}: []
3-APs in {1,4,7}: [(1,4,7)]
```

These finite checks corroborate the elementary proof; they are not evidence that the extremal series converges. The useful outcome is a restriction on the search: cross-scale interaction alone cannot rule out divergence, because an arbitrary sequence of individual extremizers can be placed at factor-four scales without introducing new k-term progressions.
