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

## Continuation: proof bridges in the pinned image

After the local evaluator was ready, the next fan-out assigned disjoint files:

| Owner | Bounded output | Dependency |
| --- | --- | --- |
| `math_research` | `lean/Erdos3Divergence.lean`: consequences of reciprocal divergence | Actual imported summability and AP definitions |
| `autolab_recon` | `lean/Erdos3Bridge.lean`: connect explicit witnesses to the hill | Original 14 elementary results and actual AP definitions |
| `pages_demo` | Read-only recommendation for the next analytic reduction | Archived mathematical status and library source |
| Coordinator | Container module checker, integration, public evidence | Both proof files must compile and pass axiom audits first |

All proof workers use the cached original image. There is no nested fan-out or external model call. The existing scopes are held fixed until compiler evidence supports a change. The next meaningful mathematical obstacle, rather than an arbitrary number of attempts, determines where this continuation stops.

The resumed workers retained a sandbox that could not access the Docker socket. The coordinator extracted the pinned library sources into an ignored local directory and ran compilation centrally. The coordinator also took over the short divergence module; the mathematical worker then reviewed it independently. The bridge worker delivered five theorems, and the read-only reviewer checked both the bridge and the conditional reduction. Final aggregate compilation and all 23 axiom audits passed. This adjustment avoids further blocked worker-side runtime calls.

## Full-proof attempt: independent routes and an analytic transfer

The user's subsequent instruction to prove Erdős 3 retained the original statement and axiom policy. Two tasks could run independently: a primary-source check of three full-proof routes (read-only, `math_research`) and finite dyadic block estimates (`lean/Erdos3Blocks.lean`, `autolab_recon`). The coordinator owned `lean/Erdos3Dyadic.lean` and composed the block estimates with summability. The aggregation depends on the block API; it cannot be treated as fully independent. A third worker reviewed the completed source without editing it. All container execution remained with the coordinator to avoid the earlier worker socket blockage.

The graph reused the first run's bounded width and soft planning allowance: two concurrent worker tasks, one later review, no nested agents, at most three mathematical routes, and four primary-source searches in the research worker. No additional paid model API was used. Publication was already authorized; every public mathematical claim still required compilation, axiom audit, and scope review.

```text
RUN RETRO — dyadic-transfer · 2026-09-27
VERIFIER KILL RATE   1 failed aggregation draft rejected; corrected final7 declarations accepted
FAN-OUT EFFICIENCY   3/3 tasks returned useful output
COMPRESSION RATIO    three candidate routes → three explicit gaps; seven new checked declarations
RETURNED VS SENT     3/3
COST                 inherited soft planning allowance → actual delegated token usage unavailable
```

Recommendation: narrow future work to a concrete new progression-free estimate. Further repackaging of the conditional reduction does not prove the conjecture.

## Continuation: direct attacks on the missing estimate

The next executed round used two independent mathematical attacks and one adversarial reviewer. It tested cross-scale constraints and induction on progression length, rather than adding further conditional Lean wrappers. The [full graph, ownership, caps, verified obstructions, and retrospective](../research/full-proof-graph/README.md) record the result. No full proof emerged. The original 30 checked declarations and the unsuccessful hill submission remain unchanged.
