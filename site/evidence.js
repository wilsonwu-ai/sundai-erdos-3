/* Updated only from recorded local verification evidence. */
window.PROJECT_EVIDENCE = {
  repository: "https://github.com/wilsonwu-ai/sundai-erdos-3",
  summary: "23 checked declarations. The full problem remains open.",
  description: "The pinned Lean 4.33.1 environment connects our constructive special cases to AutoLab’s exact definitions. Reciprocal divergence now gives a checked two-term progression. A conditional route to the full hill still requires an unproved mathematical assumption.",
  note: "14 elementary results + 5 bridges + 3 divergence consequences + 1 conditional reduction. All axiom audits passed. The reduction’s assumption remains unproved; no full-hill proof or official AutoLab score is claimed.",
  results: [
    { claim: "Cofinite sets (only finitely many numbers missing) contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Fixed-step progression tails, including positive multiples, contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "A divergent reciprocal sum forces infinitude and a two-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Powers of two: unbounded, but no nonconstant three-term progression", status: "LEAN CHECKED · 4.33.1", verified: true }
  ]
};
