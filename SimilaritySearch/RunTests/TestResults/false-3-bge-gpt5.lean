import Mathlib

universe u v w u_1 u_2 u_3 u₁ u₂ u₃

open Nat

/-
  Translation of 40 statements from `data/false-prompts.txt`
  Using similarity search

  SUMMARY:

  Time:
  · Total time to translate 40 statements = 1553.18 s
  · Avg time to translate one statement = 38.83 s

  Results:
  · Success = 38
    · Without error =
    · With error =
  · Fallback = 2
-/

--Result: success
--Time: 27.84 s
/--Every ring is a field.-/
theorem t1 : ∀ (R : Type u) [inst : Ring R], IsField R :=
  by sorry

--Result: success
--Time: 16.39 s
/--Every vector space is finite dimensional.-/
theorem t2 : ∀ {K : Type u} {V : Type v} [inst : DivisionRing K] [inst_1 : AddCommGroup V] [inst_2 : Module K V],
  FiniteDimensional K V :=
  by sorry

--Result: success
--Time: 17.32 s
/--Every group is a torsion monoid.-/
theorem t3 : ∀ {G : Type u_1} [inst : Group G], Monoid.IsTorsion G :=
  by sorry

--Result: success
--Time: 23.17 s
/--Every finite simple group has prime order.-/
theorem t4 : ∀ {G : Type u_1} [inst : Group G] [Finite G], IsSimpleGroup G → Nat.Prime (Nat.card G) :=
  by sorry

--Result: success
--Time: 14.80 s
/--Every finite group is simple.-/
theorem t5 : ∀ {G : Type u_1} [inst : Group G] [Finite G], IsSimpleGroup G :=
  by sorry

--Result: success
--Time: 17.30 s
/--Every finite group has prime order.-/
theorem t6 : ∀ {G : Type u_1} [inst : Group G] [Finite G], Nat.Prime (Nat.card G) :=
  by sorry

--Result: success
--Time: 16.68 s
/--Every set has Lebesgue measure zero.-/
theorem t7 : ∀ (s : Set ℝ), MeasureTheory.volume s = 0 :=
  by sorry

--Result: success
--Time: 28.20 s
/--If a topological space is compact, then every subset is compact.-/
theorem t8 : ∀ {X : Type u} [inst : TopologicalSpace X] [CompactSpace X] (s : Set X), IsCompact s :=
  by sorry

--Result: success
--Time: 63.47 s
/--Every set that is Lebesgue measurable but not Borel measurable has Lebesgue measure zero.-/
theorem t9 : ∀ (s : Set ℝ), MeasureTheory.volume s = 0 :=
  by sorry

--Result: fallback
--Time: 33.58 s
/--A finitely-presented group containing a torsion element is finite.-/
theorem t10 : ∀ {G : Type u_1} [inst : Group G], Group.FP G → (∃ g : G, g ≠ 1 ∧ IsOfFinOrder g) → Finite G :=
  by sorry

--Result: success
--Time: 54.47 s
/--If every point of a subset of a topological space is contained in some closed set, the subset itself is closed.-/
theorem t11 : ∀ {X : Type u} [inst : TopologicalSpace X] {s : Set X}, (∀ x ∈ s, ∃ C, IsClosed C ∧ x ∈ C) → IsClosed s :=
  by sorry

--Result: success
--Time: 40.26 s
/--A topological space $X$ is Hausdorff if and only if the diagonal map is an open map from $X$ to $X × X$.-/
theorem t12 : ∀ {X : Type u_1} [inst : TopologicalSpace X], T2Space X ↔ IsOpenMap fun x => (x, x) :=
  by sorry

--Result: success
--Time: 20.68 s
/--Any finite order element in a group is equal to the identity.-/
theorem t13 : ∀ {G : Type u_1} [inst : Group G] {x : G}, IsOfFinOrder x → x = 1 :=
  by sorry

--Result: success
--Time: 24.60 s
/--If a subgroup of a group is torsion-free, then the group itself is torsion free.-/
theorem t14 : ∀ {G : Type u_1} [inst : Group G] (H : Subgroup G), Monoid.IsTorsionFree ↥H → Monoid.IsTorsionFree G :=
  by sorry

--Result: success
--Time: 57.24 s
/--Every injective homomorphism from a finitely generated free group to itself is surjective.-/
theorem t15 : ∀ {G : Type u_1} [inst : Group G] [inst_1 : IsFreeGroup G] [inst_2 : Fintype (IsFreeGroup.Generators G)] (f : G →* G),
  Function.Injective ⇑f → Function.Surjective ⇑f :=
  by sorry

--Result: success
--Time: 63.70 s
/--Every division ring is either a field or finite.-/
theorem t16 : ∀ (D : Type u) [inst : DivisionRing D], IsField D ∨ Finite D :=
  by sorry

--Result: success
--Time: 16.08 s
/--Every natural number is the product of two primes.-/
theorem t17 : ∀ (n : ℕ), ∃ p q, Nat.Prime p ∧ Nat.Prime q ∧ n = p * q :=
  by sorry

--Result: success
--Time: 18.24 s
/--Every even number is the square of a natural number.-/
theorem t18 : ∀ (n : ℕ), Even n → ∃ m, n = m ^ 2 :=
  by sorry

--Result: success
--Time: 32.68 s
/--Every normal subgroup of a group has finite index.-/
theorem t19 : ∀ {G : Type u_1} [inst : Group G] {H : Subgroup G}, H.Normal → H.FiniteIndex :=
  by sorry

--Result: success
--Time: 48.57 s
/--The characteristic polynomial of every matrix has real roots.-/
theorem t20 : ∀ {n : Type u_1} [inst_1 : DecidableEq n] [inst_2 : Fintype n] (M : Matrix n n ℝ), ∃ r, M.charpoly.IsRoot r :=
  by sorry

--Result: success
--Time: 28.71 s
/--In a commutative ring, every prime ideal is contained in a unique maximal ideal.-/
theorem t21 : ∀ {R : Type u_1} [inst : CommRing R] (P : Ideal R), P.IsPrime → ∃! M, M.IsMaximal ∧ P ≤ M :=
  by sorry

--Result: fallback
--Time: 29.28 s
/--Every continuous function is uniformly continuous.-/
theorem t22 : ∀ {α : Type ua} {β : Type ub} [inst : UniformSpace α] [inst_1 : UniformSpace β] {f : α → β},
  Continuous f → UniformContinuous f :=
  by sorry

--Result: success
--Time: 45.71 s
/--Every uniformly continuous function is bounded above.-/
theorem t23 : ∀ {α : Type u} {β : Type v} [inst : UniformSpace α] [inst_1 : UniformSpace β] [inst_2 : Preorder β] (f : α → β),
  UniformContinuous f → BddAbove (Set.range f) :=
  by sorry

--Result: success
--Time: 37.50 s
/--If every compact subset of a topological space is closed, then the space is compact.-/
theorem t24 : ∀ {X : Type u} [inst : TopologicalSpace X], (∀ (s : Set X), IsCompact s → IsClosed s) → CompactSpace X :=
  by sorry

--Result: success
--Time: 39.96 s
/--In a commutative ring, the sum of idempotent elements is idempotent.-/
theorem t25 : ∀ {R : Type u_1} [inst : CommRing R] {ι : Type u_2} {t : Finset ι} {f : ι → R},
  (∀ i ∈ t, IsIdempotentElem (f i)) → IsIdempotentElem (∑ i ∈ t, f i) :=
  by sorry

--Result: success
--Time: 58.41 s
/--The number of partitions of a finite set is a prime number.-/
theorem t26 : ∀ {α : Type u_1} [inst : DecidableEq α] (s : Finset α), Nat.Prime (Fintype.card (Finpartition s)) :=
  by sorry

--Result: success
--Time: 43.66 s
/--If a poset has a maximal element, then it has a unique minimal element.-/
theorem t27 : ∀ {α : Type u_1} [inst : PartialOrder α], (∃ a, Maximal (fun x => True) a) → ∃! b, Minimal (fun x => True) b :=
  by sorry

--Result: success
--Time: 40.28 s
/--The automorphism group of an Abelian group is cyclic.-/
theorem t28 : ∀ (G : Type u_1) [inst : CommGroup G], IsCyclic (MulAut G) :=
  by sorry

--Result: success
--Time: 88.46 s
/--If a function from the unit interval to itself has a fixed point, then it has points of all positive periods.-/
theorem t29 : ∀ {f : ↑(Set.Icc 0 1) → ↑(Set.Icc 0 1)},
  (∃ x, Function.IsFixedPt f x) → ∀ (n : ℕ), 0 < n → ∃ x, Function.IsPeriodicPt f n x :=
  by sorry

--Result: success
--Time: 37.08 s
/--The complement of the union of two sets contains the union of their complements.-/
theorem t30 : ∀ {α : Type u_1} (s t : Set α), (s ∪ t)ᶜ ⊇ sᶜ ∪ tᶜ :=
  by sorry

--Result: success
--Time: 45.86 s
/--The square root of an rational number is rational.-/
theorem t31 : ∀ {q : ℚ}, ∃ r, √↑q = ↑r :=
  by sorry

--Result: success
--Time: 88.47 s
/--If a module over a ring is free, then the ring is commutative.-/
theorem t32 : {R : Type u} →
  {M : Type v} → [inst : Ring R] → [inst_1 : AddCommMonoid M] → [inst_2 : Module R M] → Module.Free R M → CommRing R :=
  by sorry

--Result: success
--Time: 99.83 s
/--If the set of units of a ring forms a group then the ring is commutative.-/
theorem t33 : {R : Type u_1} → [inst : Ring R] → Group Rˣ → CommRing R :=
  by sorry

--Result: success
--Time: 37.34 s
/--Every natural number larger than `10` is the sum of a square and a prime.-/
theorem t34 : ∀ {n : ℕ}, 10 < n → ∃ a p, Nat.Prime p ∧ n = a ^ 2 + p :=
  by sorry

--Result: success
--Time: 78.58 s
/--The initial object of a category is isomorphic to its terminal object.-/
theorem t35 : {C : Type u} →
  [inst : CategoryTheory.Category.{v, u} C] → [inst_1 : CategoryTheory.Limits.HasZeroObject C] → ⊥_ C ≅ ⊤_ C :=
  by sorry

--Result: success
--Time: 27.89 s
/--If the composition of two functions is continuous, then each of them is continuous.-/
theorem t36 : ∀ {X : Type u_1} {Y : Type u_2} {Z : Type u_3} [inst : TopologicalSpace X] [inst_1 : TopologicalSpace Y]
  [inst_2 : TopologicalSpace Z] {f : X → Y} {g : Y → Z}, Continuous (g ∘ f) → Continuous f ∧ Continuous g :=
  by sorry

--Result: success
--Time: 21.10 s
/--If `a` commutes with `b` and `b` commutes with `c` then `a` commutes with `c`.-/
theorem t37 : ∀ {S : Type u_3} [inst : Mul S] {a b c : S}, Commute a b → Commute b c → Commute a c :=
  by sorry

--Result: success
--Time: 30.36 s
/--If an element maps to zero under a ring homomorphism, then it is zero.-/
theorem t38 : ∀ {R : Type u} {S : Type v} [inst : Semiring R] [inst_1 : Semiring S] (f : R →+* S),
  Function.Injective ⇑f → ∀ {x : R}, f x = 0 → x = 0 :=
  by sorry

--Result: success
--Time: 19.78 s
/--Implication `→` is symmetric. If `P → Q` then `Q → P`.-/
theorem t39 : ∀ {p q : Prop}, (p → q) → q → p :=
  by sorry

--Result: success
--Time: 19.64 s
/--Two natural numbers are equal if and only if they are both divisible by some prime number.-/
theorem t40 : ∀ {m n : ℕ}, (∃ p, Nat.Prime p ∧ p ∣ m ∧ p ∣ n) ↔ m = n :=
  by sorry
