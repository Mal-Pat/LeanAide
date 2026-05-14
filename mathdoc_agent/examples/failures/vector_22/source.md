### Theorem:
Let $T : V \to V$ be a linear transformation on a finite-dimensional vector space
satisfying $T^2 = T$.
Let $\lambda$ be a scalar with $\lambda \neq 0,1$.
Define
\[
S = T - \lambda I.
\]
Prove that $S$ is invertible.

### Proof:

Assume that $V$ is a finite-dimensional vector space and that $T : V \to V$ is a linear map satisfying $T^2 = T$. Let $\lambda$ be a scalar with $\lambda \neq 0$ and $\lambda \neq 1$, and define $S = T - \lambda I$, where $I : V \to V$ denotes the identity map.

First, note that the condition $T^2 = T$ implies that for every $v \in V$ we have $T(T(v)) = T(v)$. In particular, if $v \in \operatorname{im}(T)$, then there exists $u \in V$ such that $v = T(u)$, and hence
\[
T(v) = T(T(u)) = T(u) = v.
\]
Therefore $T$ restricts to the identity map on $\operatorname{im}(T)$.

Next, we show that every vector $v \in V$ can be written as a sum of a vector in $\ker(T)$ and a vector in $\operatorname{im}(T)$. Let $v \in V$ be arbitrary and define
\[
w := v - T(v).
\]
Then
\[
T(w) = T(v - T(v)) = T(v) - T(T(v)) = T(v) - T(v) = 0,
\]
so $w \in \ker(T)$. By definition, $T(v) \in \operatorname{im}(T)$. Hence every $v \in V$ can be written as
\[
v = w + T(v)
\]
with $w \in \ker(T)$ and $T(v) \in \operatorname{im}(T)$, which shows that
\[
V = \ker(T) + \operatorname{im}(T).
\]

We now prove that the sum $\ker(T) + \operatorname{im}(T)$ is direct. Let $v \in \ker(T) \cap \operatorname{im}(T)$. Since $v \in \ker(T)$, we have $T(v) = 0$. Since $v \in \operatorname{im}(T)$, we have seen above that $T(v) = v$. Combining these equalities, we obtain
\[
v = T(v) = 0.
\]
Thus $\ker(T) \cap \operatorname{im}(T) = \{0\}$, and hence
\[
V = \ker(T) \oplus \operatorname{im}(T).
\]

We describe the action of $S$ on $\ker(T)$ and on $\operatorname{im}(T)$. Let $v \in \ker(T)$. Then $T(v) = 0$, and therefore
\[
S(v) = (T - \lambda I)(v) = T(v) - \lambda v = 0 - \lambda v = -\lambda v.
\]
Thus $S$ acts on $\ker(T)$ as multiplication by the scalar $-\lambda$. Since $\lambda \neq 0$, the scalar $-\lambda$ is invertible, and hence the restriction of $S$ to $\ker(T)$ is an invertible linear map from $\ker(T)$ to itself.

Similarly, let $v \in \operatorname{im}(T)$. Then, as shown above, $T(v) = v$, and therefore
\[
S(v) = (T - \lambda I)(v) = T(v) - \lambda v = v - \lambda v = (1 - \lambda)v.
\]
Thus $S$ acts on $\operatorname{im}(T)$ as multiplication by the scalar $1 - \lambda$. Since $\lambda \neq 1$, the scalar $1 - \lambda$ is invertible, and hence the restriction of $S$ to $\operatorname{im}(T)$ is an invertible linear map from $\operatorname{im}(T)$ to itself.

Because $V$ is the internal direct sum
\[
V = \ker(T) \oplus \operatorname{im}(T),
\]
every vector $v \in V$ can be written uniquely as $v = x + y$ with $x \in \ker(T)$ and $y \in \operatorname{im}(T)$. On such a decomposition, the map $S$ is given by
\[
S(v) = S(x + y) = S(x) + S(y) = -\lambda x + (1 - \lambda)y.
\]
The map $S$ is block-diagonal with respect to the decomposition $V = \ker(T) \oplus \operatorname{im}(T)$, with invertible diagonal blocks $-\lambda \cdot \operatorname{id}_{\ker(T)}$ on $\ker(T)$ and $(1 - \lambda) \cdot \operatorname{id}_{\operatorname{im}(T)}$ on $\operatorname{im}(T)$. A linear map that is invertible on each direct summand of a direct sum decomposition, and preserves that decomposition in this way, is invertible on the whole space.

More explicitly, define a linear map $R : V \to V$ as follows. For $v \in V$, write uniquely $v = x + y$ with $x \in \ker(T)$ and $y \in \operatorname{im}(T)$, and set
\[
R(v) := -\tfrac{1}{\lambda}x + \tfrac{1}{1 - \lambda}y.
\]
This is well-defined and linear because the decomposition is direct and the coefficients are scalars. Then, for such $v = x + y$, we compute
\[
S(R(v)) = S\bigl(-\tfrac{1}{\lambda}x + \tfrac{1}{1 - \lambda}y\bigr)
= -\lambda\bigl(-\tfrac{1}{\lambda}x\bigr) + (1 - \lambda)\bigl(\tfrac{1}{1 - \lambda}y\bigr)
= x + y
= v,
\]
and
\[
R(S(v)) = R\bigl(-\lambda x + (1 - \lambda)y\bigr)
= -\tfrac{1}{\lambda}(-\lambda x) + \tfrac{1}{1 - \lambda}((1 - \lambda)y)
= x + y
= v.
\]
Thus $R$ is both a left and right inverse of $S$, so $S$ is invertible.