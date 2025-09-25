import LeanAideCore

import Mathlib

open LeanAide

universe u v w u_1 u_2 u_3 u₁ u₂ u₃

#leanaide_connect

/--
Translating a theorem here will result in the top 10 closest prompts being written into
-/
#quote test_quote

#eval test_quote

/-- If a sequence of real numbers is monotone and bounded, then the sequence converges. -/
theorem monotone_bounded_convergent_sequence :
    ∀ (s : ℕ → ℝ),
      Monotone s →
        BddAbove (Set.range s) ∨ BddBelow (Set.range s) →
          ∃ l, Filter.Tendsto s Filter.atTop (nhds l) :=
  by sorry

-- #theorem :
--   "Let $D_n$ be the determinant of the $n$ by $n$ matrix whose value in the $i$th row and $j$th column is $|i-j|$. Show that $D_n = (-1)^{n-1} * (n-1) * (2^{n-2}).$"
--   --lean
--    >> translate_theorem --lean


/--
Find every real-valued function $f$ whose domain is an interval $I$ (finite or infinite) having 0 as a left-hand endpoint, such that for every positive member $x$ of $I$ the average of $f$ over the closed interval $[0, x]$ is equal to the geometric mean of the numbers $f(0)$ and $f(x)$.Show that \[ f(x) = \frac{a}{(1 - cx)^2} \begin{cases} \text{for } 0 \le x < \frac{1}{c}, & \text{if } c > 0\\ \text{for } 0 \le x < \infty, & \text{if } c \le 0, \end{cases} \] where $a > 0$. -/
theorem real_interval_avg_eq_geom_mean_fn_eq :
    ∀ (f : ℝ → ℝ) (I : Set ℝ),
      I = Set.Icc 0 1 ∨ I = Set.Ici 0 →
        (∀ x ∈ I, 0 < x → (∫ (t : ℝ) in 0..x, f t) / x = √(f 0 * f x)) →
          ∃ a c,
            0 < a ∧
              ∀ x ∈ I,
                (c > 0 → f x = a / (1 - c * x) ^ 2 ∧ x < 1 / c) ∧
                  (c ≤ 0 → f x = a / (1 - c * x) ^ 2) :=
  by sorry


/--
Let $S$ be the set of all numbers of the form $2^m3^n$, where $m$ and $n$ are integers, and let $P$ be the set of all positive real numbers. Is $S$ dense in $P$?Show that $S$ is dense in $P$. -/
theorem dense_powers_two_three_in_positive_reals :
    Dense (Set.range fun p => 2 ^ ?m.3863 * 3 ^ ?m.3883) := by sorry


/--
Let $\{a_n\}$ be a sequence of real numbers satisfying the inequalities $0 \leq a_k \leq 100a_n$ for $n \leq k \leq 2n$ and $n=1,2,\dots$, and such that the series $\sum_{n=0}^\infty a_n$ converges. Prove that $\lim_{n \to \infty}na_n=0$. -/
theorem limit_of_convergent_series_with_bounded_sequence :
    ∀ {a : ℕ → ℝ},
      (∀ (n k : ℕ), n ≤ k ∧ k ≤ 2 * n → 0 ≤ a k ∧ a k ≤ 100 * a n) →
        Summable a → Filter.Tendsto (fun n => ?m.8446 * a n) Filter.atTop (nhds 0) :=
  by sorry


-- #theorem :
--   "Let $E$ be a Euclidean space of at most three dimensions. If $A$ is a nonempty subset of $E$, define $S(A)$ to be the set of all points that lie on closed segments joining pairs of points of $A$. For a given nonempty set $A_0$, define $A_n=S(A_{n-1})$ for $n=1,2,\\dots$. Prove that $A_2=A_3=\\cdots$. (A one-point set should be considered to be a special case of a closed segment.)"
--   >> translate_theorem


-- #theorem :
--   "Let $\\triangle ABC$ be a triangle in the Euclidean plane, with points $P$, $Q$, and $R$ lying on segments $\\overline{BC}$, $\\overline{CA}$, $\\overline{AB}$ respectively such that $$\\frac{AQ}{QC} = \\frac{BR}{RA} = \\frac{CP}{PB} = k$$ for some positive constant $k$. If $\\triangle UVW$ is the triangle formed by parts of segments $\\overline{AP}$, $\\overline{BQ}$, and $\\overline{CR}$, prove that $$\\frac{[\\triangle UVW]}{[\\triangle ABC]} = \\frac{(k - 1)^2}{k^2 + k + 1},$$ where $[\\triangle]$ denotes the area of the triangle $\\triangle$."
--   >> translate_theorem


-- #theorem :
--   "Let $S$ be a finite set. A set $P$ of subsets of $S$ has the property that any two members of $P$ have at least one element in common and that $P$ cannot be extended (whilst keeping this property). Prove that $P$ contains exactly half of the subsets of $S$."
--   >> translate_theorem


/--
Let $D$ be the unit disk in the plane. Show that we cannot find congruent sets $A, B$ with $A \cap B = \emptyset$ and $A \cup B = D$. -/
theorem unit_disk_no_congruent_disjoint_cover :
    ∀ (A B : Set (ℝ × ℝ)),
      A ∩ B = ∅ → A ∪ B = {z | √(z.1 ^ 2 + z.2 ^ 2) ≤ 1} → ¬∃ f, sorry '' A = B :=
  by sorry


-- #theorem :
--   "Assume that $\\lvert f(x) \\rvert \\le 1$ and $\\lvert f''(x) \\rvert \\le 1$ for all $x$ on an interval of length at least 2. Show that $\\lvert f'(x) \\rvert \\le 2$ on the interval."
--   >> translate_theorem


-- #theorem :
--   "Prove that $$\\sum_{r=0}^{\\lfloor\\frac{n-1}{2}\\rfloor} \\left(\\frac{n - 2r}{n} {n \\choose r}\\right)^2 = \\frac{1}{n} {{2n - 2} \\choose {n - 1}}$$ for every positive integer $n$."
--   >> translate_theorem
