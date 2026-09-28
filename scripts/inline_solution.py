#!/usr/bin/env python3
"""Inline the checked supporting modules into one proof body for the equivalence hill.

Regenerate with: python3 scripts/inline_solution.py submissions/equivalence
Writes <out>/solution.lean: a single `by` block. Each supporting theorem becomes a
local `have` with its original binders and proof; each definition becomes a local
`let`. Output is compiled against the hill statement by the caller.
"""
import re
import sys
from pathlib import Path

ROOT = Path("/Applications/sundai-erdos-3")
# (module, declarations to keep, in dependency order). Definitions are `def`/`abbrev`.
PLAN = [
    ("Erdos3Blocks", ["logBlock", "logBlock_lt_upper", "logBlock_finite",
                      "logBlock_reciprocal_le", "logBlock_mass_le"]),
    ("Erdos3Dyadic", ["reciprocal_summable_of_dyadic_counts"]),
    ("Erdos3Reduction", ["APFreeSummability", "hill_of_apFreeSummability"]),
    ("Erdos3CrossScale", None),  # everything except the fidelity restatement
]
SKIP = {"hill_statement_iff_extremal"}
NAMESPACES = ["Erdos3Blocks.", "Erdos3Dyadic.", "Erdos3Reduction.", "Erdos3CrossScale."]


def declarations(text):
    """Yield (kind, name, text) for each top-level def/abbrev/theorem, docstrings dropped."""
    lines = text.split("\n")
    starts = [i for i, l in enumerate(lines)
              if re.match(r"^(noncomputable\s+)?(abbrev|def|theorem)\s+\w+", l)]
    stops = [i for i, l in enumerate(lines)
             if re.match(r"^(/--|/-!|#print|#check|end\s|namespace|open\s|-- ##)", l)
             or re.match(r"^(noncomputable\s+)?(abbrev|def|theorem)\s+\w+", l)]
    for s in starts:
        e = min([x for x in stops if x > s] + [len(lines)])
        block = "\n".join(lines[s:e]).rstrip()
        m = re.match(r"^(?:noncomputable\s+)?(abbrev|def|theorem)\s+(\w+)", block)
        yield m[1], m[2], block


def to_local(kind, name, block):
    body = re.sub(r"^(?:noncomputable\s+)?(abbrev|def|theorem)\s+", "", block, count=1)
    for ns in NAMESPACES:
        body = body.replace(ns, "")
    if kind in ("abbrev", "def"):
        # `name binders : T :=\n  body`  ->  `let name : binders → T := fun binders ↦ body`
        m = re.match(r"(\w+)\s*(.*?)\s*:\s*([^:=]+?)\s*:=\s*(.*)$", body, re.S)
        n, binders, typ, value = m[1], m[2].strip(), m[3].strip(), m[4].strip()
        names = re.findall(r"\(([^:()]+):", binders)
        args = " ".join(" ".join(x.split()) for x in names)
        pi = " → ".join([f"({b.strip()})" for b in re.findall(r"\(([^()]+)\)", binders)] + [typ])
        text = (f"let {n} : {pi} := fun {args} ↦\n  {value}" if args.strip()
                else f"let {n} : {typ} :=\n  {value}")
    else:
        text = "have " + body
    return "\n".join(("  " + l) if l.strip() else "" for l in text.split("\n"))


def main():
    out = Path(sys.argv[1])
    parts = ["by", "  classical"]
    for module, keep in PLAN:
        text = (ROOT / "lean" / f"{module}.lean").read_text()
        decls = {name: (kind, block) for kind, name, block in declarations(text)}
        order = keep if keep is not None else [n for _, n, _ in declarations(text) if n not in SKIP]
        for name in order:
            kind, block = decls[name]
            parts.append(to_local(kind, name, block))
    parts.append("  exact hill_iff_extremal")
    out.mkdir(parents=True, exist_ok=True)
    (out / "solution.lean").write_text("\n".join(parts) + "\n")
    print(f"wrote {out/'solution.lean'}: {len(parts)} parts, {sum(p.count(chr(10))+1 for p in parts)} lines")


if __name__ == "__main__":
    main()
