Calculational proofs are proofs where a large part of the reasoning is a **structured chain of transformations**. In Lean-style terms, many of these correspond to `calc` blocks, but the underlying mathematical schemas are more varied than a single equality chain.

Below is a taxonomy of useful schemas.

---

# 1. Pure equality chain

The simplest calculational proof proves (A = B) by a sequence of equalities.

[
A = A_1 = A_2 = \cdots = B.
]

Schema:

```text
To prove A = B:
  calc
    A = A₁ := by ...
    _ = A₂ := by ...
    ...
    _ = B  := by ...
```

Example:

[
(n+1)^2
= n^2 + 2n + 1
= n^2 + n + n + 1
= n(n+1) + (n+1)
= (n+1)^2.
]

Typical justifications:

```text
by ring
by simp
by rw [...]
by unfold ...
by exact ...
```

This is the most common algebraic calculation pattern.

---

# 2. Equality by rewriting one side to a normal form

Instead of explicitly calculating from (A) to (B), one proves both reduce to the same canonical expression.

[
A = N, \qquad B = N.
]

Schema:

```text
To prove A = B:
  show normalize(A) = normalize(B)
  both sides simplify to N
```

Mathematically:

[
A = N = B.
]

or

[
A = N \quad\text{and}\quad B = N.
]

Examples:

* polynomial identities by expansion;
* group identities by associativity and inverses;
* set identities by Boolean algebra;
* trigonometric identities after rewriting into (\sin) and (\cos).

Lean-style schema:

```lean
by
  ring
```

or

```lean
by
  simp [defs]
```

or

```lean
by
  abel
```

This is not always written as a visible chain, but it is still a calculational proof.

---

# 3. Equality by substituting known equalities

Here the proof is a chain where some steps use hypotheses.

Suppose:

[
a = b,\qquad f(b) = c.
]

Then:

[
f(a) = f(b) = c.
]

Schema:

```text
Given h₁ : a = b, h₂ : f b = c.
To prove f a = c:
  calc
    f a = f b := by rw [h₁]
    _   = c   := h₂
```

Common mathematical form:

[
\begin{aligned}
f(a)
&= f(b) &&\text{since } a=b \
&= c &&\text{by the second hypothesis.}
\end{aligned}
]

This is the basic “rewrite by hypotheses” pattern.

---

# 4. Equational reasoning using congruence

A known equality is placed inside a larger context.

If

[
x = y,
]

then

[
f(x) = f(y),
]

or

[
a + x = a + y,
]

or

[
g(u,x,v) = g(u,y,v).
]

Schema:

```text
Given h : x = y.
To prove C[x] = C[y]:
  apply congruence of context C to h.
```

Examples:

[
x = y \implies x^2 + 3x = y^2 + 3y.
]

In Lean this often appears as:

```lean
rw [h]
```

or

```lean
congr
```

or

```lean
exact congrArg f h
```

This is a key schema because many calculational steps are really contextual rewrites.

---

# 5. Equality by unfolding definitions

Many calculations are definitional: expand definitions, simplify, then fold back.

Schema:

```text
To prove expression involving F:
  unfold F
  calculate using the definition
  optionally fold the result back into another definition
```

Example:

If

[
\operatorname{dist}(x,y) = |x-y|,
]

then:

[
\operatorname{dist}(x,z)
= |x-z|
= |(x-y)+(y-z)|
\le |x-y| + |y-z|
= \operatorname{dist}(x,y)+\operatorname{dist}(y,z).
]

This is both a definitional calculation and an inequality calculation.

Lean-style:

```lean
calc
  dist x z = |x - z| := by unfold dist
  _ = |(x - y) + (y - z)| := by ring_nf
  _ ≤ |x - y| + |y - z| := by exact abs_add _ _
  _ = dist x y + dist y z := by unfold dist
```

---

# 6. Inequality chain

Instead of equalities, one proves:

[
A \le A_1 \le A_2 \le \cdots \le B.
]

Schema:

```text
To prove A ≤ B:
  calc
    A ≤ A₁ := by ...
    _ ≤ A₂ := by ...
    ...
    _ ≤ B  := by ...
```

Example:

[
x
\le x+y
\le x+y+z
]

assuming (y,z \ge 0).

Common step types:

* monotonicity;
* positivity;
* triangle inequality;
* known bounds;
* replacing a term by a larger term;
* dropping a negative term;
* estimating each summand.

This is the main structure of estimates in analysis.

---

# 7. Mixed equality-inequality chain

Many useful calculations mix (=), (\le), (<), (\ge), etc.

Example:

[
A
= A_1
\le A_2
= A_3
< A_4
\le B.
]

Schema:

```text
To prove A < B:
  calc
    A = A₁ := by ...
    _ ≤ A₂ := by ...
    _ = A₃ := by ...
    _ < A₄ := by ...
    _ ≤ B  := by ...
```

The final relation is obtained by transitivity of the relations involved.

Typical example:

[
\begin{aligned}
|f(x)-f(y)|
&= |(f(x)-L)+(L-f(y))| \
&\le |f(x)-L| + |f(y)-L| \
&< \varepsilon/2 + \varepsilon/2 \
&= \varepsilon.
\end{aligned}
]

This is extremely common in analysis.

---

# 8. Two-sided estimate / sandwich calculation

To prove equality or convergence, one bounds a quantity above and below.

Schema:

[
L \le A \le L
]

therefore

[
A = L.
]

Or for convergence:

[
a_n \le b_n \le c_n,
]

with

[
a_n \to L,\qquad c_n \to L,
]

therefore

[
b_n \to L.
]

For a concrete equality:

```text
To prove A = L:
  prove A ≤ L
  prove L ≤ A
  conclude by antisymmetry
```

Lean-style:

```lean
apply le_antisymm
· -- prove A ≤ L
· -- prove L ≤ A
```

This is a calculational structure even if each side is itself a chain.

---

# 9. Strict inequality via non-strict inequality plus strict step

To prove (A < C), often one inserts one genuinely strict step among weak steps:

[
A \le B < C.
]

or

[
A < B \le C.
]

Schema:

```text
To prove A < C:
  calc
    A ≤ B := by ...
    _ < C := by ...
```

or

```text
To prove A < C:
  calc
    A < B := by ...
    _ ≤ C := by ...
```

This is useful because many estimates naturally give weak inequalities except for one strict bound.

Example:

[
|x|
\le |x-y| + |y|
< \varepsilon + |y|.
]

---

# 10. Positivity calculation

Many arguments require proving that an expression is positive or nonnegative.

Schema:

```text
To prove 0 ≤ E:
  decompose E into known nonnegative pieces.
```

Examples:

[
0 \le x^2,
]

[
0 \le a^2 + b^2,
]

[
0 < e^x,
]

[
0 < \frac{\varepsilon}{2}
\quad\text{if}\quad
0 < \varepsilon.
]

More structured version:

[
0 \le A,\quad 0 \le B
\implies
0 \le A+B.
]

[
0 \le A,\quad 0 \le B
\implies
0 \le AB.
]

Lean-style:

```lean
positivity
```

or:

```lean
nlinarith [sq_nonneg x]
```

This is often a subcalculation inside an inequality proof.

---

# 11. Monotonicity calculation

A term is transformed using monotonicity of a function or operation.

Schema:

```text
Given a ≤ b and f monotone.
Then f a ≤ f b.
```

Examples:

[
a \le b \implies a+c \le b+c.
]

[
0 \le c,\ a \le b \implies ca \le cb.
]

[
a \le b \implies e^a \le e^b.
]

[
0 < a \le b \implies \log a \le \log b.
]

Calculation form:

[
f(A)
\le f(B)
\le f(C).
]

This schema is crucial for estimates where one replaces an argument by a bound.

---

# 12. Calculation by applying a function to both sides

Sometimes one transforms an equation or inequality by applying a function.

For equalities:

[
A = B \implies f(A) = f(B).
]

For inequalities:

[
A \le B \implies f(A) \le f(B)
]

if (f) is monotone.

For order-reversing functions:

[
A \le B \implies f(B) \le f(A).
]

Example:

[
0 < a \le b
\implies
\frac{1}{b} \le \frac{1}{a}.
]

Schema:

```text
Given h : A ≤ B.
If f is monotone, derive f A ≤ f B.
If f is antitone, derive f B ≤ f A.
```

This is a common source of side conditions, especially positivity.

---

# 13. Algebraic rearrangement calculation

The goal is transformed into an equivalent algebraic form.

Example:

To prove

[
a \le b,
]

it may be enough to prove

[
a-b \le 0.
]

Or:

[
a = b
\iff
a-b = 0.
]

Schema:

```text
Transform the target into an equivalent normalized statement.
Prove the normalized statement.
```

Examples:

[
a^2 - 2ab + b^2 = (a-b)^2 \ge 0
]

so

[
2ab \le a^2+b^2.
]

Calculation:

[
a^2+b^2-2ab
= (a-b)^2
\ge 0.
]

Then conclude:

[
2ab \le a^2+b^2.
]

This pattern is common in inequalities.

---

# 14. Completing the square

A special algebraic rearrangement pattern.

Schema:

[
ax^2 + bx + c
=============

a\left(x + \frac{b}{2a}\right)^2
+
\left(c - \frac{b^2}{4a}\right).
]

Use it to show nonnegativity, find minima, or derive bounds.

Example:

[
x^2 - 2x + 2
= (x-1)^2 + 1
\ge 1.
]

Proof structure:

```text
Rewrite expression as square plus constant.
Use square ≥ 0.
Conclude desired bound.
```

---

# 15. Telescoping calculation

A sum is rewritten so that most terms cancel.

Schema:

[
\sum_{k=m}^{n} (a_{k+1}-a_k)
= a_{n+1}-a_m.
]

Example:

[
\sum_{k=1}^{n} \left(\frac1k - \frac1{k+1}\right)
= 1 - \frac1{n+1}.
]

Proof structure:

```text
Rewrite summand as consecutive difference.
Expand or invoke telescoping lemma.
Cancel intermediate terms.
```

Useful schema for JSON/proof representation:

```json
{
  "type": "telescoping_sum",
  "summand": "a_{k+1} - a_k",
  "range": "k = m to n",
  "result": "a_{n+1} - a_m"
}
```

---

# 16. Inductive calculation

The proof uses induction, and the induction step is a calculation.

Schema:

```text
To prove formula F(n):
  Base case: direct calculation.
  Step:
    calculate expression at n+1
    rewrite using induction hypothesis
    simplify to desired formula.
```

Example:

[
\sum_{k=1}^{n} k = \frac{n(n+1)}2.
]

Step:

[
\begin{aligned}
\sum_{k=1}^{n+1} k
&= \sum_{k=1}^{n} k + (n+1) \
&= \frac{n(n+1)}2 + (n+1) \
&= \frac{(n+1)(n+2)}2.
\end{aligned}
]

Schema:

```text
calc
  expression(n+1)
    = expression(n) + new_term
    = closed_form(n) + new_term     by induction hypothesis
    = closed_form(n+1)              by algebra
```

This is one of the most important schemas.

---

# 17. Recursive unfolding calculation

A recursively defined function is calculated by unfolding its defining equation.

Schema:

```text
To prove property of f(input):
  unfold f on input
  use recursive hypothesis or known value
  simplify
```

Example for lists:

[
\operatorname{length}(a :: xs)
= 1 + \operatorname{length}(xs).
]

Then, in a proof:

[
\operatorname{length}(\operatorname{map} f (a :: xs))
= \operatorname{length}(f(a) :: \operatorname{map} f xs)
= 1 + \operatorname{length}(\operatorname{map} f xs)
= 1 + \operatorname{length}(xs)
= \operatorname{length}(a :: xs).
]

This is the structural-induction analogue of an inductive calculation.

---

# 18. Calculation under cases

The calculation splits according to cases, and each case has its own chain.

Schema:

```text
To prove C:
  cases on condition P
  Case P:
    calculation using P
  Case not P:
    calculation using not P
```

Examples:

For absolute value:

[
|x| =
\begin{cases}
x, & x \ge 0, \
-x, & x < 0.
\end{cases}
]

To prove something involving (|x|), split into (x \ge 0) and (x < 0).

Calculation:

Case (x \ge 0):

[
|x| = x.
]

Case (x < 0):

[
|x| = -x.
]

Useful schema:

```json
{
  "type": "cases_calculation",
  "split": "P ∨ ¬P",
  "cases": [
    {
      "assumption": "P",
      "calculation": [...]
    },
    {
      "assumption": "¬P",
      "calculation": [...]
    }
  ]
}
```

---

# 19. Piecewise-function calculation

A special case of calculation under cases.

Suppose:

[
f(x) =
\begin{cases}
g(x), & x \in A, \
h(x), & x \notin A.
\end{cases}
]

Then proofs about (f(x)) often have this structure:

```text
By cases on x ∈ A:
  If x ∈ A, rewrite f x as g x and calculate.
  If x ∉ A, rewrite f x as h x and calculate.
```

This appears in:

* absolute value;
* min/max;
* indicator functions;
* piecewise-defined functions;
* conditional expressions in programming semantics.

---

# 20. Calculation with min/max

These often require case splits or lattice identities.

Examples:

[
\min(a,b) \le a,
\qquad
\min(a,b) \le b,
]

[
a \le \max(a,b),
\qquad
b \le \max(a,b).
]

Schema 1: use universal property.

```text
To prove max a b ≤ c:
  prove a ≤ c and b ≤ c.
```

Schema 2: use case split.

```text
By cases a ≤ b:
  max a b = b
  min a b = a
Otherwise:
  max a b = a
  min a b = b
```

This is very useful for order-theoretic calculational proofs.

---

# 21. Calculation by cancellation

One cancels a common term or factor.

For addition:

[
a+c = b+c \iff a=b.
]

For multiplication:

[
ac = bc,\quad c \ne 0 \implies a=b.
]

For inequalities:

[
a+c \le b+c \iff a \le b.
]

If (c>0):

[
ac \le bc \iff a \le b.
]

If (c<0):

[
ac \le bc \iff b \le a.
]

Schema:

```text
Transform a relation by cancelling a common expression,
checking side conditions if needed.
```

This is a distinct schema because the side conditions matter.

---

# 22. Calculation by division or reciprocals

Frequently used in inequalities and estimates.

Schema:

```text
To divide inequality A ≤ B by c:
  prove 0 < c;
  conclude A / c ≤ B / c.
```

For negative divisor, inequality reverses.

For reciprocals:

[
0 < a \le b \implies \frac1b \le \frac1a.
]

This pattern is common enough to deserve a separate schema because it generates positivity obligations.

---

# 23. Calculation by estimates of individual terms

To bound a compound expression, bound each component separately.

Schema for sums:

[
a_i \le b_i \text{ for all } i
\implies
\sum_i a_i \le \sum_i b_i.
]

Schema for products:

If all terms are nonnegative and

[
a_i \le b_i,
]

then

[
\prod_i a_i \le \prod_i b_i.
]

Example:

[
|x+y+z|
\le |x|+|y|+|z|.
]

Calculation:

[
|x+y+z|
= |(x+y)+z|
\le |x+y|+|z|
\le |x|+|y|+|z|.
]

This is a standard analytic estimate schema.

---

# 24. Triangle-inequality calculation

A particularly important estimate pattern.

Basic form:

[
d(x,z) \le d(x,y)+d(y,z).
]

For norms:

[
|u+v| \le |u|+|v|.
]

For absolute values:

[
|a+b| \le |a|+|b|.
]

Common schema:

```text
Insert and subtract an intermediate term.
Apply triangle inequality.
Estimate resulting pieces.
```

Example:

[
\begin{aligned}
|f(x)-g(x)|
&= |f(x)-h(x)+h(x)-g(x)| \
&\le |f(x)-h(x)| + |h(x)-g(x)|.
\end{aligned}
]

This is one of the central schemas in analysis.

---

# 25. Add-and-subtract calculation

A term is artificially inserted to make the triangle inequality or cancellation usable.

Schema:

[
A-B = (A-C)+(C-B).
]

Then:

[
|A-B|
\le |A-C|+|C-B|.
]

Example:

[
|f_n(x)-f(x)|
\le |f_n(x)-g_n(x)| + |g_n(x)-g(x)| + |g(x)-f(x)|.
]

This is a very common “intermediate object” calculation.

---

# 26. Multiplicative add-and-subtract

For products, insert a mixed term:

[
ab-cd = ab-ad+ad-cd = a(b-d)+d(a-c).
]

or

[
ab-cd = ab-cb+cb-cd = b(a-c)+c(b-d).
]

Schema:

```text
To estimate |ab - cd|:
  insert intermediate term ad or cb.
  factor.
  apply triangle inequality.
```

Example:

[
\begin{aligned}
|ab-cd|
&= |ab-ad+ad-cd| \
&\le |a||b-d| + |d||a-c|.
\end{aligned}
]

This is crucial for proving continuity of multiplication, convergence of products, etc.

---

# 27. Calculation using a lemma as a rewrite rule

Some calculations are chains of named lemma applications.

Schema:

```text
calc
  expression₀
    = expression₁ := by rw [lemma₁]
    = expression₂ := by rw [lemma₂]
    = expression₃ := by rw [lemma₃]
```

Example group calculation:

[
\begin{aligned}
a^{-1}(ab)
&= (a^{-1}a)b \
&= eb \
&= b.
\end{aligned}
]

Justifications:

* associativity;
* inverse law;
* identity law.

This is not merely simplification: it may require choosing the right rewrite direction.

---

# 28. Directional rewrite calculation

A lemma (L : A = B) can be used in either direction.

Schema:

```text
Use L forward:
  A ↦ B

Use L backward:
  B ↦ A
```

Mathematical example:

[
\sin^2 x + \cos^2 x = 1
]

can be used forward to simplify, or backward to introduce a useful decomposition:

[
1 = \sin^2 x + \cos^2 x.
]

Useful schema field:

```json
{
  "type": "rewrite",
  "lemma": "sin_sq_add_cos_sq",
  "direction": "forward"
}
```

or

```json
{
  "type": "rewrite",
  "lemma": "sin_sq_add_cos_sq",
  "direction": "backward"
}
```

Direction is essential for formalization.

---

# 29. Calculation modulo an equivalence relation

Not all calculations are under equality. One may calculate modulo:

* congruence modulo (n);
* isomorphism;
* homotopy;
* almost everywhere equality;
* equivalence of functions;
* logical equivalence.

Examples:

[
a \equiv b \pmod n,
]

[
f \sim g,
]

[
A \simeq B.
]

Schema:

```text
To prove A ~ B:
  chain A ~ A₁ ~ A₂ ~ B
  using transitivity of ~.
```

Example:

[
a^2 \equiv b^2 \pmod n
]

from

[
a \equiv b \pmod n.
]

This is a generalized `calc` chain where the relation is not equality.

---

# 30. Calculation of logical equivalences

Some proofs calculate propositions.

Schema:

[
P
\iff P_1
\iff P_2
\iff Q.
]

Example set membership calculation:

[
\begin{aligned}
x \in A \cap (B \cup C)
&\iff x \in A \land x \in B \cup C \
&\iff x \in A \land (x \in B \lor x \in C) \
&\iff (x \in A \land x \in B) \lor (x \in A \land x \in C) \
&\iff x \in (A \cap B) \cup (A \cap C).
\end{aligned}
]

Then conclude:

[
A \cap (B \cup C) = (A \cap B) \cup (A \cap C).
]

This is a central schema for set-theoretic, order-theoretic, and logical calculations.

---

# 31. Membership calculation

A special logical-equivalence calculation used for set equality.

Schema:

```text
To prove A = B:
  ext x
  calc
    x ∈ A
      ↔ P₁ x := by ...
      ↔ P₂ x := by ...
      ↔ x ∈ B := by ...
```

Mathematical form:

[
x \in A
\iff \cdots
\iff x \in B.
]

Then by extensionality:

[
A = B.
]

Lean-style:

```lean
ext x
constructor
...
```

or more calculationally:

```lean
ext x
simp [Set.mem_inter_iff, Set.mem_union]
```

This is an important schema for formalization because the top-level proof is extensional, and the inner proof is propositional calculation.

---

# 32. Function extensionality plus pointwise calculation

To prove two functions are equal:

[
f = g,
]

prove for arbitrary (x):

[
f(x) = g(x).
]

Schema:

```text
To prove f = g:
  take arbitrary x
  calculate f x = ... = g x
```

Lean-style:

```lean
funext x
calc
  f x = ... := by ...
  _ = g x := by ...
```

Example:

[
(f \circ g)(x) = f(g(x)).
]

Thus:

[
f \circ g = x \mapsto f(g(x)).
]

This schema is ubiquitous.

---

# 33. Relation extensionality calculation

For relations (R,S : X \to X \to Prop), prove equality by pointwise logical equivalence.

Schema:

```text
To prove R = S:
  ext x y
  calc
    R x y ↔ ... ↔ S x y
```

Similarly for predicates:

[
P = Q
]

by proving:

[
\forall x,; P(x) \leftrightarrow Q(x).
]

This is the predicate analogue of function extensionality.

---

# 34. Calculation inside existential witness verification

An existence proof often has a calculational tail.

Schema:

```text
To prove ∃ x, P x:
  choose witness w
  prove P w by calculation
```

Example:

To prove (n^2+n) is even:

[
n^2+n = n(n+1).
]

Since one of (n,n+1) is even, the product is even.

Or more explicitly:

```text
Take k = n(n+1)/2.
Calculate n²+n = 2k.
```

Formal schema:

```json
{
  "type": "exists_by_witness",
  "witness": "w",
  "verification": {
    "type": "calculation",
    "steps": [...]
  }
}
```

---

# 35. Calculation inside uniqueness proof

Uniqueness proofs often use a calculation showing two arbitrary candidates are equal.

Schema:

```text
Suppose x and y both satisfy P.
Calculate:
  x = ... = y.
```

Example for identity element in a monoid:

Suppose (e) and (e') are both identities. Then:

[
e = ee' = e'.
]

More explicitly:

[
e = e e' \quad\text{since } e' \text{ is a right identity},
]

[
e e' = e' \quad\text{since } e \text{ is a left identity}.
]

Schema:

```text
Given P x and P y:
  calc
    x = expression := by use property of y
    _ = y          := by use property of x
```

This is a small but very common calculational pattern.

---

# 36. Calculation inside induction hypothesis rewriting

A common induction step is:

```text
unfold recursive definition
rewrite using induction hypothesis
calculate remaining algebra
```

Schema:

```text
calc
  F(n+1)
    = G(F n)       := by recursive_definition
    = G(H n)       := by rw [induction_hypothesis]
    = H(n+1)       := by algebra
```

Example:

For Fibonacci-like recurrences, list functions, sums, products, recursively defined syntax.

This is worth separating from general induction because the calculational core has a stable shape.

---

# 37. Calculation proving preservation of invariant

Invariant proofs often have a calculational subproof:

```text
To show operation T preserves invariant I:
  calculate I(T x) = I(x).
```

Schema:

[
I(T(x)) = I(x).
]

Example:

If an operation swaps two entries of a list, the sum is invariant:

[
\operatorname{sum}(\operatorname{swap}_{ij}(xs))
================================================

\operatorname{sum}(xs).
]

Proof structure:

```text
For each allowed move:
  calculate invariant after move
  simplify to invariant before move
```

This is central for games, algorithms, algebraic transformations, and formal verification.

---

# 38. Calculation proving compatibility with structure

For homomorphisms, functors, maps, actions, etc., the proof is often a calculation.

Example group homomorphism:

[
f(xy) = f(x)f(y).
]

For a composition of homomorphisms:

[
(g \circ f)(xy)
= g(f(xy))
= g(f(x)f(y))
= g(f(x))g(f(y))
= (g \circ f)(x)(g \circ f)(y).
]

Schema:

```text
To show map preserves operation:
  unfold map/composition
  use preservation property of first structure
  use preservation property of second structure
  fold back definitions
```

This is very common in algebra and category theory.

---

# 39. Diagram chase as calculational proof

A diagram chase often reduces to repeated calculations with commutative squares.

Schema:

Given a commutative square:

[
g \circ f = f' \circ h,
]

calculate:

[
g(f(x)) = f'(h(x)).
]

In a longer diagram:

[
a
\mapsto f(a)
\mapsto g(f(a))
===============

g'(f'(a)).
]

Schema:

```text
Start with an element.
Apply maps.
Use commutativity to replace one path by another.
Use exactness/kernel/image facts.
Continue calculation.
```

A formal schema may have steps like:

```json
{
  "type": "diagrammatic_rewrite",
  "commutative_square": "g ∘ f = f' ∘ h",
  "rewrite": "g (f x) = f' (h x)"
}
```

This is essentially calculational reasoning in a category or algebraic structure.

---

# 40. Calculation by naturality

Naturality proofs are almost always calculations.

Given a natural transformation (\eta : F \Rightarrow G), naturality says:

[
G(f) \circ \eta_X = \eta_Y \circ F(f).
]

A typical proof calculates two composites and shows equality.

Schema:

```text
To prove two morphism composites are equal:
  start from one composite
  use associativity
  use naturality square
  use functoriality
  reach the other composite
```

Example shape:

[
\begin{aligned}
H(f) \circ \alpha_X \circ \beta_X
&= H(f) \circ \alpha_X \circ \beta_X \
&= \alpha_Y \circ G(f) \circ \beta_X \
&= \alpha_Y \circ \beta_Y \circ F(f).
\end{aligned}
]

This is a high-level calculational schema in category theory.

---

# 41. Calculation with side conditions

Many calculations are only valid under side conditions.

Example:

[
\frac{a}{b} + \frac{c}{d}
=========================

\frac{ad+bc}{bd}
]

requires:

[
b \ne 0,\quad d \ne 0.
]

Inequality division requires positivity or negativity.

Logarithm laws require positivity:

[
\log(xy)=\log x+\log y
]

requires:

[
x>0,\quad y>0.
]

Schema:

```text
Main calculation:
  expression₀ = expression₁ = expression₂

Side obligations:
  denominator_nonzero
  positivity
  domain_membership
  differentiability
  measurability
  integrability
```

For formal schemas, this is important:

```json
{
  "type": "calculation_step",
  "from": "log(xy)",
  "to": "log x + log y",
  "justification": "log_mul",
  "side_conditions": ["0 < x", "0 < y"]
}
```

---

# 42. Domain-restricted calculation

A formula is valid only on a domain.

Schema:

```text
For x ∈ D:
  calculate using identities valid on D.
```

Example:

[
\sqrt{x^2} = x
]

is valid if (x \ge 0), but in general:

[
\sqrt{x^2} = |x|.
]

So a proof may need:

```text
Assume x ≥ 0.
Then sqrt(x²) = x.
```

This is common with:

* square roots;
* logarithms;
* division;
* inverse functions;
* branches of complex functions;
* local coordinates;
* charts;
* measurable representatives.

---

# 43. Calculation after changing variables

Common in sums, integrals, limits, and algebra.

Schema:

```text
Make substitution y = φ(x).
Rewrite expression in new variable.
Calculate.
Translate back.
```

Examples:

For sums:

[
\sum_{k=1}^{n} a_{k+1}
======================

\sum_{j=2}^{n+1} a_j.
]

For integrals:

[
\int_a^b f(\phi(x))\phi'(x),dx
==============================

\int_{\phi(a)}^{\phi(b)} f(u),du.
]

For group theory:

[
\sum_{g \in G} f(hg)
====================

\sum_{g \in G} f(g).
]

Useful schema:

```json
{
  "type": "change_of_variables",
  "old_variable": "x",
  "new_variable": "u = φ(x)",
  "transformed_expression": "...",
  "side_conditions": ["φ bijective", "Jacobian condition"]
}
```

---

# 44. Reindexing calculation

A special case of change of variables for sums/products.

Schema:

[
\sum_{i \in I} a_i
==================

\sum_{j \in J} a_{\phi(j)}
]

where (\phi : J \to I) is a bijection.

Example:

[
\sum_{k=0}^{n} a_{n-k}
======================

\sum_{k=0}^{n} a_k.
]

Proof structure:

```text
Define bijection k ↦ n-k.
Use sum_bij or reindexing lemma.
Simplify.
```

This is very common in combinatorics and algebra.

---

# 45. Integral calculation

An integral proof is often a chain combining linearity, monotonicity, substitution, and known integral evaluations.

Schema:

```text
calc
  ∫ x in A, f x + g x
    = ∫ x in A, f x + ∫ x in A, g x := by integral linearity
    ≤ ∫ x in A, h x + ∫ x in A, k x := by monotonicity
    = ... := by known integral computation
```

Common step types:

* linearity;
* monotone convergence;
* dominated convergence;
* Fubini/Tonelli;
* substitution;
* integration by parts;
* evaluation of antiderivative;
* measure-preserving change of variables.

For formal schemas, integral calculation steps often need assumptions:

```text
integrable f
measurable f
ae_strongly_measurable f
finite measure
nonnegative integrand
```

---

# 46. Limit calculation

Limit proofs may be calculational at two levels.

High-level theorem calculation:

[
\lim (a_n+b_n)
==============

# \lim a_n + \lim b_n

A+B.
]

Epsilon-level calculation:

[
|a_n+b_n-(A+B)|
\le |a_n-A|+|b_n-B|
< \varepsilon/2+\varepsilon/2
= \varepsilon.
]

Schema:

```text
To prove limit of expression:
  either use limit laws as calculation;
  or perform epsilon-estimate calculation.
```

Formal schema:

```json
{
  "type": "limit_calculation",
  "method": "epsilon_estimate",
  "target_expression": "|E_n - L|",
  "bound_chain": [...]
}
```

---

# 47. Asymptotic calculation

For (O), (o), (\Theta), (\sim).

Schema:

[
f(n)
= O(g(n))
]

by calculating:

[
|f(n)| \le C |g(n)|
]

eventually.

For asymptotic equivalence:

[
\frac{f(n)}{g(n)} \to 1.
]

Calculation:

[
\frac{f(n)}{g(n)}
=================

1 + \frac{r(n)}{g(n)}
\to 1.
]

Useful schema:

```text
Rewrite expression into main term plus error.
Bound or show error tends to zero.
Conclude asymptotic relation.
```

This is distinct from ordinary limit proofs because the target relation is not equality but asymptotic comparison.

---

# 48. Differentiation calculation

To prove a derivative formula:

[
(fg)' = f'g + fg',
]

one may either use a theorem or calculate from the difference quotient.

Schema from first principles:

[
\frac{f(x+h)g(x+h)-f(x)g(x)}{h}
]

insert and subtract:

[
f(x+h)g(x)
]

then factor:

[
\frac{(f(x+h)-f(x))g(x)}{h}
+
\frac{f(x+h)(g(x+h)-g(x))}{h}.
]

Then pass to the limit.

This follows the multiplicative add-and-subtract schema.

---

# 49. Normalization by computation

In formal proofs, some calculations are simply computation.

Examples:

[
2+3 = 5.
]

[
\operatorname{length}([a,b,c]) = 3.
]

[
\operatorname{map} f [a,b] = [f(a),f(b)].
]

Schema:

```text
Evaluate expression by computation.
```

Lean-style:

```lean
rfl
norm_num
native_decide
decide
simp
```

This is important for schemas involving finite enumeration or executable definitions.

---

# 50. Finite exhaustive calculation

Used when a finite number of cases are computationally checked.

Schema:

```text
For all x in finite set S:
  evaluate expression/property for each x.
```

Example:

To show every square mod (4) is (0) or (1):

[
0^2 \equiv 0,\quad
1^2 \equiv 1,\quad
2^2 \equiv 0,\quad
3^2 \equiv 1
\pmod 4.
]

Formal schema:

```json
{
  "type": "finite_exhaustive_calculation",
  "domain": "Fin 4",
  "cases": [
    {"case": "0", "calculation": "..."},
    {"case": "1", "calculation": "..."},
    {"case": "2", "calculation": "..."},
    {"case": "3", "calculation": "..."}
  ]
}
```

---

# 51. Modular arithmetic calculation

A special calculational structure modulo (n).

Schema:

[
A \equiv A_1 \equiv A_2 \equiv B \pmod n.
]

Example:

[
a \equiv b \pmod n
\implies
a^2 \equiv b^2 \pmod n.
]

Another example:

[
x^2 \equiv 0 \text{ or } 1 \pmod 4.
]

Formal structure:

```json
{
  "type": "modular_calculation",
  "modulus": "n",
  "steps": [
    {"from": "A", "relation": "≡ mod n", "to": "A₁"},
    {"from": "A₁", "relation": "≡ mod n", "to": "B"}
  ]
}
```

This is useful because the ambient transitive relation is congruence, not equality.

---

# 52. Calculation in a quotient

Closely related to modular arithmetic.

Schema:

```text
To prove equality in quotient:
  choose representatives.
  calculate representatives are related.
  conclude quotient classes are equal.
```

Example:

[
[a] + [b] = [a+b].
]

or:

[
[a] = [b]
\quad\text{iff}\quad
a \sim b.
]

This matters in algebraic structures such as quotient groups, quotient rings, quotient spaces.

---

# 53. Matrix/vector calculation

Calculations involving linear algebra often have specialized schemas.

Example:

[
A(Bx) = (AB)x.
]

or inner products:

[
\langle Ax,y\rangle = \langle x,A^*y\rangle.
]

Schema:

```text
Expand definition of matrix multiplication / inner product.
Reindex sums if needed.
Use associativity/distributivity.
Fold back into matrix/vector notation.
```

Typical steps:

* componentwise extensionality;
* sum expansion;
* reindexing;
* linearity;
* associativity of scalar multiplication.

Formal pattern:

```text
ext i
calc
  ((A * B) * x) i
    = ∑ j, (∑ k, A i k * B k j) * x j := by unfold matrix multiplication
    = ...
    = (A * (B * x)) i := by ...
```

---

# 54. Polynomial/ring calculation

A common algebraic schema uses ring normalization.

Schema:

```text
To prove polynomial identity:
  move all terms to one side;
  normalize;
  show the resulting polynomial is zero.
```

Example:

[
(a+b)^2 = a^2 + 2ab + b^2.
]

Formal:

```lean
ring
```

or, for semirings:

```lean
ring_nf
```

Schema representation:

```json
{
  "type": "ring_normalization",
  "goal": "A = B",
  "normalized_difference": "0"
}
```

This is useful as a separate schema because its proof justification is often automation rather than human-step calculation.

---

# 55. Linear arithmetic calculation

For linear inequalities over ordered rings/fields.

Schema:

```text
Collect linear hypotheses.
Derive target by linear combination.
```

Example:

Given:

[
a \le b,\quad c \le d,
]

prove:

[
a+c \le b+d.
]

Or:

[
x \le 3,\quad y \le 5
\implies x+y \le 8.
]

Lean-style:

```lean
linarith
```

Schema:

```json
{
  "type": "linear_arithmetic",
  "hypotheses": ["x ≤ 3", "y ≤ 5"],
  "conclusion": "x + y ≤ 8"
}
```

---

# 56. Nonlinear arithmetic calculation

For polynomial inequalities.

Schema:

```text
Use known nonnegative quantities such as squares.
Combine with algebraic normalization.
```

Example:

[
(x-y)^2 \ge 0
\implies
2xy \le x^2+y^2.
]

Lean-style:

```lean
nlinarith [sq_nonneg (x-y)]
```

Mathematical calculation:

[
0 \le (x-y)^2 = x^2 - 2xy + y^2.
]

Therefore:

[
2xy \le x^2+y^2.
]

This is a distinct schema because the proof depends on nonlinear positivity certificates.

---

# 57. Calculation by “without loss of generality” normalization

Sometimes before calculating one normalizes by symmetry.

Schema:

```text
By symmetry, assume a ≤ b.
Then calculate under this assumption.
```

Example:

For proving:

[
\min(a,b)+\max(a,b)=a+b.
]

Assume (a \le b). Then:

[
\min(a,b)+\max(a,b)=a+b.
]

The other case follows by symmetry or cases.

Formal schema:

```json
{
  "type": "wlog_calculation",
  "normalizing_assumption": "a ≤ b",
  "symmetry": "swap a b",
  "calculation": [...]
}
```

---

# 58. Calculation after choosing coordinates

Common in geometry, topology, manifolds, vector spaces.

Schema:

```text
Choose a convenient coordinate system/basis/chart.
Express objects in coordinates.
Calculate.
Translate coordinate result back invariantly.
```

Examples:

* diagonalize a symmetric matrix;
* choose an orthonormal basis;
* work in a local chart;
* identify a tangent vector with coordinates.

This is a calculational proof with a preliminary reduction.

---

# 59. Calculation after applying an isomorphism

To prove a statement in object (X), transport it to an isomorphic object (Y), calculate there, and transport back.

Schema:

```text
Let φ : X ≅ Y.
It suffices to prove the transported statement in Y.
Calculate in Y.
Pull back the result to X.
```

Example:

For diagonalizable matrices:

[
A = PDP^{-1}.
]

Then:

[
A^n = PD^nP^{-1}.
]

Calculation:

[
A^n
===

# (PDP^{-1})^n

PD^nP^{-1}.
]

This is a common high-level calculational structure.

---

# 60. Calculation with a canonical decomposition

One decomposes an object and calculates componentwise.

Examples:

* real and imaginary parts;
* positive and negative parts of a function;
* symmetric and antisymmetric parts;
* Jordan decomposition;
* primary decomposition;
* basis expansion.

Schema:

```text
Decompose x = x₁ + x₂.
Calculate on each component.
Recombine.
```

Example:

For a linear map:

[
T(x+y)=T(x)+T(y).
]

For projections:

[
x = Px + (I-P)x.
]

Then calculate separately on (Px) and ((I-P)x).

---

# 61. Calculation using universal property

Even universal-property proofs often contain calculations.

Example: to prove a map (h : X \to A \times B) equals another map (h'), it suffices to show:

[
\pi_1 h = \pi_1 h',
\qquad
\pi_2 h = \pi_2 h'.
]

Then each projection equality is calculated.

Schema:

```text
Use universal property to reduce equality of objects/maps
to component equations.
Prove each component equation by calculation.
```

For products:

[
h = \langle f,g\rangle
]

because:

[
\pi_1 h = f,\qquad \pi_2 h = g.
]

---

# 62. Calculation of composites

Common in category theory, algebra, topology, and programming semantics.

Schema:

[
(f \circ g) \circ h
= f \circ (g \circ h)
= \cdots.
]

Examples:

[
\operatorname{id} \circ f = f,
\qquad
f \circ \operatorname{id} = f.
]

Proof structure:

```text
Reassociate composites.
Use identity laws.
Use naturality or commutativity.
Reassociate back.
```

In Lean, this may be:

```lean
simp [Category.assoc]
```

or explicit `calc`.

---

# 63. Calculation of preimages/images

Set calculations involving functions.

Preimage schema:

[
x \in f^{-1}(A \cap B)
\iff f(x) \in A \cap B
\iff f(x) \in A \land f(x) \in B
\iff x \in f^{-1}(A) \land x \in f^{-1}(B)
\iff x \in f^{-1}(A) \cap f^{-1}(B).
]

Thus:

[
f^{-1}(A \cap B)=f^{-1}(A)\cap f^{-1}(B).
]

This combines:

* extensionality;
* membership calculation;
* logical equivalence.

Images often require existential calculations:

[
y \in f(A \cup B)
\iff \exists x,\ x\in A\cup B \land f(x)=y.
]

Then distribute the existential over disjunction.

---

# 64. Calculation with generated objects

Common in algebra and topology.

Examples:

* subgroup generated by (S);
* ideal generated by (S);
* span of a set;
* sigma-algebra generated by a collection.

Schema:

```text
To show generated object ≤ target:
  show generators lie in target.
  use closure properties.
```

The calculation part often verifies closure:

[
a,b \in H \implies ab^{-1}\in H.
]

or:

[
r(\sum a_i s_i) + r'(\sum b_j t_j)
= \sum (ra_i)s_i + \sum(r'b_j)t_j.
]

This is a “closure calculation.”

---

# 65. Calculation showing closure under operations

Schema:

```text
Given x,y ∈ S.
Calculate operation(x,y) has defining property of S.
```

Example: if (S = {x : f(x)=0}) and (f) is linear, then (S) is a subspace:

[
f(x+y)
= f(x)+f(y)
= 0+0
= 0.
]

and

[
f(cx)
= c f(x)
= c0
= 0.
]

This schema is central in algebra.

---

# 66. Calculation for homotopy/equivalence relations

To prove transitivity-like relations, one concatenates/calculates.

Example:

If

[
f \simeq g,\qquad g \simeq h,
]

then

[
f \simeq h
]

by concatenating homotopies.

The calculation might be at parameter endpoints:

[
H(x,0)=f(x),\quad H(x,1)=g(x),
]

[
K(x,0)=g(x),\quad K(x,1)=h(x).
]

Define composite homotopy and calculate boundary values.

Schema:

```text
Define piecewise/interpolated object.
Calculate endpoint/boundary conditions.
Verify continuity/smoothness/compatibility.
```

---

# 67. Calculation with finite products/sums and homomorphisms

A common algebraic schema:

[
\phi\left(\prod_i g_i\right)
============================

\prod_i \phi(g_i).
]

or:

[
T\left(\sum_i v_i\right)
========================

\sum_i T(v_i).
]

Proof may be by induction, but the step is calculational.

Schema:

```text
Use homomorphism property repeatedly.
Use induction over finite list/index set.
Simplify base case using identity/zero preservation.
```

Example:

[
T\left(\sum_{i=1}^n a_i v_i\right)
==================================

\sum_{i=1}^n a_i T(v_i).
]

---

# 68. Calculation with inequalities and epsilons

This deserves its own schema because it is extremely common.

To prove something is (<\varepsilon), split (\varepsilon) into pieces.

Schema:

```text
Given ε > 0:
  choose δ or N so that term₁ < ε/2 and term₂ < ε/2.
  calculate:
    target ≤ term₁ + term₂ < ε/2 + ε/2 = ε.
```

For three terms:

[
\varepsilon/3+\varepsilon/3+\varepsilon/3=\varepsilon.
]

General schema:

[
\text{target}
\le E_1+\cdots+E_k
< \frac{\varepsilon}{k}+\cdots+\frac{\varepsilon}{k}
= \varepsilon.
]

Formal schema:

```json
{
  "type": "epsilon_split_estimate",
  "epsilon": "ε",
  "number_of_terms": 3,
  "target_bound": "ε",
  "terms": ["E₁", "E₂", "E₃"]
}
```

---

# 69. Calculation with constants chosen in advance

Many estimates choose a constant (C), (M), (N), or (\delta), then verify.

Example continuity proof:

Choose:

[
\delta = \min(1,\varepsilon/(2M)).
]

Then calculate:

[
|f(x)g(x)-f(a)g(a)|
\le |f(x)||g(x)-g(a)| + |g(a)||f(x)-f(a)|
< \varepsilon.
]

Schema:

```text
Choose control constants.
Prove side bounds from the choice.
Use them in final calculation.
```

This is not just a calculation chain; it includes a “parameter choice” stage.

---

# 70. Calculation with boundedness assumptions

Common in analysis.

Schema:

```text
Given |f(x)| ≤ M and |g(x)| ≤ N.
Estimate compound expression using M,N.
```

Example:

[
|f(x)g(x)|
==========

|f(x)||g(x)|
\le MN.
]

For differences:

[
|f_ng_n - fg|
\le |f_n||g_n-g| + |g||f_n-f|.
]

Then use boundedness to obtain:

[
\le M|g_n-g| + N|f_n-f|.
]

This is a standard estimate schema.

---

# 71. Calculation with coercions/casts

In formal mathematics, especially Lean, calculations often involve coercions:

[
(n : \mathbb R) + 1 = (n+1 : \mathbb R).
]

Schema:

```text
Move between Nat, Int, Rat, Real, etc.
Normalize casts.
Then perform algebra.
```

Lean-style:

```lean
norm_num
norm_cast
exact_mod_cast h
```

Formal schema:

```json
{
  "type": "cast_normalization",
  "source_type": "ℕ",
  "target_type": "ℝ",
  "expression": "((n + 1 : ℕ) : ℝ)",
  "normalized": "(n : ℝ) + 1"
}
```

This is crucial for autoformalization because many natural-language calculations silently ignore coercions.

---

# 72. Calculation by transporting across equality of types or structures

In dependent type theory, one sometimes calculates after transport.

Schema:

```text
Given h : A = B.
Transport object/proof from A to B.
Calculate after rewriting h.
```

Mathematically this corresponds to “identifying” two equal structures, but formally it may require rewriting.

Examples:

* substituting equal indices;
* vector lengths;
* dependent functions;
* fiberwise constructions.

This is especially relevant for Lean schemas.

---

# 73. Calculation with simplification lemmas

A proof may not be an explicit chain, but a directed simplification process.

Schema:

```text
Use a set of simplification lemmas to rewrite expression to normal form.
```

Example:

[
x + 0 + (0 + y) = x+y.
]

Simplification rules:

[
x+0 \to x,
\quad
0+x \to x.
]

Lean:

```lean
simp
```

With definitions:

```lean
simp [foo, bar]
```

Useful schema:

```json
{
  "type": "simplification",
  "simp_lemmas": ["foo_def", "bar_def", "zero_add", "add_zero"],
  "target_normal_form": "x + y"
}
```

---

# 74. Calculation with normalization plus side lemma

Common in formal proofs:

```text
First normalize algebraically.
Then use a non-algebraic lemma.
Then normalize again.
```

Example:

[
|x-y|
= |-(y-x)|
= |y-x|.
]

Uses:

[
|{-z}|=|z|.
]

Schema:

```text
ring normalization → rewrite by analytic/order lemma → ring normalization
```

This is a frequent hybrid pattern.

---

# 75. Calculation producing contradiction

A contradiction proof may end with a calculation such as:

[
0 < 0
]

or

[
1 = 0
]

or

[
n < n.
]

Schema:

```text
Assume bad hypothesis.
Calculate impossible relation.
Contradict irreflexivity/nonzero fact.
```

Example:

Suppose (a<b) and (b<a). Then:

[
a < b < a,
]

so:

[
a<a,
]

contradiction.

Another:

[
1 = 0
]

contradicts (1 \ne 0).

Formal schema:

```json
{
  "type": "contradiction_by_calculation",
  "assumption": "H",
  "calculation_result": "False relation",
  "contradiction_rule": "lt_irrefl / zero_ne_one / no_confusion"
}
```

---

# A useful top-level schema hierarchy

For designing proof schemas, I would separate calculational proofs into the following major families.

```text
CalculationalProof
├── ChainCalculation
│   ├── EqualityChain
│   ├── InequalityChain
│   ├── MixedRelationChain
│   ├── EquivalenceChain
│   └── Modular/Quotient/SetoidChain
│
├── NormalizationCalculation
│   ├── RingNormalization
│   ├── LinearArithmetic
│   ├── NonlinearArithmetic
│   ├── Simplification
│   ├── CastNormalization
│   └── DefinitionalReduction
│
├── EstimateCalculation
│   ├── TriangleInequalityEstimate
│   ├── AddSubtractIntermediate
│   ├── ProductDifferenceEstimate
│   ├── EpsilonSplitEstimate
│   ├── TermwiseEstimate
│   └── BoundednessEstimate
│
├── ExtensionalCalculation
│   ├── SetExtensionalityMembershipCalc
│   ├── FunctionExtensionalityPointwiseCalc
│   ├── RelationExtensionalityCalc
│   └── ComponentwiseCalc
│
├── RecursiveCalculation
│   ├── InductiveStepCalculation
│   ├── StructuralRecursiveUnfolding
│   ├── TelescopingSum
│   └── FiniteExhaustiveCalculation
│
├── CasewiseCalculation
│   ├── AbsoluteValueCases
│   ├── MinMaxCases
│   ├── PiecewiseFunctionCases
│   └── DomainRestrictedCases
│
├── TransformationCalculation
│   ├── ChangeOfVariables
│   ├── Reindexing
│   ├── CoordinateChoice
│   ├── TransportAcrossIsomorphism
│   └── UniversalPropertyReduction
│
└── VerificationCalculation
    ├── WitnessVerification
    ├── UniquenessCalculation
    ├── InvariantPreservation
    ├── ClosureVerification
    ├── HomomorphismCompatibility
    └── ContradictionByCalculation
```

---

# A possible JSON-like schema for calculation chains

For autoformalization, a general chain schema could look like this:

```json
{
  "type": "calculation_chain",
  "start": "A",
  "target": "B",
  "goal_relation": "=",
  "steps": [
    {
      "from": "A",
      "relation": "=",
      "to": "A₁",
      "justification": {
        "type": "rewrite",
        "lemma": "lemma_name",
        "direction": "forward"
      },
      "side_conditions": []
    },
    {
      "from": "A₁",
      "relation": "≤",
      "to": "A₂",
      "justification": {
        "type": "known_inequality",
        "lemma": "triangle_inequality"
      },
      "side_conditions": ["..."]
    },
    {
      "from": "A₂",
      "relation": "=",
      "to": "B",
      "justification": {
        "type": "normalization",
        "method": "ring"
      },
      "side_conditions": []
    }
  ]
}
```

Then specialized schemas can elaborate the `justification` field.

---

# A useful smaller set of core schemas

For practical purposes, I would start with perhaps these 15:

1. `equality_chain`
2. `inequality_chain`
3. `mixed_relation_chain`
4. `rewrite_by_hypothesis`
5. `rewrite_by_lemma`
6. `definition_unfolding`
7. `normalization`
8. `positivity_side_goal`
9. `monotonicity_step`
10. `triangle_inequality_estimate`
11. `add_subtract_intermediate`
12. `casewise_calculation`
13. `inductive_step_calculation`
14. `extensionality_then_pointwise_calculation`
15. `calculation_to_contradiction`

These cover a surprisingly large fraction of ordinary mathematical calculational proofs.
