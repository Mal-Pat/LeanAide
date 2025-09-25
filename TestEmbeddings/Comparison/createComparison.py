theorem = "If a sequence of real numbers is monotone and bounded, then the sequence converges."

num = 1

faiss = """
A sequence converges if every subsequence has a convergent subsequence.
-----------------------------------------
Monotone convergence theorem expressed with limits
-----------------------------------------
A Cauchy sequence on the natural numbers is bounded.
-----------------------------------------
The limit of a bounded-below subadditive sequence. The fact that the sequence indeed tends to
this limit is given in `Subadditive.tendsto_lim`
-----------------------------------------
If a Cauchy sequence has a convergent subsequence, then it converges.
-----------------------------------------
Shows that the sequence of denominators is monotone, that is `Bₙ ≤ Bₙ₊₁`.
-----------------------------------------
Assume that, for any `a < b`, a sequence can not be infinitely many times below `a` and
above `b`. If it is also ultimately bounded above and below, then it has to converge. This even
works if `a` and `b` are restricted to a dense subset.
-----------------------------------------
**Dirichlet's Test** for monotone sequences.
-----------------------------------------
A version of Bolzano-Weistrass: in a proper metric space (eg. $ℝ^n$),
every bounded sequence has a converging subsequence.
-----------------------------------------
The monotone sequence whose value at `n` is the supremum of the `f m` where `m ≤ n`.
"""

nearestemb = """
If `A` is subterminal, the unique morphism from it to a terminal object is a monomorphism.
The converse of `isSubterminal_of_mono_isTerminal_from`.



-----------------------------------------

`assert_exists n` is a user command that asserts that a declaration named `n` exists
in the current import scope.

Be careful to use names (e.g. `Rat`) rather than notations (e.g. `ℚ`).



-----------------------------------------

(Implementation detail).
The function underlying `(A ⊗[R] Matrix n n R) →ₐ[R] Matrix n n A`,
as an `R`-linear map.



-----------------------------------------

Given a submodule, corestrict to the pairing on `M ⧸ W` by
simultaneously restricting to `W.dualAnnihilator`.

See `Subspace.dualCopairing_nondegenerate`. 


-----------------------------------------

See `rank_subsingleton` for the reason that `Nontrivial R` is needed.
Also see `rank_eq_zero_iff` for the version without `NoZeroSMulDivisor R M`. 


-----------------------------------------

`a <|> b` executes `a` and returns the result, unless it fails in which
case it executes and returns `b`. Because `b` is not always executed, it
is passed as a thunk so it can be forced only when needed.
The meaning of this notation is type-dependent. 


-----------------------------------------

`G.CliqueFree n` means that `G` has no `n`-cliques. 


-----------------------------------------

The rank of a module as a natural number.

Defined by convention to be `0` if the space has infinite rank.

For a vector space `M` over a field `R`, this is the same as the finite dimension
of `M` over `R`.



-----------------------------------------

At `-n` for `n ∈ ℕ`, the Gamma function is undefined; by convention we assign it the value `0`.



-----------------------------------------

(Implementation detail).
The function underlying `(A ⊗[R] Matrix n n R) →ₐ[R] Matrix n n A`,
as an `R`-bilinear map.



-----------------------------------------

If `A` is subterminal, the unique morphism from it to the terminal object is a monomorphism.
The converse of `isSubterminal_of_mono_terminal_from`.



-----------------------------------------

`N.annihilator` is the ideal of all elements `r : R` such that `r • N = 0`. 


-----------------------------------------

The elements of `A.nonunits` are those of the maximal ideal of `A` after coercion to `K`.

See also `mem_nonunits_iff_exists_mem_maximalIdeal`, which gets rid of the coercion to `K`,
at the expense of a more complicated right hand side.
 


-----------------------------------------

Auxiliary for `eraseTR`: `eraseTR.go l a xs acc = acc.toList ++ erase xs a`,
unless `a` is not present in which case it returns `l` 


-----------------------------------------

The length of a list: `[].length = 0` and `(a :: l).length = l.length + 1`.

This function is overridden in the compiler to `lengthTR`, which uses constant
stack space, while leaving this function to use the "naive" recursion which is
easier for reasoning.



-----------------------------------------

`O(n)`. `range n` is the numbers from `0` to `n` exclusive, in increasing order.
* `range 5 = [0, 1, 2, 3, 4]`



-----------------------------------------

Given an element `x : α` of `l : List α` such that `x ∈ l`, get the previous
element of `l`. This works from head to tail, (including a check for last element)
so it will match on first hit, ignoring later duplicates.

 * `prev [1, 2, 3] 2 _ = 1`
 * `prev [1, 2, 3] 1 _ = 3`
 * `prev [1, 2, 3, 2, 4] 2 _ = 1`
 * `prev [1, 2, 3, 4, 2] 2 _ = 1`
 * `prev [1, 1, 2] 1 _ = 2`



-----------------------------------------

 For any group element `a` in `G₀` different from zero and any integer `n`, the `(n + 1)`-th power of `a` equals the `n`-th power of `a` multiplied by `a`. In Lean notation: `(a ^ (n + 1)) = a ^ n * a`.


-----------------------------------------

Auxiliary for `range'TR`: `range'TR.go n e = [e-n, ..., e-1] ++ acc`. 


-----------------------------------------

The theorem `Matrix.det_succ_row` states that for any commutative ring `R`, and for any natural number `n`, if `A` is an `(n+1) x (n+1)` matrix with entries from `R`, and `i` is a row index in `A`, then the determinant of `A` can be computed by summing over all columns `j` in `A`, the product of `(-1) ^ (i + j)`, the element at row `i` and column `j` in `A`, and the determinant of the submatrix of `A` that results from removing the `i`-th row and `j`-th column. This is known as the Laplacian expansion of a determinant along a row.


-----------------------------------------

 If matrix `A` over commutative ring `R` with decidable equality and finite index type `n` has a zero row, then its determinant is zero.


-----------------------------------------

Auxiliary for `eraseIdxTR`: `eraseIdxTR.go l n xs acc = acc.toList ++ eraseIdx xs a`,
unless `a` is not present in which case it returns `l`
"""

faisslist = [thm.strip().replace("|", "\|").replace("\n"," ") for thm in faiss.split("-----------------------------------------")]
nearestemblist = [thm.strip().replace("|", "\|").replace("\n"," ") for thm in nearestemb.split("-----------------------------------------")]

def write(filename):
  with open(filename, "a", encoding='utf-8') as file:
    file.write(f"## Theorem {num}\n")
    file.write(f"{theorem}\n")
    file.write("| No. | FAISS Similarity Search | NearestEmbed |\n")
    file.write("|:---:|:---:|:---:|\n")
    for i in range(10):
      file.write(f"|{i+1}|{faisslist[i]}|{nearestemblist[i]}|\n")


write("/home/malpat/LeanAide/TestEmbeddings/Comparison/comparison.md")

