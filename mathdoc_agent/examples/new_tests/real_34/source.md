## Theorem
Prove that 2 is an upper bound for the set of real numbers
whose square is less than 4.
-/

/- ## Proof
Definitions and Lemmas

Let S := { x ∈ ℝ ∣ x² < 4 }.
We prove that 2 is an upper bound of S, i.e. ∀ x ∈ S, x ≤ 2.

Lemma 1 (nonnegativity of squares):
  ∀ x : ℝ, 0 ≤ x².

Proof of Lemma 1.
  For each x : ℝ, x² = x * x.  By the order‐field axiom that squares are nonnegative, 0 ≤ x * x. □

Lemma 2 (strict monotonicity of sqrt on nonnegatives):
  ∀ a b : ℝ, 0 ≤ a → 0 ≤ b → a < b → sqrt a < sqrt b.

Proof of Lemma 2.
  This follows from the property `real.sqrt_lt_iff_lt` and the fact that `sqrt` maps nonnegatives to nonnegatives. □

Lemma 3 (sqrt of a square is absolute value):
  ∀ x : ℝ, sqrt (x²) = |x|.

Proof of Lemma 3.
  This is the defining property of `real.sqrt` on nonnegative arguments together with `abs_eq_sqrt_sq`. □

Lemma 4 (strict‐to‐weak inequality):
  ∀ a b : ℝ, a < b → a ≤ b.

Proof of Lemma 4.
  This is the axiom `lt.le`. □

Lemma 5 (abs bounds the number):
  ∀ x : ℝ, -|x| ≤ x ∧ x ≤ |x|.

Proof of Lemma 5.
  This is the definition of `abs`. □

Lemma 6 (from |x| < 2 to x ≤ 2):
  ∀ x : ℝ, |x| < 2 → x ≤ 2.

Proof of Lemma 6.
  Let x : ℝ and h₁₀ : |x| < 2.
  From Lemma 5 we have h₅.1 : x ≤ |x|.
  From h₅.1 and h₁₀, by transitivity of ≤ and <, we get h₆₁ : x < 2.
  From h₆₁ and Lemma 4 we conclude x ≤ 2. □

Main proof

Let x : ℝ and assume h : x² < 4.
1. From Lemma 1 we have h₁ : 0 ≤ x².
2. From h₁, the fact 0 ≤ 4, and h, Lemma 2 gives
     sqrt (x²) < sqrt 4 = 2.
3. Lemma 3 yields |x| = sqrt (x²), so |x| < 2.
4. Lemma 6 applied to |x| < 2 yields x ≤ 2.

Since x : ℝ with x² < 4 was arbitrary, we conclude ∀ x ∈ S, x ≤ 2. Hence 2 is an upper bound of S.