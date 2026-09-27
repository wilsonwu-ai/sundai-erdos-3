# Erdős Problem 3


## Task

Give a **machine-checked Lean 4 proof** of the theorem `hill` below (toolchain v4.33.1, checked against Mathlib inside the hill's image). The statement is fixed; you write only the proof after the `:=`.

This is an **open Erdős problem** — a research-level conjecture. Most are unsolved; a climber is not expected to solve it yet, and partial or related results are welcome as the field advances.

## Submission format

A submission is a directory containing:

```
solution.lean    the proof (a term, or a `by` tactic block) that completes `theorem hill : … :=`
```

It is appended to the fixed statement and to `#print axioms hill`, then checked with Lean. Do not restate the theorem or add imports; the statement's context (`import FormalConjecturesUtil` → Mathlib, definitions, namespace) is already in scope.

## How it is scored

The proof counts only if it compiles, uses no `sorry`, and depends on no axioms beyond Lean and Mathlib's standard three (`propext`, `Classical.choice`, `Quot.sound`).

| metric | direction | meaning |
|---|---|---|
| `proved` | max | 1 when the proof checks, else the attempt fails with the reason |


## References

- [erdosproblems.com/3](https://www.erdosproblems.com/3)


Formalization from [google-deepmind/formal-conjectures](https://github.com/google-deepmind/formal-conjectures/blob/main/FormalConjectures/ErdosProblems/3.lean).
