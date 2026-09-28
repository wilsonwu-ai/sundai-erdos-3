# Submission: the equivalence hill

`solution.lean` is the complete proof body for the fixed statement in `statement.lean`, which is also the statement of [`wilsonwu-ai/erdos-3-extremal-equivalence`](https://app.autolab.ai/hills/wilsonwu-ai/erdos-3-extremal-equivalence). The statement says the verbatim Erdős 3 proposition is equivalent to convergence of ∑ⱼ maxCard k (2ʲ) / 2ʲ for every k ≥ 4. It does **not** prove Erdős 3.

It is generated from the checked modules in `lean/` by:

```sh
python3 scripts/inline_solution.py submissions/equivalence
```

Each supporting theorem becomes a local `have`, and each definition becomes a local `let`. The result passed the hill's unchanged evaluator in the pinned image: `proved = 1`, axioms `propext`, `Classical.choice`, `Quot.sound`. [Publication record](../../artifacts/equivalence-hill-publication.json).
