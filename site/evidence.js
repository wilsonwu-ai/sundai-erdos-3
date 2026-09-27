/* Updated only from recorded local verification evidence. */
window.PROJECT_EVIDENCE = {
  repository: "https://github.com/wilsonwu-ai/sundai-erdos-3",
  summary: "A summability step is checked. The full problem remains open.",
  description: "Bounds on the number of chosen integers in each doubled range can prove that the reciprocal sum converges. Lean now checks this implication. Establishing the needed bounds for all progression lengths remains the open step.",
  note: "Lean 4.33.1 checked 30 supporting declarations in the pinned image. All axiom audits passed. The progression-free counting bound remains an unproved assumption; no full-hill proof or official AutoLab score is claimed.",
  results: [
    { claim: "Cofinite sets (only finitely many numbers missing) contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Fixed-step progression tails, including positive multiples, contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "A divergent reciprocal sum forces infinitude and a two-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Powers of two: unbounded, but no nonconstant three-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Summable normalized block counts imply summable reciprocals", status: "LEAN CHECKED · 4.33.1", verified: true }
  ]
};
