# APAP integer statement: a counterexample

[`IntStatementCounterexample.lean`](IntStatementCounterexample.lean) proves, in Lean, that the statement of `int` in [APAP](https://github.com/YaelDillies/APAP) (`APAP/Integer.lean`, commit `3b79412`, Apache-2.0) is false as written. The statement is copied verbatim as a proposition.

The statement puts `∃ c > 0` after `A` and `N`. For N = 2 and A = {0, 1}, which is three-term-progression-free, it would need 2 ≤ 2 / exp(c · (log 2)^(1/12)). That fails for every c > 0.

The intended theorem presumably fixes c before A and N, and either restricts to large N or allows a constant factor. This does not affect APAP's completed finite-field theorem `ff`, and it does not bear on the mathematics of Kelley–Meka or Bloom–Sisask. It matters here because [Goal A](../roadmap.md#goal-a-status-27-september-2026) must not build on the statement as written.

The file imports only Mathlib. It compiled in the pinned hill image (Lean 4.33.1) using only `propext`, `Classical.choice` and `Quot.sound`. It has not yet been reported upstream.
