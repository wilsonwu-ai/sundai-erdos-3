# The execution graph

This is the graph actually used for the September 27, 2026 Sundai Hack 142 session. The user authorized planning, agent execution, a public personal GitHub repository, and GitHub Pages publication.

## Remove false dependencies

| Task pair | Reads the other's output? | Decision |
| --- | --- | --- |
| Research mathematical status / recover AutoLab hill | No | Run concurrently |
| Recover hill / inspect installed Lean and GitHub | No | Run concurrently |
| Build visual finite experiment / prove local lemmas | Only final result labels | Develop separately; join before publication |
| Evaluate exact hill / recover its statement and checker | Yes | Real dependency |
| Announce proof / compile and audit it | Yes | Real dependency |
| Publish / inspect staged files and result claims | Yes | Real dependency |

Shared writes are avoided: `math_research` owns `research/math*` and `lean/`; `autolab_recon` owns `research/autolab*`; `pages_demo` owns `site/`; the coordinator owns scripts, documentation, integration, and publication. Only the coordinator commits and pushes.

```mermaid
flowchart TB
    Request[User's problem] --> Math[Mathematical status]
    Request --> Hill[Exact hill and checker]
    Request --> Tools[Local toolchain]
    Math --> Lemmas[Scoped Lean lemmas]
    Hill --> Audit[Statement audit]
    Tools --> Audit
    Lemmas --> Verify[Compile and inspect axioms]
```

The second graph separates proof evidence from a finite demonstration.

```mermaid
flowchart TB
    Verify[Checked Lean output] --> Scope[State the achieved scope]
    Audit[Hill statement audit] --> Scope
    Demo[Finite AP explorer] --> Browser[Browser and algorithm tests]
    Scope --> Review[Review public artifacts]
    Browser --> Review
    Review --> GitHub[Public GitHub and Pages]
```

## Graph specification

```text
GOAL: A reproducible Erdős 3 research project, checked local results, and honest public demo.
FAN OUT: Mathematical research, hill/interface recovery, and environment work are independent.
CONTRACT: Each worker returns paths, exact claims, evidence, verification, and blockers.
ANCHOR: Primary sources; downloaded hill bytes; actual Lean output; browser observations.
VERIFY: Coordinator reruns Lean and axiom checks; cross-review of hill placeholder; UI tests.
REDUCE: Keep sourced status, passing theorems, reproducible failures, and working interactions.
CAP: Three delegated tasks; four active agents including coordinator; no nested agents.
REPORT: Links, exact achieved scope, checks, remaining original-problem blockers.
HUMAN GATE: Public repo and Pages already authorized. No paid cloud climb authorized.
FROZEN: Original hill statement, axiom whitelist, and distinction between examples and proof.
```

Planning estimate: parallel fraction `p = 0.7`, three independent tracks `N = 3`; Amdahl speedup `1 / (0.3 + 0.7/3) ≈ 1.88`; theoretical ceiling `3.33`. Integration and verification still take sequential time. Maximum fan-in is three concise worker reports. Workers inherit the session model and reasoning tier; no additional external model API is used. A soft planning allowance is approximately 8,000 tokens per delegated task (24,000 total) plus coordinator integration; this is an estimate, not a runtime-enforced budget or measured bill. Workers are bounded by outputs and probes rather than recursive spawning.

The first pass searches at most eight primary math sources and about ten interface probes; broaden only when a concrete blocker warrants it. Cache downloaded context, batch independent reads, and test small changes locally before requesting more model reasoning.
