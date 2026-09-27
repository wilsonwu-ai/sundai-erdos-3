"use strict";
/* Pure finite mathematics; no dependencies or browser APIs. */
(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.ErdosExplorer = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  function isPrime(n) {
    if (!Number.isSafeInteger(n) || n < 2) return false;
    for (let d = 2; d * d <= n; d++) if (n % d === 0) return false;
    return true;
  }
  function findProgressions(input, k) {
    if (!Array.isArray(input) || input.some(n => !Number.isSafeInteger(n) || n < 1 || n > 300)) throw new RangeError("Set members must be positive integers at most 300.");
    if (!Number.isInteger(k) || k < 2 || k > 8) throw new RangeError("Pattern length must be an integer from 2 to 8.");
    const numbers = [...new Set(input)].sort((a, b) => a - b);
    const set = new Set(numbers), found = [], max = numbers[numbers.length - 1] || 0;
    for (let i = 0; i < numbers.length; i++) for (let j = i + 1; j < numbers.length; j++) {
      const a = numbers[i], d = numbers[j] - a;
      if (a + (k - 1) * d > max) break;
      const terms = Array.from({ length: k }, (_, index) => a + index * d);
      if (terms.every(n => set.has(n))) found.push({ terms, d });
    }
    return found;
  }
  return { isPrime, findProgressions };
});
