#!/usr/bin/env python3
"""Reject a proposed amplification inequality by a finite counterexample.

This is exhaustive integer arithmetic for N=3 and N=9, not a proof or a
counterexample to the infinite Erdős 3 conjecture.
"""
from itertools import combinations
import json
from pathlib import Path


def ap_free(values):
    return all(a + c != 2 * b for a, b, c in combinations(values, 3))


def extremal(size):
    for cardinality in range(size, -1, -1):
        for values in combinations(range(1, size + 1), cardinality):
            if ap_free(values):
                return cardinality, list(values)
    raise AssertionError("The empty set must be admissible")


def main():
    small, small_witness = extremal(3)
    large, large_witness = extremal(9)
    assert small == 2 and large == 5
    assert ap_free((1, 2, 4, 8, 9)) and large > small * small
    record = {
        "scope": "finite counterexample to a candidate amplification inequality, not a solution of Erdős3",
        "method": "exhaustive subsets, all three-element combinations checked by a+c!=2*b",
        "script": "research/check_amplification.py",
        "r3_3": small, "r3_9": large,
        "witness_3": small_witness, "witness_9": large_witness,
        "proposed_bound": "r_3(m*n) <= r_3(m)*r_3(n)",
        "counterexample": {"m": 3, "n": 3, "left": large, "right": small * small},
        "original_conjecture_proved": False,
    }
    target = Path(__file__).resolve().parents[1] / "artifacts/amplification-counterexample.json"
    target.write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: proposed multiplicative bound is false: r_3(9)=5 > r_3(3)^2=4")


if __name__ == "__main__":
    main()
