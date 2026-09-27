#!/usr/bin/env python3
"""Finite exact checks for the fixed-gap obstruction described in the review.

These checks illustrate an ordinary mathematical counterexample to a proposed
lemma. They neither certify the infinite argument nor solve Erdős Problem 3.
"""
from fractions import Fraction
import json
from pathlib import Path


def value(n):
    if n < 1:
        raise ValueError("Indices start at one")
    return n * n.bit_length()


def main():
    blocks = []
    for j in range(11):
        lo, hi = 1 << j, 1 << (j + 1)
        values = [value(n) for n in range(lo, hi)]
        assert all(a == (j + 1) * n for n, a in zip(range(lo, hi), values))
        assert all(b - a == j + 1 for a, b in zip(values, values[1:]))
        mass = sum((Fraction(1, a) for a in values), Fraction())
        lower = Fraction(1, 2 * (j + 1))
        assert mass >= lower
        blocks.append({
            "j": j, "first_index": lo, "last_index": hi - 1,
            "members": len(values), "step": j + 1,
            "first_value": values[0], "last_value": values[-1],
            "reciprocal_mass_lower_bound": str(lower),
            "exact_rational_comparison_passed": True,
        })

    limit = (1 << 11) - 1
    for n in range(1, limit):
        assert value(n + 1) - value(n) >= n.bit_length()
    members = {value(n) for n in range(1, limit + 1)}
    differences = []
    for d in range(1, 11):
        # The written proof shows every starting index n >= 2**d has gap > d.
        starts = [n for n in range(1, limit + 1) if value(n) + d in members]
        assert all(n < (1 << d) for n in starts)
        differences.append({"d": d, "observed_start_count": len(starts),
                            "largest_observed_start_index": max(starts, default=None),
                            "proved_cutoff_in_written_argument": 1 << d})

    record = {
        "scope": "finite exact sanity checks; infinite argument is in research/full-proof-graph/review.md",
        "candidate_lemma": "Divergent reciprocal mass implies a fixed positive difference with infinitely many pairs",
        "candidate_status_by_written_argument": "REFUTED",
        "construction": "a_n = n * (1 + floor(log_2(n))), n >= 1",
        "method": "integer bit lengths and exact rational block-sum comparisons",
        "largest_index_checked": limit, "blocks": blocks, "differences": differences,
        "infinite_claim_lean_checked": False,
        "original_conjecture_proved": False,
    }
    target = Path(__file__).resolve().parents[1] / "artifacts/fixed-gap-counterexample.json"
    target.write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: 11 exact block comparisons and fixed-gap cutoffs through index 2047")


if __name__ == "__main__":
    main()
