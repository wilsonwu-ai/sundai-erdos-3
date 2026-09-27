# What the Lean files prove

The full reciprocal-divergence conjecture is not proved. The modules below formalize known elementary results, connect them to the exact AutoLab definitions, and isolate an explicit remaining research assumption.

| Module | Checked scope |
| --- | --- |
| `Erdos3SpecialCases.lean` | Fourteen elementary results: cofinite sets, affine tails, multiples, prefixes, supersets, two-term progressions, and the powers-of-two obstruction. Imports only `Std`. |
| `Erdos3Bridge.lean` | Five forward bridges: explicit positive-step witnesses give the hill's exact `Set.IsAPOfLength`; arbitrary lengths give its filter conclusion. Cofinite and affine-tail cases now use those exact definitions. |
| `Erdos3Divergence.lean` | Reciprocal non-summability forces infinitude and unboundedness, and therefore a two-term progression in the hill's definition. |
| `Erdos3Reduction.lean` | A conditional proof of the elaborated full hill, assuming `APFreeSummability`. That assumption remains unproved. |

The original predicate `ContainsAP A k` supplies a start `a`, a positive step `d`, and membership of all terms `a + i*d` for `i < k`. The bridge constructs the range of `Fin k`, proves it has exactly `k` distinct elements, and checks the imported progression definition. This handles length zero too. It proves the forward direction; it does not claim an equivalence of the two definitions.

The cofinite and affine-tail assumptions are stronger than reciprocal divergence. The two-term consequence cannot be extended to every length using unboundedness alone: the original module proves powers of two are unbounded yet have no nonconstant three-term progression. Their reciprocal convergence is explanatory mathematics, not yet a theorem in these files.

`APFreeSummability` says that, for every `k ≥ 3`, a set containing no `k`-term progression has summable reciprocals. The reduction accepts this as a theorem parameter. An axiom audit cannot turn an unproved parameter into an established theorem; the parameter is explicitly printed in the verification record. Supplying it would settle the full hill.

From the repository root, run all modules against the exact pinned image:

```sh
python3 scripts/local_evaluator.py start
python3 scripts/local_evaluator.py check-lean
```

[Executed module evidence](../artifacts/mathlib-verification.json) records source hashes, Lean 4.33.1, each theorem's axiom dependencies, and each module's scope. The checker compiles fresh module copies in a temporary directory and permits only `propext`, `Classical.choice`, and `Quot.sound`. No proof uses an admission or `native_decide`.

For just the original dependency-free fourteen theorems, run `python3 scripts/verify_lean.py` with Lean 4.33.1 on the host. To test the unfinished full target, run `python3 scripts/local_evaluator.py eval submissions/current`. That attempt still exits `2`: it reaches the unproved reciprocal-summability claim for a progression-free set. The supporting modules are not substituted for the fixed hill.
