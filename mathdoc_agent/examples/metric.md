## Theorem:

Let $(X, d)$ be a metric space. Let $x$ and $y$ be two distinct points with distance $d(x, y) = \epsilon > 0$. Prove that the open balls $B(x, \epsilon/3)$ and $B(y, \epsilon/3)$ do not intersect.

## Proof:

Let $(X,d)$ be a metric space, and let $x,y \in X$ be distinct points such that $d(x,y) = \varepsilon > 0$. Consider the open balls
\[
B(x,\varepsilon/3) = \{ z \in X \mid d(z,x) < \varepsilon/3 \}
\quad\text{and}\quad
B(y,\varepsilon/3) = \{ z \in X \mid d(z,y) < \varepsilon/3 \}.
\]
The claim is that these two sets are disjoint.

Assume for contradiction that the two open balls intersect. Then there exists a point $z \in X$ such that $z \in B(x,\varepsilon/3)$ and $z \in B(y,\varepsilon/3)$. By the definition of open ball, the membership $z \in B(x,\varepsilon/3)$ means that
\[
d(z,x) < \varepsilon/3,
\]
and the membership $z \in B(y,\varepsilon/3)$ means that
\[
d(z,y) < \varepsilon/3.
\]

Using the triangle inequality for the metric $d$, applied to the points $x,z,y$, we obtain
\[
d(x,y) \le d(x,z) + d(z,y).
\]
Substituting the strict inequalities for $d(x,z)$ and $d(z,y)$ into the right-hand side, we find
\[
d(x,y) \le d(x,z) + d(z,y) < \varepsilon/3 + \varepsilon/3 = 2\varepsilon/3.
\]

On the other hand, by hypothesis we have $d(x,y) = \varepsilon$. Combining this with the strict inequality above gives
\[
\varepsilon = d(x,y) < 2\varepsilon/3.
\]
Since $\varepsilon > 0$, we may divide both sides of this inequality by $\varepsilon$ and obtain
\[
1 < 2/3,
\]
which is impossible.

This contradiction arises from the assumption that a point $z$ lies in the intersection of $B(x,\varepsilon/3)$ and $B(y,\varepsilon/3)$. Therefore no such $z$ exists, and the intersection of the two open balls is empty. In other words,
\[
B(x,\varepsilon/3) \cap B(y,\varepsilon/3) = \varnothing.
\]