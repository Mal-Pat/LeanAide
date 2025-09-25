# FAISS vs Nearest Embeddings

## Theorem 1
If a sequence of real numbers is monotone and bounded, then the sequence converges.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|A sequence converges if every subsequence has a convergent subsequence.|If `A` is subterminal, the unique morphism from it to a terminal object is a monomorphism. The converse of `isSubterminal_of_mono_isTerminal_from`.|
|2|Monotone convergence theorem expressed with limits|`assert_exists n` is a user command that asserts that a declaration named `n` exists in the current import scope.  Be careful to use names (e.g. `Rat`) rather than notations (e.g. `ℚ`).|
|3|A Cauchy sequence on the natural numbers is bounded.|(Implementation detail). The function underlying `(A ⊗[R] Matrix n n R) →ₐ[R] Matrix n n A`, as an `R`-linear map.|
|4|The limit of a bounded-below subadditive sequence. The fact that the sequence indeed tends to this limit is given in `Subadditive.tendsto_lim`|Given a submodule, corestrict to the pairing on `M ⧸ W` by simultaneously restricting to `W.dualAnnihilator`.  See `Subspace.dualCopairing_nondegenerate`.|
|5|If a Cauchy sequence has a convergent subsequence, then it converges.|See `rank_subsingleton` for the reason that `Nontrivial R` is needed. Also see `rank_eq_zero_iff` for the version without `NoZeroSMulDivisor R M`.|
|6|Shows that the sequence of denominators is monotone, that is `Bₙ ≤ Bₙ₊₁`.|`a <\|> b` executes `a` and returns the result, unless it fails in which case it executes and returns `b`. Because `b` is not always executed, it is passed as a thunk so it can be forced only when needed. The meaning of this notation is type-dependent.|
|7|Assume that, for any `a < b`, a sequence can not be infinitely many times below `a` and above `b`. If it is also ultimately bounded above and below, then it has to converge. This even works if `a` and `b` are restricted to a dense subset.|`G.CliqueFree n` means that `G` has no `n`-cliques.|
|8|**Dirichlet's Test** for monotone sequences.|The rank of a module as a natural number.  Defined by convention to be `0` if the space has infinite rank.  For a vector space `M` over a field `R`, this is the same as the finite dimension of `M` over `R`.|
|9|A version of Bolzano-Weistrass: in a proper metric space (eg. $ℝ^n$), every bounded sequence has a converging subsequence.|At `-n` for `n ∈ ℕ`, the Gamma function is undefined; by convention we assign it the value `0`.|
|10|The monotone sequence whose value at `n` is the supremum of the `f m` where `m ≤ n`.|(Implementation detail). The function underlying `(A ⊗[R] Matrix n n R) →ₐ[R] Matrix n n A`, as an `R`-bilinear map.|

## Theorem 2 (Putnam)
Let $D_n$ be the determinant of the $n$ by $n$ matrix whose value in the $i$ th row and $j$ th column is $|i-j|$. Show that $D_n = (-1)^{n-1} * (n-1) * (2^{n-2}).$
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|Determinant of 2x2 matrix|The center of a group `G` is the set of elements that commute with everything in `G`|
|2|Laplacian expansion of the determinant of an `n+1 × n+1` matrix along column `j`.|`Polynomial.Gal.restrictProd` is actually a subgroup embedding.|
|3|Laplacian expansion of the determinant of an `n+1 × n+1` matrix along row `i`.|The vector given in euclidean space by being `1 : 𝕜` at coordinate `i : ι` and `0 : 𝕜` at all other coordinates.|
|4|Determinant of 1x1 matrix|The underlying set of the center of a group.|
|5|Laplacian expansion of the determinant of an `n+1 × n+1` matrix along row 0.|The center of a multiplication with unit `M` is the set of elements that commute with everything in `M`|
|6|The determinant of a matrix given by the Leibniz formula.|The base space of a fiber bundle core, as a convenience function for dot notation|
|7|Laplacian expansion of the determinant of an `n+1 × n+1` matrix along column 0.|Add extra prefix to context-free producing.|
|8|The determinant of a permutation matrix equals its sign.|The center of an additive group `G` is the set of elements that commute with everything in `G`|
|9|Multiplying each column by a fixed `v j` multiplies the determinant by the product of the `v`s.|The unit object is always closed. This isn't an instance because most of the time we'll prove closedness for all objects at once, rather than just for this one.|
|10|A matrix whose nondiagonal entries are negative with the sum of the entries of each row positive has nonzero determinant.|The end point of a `Path`.|

## Theorem 3 (Putnam)
Find every real-valued function $f$ whose domain is an interval $I$ (finite or infinite) having 0 as a left-hand endpoint, such that for every positive member $x$ of $I$ the average of $f$ over the closed interval $[0, x]$ is equal to the geometric mean of the numbers $f(0)$ and $f(x)$.Show that \[ f(x) = \frac{a}{(1 - cx)^2} \begin{cases} 	ext{for } 0 \le x < \frac{1}{c}, & 	ext{if } c > 0\ 	ext{for } 0 \le x < \infty, & 	ext{if } c \le 0, \end{cases} \] where $a > 0$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|A function on `[a, b]` with the norm of the right derivative bounded by `C` satisfies `‖f x - f a‖ ≤ C * (x - a)`.|**Alias** of `dvd_trans`.|
|2|A continuous function `f : X → ℝ` such that  * `0 ≤ f x ≤ 1` for all `x`; * `f` equals zero on `c.C` and equals one outside of `c.U`;|Display a widget panel allowing to generate a `conv` call zooming to the subexpression selected in the goal.|
|3|If `f` grows in the punctured neighborhood of `c : ℝ` at least as fast as `1 / (x - c)`, then it is not interval integrable on any nontrivial interval `a..b`, `c ∈ [a, b]`.|`-[n+1]` is suggestive notation for `negSucc n`, which is the second constructor of `Int` for making strictly negative numbers by mapping `n : Nat` to `-(n + 1)`.|
|4|If an integrable function `f : α → E` takes values in a convex set `s` and for some set `t` of positive measure, the average value of `f` over `t` belongs to the interior of `s`, then the average of `f` over the whole space belongs to the interior of `s`.|Notation for `closure` with respect to a non-standard topology.|
|5|Weighted generalized mean inequality, version for sums over finite sets, with `ℝ≥0∞`-valued functions and real exponents.|Auxiliary function for `getRawProjections`. Find custom projections, automatically found by simps. These come from `DFunLike` and `SetLike` instances.|
|6|A negative exponential function is integrable on intervals in `R≥0`|A variant of `aesop_cat` which does not fail when it is unable to solve the goal. Use this only for exploration! Nonterminal `aesop` is even worse than nonterminal `simp`.|
|7|An infinitely smooth function `f : ℝ → ℝ` such that `f x = 0` for `x ≤ 0`, `f x = 1` for `1 ≤ x`, and `0 < f x < 1` for `0 < x < 1`.|elaborate the syntax and run `simpsTac`.|
|8|Average value of an `ℝ≥0∞`-valued function `f` w.r.t. to the standard measure on a set `s`.  It is equal to `(volume s)⁻¹ * ∫⁻ x, f x`, so it takes value zero if `s` has infinite measure. If `s` has measure `1`, then the average of any function is equal to its integral.|Attribute for identifying `positivity` extensions.|
|9|If `f` is continuous on `[a, ∞)`, and is `O (exp (-b * x))` at `∞` for some `b > 0`, then `f` is integrable on `(a, ∞)`.|Default value for `IntCast.intCast` in an `AddGroupWithOne`.|
|10|Weighted generalized mean inequality, version for sums over finite sets, with `ℝ≥0`-valued functions and real exponents.|The `bot` subgraph is the subgraph with no vertices or edges.|

## Theorem 4 (Putnam)
Let $S$ be the set of all numbers of the form $2^m3^n$, where $m$ and $n$ are integers, and let $P$ be the set of all positive real numbers. Is $S$ dense in $P$? Show that $S$ is dense in $P$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|The closure of a set `s` is dense if and only if `s` is dense.|If `α` has no zero divisors, then the product of two elements is nonzero iff both of them are nonzero.|
|2|If a set `s` is nowhere dense, so is its closure.|If a polynomial of degree 2 is always positive, then its discriminant is negative, at least when the coefficient of the quadratic term is nonzero.|
|3|A set is dense if and only if it has a nonempty intersection with each nonempty open set.|`testBit m n` returns whether the `(n+1)ˢᵗ` least significant bit is `1` or `0`|
|4|There exists a countable dense set.|The property that `f 0 = 0` in terms of the graph.|
|5|A set in a nontrivial densely linear ordered type is dense in the sense of topology if and only if for any `a < b` there exists `c ∈ s`, `a < c < b`. Each implication requires less typeclass assumptions.|A subgroup is either the trivial subgroup or contains a nonzero element.|
|6|The set of Liouville numbers in dense.|Given a nonempty finset `s` in a linear order `α`, then `s.min' h` is its minimum, as an element of `α`, where `h` is a proof of nonemptiness. Without this assumption, use instead `s.min`, taking values in `WithTop α`.|
|7|A set `s` is closed and nowhere dense iff its complement `sᶜ` is open and dense.|`f : α →+* β` has a trivial codomain iff its range is `{0}`.|
|8|The product of two dense sets is a dense set.|If `α` has no zero divisors, then the product of two elements equals zero iff one of them equals zero.|
|9|If a set `s` is separable in a (pseudo extended) metric space, then it admits a countable dense subset. This is not obvious, as the countable set whose closure covers `s` given by the definition of separability does not need in general to be contained in `s`.|The second-lowest coefficient, or 0 for constants|
|10|A set is dense iff it has non-trivial intersection with all basis sets.|`normalizeDenominatorsLHS h lhs` assumes that `h` is a proof of `lhs R 0`. It creates a proof of `lhs' R 0`, where all numeric division in `lhs` has been cancelled.|

## Theorem 5 (Putnam)
Let $\{a_n\}$ be a sequence of real numbers satisfying the inequalities $0 \leq a_k \leq 100a_n$ for $n \leq k \leq 2n$ and $n=1,2,\dots$, and such that the series $\sum_{n=0}^\infty a_n$ converges. Prove that $\lim_{n 	o \infty}na_n=0$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|A series of non-negative real numbers converges to `r` in the sense of `HasSum` if and only if the sequence of partial sum converges to `r`.|Returns the next numerator `Aₙ = bₙ₋₁ * Aₙ₋₁ + aₙ₋₁ * Aₙ₋₂`, where `predA` is `Aₙ₋₁`, `ppredA` is `Aₙ₋₂`, `a` is `aₙ₋₁`, and `b` is `bₙ₋₁`.|
|2|A series whose terms are bounded by the terms of a converging geometric series converges.|Marks given value and its object graph closure as persistent. This will remove reference counter updates but prevent the closure from being deallocated until the end of the process! It can still be useful to do eagerly when the value will be marked persistent later anyway and there is available time budget to mark it now or it would be unnecessarily marked multi-threaded in between.|
|3|All convergents of `0` are zero.|`G.incMatrix R` is the `α × Sym2 α` matrix whose `(a, e)`-entry is `1` if `e` is incident to `a` and `0` otherwise.|
|4|Comparison test of convergence of series of non-negative real numbers.|An encoding function of the positive binary numbers in bool.|
|5|Comparison test of convergence of `ℝ≥0`-valued series.|If `A` is subterminal, the unique morphism from it to the terminal object is a monomorphism. The converse of `isSubterminal_of_mono_terminal_from`.|
|6|Cauchy condensation test for series of nonnegative real numbers.|The stabilizer of an element under an action, i.e. what sends the element to itself. A subgroup.|
|7|The limit `a` of the sequence `stirlingSeq` satisfies `0 < a`|If `A` is subterminal, the unique morphism from it to a terminal object is a monomorphism. The converse of `isSubterminal_of_mono_isTerminal_from`.|
|8|The number of inequalities in the series|If the unique morphism from `A` to a terminal object is a monomorphism, `A` is subterminal. The converse of `IsSubterminal.mono_isTerminal_from`.|
|9|The Cesaro average of a converging sequence converges to the same limit.|`A.HasOrthogonalCols` means matrix `A` has orthogonal columns (with respect to `Matrix.dotProduct`).|
|10|The terms of the sequence are nonzero.|`A.HasOrthogonalRows` means matrix `A` has orthogonal rows (with respect to `Matrix.dotProduct`).|

## Theorem 6 (Putnam)
Let $E$ be a Euclidean space of at most three dimensions. If $A$ is a nonempty subset of $E$, define $S(A)$ to be the set of all points that lie on closed segments joining pairs of points of $A$. For a given nonempty set $A_0$, define $A_n=S(A_{n-1})$ for $n=1,2,\dots$. Prove that $A_2=A_3=\cdots$. (A one-point set should be considered to be a special case of a closed segment.)
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|Star-convexity of sets. `s` is star-convex at `x` if every segment from `x` to a point in `s` is contained in `s`.|Gets the word size of the platform. That is, whether the platform is 64 or 32 bits.|
|2|Segments in a vector space.|`ratNorm q`, for a `p`-adic number `q` is the `p`-adic norm of `q`, as rational number.  The lemma `padicNormE.eq_ratNorm` asserts `‖q‖ = ratNorm q`.|
|3|Given a closed set `s`, a point belongs to `s` iff its infimum edistance to this set vanishes|Because we use binary encoding, we define `trNat` in terms of `trNum`, using `Num`, which are binary natural numbers. (We could also use `Nat.binaryRecOn`, but `Num` and `PosNum` make for easy inductions.)|
|4|Given a closed set `s`, a point belongs to `s` iff its infimum distance to this set vanishes|If `q ≠ 0`, the `p`-adic norm of a rational `q` is `p ^ (-padicValRat p q)`. If `q = 0`, the `p`-adic norm of `q` is `0`.|
|5|Given a closed set `s`, a point belongs to `s` iff its infimum distance to this set vanishes.|Distance on `GHSpace`: the distance between two nonempty compact spaces is the infimum Hausdorff distance between isometric copies of the two spaces in a metric space. For the definition, we only consider embeddings in `ℓ^∞(ℝ)`, but we will prove below that it works for all spaces.|
|6|A point belongs to the closure of `s` iff its infimum distance to this set vanishes.|A list of natural numbers is a Zeckendorf representation (of a natural number) if it is an increasing sequence of non-consecutive numbers greater than or equal to `2`.  This is relevant for Zeckendorf's theorem, since if we write a natural `n` as a sum of Fibonacci numbers `(l.map fib).sum`, `IsZeckendorfRep l` exactly means that we can't simplify any expression of the form `fib n + fib (n + 1) = fib (n + 2)`, `fib 1 = fib 2` or `fib 0 = 0` in the sum.|
|7|A set of points, whose `vectorSpan` is finite-dimensional, is collinear if and only if their `vectorSpan` has dimension at most `1`.|`-[n+1]` is suggestive notation for `negSucc n`, which is the second constructor of `Int` for making strictly negative numbers by mapping `n : Nat` to `-(n + 1)`.|
|8|The set of points.|A type endowed with `0` and unary `-` is an `NegZeroClass`, if it admits an injective map that preserves `0` and unary `-` to an `NegZeroClass`.|
|9|A point in a collinear set of points lies in the affine span of any two distinct points of that set.|A decision procedure for equality of natural numbers.  This definition is overridden in the compiler to efficiently evaluate using the "bignum" representation (see `Nat`). The definition provided here is the logical model.|
|10|The span of a set of points contains the set of points.|The index of a subgroup as a natural number, and returns 0 if the index is infinite.|

## Theorem 7 (Putnam)
Let $S$ be a finite set. A set $P$ of subsets of $S$ has the property that any two members of $P$ have at least one element in common and that $P$ cannot be extended (whilst keeping this property). Prove that $P$ contains exactly half of the subsets of $S$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|There are finitely many subsets of a given finite set|`SameRay` is symmetric.|
|2|If there is an absolute upper bound on the size of a set satisfying `P`, then the maximal subset property always holds.|Assumes right covariance. The lemma assuming left covariance is `Left.add_pos`.|
|3|Induction up to a finite set `S`.|Extend a `SimpleFunc` along a measurable embedding: `f₁.extend g hg f₂` is the function `F : β →ₛ γ` such that `F ∘ g = f₁` and `F y = f₂ y` whenever `y ∉ range g`.|
|4|`𝒫 s` is the set of all subsets of `s`.|Conditional measure on the second space of the product given the value on the first, as a kernel. Use the more general `condKernel`.|
|5|A set `s` is `Set.Nontrivial` if it has at least two distinct elements.|Only assumes right strict covariance.|
|6|**Kleitman's theorem**. An intersecting family on `n` elements contains at most `2ⁿ⁻¹` sets, and each further intersecting family takes at most half of the sets that are in no previous family.|Two nonzero vectors `x y` in a real normed space are on the same ray if and only if the unit vectors `‖x‖⁻¹ • x` and `‖y‖⁻¹ • y` are equal.|
|7|The partial ordering by subset inclusion, inherited from `Set P`.|**Gram-Schmidt Orthonormalization**: `gramSchmidtNormed` applied to a linearly independent set of vectors produces an orthornormal system of vectors.|
|8|Membership in a set|In a strictly convex space, the triangle inequality turns into an equality if and only if the middle point belongs to the segment joining two other points.|
|9|A set `s` is a `Subsingleton` if it has at most one element.|`(k*x, k*y, k*z)` is a Pythagorean triple if and only if `(x, y, z)` is also a triple.|
|10|If `a` is a least upper bound for sets `s` and `p`, then it is a least upper bound for any set `t`, `s ⊆ t ⊆ p`.|Given two isometric embeddings `Φ : Z → X` and `Ψ : Z → Y`, we define a space `GlueSpace hΦ hΨ` by identifying in `X ⊕ Y` the points `Φ x` and `Ψ x`.|

## Theorem 8 (Putnam)
Let $	riangle ABC$ be a triangle in the Euclidean plane, with points $P$, $Q$, and $R$ lying on segments $\overline{BC}$, $\overline{CA}$, $\overline{AB}$ respectively such that $$\frac{AQ}{QC} = \frac{BR}{RA} = \frac{CP}{PB} = k$$ for some positive constant $k$. If $	riangle UVW$ is the triangle formed by parts of segments $\overline{AP}$, $\overline{BQ}$, and $\overline{CR}$, prove that $$\frac{[	riangle UVW]}{[	riangle ABC]} = \frac{(k - 1)^2}{k^2 + k + 1},$$ where $[	riangle]$ denotes the area of the triangle $	riangle$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|Two triangles with the same points have the same orthocenter.|The canonical embedding from a tensor power to the tensor algebra|
|2|**Isosceles Triangle Theorem**: Pons asinorum, angle-at-point form.|A constructor for objects of the category `CompHaus`, taking a type, and bundling the compact Hausdorff topology found by typeclass inference.|
|3|**Ptolemy's inequality**: in a quadrangle `ABCD`, `\|AC\| * \|BD\| ≤ \|AB\| * \|CD\| + \|BC\| * \|AD\|`. If `ABCD` is a convex cyclic polygon, then this inequality becomes an equality, see `EuclideanGeometry.mul_dist_add_mul_dist_eq_mul_dist_of_cospherical`.|The Yoneda embedding is faithful.  See <https://stacks.math.columbia.edu/tag/001P>.|
|4|If M is the midpoint of the segment AB and C is the same distance from A as it is from B then ∠CMB = π / 2.|The cofork defined in `BinaryBicone.inrCokernelCofork` is indeed a cokernel.|
|5|If M is the midpoint of the segment AB and C is the same distance from A as it is from B then ∠CMA = π / 2.|The label of the root of the tree for a non-trivial approximation of the cofix of a pfunctor.|
|6|The midpoint of the segment AB is the same distance from A as it is from B.|A constructor for a subbimodule which demands closure under the two sets of scalars individually, rather than jointly via their tensor product.  Note that `R` plays no role but it is convenient to make this generalisation to support the cases `R = ℕ` and `R = ℤ` which both show up naturally. See also `Subbimodule.baseChange`.|
|7|The other triangle equality. The proof follows the following proof in Globular: http://globular.science/1905.001|Embeddings of types induce embeddings of complete graphs on those types.|
|8|If `P` is a point on the line `AB` and `Q` is equidistant from `A` and `B`, then `AP * BP = abs (BQ ^ 2 - PQ ^ 2)`.|Provide a coercion to `Type u` for a concrete category. This is not marked as an instance as it could potentially apply to every type, and so is too expensive in typeclass search.  You can use it on particular examples as: ``` instance : HasCoeToSort X := ConcreteCategory.hasCoeToSort X ```|
|9|The product of a family of triangles.|The adjunction between the cofree and forgetful constructions for Eilenberg-Moore coalgebras for a comonad.|
|10|Suppose lines from two vertices of a triangle to interior points of the opposite side meet at `p`. Then `p` lies in the interior of the first (and by symmetry the other) segment from a vertex to the point on the opposite side.|If the domain of a `DenseEmbedding` is a separable space, then so is its codomain.|

## Theorem 9 (Putnam)
Let $D$ be the unit disk in the plane. Show that we cannot find congruent sets $A, B$ with $A \cap B = \emptyset$ and $A \cup B = D$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|The empty set has zero diameter|If the input vectors of `gramSchmidt` are linearly independent, then the output vectors are non-zero.|
|2|Real part of a point of the unit disc.|Open segment in a vector space. Note that `openSegment 𝕜 x x = {x}` instead of being `∅` when the base semiring has some element between `0` and `1`.|
|3|The finset of elements of the form `a ⊔ b` where `a ∈ s`, `b ∈ t` and `a` and `b` are disjoint.|A finite Hilbert basis is an orthonormal basis.|
|4|For `A B` two nonempty finite sets, there always exist `a0 ∈ A, b0 ∈ B` such that `UniqueAdd A B a0 b0`|The Gram-Schmidt process takes a set of vectors as input and outputs a set of orthogonal vectors which have the same span.|
|5|The empty set is collinear.|The `orthogonalProjection` lies in the orthogonal subspace.|
|6|If two sets intersect, the diameter of the union is bounded by the sum of the diameters.|Each vector space has a basis.|
|7|Union of a set of sets.|Adding a vector to a point in the given subspace, then taking the orthogonal projection, produces the original point if the vector was in the orthogonal direction.|
|8|Conjugate point of the unit disc.|Given an orthonormal basis and an orientation, return an orthonormal basis giving that orientation: either the original basis, or one constructed by negating a single (arbitrary) basis vector.|
|9|The sets of factors of coprime `a` and `b` are disjoint|The eigenspaces of a self-adjoint operator are mutually orthogonal.|
|10|Intersection of a set of sets.|A Jordan decomposition provides a Hahn decomposition.|

## Theorem 10 (Putnam)
Assume that $\lvert f(x) \rvert \le 1$ and $\lvert f''(x) \rvert \le 1$ for all $x$ on an interval of length at least 2. Show that $\lvert f'(x) \rvert \le 2$ on the interval.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|A function on `[0, 1]` with the norm of the derivative within `[0, 1]` bounded by `C` satisfies `‖f 1 - f 0‖ ≤ C`, `HasDerivWithinAt` version.|Transport dependent functions through an equivalence of the base space.  This is `Equiv.piCongrLeft'` as a `LinearEquiv`.|
|2|A function on `[0, 1]` with the norm of the derivative within `[0, 1]` bounded by `C` satisfies `‖f 1 - f 0‖ ≤ C`, `derivWithin` version.|We use `Num` to define the translation of binary natural numbers. Positive numbers are translated using `trPosNum`, and `trNum 0 = []`. So there are never any trailing `bit0`'s in a translated `Num`.      0 = []     1 = [bit1]     2 = [bit0, bit1]     3 = [bit1, bit1]     4 = [bit0, bit0, bit1]|
|3|If a function has a Taylor series at order at least `1`, then the term of order `1` of this series is a derivative of `f`.|Left-shift the binary representation of a `Num`.|
|4|If a function has a Taylor series at order at least `1` on a neighborhood of `x`, then the term of order `1` of this series is a derivative of `f` at `x`.|Retrieves an element uniquely determined by a `PosNum` from the tree, taking the following path to get to the element: - `bit0` - go to left child - `bit1` - go to right child - `PosNum.one` - retrieve from here|
|5|Converse to the mean value inequality: if `f` is `C`-lipschitz then its derivative at `x₀` has norm bounded by `C`. Version using `deriv`.|`WithTerminal.star` is terminal.|
|6|An inequality involving `2`.|The injection into an additive pi group with the same values commutes.|
|7|If a function `f` is twice differentiable on `ℝ`, and `f''` is nonpositive on `ℝ`, then `f` is concave on `ℝ`.|Auxiliary function for `getRawProjections`. Find custom projections, automatically found by simps. These come from `DFunLike` and `SetLike` instances.|
|8|Converse to the mean value inequality: if `f` is `C`-lipschitz then its derivative at `x₀` has norm bounded by `C`. Version using `fderiv`.|In a preconnected space, if a symmetric transitive relation `P x y` is true for `y` close enough to `x`, then it holds for all `x, y`. This is a version of the fact that, if an equivalence relation has open classes, then it has a single equivalence class.|
|9|A function on `[a, b]` with the norm of the derivative within `[a, b]` bounded by `C` satisfies `‖f x - f a‖ ≤ C * (x - a)`, `HasDerivWithinAt` version.|The type of methods to find arguments for automatic projections for `simps`. We partly define this as a separate definition so that the unused arguments linter doesn't complain.|
|10|**Rolle's Theorem** `HasDerivAt` version|name for this projection used in the generated `simp` lemmas|

## Theorem 11 (Putnam)
Prove that $$\sum_{r=0}^{\lfloor\frac{n-1}{2}\rfloor} \left(\frac{n - 2r}{n} {n \choose r}\right)^2 = \frac{1}{n} {{2n - 2} \choose {n - 1}}$$ for every positive integer $n$.
| No. | FAISS Similarity Search | NearestEmbed |
|:---:|:---:|:---:|
|1|`choose n r` is maximised when `r` is `n/2`.|`X ∣_ᵤ U` is notation for `X.restrict U.openEmbedding`, the restriction of `X` to an open set `U` of `X`.|
|2|An inductive property of the central binomial coefficient.|A convenience function for `ReflectsColimit`, which takes the functor as an explicit argument to guide typeclass resolution.|
|3|The central binomial coefficient, `Nat.choose (2 * n) n`.|An enriched functor induces an honest functor of the underlying categories, by mapping the `(𝟙_ W)`-shaped morphisms.|
|4|`choose n 2` is the `n`-th triangle number.|Rpc function for the calc widget.|
|5|The sum of entries in a row of Pascal's triangle|Interpret a natural isomorphism of the underlying monoidal functors as an isomorphism of the braided monoidal functors.|
|6|Vandermonde's identity|The equivalence between `X` and the underlying type of its fundamental groupoid. This is useful for transferring constructions (instances, etc.) from `X` to `πₓ X`.|
|7|proof that the `parts` sum to `n`|The functor `restrictedYoneda` is isomorphic to the identity functor when evaluated at the yoneda embedding.|
|8|`FloorSemiring.floor a` computes the greatest natural `n` such that `(n : α) ≤ a`.|The category of types has `X × Y`, the usual cartesian product, as the binary product of `X` and `Y`.|
|9|The **binomial theorem**|Sending objects to cochain complexes supported at `0` then taking `0`-th homology is the same as doing nothing.|
|10|The `n`th central binomial coefficient is the product of its prime factors, which are at most `2n`.|Construct a bundled `CommGroup` from the underlying type and typeclass.|

