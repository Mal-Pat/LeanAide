## Theorem
If ac is bc modulo mc, then prove that a is b modulo m for c > 0.
-/

/- ## Text Proof
Assume $c>0$ and that $ac$ is congruent to $bc$ modulo $mc$. By the definition of congruence modulo $mc$, this means that $mc$ divides $ac-bc$. Hence there exists an integer $k$ such that
\[
ac - bc = (a-b)c = kmc.
\]
Thus we have the equality
\[
(a-b)c = (km)c.
\]

Since $c>0$, it follows that $c\neq 0$. We can therefore cancel the factor $c$ from both sides of the equality. This implies
\[
a - b = km.
\]
Hence $m$ divides $a-b$. By the definition of congruence modulo $m$, this means that $a$ is congruent to $b$ modulo $m$.