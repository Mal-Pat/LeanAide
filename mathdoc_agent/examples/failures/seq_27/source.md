### Theorem:
Let $(a_n)$ be a sequence such that
\[
\forall \varepsilon > 0,\;
\exists N,\;
\forall n \ge N,\;
\exists m \ge n,\;
|a_m - L| < \varepsilon.
\]
Prove that $\liminf a_n \le L \le \limsup a_n$.

### Proof:
Assume that $(a_n)$ is a real sequence and $L \in \mathbb{R}$ satisfies the following property:

For every $\varepsilon > 0$ there exists $N \in \mathbb{N}$ such that for every $n \ge N$ there exists $m \ge n$ with $|a_m - L| < \varepsilon$.

The goal is to prove that $\liminf_{n \to \infty} a_n \le L \le \limsup_{n \to \infty} a_n$.

First, recall the standard definitions of $\limsup$ and $\liminf$ in terms of suprema and infima of tails. For each $n \in \mathbb{N}$ define
\[
s_n := \sup\{ a_k : k \ge n \}, \qquad i_n := \inf\{ a_k : k \ge n \}.
\]
Then the sequence $(s_n)$ is decreasing, the sequence $(i_n)$ is increasing, and by definition
\[
\limsup_{n \to \infty} a_n = \inf_{n \in \mathbb{N}} s_n, \qquad
\liminf_{n \to \infty} a_n = \sup_{n \in \mathbb{N}} i_n.
\]

To prove $L \le \limsup_{n \to \infty} a_n$, it is enough to show that $L \le s_n$ for every $n \in \mathbb{N}$. Indeed, if $L \le s_n$ holds for all $n$, then $L$ is a lower bound of the set $\{s_n : n \in \mathbb{N}\}$, and consequently $L \le \inf_{n \in \mathbb{N}} s_n = \limsup_{n \to \infty} a_n$.

Fix an arbitrary $n \in \mathbb{N}$. Let
\[
E_n := \{ a_k : k \ge n \},
\]
so that $s_n = \sup E_n$. Assume for contradiction that $L > s_n$. Define
\[
\delta := L - s_n.
\]
Then $\delta > 0$. Apply the hypothesis to $\varepsilon := \delta/2 > 0$. By the assumption on $(a_n)$ and $L$, there exists $N \in \mathbb{N}$ such that for every $p \ge N$ there exists $m \ge p$ with
\[
|a_m - L| < \delta/2.
\]
Set $p := \max\{N, n\}$. Then $p \ge N$ and $p \ge n$. By the choice of $N$, there exists $m \ge p$ with
\[
|a_m - L| < \delta/2.
\]
Since $m \ge p \ge n$, we have $a_m \in E_n$, and hence by the definition of $s_n$ as a supremum we obtain
\[
a_m \le s_n.
\]

On the other hand, from $|a_m - L| < \delta/2$ we deduce
\[
L - \delta/2 < a_m < L + \delta/2.
\]
Using the definition $\delta = L - s_n$, the left inequality becomes
\[
L - \frac{L - s_n}{2} < a_m,
\]
which simplifies to
\[
\frac{L + s_n}{2} < a_m.
\]
Combining this with $a_m \le s_n$ yields
\[
\frac{L + s_n}{2} < s_n.
\]
Multiplying by $2$ gives
\[
L + s_n < 2 s_n,
\]
and hence
\[
L < s_n.
\]
This contradicts the assumption $L > s_n$. Therefore the assumption $L > s_n$ is impossible, and it follows that
\[
L \le s_n \quad \text{for all } n \in \mathbb{N}.
\]
Taking the infimum over all $n$ yields
\[
L \le \inf_{n \in \mathbb{N}} s_n = \limsup_{n \to \infty} a_n.
\]

Next, to prove $\liminf_{n \to \infty} a_n \le L$, it suffices to show that $i_n \le L$ for every $n \in \mathbb{N}$. Indeed, if $i_n \le L$ for all $n$, then $L$ is an upper bound of the set $\{i_n : n \in \mathbb{N}\}$ and therefore
\[
\sup_{n \in \mathbb{N}} i_n \le L,
\]
that is,
\[
\liminf_{n \to \infty} a_n = \sup_{n \in \mathbb{N}} i_n \le L.
\]

Fix an arbitrary $n \in \mathbb{N}$. As before, let
\[
E_n := \{ a_k : k \ge n \},
\]
so that $i_n = \inf E_n$. Assume for contradiction that $i_n > L$. Define
\[
\eta := i_n - L.
\]
Then $\eta > 0$. Apply the hypothesis to $\varepsilon := \eta/2 > 0$. By the assumption on $(a_n)$ and $L$, there exists $N \in \mathbb{N}$ such that for every $p \ge N$ there exists $m \ge p$ with
\[
|a_m - L| < \eta/2.
\]
Again set $p := \max\{N, n\}$. Then $p \ge N$ and $p \ge n$. By the choice of $N$, there exists $m \ge p$ with
\[
|a_m - L| < \eta/2.
\]
Since $m \ge p \ge n$, we have $a_m \in E_n$, and by the definition of $i_n$ as an infimum we conclude
\[
i_n \le a_m.
\]

From $|a_m - L| < \eta/2$ we have
\[
L - \eta/2 < a_m < L + \eta/2.
\]
Using $\eta = i_n - L$, the right inequality becomes
\[
a_m < L + \frac{i_n - L}{2} = \frac{L + i_n}{2}.
\]
Combining this with $i_n \le a_m$ yields
\[
i_n \le a_m < \frac{L + i_n}{2}.
\]
Thus
\[
i_n < \frac{L + i_n}{2}.
\]
Multiplying by $2$ gives
\[
2 i_n < L + i_n,
\]
and hence
\[
i_n < L.
\]
This contradicts the assumption $i_n > L$. Therefore the assumption $i_n > L$ is impossible, and it follows that
\[
i_n \le L \quad \text{for all } n \in \mathbb{N}.
\]
Taking the supremum over all $n$ yields
\[
\sup_{n \in \mathbb{N}} i_n \le L,
\]
that is,
\[
\liminf_{n \to \infty} a_n = \sup_{n \in \mathbb{N}} i_n \le L.
\]

Combining the two inequalities obtained above, one obtains
\[
\liminf_{n \to \infty} a_n \le L \le \limsup_{n \to \infty} a_n.
\]