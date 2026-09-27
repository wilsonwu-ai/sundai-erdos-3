import Lean

/- Minimal reproduction of the proposition-placeholder branch in the current
upstream Google.answerElab (default setting .alwaysTrue). This is an audit of
that branch, not verification of the exact AutoLab image's imported library. -/
open Lean Elab Term
syntax (name := answer) "answer(" term ")" : term
@[term_elab answer]
def answerElab : TermElab := fun stx expectedType? => do
  match stx with
  | `(answer($a:term)) =>
    if expectedType? == some (Expr.sort .zero) && a == (← `(term| sorry)) then
      return .const `True []
    else
      elabTerm a expectedType?
  | _ => throwUnsupportedSyntax

theorem proposition_placeholder : answer(sorry) ↔ True := by rfl
theorem proposition_placeholder_is_true : (answer(sorry) : Prop) := by trivial
#print proposition_placeholder
#print axioms proposition_placeholder
#print axioms proposition_placeholder_is_true
