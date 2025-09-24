import LeanAideCore

import Mathlib

open LeanAide

universe u v w u_1 u_2 u_3 u₁ u₂ u₃

#leanaide_connect

/--
Indeed this is
This is the basic form of the quote command syntax
-/

#quote test_quote

#eval test_quote

#theorem : "There are infinitely many odd numbers." --lean
   >> translate_theorem --lean
