theorem = "Prove that $$\sum_{r=0}^{\lfloor\frac{n-1}{2}\rfloor} \left(\frac{n - 2r}{n} {n \choose r}\right)^2 = \frac{1}{n} {{2n - 2} \choose {n - 1}}$$ for every positive integer $n$."

num = 11

faiss = """
`choose n r` is maximised when `r` is `n/2`.
-----------------------------------------
An inductive property of the central binomial coefficient.
-----------------------------------------
The central binomial coefficient, `Nat.choose (2 * n) n`.
-----------------------------------------
`choose n 2` is the `n`-th triangle number.
-----------------------------------------
The sum of entries in a row of Pascal's triangle
-----------------------------------------
Vandermonde's identity
-----------------------------------------
proof that the `parts` sum to `n`
-----------------------------------------
`FloorSemiring.floor a` computes the greatest natural `n` such that `(n : α) ≤ a`.
-----------------------------------------
The **binomial theorem**
-----------------------------------------
The `n`th central binomial coefficient is the product of its prime factors, which are
at most `2n`.
"""

nearestemb = """
`X ∣_ᵤ U` is notation for `X.restrict U.openEmbedding`, the restriction of `X` to an open set
`U` of `X`. 
-----------------------------------------
A convenience function for `ReflectsColimit`, which takes the functor as an explicit argument to
guide typeclass resolution.

-----------------------------------------
An enriched functor induces an honest functor of the underlying categories,
by mapping the `(𝟙_ W)`-shaped morphisms.

-----------------------------------------
Rpc function for the calc widget. 
-----------------------------------------
Interpret a natural isomorphism of the underlying monoidal functors as an
isomorphism of the braided monoidal functors.

-----------------------------------------
The equivalence between `X` and the underlying type of its fundamental groupoid.
This is useful for transferring constructions (instances, etc.)
from `X` to `πₓ X`. 
-----------------------------------------
The functor `restrictedYoneda` is isomorphic to the identity functor when evaluated at the yoneda
embedding.

-----------------------------------------
The category of types has `X × Y`, the usual cartesian product,
as the binary product of `X` and `Y`.

-----------------------------------------
Sending objects to cochain complexes supported at `0` then taking `0`-th homology
is the same as doing nothing.

-----------------------------------------
Construct a bundled `CommGroup` from the underlying type and typeclass. 
-----------------------------------------
The cofree functor from the Eilenberg-Moore category, constructing a coalgebra for any
object. 
-----------------------------------------
The greatest common divisor (gcd) of two positive natural numbers,
viewed as positive natural number. 
-----------------------------------------
If the domain has a zero (and is nontrivial), then `χ 0 = 0`. 
-----------------------------------------
Construct a `Zero C` for a category with a zero object.
This can not be a global instance as it will trigger for every `Zero C` typeclass search.
"""

faisslist = [thm.strip().replace("|", "\|").replace("\n"," ") for thm in faiss.split("-----------------------------------------")]
nearestemblist = [thm.strip().replace("|", "\|").replace("\n"," ") for thm in nearestemb.split("-----------------------------------------")]

def write(filename):
  with open(filename, "a", encoding='utf-8') as file:
    file.write(f"## Theorem {num} (Putnam)\n")
    file.write(f"{theorem}\n")
    file.write("| No. | FAISS Similarity Search | NearestEmbed |\n")
    file.write("|:---:|:---:|:---:|\n")
    for i in range(10):
      file.write(f"|{i+1}|{faisslist[i]}|{nearestemblist[i]}|\n")
    file.write("\n")


write("/home/malpat/LeanAide/TestEmbeddings/Comparison/comparison.md")

