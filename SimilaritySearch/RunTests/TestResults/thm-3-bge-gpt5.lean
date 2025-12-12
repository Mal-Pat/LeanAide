import Mathlib

universe u v w u_1 u_2 u_3 u₁ u₂ u₃

open Nat

/-
  Translation of 40 statements from `data/thm-prompts.txt`
  Using similarity search

  SUMMARY:

  Time:
  · Total time to translate 40 statements = 1237.58 s
  · Avg time to translate one statement = 30.94 s

  Results:
  · Success = 39
    · Without error =
    · With error =
  · Fallback = 1
-/

--Result: success
--Time: 35.79 s
/--If every proper closed subset of a topological space is compact, then the space itself is compact.-/
theorem t1 : ∀ {X : Type u} [inst : TopologicalSpace X], (∀ (s : Set X), IsClosed s → s ≠ Set.univ → IsCompact s) → CompactSpace X :=
  by sorry

--Result: success
--Time: 25.68 s
/--Every prime that is `1` greater than a multiple of `4` can be expressed as the sum of two squares.-/
theorem t2 : ∀ {p : ℕ}, Nat.Prime p → p % 4 = 1 → ∃ a b, p = a ^ 2 + b ^ 2 :=
  by sorry

--Result: success
--Time: 35.65 s
/--The product of two numbers, each of which is the sum of four squares, is itself a sum of four squares.-/
theorem t3 : ∀ {a b a1 a2 a3 a4 b1 b2 b3 b4 : ℕ},
  a = a1 ^ 2 + a2 ^ 2 + a3 ^ 2 + a4 ^ 2 →
    b = b1 ^ 2 + b2 ^ 2 + b3 ^ 2 + b4 ^ 2 → ∃ c1 c2 c3 c4, a * b = c1 ^ 2 + c2 ^ 2 + c3 ^ 2 + c4 ^ 2 :=
  by sorry

--Result: success
--Time: 41.35 s
/--A ring with all elements idempotent is commutative.-/
theorem t4 : {R : Type u_1} → [inst : Ring R] → (∀ (a : R), IsIdempotentElem a) → CommRing R :=
  by sorry

--Result: success
--Time: 34.89 s
/--There are infinitely many pairs of primes that differ exactly by `2`.-/
theorem t5 : {p | Nat.Prime p ∧ Nat.Prime (p + 2)}.Infinite :=
  by sorry

--Result: success
--Time: 14.96 s
/--Every finite division ring is a field.-/
theorem t6 : (D : Type u_1) → [DivisionRing D] → [Finite D] → Field D :=
  by sorry

--Result: success
--Time: 22.50 s
/--If each of two types can be mapped injectively into the other, then there is a bijection between them.-/
theorem t7 : ∀ {α : Type u} {β : Type v} (a : α ↪ β) (a : β ↪ α), Nonempty (α ≃ β) :=
  by sorry

--Result: success
--Time: 86.44 s
/--A finite graph in which every pair of vertices have precisely one common neighbour contains a vertex that is adjacent to all other vertices.-/
theorem t8 : ∀ {V : Type u} {G : SimpleGraph V} [Finite V] [Nonempty V],
  (∀ (u w : V), u ≠ w → ∃! x, G.Adj u x ∧ G.Adj w x) → ∃ v, ∀ (w : V), w ≠ v → G.Adj v w :=
  by sorry

--Result: success
--Time: 75.59 s
/--The number of partitions with odd parts is equal to the number of partitions with distinct parts.-/
theorem t9 : ∀ (n : ℕ), Fintype.card { p // ∀ a ∈ p.parts, Odd a } = Fintype.card { p // p.parts.Nodup } :=
  by sorry

--Result: success
--Time: 50.36 s
/--Every non-empty poset in which every chain has an upper bound contains a maximal element.-/
theorem t10 : ∀ {α : Type u_1} [inst : PartialOrder α] [Nonempty α],
  (∀ (c : Set α), IsChain (fun x1 x2 => x1 ≤ x2) c → ∃ ub, ∀ a ∈ c, a ≤ ub) → ∃ m, ∀ (a : α), m ≤ a → a ≤ m :=
  by sorry

--Result: success
--Time: 50.66 s
/--A group whose automorphism group is cyclic is Abelian.-/
theorem t11 : {G : Type u_1} → [inst : Group G] → [IsCyclic (MulAut G)] → CommGroup G :=
  by sorry

--Result: success
--Time: 33.04 s
/--A uniformly continuous function of a uniformly continuous function is uniformly continuous.-/
theorem t12 : ∀ {α : Type u_1} {β : Type u_2} {γ : Type u_3} [inst : UniformSpace α] [inst_1 : UniformSpace β]
  [inst_2 : UniformSpace γ] {f : α → β} {g : β → γ},
  UniformContinuous f → UniformContinuous g → UniformContinuous (g ∘ f) :=
  by sorry

--Result: success
--Time: 0.04 s
/--A uniformly continuous function of a uniformly continuous function is uniformly continuous.-/
theorem t13 : ∀ {α : Type u_1} {β : Type u_2} {γ : Type u_3} [inst : UniformSpace α] [inst_1 : UniformSpace β]
  [inst_2 : UniformSpace γ] {f : α → β} {g : β → γ},
  UniformContinuous f → UniformContinuous g → UniformContinuous (g ∘ f) :=
  by sorry

--Result: success
--Time: 39.89 s
/--A topological space is normal if and only if any two disjoint closed subsets can be separated by a continuous function.-/
theorem t14 : ∀ {X : Type u_1} [inst : TopologicalSpace X],
  NormalSpace X ↔ ∀ {s t : Set X}, IsClosed s → IsClosed t → Disjoint s t → ∃ f, Set.EqOn (⇑f) 0 s ∧ Set.EqOn (⇑f) 1 t :=
  by sorry

--Result: success
--Time: 74.67 s
/--If a function from the unit interval to itself has a point of period three, then it has points of all positive periods.-/
theorem t15 : ∀ (f : ↑(Set.Icc 0 1) → ↑(Set.Icc 0 1)),
  (∃ x, Function.IsPeriodicPt f 3 x) → ∀ (n : ℕ), 0 < n → ∃ y, Function.IsPeriodicPt f n y :=
  by sorry

--Result: fallback
--Time: 53.82 s
/--A terminal object in a category is unique up to unique isomorphism.-/
theorem t16 : ∀ {C : Type u₁} [inst : CategoryTheory.Category.{v₁, u₁} C] {X Y : C} (hX : CategoryTheory.Limits.IsTerminal X)
  (hY : CategoryTheory.Limits.IsTerminal Y), Unique (X ≅ Y) :=
  by sorry

--Result: success
--Time: 7.28 s
/--The complement of the union of two sets is the intersection of their complements.-/
theorem t17 : ∀ {α : Type u_1} (s t : Set α), (s ∪ t)ᶜ = sᶜ ∩ tᶜ :=
  by sorry

--Result: success
--Time: 19.61 s
/--The sum of the cubes of two positive integers is never equal to the cube of a third integer.-/
theorem t18 : ∀ (a b c : ℕ+), ↑a ^ 3 + ↑b ^ 3 ≠ ↑c ^ 3 :=
  by sorry

--Result: success
--Time: 25.35 s
/--If every element of a group `G` has order `2`, then every pair of elements of `G` commutes.-/
theorem t19 : ∀ {G : Type u_1} [inst : Group G], (∀ (x : G), x ^ 2 = 1) → ∀ (x y : G), Commute x y :=
  by sorry

--Result: success
--Time: 13.53 s
/--The product of two consecutive natural numbers is even.-/
theorem t20 : ∀ {n : ℕ}, Even (n * (n + 1)) :=
  by sorry

--Result: success
--Time: 11.09 s
/--Every index 2 subgroup of a group is normal.-/
theorem t21 : ∀ {G : Type u_1} [inst : Group G] {H : Subgroup G}, H.index = 2 → H.Normal :=
  by sorry

--Result: success
--Time: 15.47 s
/--Every free group is torsion free.-/
theorem t22 : ∀ {G : Type u_1} [inst : Group G] [inst_1 : IsFreeGroup G], Monoid.IsTorsionFree G :=
  by sorry

--Result: success
--Time: 12.50 s
/--Every natural number greater than `1` is divisible by a prime number.-/
theorem t23 : ∀ {n : ℕ}, 1 < n → ∃ p, Nat.Prime p ∧ p ∣ n :=
  by sorry

--Result: success
--Time: 27.66 s
/--A finite torsion-free group is trivial-/
theorem t24 : ∀ {G : Type u_1} [inst : Group G] [Finite G], Monoid.IsTorsionFree G → Subsingleton G :=
  by sorry

--Result: success
--Time: 0.03 s
/--Every finite division ring is a field.-/
theorem t25 : (D : Type u_1) → [DivisionRing D] → [Finite D] → Field D :=
  by sorry

--Result: success
--Time: 8.35 s
/--Every finite topological space is compact.-/
theorem t26 : ∀ {X : Type u} [inst : TopologicalSpace X] [Finite X], CompactSpace X :=
  by sorry

--Result: success
--Time: 26.17 s
/--Every surjective homomorphism from a finitely generated free group to itself is injective.-/
theorem t27 : ∀ {G : Type u_1} [inst : Group G] [inst_1 : IsFreeGroup G] [Finite (IsFreeGroup.Generators G)] (f : G →* G),
  Function.Surjective ⇑f → Function.Injective ⇑f :=
  by sorry

--Result: success
--Time: 38.58 s
/--Every positive even integer greater than $4$ can be written as the sum of two primes.-/
theorem t28 : ∀ (n : ℕ), 4 < n → Even n → ∃ p q, Nat.Prime p ∧ Nat.Prime q ∧ n = p + q :=
  by sorry

--Result: success
--Time: 13.68 s
/--Every matrix satisfies its own characteristic polynomial.-/
theorem t29 : ∀ {R : Type u_1} [inst : CommRing R] {n : Type u_4} [inst_1 : DecidableEq n] [inst_2 : Fintype n] (M : Matrix n n R),
  (Polynomial.aeval M) M.charpoly = 0 :=
  by sorry

--Result: success
--Time: 21.09 s
/--The square root of an irrational number is irrational.-/
theorem t30 : ∀ {x : ℝ}, 0 ≤ x → Irrational x → Irrational √x :=
  by sorry

--Result: success
--Time: 27.94 s
/--If the square of a number is even, the number itself is even.-/
theorem t31 : ∀ {n : ℤ}, Even (n ^ 2) → Even n :=
  by sorry

--Result: success
--Time: 17.78 s
/--In a finite commutative ring, all prime ideals are maximal.-/
theorem t32 : ∀ {R : Type u_1} [inst : CommRing R] [inst_1 : Finite R] {I : Ideal R}, I.IsPrime → I.IsMaximal :=
  by sorry

--Result: success
--Time: 14.04 s
/--A topological space $X$ is Hausdorff if and only if the diagonal is a closed set in $X × X$.-/
theorem t33 : ∀ {X : Type u_1} [inst : TopologicalSpace X], T2Space X ↔ IsClosed (Set.diagonal X) :=
  by sorry

--Result: success
--Time: 12.36 s
/--If every point of a subset of a topological space is contained in some open set, the subset itself is open.-/
theorem t34 : ∀ {X : Type u} [inst : TopologicalSpace X] {s : Set X}, (∀ x ∈ s, ∃ t ⊆ s, IsOpen t ∧ x ∈ t) → IsOpen s :=
  by sorry

--Result: success
--Time: 28.62 s
/--Every non-identity element of a free group is of infinite order.-/
theorem t35 : ∀ {G : Type u_1} [inst : Group G] [inst_1 : IsFreeGroup G] {g : G}, g ≠ 1 → ¬IsOfFinOrder g :=
  by sorry

--Result: success
--Time: 102.85 s
/--An element of a discrete valuation ring is a unit if and only if it has a valuation of zero.-/
theorem t36 : ∀ {R : Type u} {K : Type v} [inst : CommRing R] [inst_1 : IsDomain R] [IsDiscreteValuationRing R] [inst_2 : Field K]
  [inst_3 : Algebra R K] [IsFractionRing R K] {v : AddValuation K (WithTop ℤ)},
  Valuation.Integers v R → ∀ {x : R}, v ((algebraMap R K) x) = 0 ↔ IsUnit x :=
  by sorry

--Result: success
--Time: 28.43 s
/--For any two relatively prime positive integers $a$ and $b$, every sufficiently large natural number $N$ can be written as a linear combination $ax + by$ of $a$ and $b$, where both $x$ and $y$ are natural numbers.-/
theorem t37 : ∀ {a b : ℕ}, a.Coprime b → 0 < a → 0 < b → ∃ N0, ∀ (N : ℕ), N0 ≤ N → ∃ x y, N = a * x + b * y :=
  by sorry

--Result: success
--Time: 44.60 s
/--Every field is a ring.-/
theorem t38 : (K : Type u) → [inst : Field K] → Ring K :=
  by sorry

--Result: success
--Time: 19.62 s
/--The set of units in a ring forms a group.-/
theorem t39 : {α : Type u} → [inst : Ring α] → Group αˣ :=
  by sorry

--Result: success
--Time: 25.60 s
/--If the direct product of two groups is torsion free then each of the groups is torsion free.-/
theorem t40 : ∀ {G : Type u_1} {H : Type u_2} [inst : Group G] [inst_1 : Group H],
  Monoid.IsTorsionFree (G × H) → Monoid.IsTorsionFree G ∧ Monoid.IsTorsionFree H :=
  by sorry
