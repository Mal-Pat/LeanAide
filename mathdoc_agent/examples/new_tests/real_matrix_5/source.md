## Theorem:

Let $A$ be an $n \times n$ matrix with entries in the field of real numbers $\mathbb{R}$. If $A^2 = -I_n$, where $I_n$ is the $n \times n$ identity matrix, then $n$ is an even integer.

## Proof:

Assume that $A$ is an $n \times n$ real matrix satisfying $A^2 = -I_n$. The goal is to prove that $n$ is an even integer.

First, consider $A$ as a linear operator on the real vector space $\mathbb{R}^n$. The equation $A^2 = -I_n$ implies that, as a linear map, $A$ satisfies the polynomial equation
\[
A^2 + I_n = 0.
\]
Equivalently, the minimal polynomial $m_A(x)$ of $A$ divides the polynomial
\[
p(x) := x^2 + 1.
\]

The polynomial $x^2 + 1$ has distinct complex roots, namely $i$ and $-i$. Therefore $x^2 + 1$ has no repeated roots. Consequently, any divisor of $x^2+1$ also has no repeated roots. Hence the minimal polynomial $m_A(x)$ of $A$ has no repeated roots.

A real matrix whose minimal polynomial has no repeated roots is diagonalizable over $\mathbb{C}$. Thus, after extending scalars from $\mathbb{R}$ to $\mathbb{C}$, there exists a basis of $\mathbb{C}^n$ with respect to which the matrix of $A$ is diagonal. In particular, all eigenvalues of $A$ (over $\mathbb{C}$) are roots of the polynomial $x^2 + 1$, hence every eigenvalue of $A$ is either $i$ or $-i$.

Let $\lambda_1, \dots, \lambda_n$ denote the eigenvalues of $A$ over $\mathbb{C}$, listed with algebraic multiplicity. Then each $\lambda_j$ belongs to the set $\{i,-i\}$. Let $k$ denote the number of indices $j$ such that $\lambda_j = i$. Then the number of indices $j$ such that $\lambda_j = -i$ is $n-k$.

Consider the determinant of $A$ viewed as a complex matrix. Since $A$ is diagonalizable over $\mathbb{C}$ with eigenvalues $\lambda_1,\dots,\lambda_n$, the determinant of $A$ equals the product of its eigenvalues:
\[
\det(A) = \prod_{j=1}^n \lambda_j = i^k \cdot (-i)^{n-k}.
\]
On the other hand, the matrix identity $A^2 = -I_n$ implies a relation for the determinant. Taking determinants on both sides and using multiplicativity of the determinant, we obtain
\[
\det(A^2) = \det(-I_n).
\]
The left-hand side is
\[
\det(A^2) = (\det A)^2.
\]
The right-hand side is
\[
\det(-I_n) = (-1)^n \det(I_n) = (-1)^n.
\]
Thus we obtain the scalar equation
\[
(\det A)^2 = (-1)^n.
\]

Since $A$ has real entries, its determinant $\det A$ is a real number. Therefore $(\det A)^2$ is a nonnegative real number. Hence $(-1)^n$ must be a nonnegative real number. This forces $(-1)^n = 1$, because the only real values of $(-1)^n$ are $1$ and $-1$, and the value $-1$ is not nonnegative. Thus
\[
(-1)^n = 1.
\]
By the basic properties of integer parity, the equality $(-1)^n = 1$ holds if and only if $n$ is an even integer.

Therefore $n$ is even.