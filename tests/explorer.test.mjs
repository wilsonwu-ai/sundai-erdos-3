import test from 'node:test';
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require = createRequire(import.meta.url);
const {findProgressions, isPrime} = require('../site/explorer.js');

// Independent oracle: enumerate k-element subsets, then inspect adjacent gaps.
// This intentionally does not construct candidates from a start and a step.
function bruteForce(values, k) {
  const answers = [];
  function visit(start, terms) {
    if (terms.length === k) {
      const d = terms[1] - terms[0];
      if (terms.slice(1).every((n, i) => n - terms[i] === d)) answers.push(terms.join(','));
      return;
    }
    for (let i = start; i <= values.length - (k - terms.length); i++) visit(i + 1, [...terms, values[i]]);
  }
  visit(0, []);
  return answers.sort();
}

test('complete and sound for every subset of {1,…,10} and k=2,…,8', () => {
  let cases = 0;
  for (let mask = 0; mask < 1024; mask++) {
    const values = Array.from({length: 10}, (_, i) => i + 1).filter((_, i) => mask & (1 << i));
    for (let k = 2; k <= 8; k++) {
      const found = findProgressions(values, k);
      assert.deepEqual(found.map(p => p.terms.join(',')).sort(), bruteForce(values, k), `mask=${mask}, k=${k}`);
      for (const p of found) assert.equal(p.d, p.terms[1] - p.terms[0]);
      cases++;
    }
  }
  assert.equal(cases, 7168);
});

test('all integers through 300 agree with independent closed-form AP counts', () => {
  const values = Array.from({length: 300}, (_, i) => i + 1);
  for (let k = 2; k <= 8; k++) {
    const D = Math.floor(299 / (k - 1));
    const expected = 300 * D - (k - 1) * D * (D + 1) / 2;
    assert.equal(findProgressions(values, k).length, expected);
  }
});

test('known examples, normalization, and input boundaries', () => {
  assert.deepEqual(findProgressions([29, 5, 11, 17, 23, 5], 5), [{terms:[5,11,17,23,29],d:6}]);
  assert.equal(findProgressions([1,2,4,8,16,32,64,128,256], 3).length, 0);
  assert.deepEqual(findProgressions([], 3), []);
  for (const bad of [[0,1],[-1,2],[1.5,3],[301],['3'],[NaN],[Infinity]]) assert.throws(() => findProgressions(bad,3), RangeError);
  for (const k of [0,1,9,2.5,NaN]) assert.throws(() => findProgressions([1,2,3],k),RangeError);
});

test('prime predicate agrees with the sieve through 300', () => {
  const sieve = Array(301).fill(true); sieve[0] = sieve[1] = false;
  for (let p = 2; p <= 300; p++) if (sieve[p]) for (let multiple = p+p; multiple <= 300; multiple += p) sieve[multiple] = false;
  for (let n = 0; n <= 300; n++) assert.equal(isPrime(n), sieve[n]);
});
