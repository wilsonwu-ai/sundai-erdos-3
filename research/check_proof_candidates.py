#!/usr/bin/env python3
"""Exact finite checks of the new structural proof candidates.

Passing a finite check is not a proof of a universally quantified claim.
Infinite arguments, assumptions, and limitations are recorded separately.
"""
from itertools import product
import json
from pathlib import Path


def progressions(values, length):
    values = set(values)
    if not values:
        return []
    last = max(values)
    return [tuple(a + i * d for i in range(length))
            for a in sorted(values)
            for d in range(1, (last - a) // (length - 1) + 1)
            if all(a + i * d in values for i in range(length))]


def starts(values):
    return {ap[0] for ap in progressions(values, 3)}


def main():
    example = {1, 2, 3, 6, 9, 10, 15}
    first_starts = starts(example)
    assert first_starts == {1, 2, 3}
    assert progressions(first_starts, 3) == [(1, 2, 3)]
    assert not progressions(example, 4)

    cube_checks = []
    for dimension in range(1, 5):
        values = {1 + sum(x * 5**i for i, x in enumerate(digits))
                  for digits in product(range(3), repeat=dimension)}
        assert not progressions(values, 4)
        iterate = values
        cardinalities = [len(iterate)]
        for _ in range(dimension):
            iterate = starts(iterate)
            cardinalities.append(len(iterate))
        assert 1 in iterate
        cube_checks.append({"dimension": dimension, "max_value": max(values),
                            "iterated_start_set_sizes": cardinalities,
                            "four_term_progressions": 0})

    block_of = {a: j for j in range(5) for a in range(4**j, 2 * 4**j)}
    block_checks = []
    for length in range(4, 9):
        patterns = progressions(block_of, length)
        crossing = [ap for ap in patterns if len({block_of[a] for a in ap}) > 1]
        assert not crossing
        block_checks.append({"length": length, "progressions_checked": len(patterns),
                             "crossing_progressions": len(crossing)})
    assert (1, 4, 7) in progressions(block_of, 3)
    assert len({block_of[a] for a in (1, 4, 7)}) == 2

    record = {
        "scope": "finite exact checks, not a full proof or counterexample to Erdős 3",
        "method": "exhaustive positive-step AP enumeration for each specified finite set",
        "three_term_starts_do_not_force_four_terms": {
            "set": sorted(example), "three_term_progressions": progressions(example, 3),
            "start_set": sorted(first_starts), "four_term_progressions": []},
        "finite_depth_start_iteration": cube_checks,
        "separated_blocks": {"indices": [0, 1, 2, 3, 4], "total_members": len(block_of),
                              "checks": block_checks, "three_term_crossing": [1, 4, 7]},
        "written_arguments": ["research/full-proof-graph/length-induction.md",
                              "research/full-proof-graph/cross-scale.md",
                              "research/full-proof-graph/review.md"],
        "new_infinite_arguments_lean_checked": False,
        "original_conjecture_proved": False,
    }
    target = Path(__file__).resolve().parents[1] / "artifacts/proof-candidate-checks.json"
    target.write_text(json.dumps(record, indent=2) + "\n")
    print("PASS: start-set counterexample, four digit cubes, and five separated-block lengths")


if __name__ == "__main__":
    main()
