import Mathlib

/-!
# Verification Boilerplate
This file contains specific definitional preferences and imports.
Always use declarative proof structures (`have`, `show`) rather than imperative tactics where possible.
-/

-- Specific definition preference for Even numbers
def MyEven (n : ℕ) : Prop := ∃ r, n = r + r
