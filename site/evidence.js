/* Updated only from recorded local verification evidence. */
window.PROJECT_EVIDENCE = {
  repository: "https://github.com/wilsonwu-ai/sundai-erdos-3",
  summary: "The exact problem is now reduced to one counting question. It remains open.",
  description: "Lean checks that the full problem is equivalent to a counting statement: sets avoiding a fixed pattern length must thin out fast enough across doubled ranges. For patterns of length four or more, the best published counting bounds are not yet strong enough.",
  note: "Lean 4.33.1 checked 57 supporting declarations in the pinned image, including the equivalence with the verbatim hill statement. All axiom audits passed. The counting bound remains unproved. No Erdős 3 proof or score is claimed; the separate equivalence hill passed on AutoLab.",
  results: [
    { claim: "Cofinite sets (only finitely many numbers missing) contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Fixed-step progression tails, including positive multiples, contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "A divergent reciprocal sum forces infinitude and a two-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Powers of two: unbounded, but no nonconstant three-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Summable normalized block counts imply summable reciprocals", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Separated blocks: pattern-free pieces at spread-out scales combine without creating a pattern of length 4+", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "The full problem is equivalent to a counting series converging for every length 4+", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "That equivalence, as its own AutoLab hill (a different theorem from Erdős 3)", status: "AUTOLAB PASSED · PROVED = 1", verified: true },
    { claim: "The published three-term bounds imply the three-term case of the problem", status: "LEAN CHECKED · 4.33.1", verified: true }
  ]
};
