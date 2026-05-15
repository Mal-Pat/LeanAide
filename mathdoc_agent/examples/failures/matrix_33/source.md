## Theorem
An orthogonal matrix $Q$ is defined by $Q Q^T = I$. A standard result is that its determinant must be $\pm 1$.
-/

/- ## Proof
**Assumptions.**
Let \(n\) be a natural number.
Let \(Q\) be a real \(n\times n\) matrix.
Assume
\[
  h_Q : Q\,Q^T = I_n.
\]
**Goal.**  Prove \(\det(Q)=1\) or \(\det(Q)=-1\).

---
**Lemma 1 (multiplicativity of the determinant).**
For all real \(n\times n\) matrices \(A\) and \(B\),
\[
  \det(A\,B)=\det(A)\,\det(B).
\]

**Proof of Lemma 1.**  Follows from the usual expansion of \(\det\) as a sum over permutations.

---
**Lemma 2 (determinant of the identity).**
For the real identity matrix \(I_n\),
\[
  \det(I_n)=1.
\]

**Proof of Lemma 2.**  In the sum defining \(\det(I_n)\), only the identity permutation contributes \(1\).

---
**Lemma 3 (invariance under transpose).**
For every real \(n\times n\) matrix \(A\),
\[
  \det(A^T)=\det(A).
\]

**Proof of Lemma 3.**  Transposing exchanges entries according to the sign of each permutation, leaving the total sum unchanged.

---
**Lemma 4 (solutions of \(x^2=1\) over \(\mathbb{R}\)).**
For every real number \(x\), if \(x^2=1\) then \(x=1\) or \(x=-1\).

**Proof of Lemma 4.**  Factor \(x^2-1=(x-1)(x+1)\) and apply the zero–product property in \(\mathbb{R}\).

---
**Main argument.**
1. From \(h_Q\) we have
   \[
     Q\,Q^T = I_n.
   \]
2.  Lemma 1 yields
   \[
     \det(Q\,Q^T)=\det(Q)\,\det(Q^T).
   \]
3.  By Lemma 2 and \(Q\,Q^T=I_n\) we obtain
   \[
     \det(Q\,Q^T)=\det(I_n)=1.
   \]
4.  Combining steps 2 and 3 gives
   \[
     \det(Q)\,\det(Q^T)=1.
   \]
5.  Lemma 3 gives \(\det(Q^T)=\det(Q)\), hence
   \[
     \det(Q)^2=1.
   \]
6.  Lemma 4 applied to \(x=\det(Q)\) yields \(\det(Q)=1\) or \(\det(Q)=-1\).

Therefore \(\det(Q)\in\{1,-1\}\).