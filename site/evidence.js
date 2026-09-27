/* Updated only from recorded local verification evidence. */
window.PROJECT_EVIDENCE = {
  repository: "https://github.com/wilsonwu-ai/sundai-erdos-3",
  summary: "14 checked theorems. The full problem remains open.",
  description: "We verified elementary special cases in Lean 4.33.1. These are known mathematical facts, formalized using our own arithmetic-progression predicate and Lean’s standard library. They do not prove the fixed AutoLab hill.",
  note: "Lean 4.33.1 checked 14 theorems; the axiom audit passed. No full-hill proof or official AutoLab score is claimed.",
  results: [
    { claim: "Cofinite sets (only finitely many numbers missing) contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Fixed-step progression tails, including positive multiples, contain every length", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "An unbounded set contains a two-term progression", status: "LEAN CHECKED · 4.33.1", verified: true },
    { claim: "Powers of two: unbounded, but no nonconstant three-term progression", status: "LEAN CHECKED · 4.33.1", verified: true }
  ]
};
