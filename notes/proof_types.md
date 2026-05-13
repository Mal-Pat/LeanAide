Mathematical proofs have a fairly small number of recurring **logical structures**, though real proofs often combine several of them.

## 1. Direct proof

You prove the conclusion by starting from the hypotheses and deriving it step by step.

**Form:**

Given assumptions (H), prove (C).

Proceed:

[
H \implies \cdots \implies C.
]

Example pattern:

> Suppose (n) is even. Then (n = 2k). Hence (n^2 = 4k^2 = 2(2k^2)), so (n^2) is even.

This is the most basic proof structure.

---

## 2. Proof by contradiction

To prove (P), assume (\neg P), derive a contradiction, and conclude (P).

**Form:**

[
\neg P \implies \bot,
]

therefore (P).

Example:

> Suppose there are finitely many primes. Let them be (p_1,\dots,p_n). Consider (N = p_1\cdots p_n + 1). No (p_i) divides (N), contradicting that every prime divisor of (N) is among the (p_i). Hence there are infinitely many primes.

---

## 3. Proof by contrapositive

To prove (P \implies Q), prove instead

[
\neg Q \implies \neg P.
]

This is often cleaner than direct proof.

Example:

> To prove “if (n^2) is even, then (n) is even”, prove the contrapositive: if (n) is odd, then (n^2) is odd.

This is not the same as contradiction, though the two are closely related.

---

## 4. Proof by cases

You split the situation into exhaustive alternatives and prove the conclusion in each case.

**Form:**

[
A_1 \lor A_2 \lor \cdots \lor A_n,
]

and prove

[
A_i \implies C
]

for each (i).

Example:

> To prove a statement about integers, split into the cases (n) even and (n) odd.

A proof by cases needs two things:

1. the cases cover all possibilities;
2. the conclusion is proved in every case.

---

## 5. Induction

Used to prove statements indexed by natural numbers or recursively defined structures.

### Ordinary induction

To prove (P(n)) for all (n \in \mathbb N):

1. prove the base case (P(0)) or (P(1));
2. prove the induction step (P(n) \implies P(n+1)).

**Form:**

[
P(0), \qquad \forall n,; P(n) \implies P(n+1).
]

Then (\forall n,;P(n)).

### Strong induction

To prove (P(n)), assume all earlier cases:

[
P(0),P(1),\dots,P(n)
]

and prove (P(n+1)).

This is useful when the proof of (P(n+1)) depends on more than just (P(n)).

### Structural induction

Used for recursively defined objects: lists, trees, formulas, expressions, terms, proofs, etc.

Example structure for lists:

1. prove the property for the empty list;
2. prove that if it holds for a list (xs), then it holds for (a :: xs).

This is the natural induction principle for inductive types.

---

## 6. Existence proof

To prove (\exists x,;P(x)), one usually gives a witness (a) and proves (P(a)).

**Form:**

[
\text{Take } x = a. \text{ Then } P(a).
]

Example:

> To prove there exists an even prime, take (2).

There are also **non-constructive existence proofs**, where one proves that something exists without explicitly constructing it, often using contradiction, compactness, choice, or counting.

---

## 7. Uniqueness proof

To prove that there exists a unique object satisfying (P), prove two things:

1. existence: there is some (x) with (P(x));
2. uniqueness: if (P(x)) and (P(y)), then (x = y).

**Form:**

[
\exists x,;P(x)
]

and

[
\forall x y,; P(x) \land P(y) \implies x = y.
]

In symbols:

[
\exists! x,;P(x).
]

---

## 8. Equivalence proof

To prove

[
P \iff Q,
]

prove both directions:

[
P \implies Q
]

and

[
Q \implies P.
]

For several equivalent conditions, one often proves a cycle:

[
P_1 \implies P_2 \implies P_3 \implies P_1.
]

This establishes all three are equivalent.

---

## 9. Proof by construction

You prove something exists by explicitly constructing the required object and verifying it has the desired properties.

Example:

> To prove every finite-dimensional vector space has a basis, one may construct a maximal linearly independent set and show it spans.

In constructive mathematics, this is often preferred over non-constructive existence arguments.

---

## 10. Proof by minimal counterexample

To prove (P(n)) for all (n), suppose not. Then there is a smallest (n) such that (P(n)) fails. Use minimality to derive a contradiction.

**Form:**

Assume

[
\exists n,; \neg P(n).
]

Let (n_0) be the least such counterexample. Then use the fact that (P(k)) holds for all (k < n_0) to contradict (\neg P(n_0)).

This is closely related to strong induction.

---

## 11. Proof by infinite descent

A special form of contradiction: assume a counterexample exists, then produce a smaller counterexample, and repeat. This contradicts well-foundedness.

Typical form:

[
x_0 > x_1 > x_2 > \cdots
]

in a domain where infinite strictly decreasing sequences cannot exist, such as (\mathbb N).

This is common in number theory.

---

## 12. Proof by exhaustion

A finite proof by cases where all possibilities are enumerated.

Example:

> To prove a statement for residues modulo (6), check the cases (0,1,2,3,4,5).

This is proof by cases, but with explicitly finite and usually computational case analysis.

---

## 13. Proof by counting / double counting

Show two quantities are equal by counting the same set in two different ways.

Example structure:

[
\text{Count set } S \text{ by rows}
]

and

[
\text{Count set } S \text{ by columns}.
]

Since both count (|S|), the two expressions are equal.

This is common in combinatorics.

---

## 14. Pigeonhole principle proof

A counting-based structure: if more objects than boxes are distributed among boxes, some box contains at least two objects.

Basic form:

If (n+1) objects are put into (n) boxes, some box contains at least two objects.

Used frequently for existence proofs.

---

## 15. Proof using invariants

Common in algebra, combinatorics, algorithms, games, and topology.

You identify a quantity or property that remains unchanged under allowed moves. Then you show the desired final state would require a different value of the invariant.

Example structure:

1. define invariant (I);
2. show (I) is preserved by every allowed operation;
3. show initial and target configurations have different (I);
4. conclude the target is impossible.

---

## 16. Proof by monotonicity / bounding

You prove a result by finding upper and lower bounds, or by showing a sequence/function is monotone.

Example structure:

[
a_n \leq b_n \leq c_n
]

and both (a_n) and (c_n) tend to (L), hence (b_n \to L).

This includes squeeze arguments, comparison arguments, and order-based proofs.

---

## 17. Proof by reduction

To prove a statement (P), reduce it to a known theorem or previously solved case (Q).

**Form:**

[
Q \implies P,
]

where (Q) is already known.

Example:

> To prove a result for diagonalizable matrices, reduce to the case of diagonal matrices by conjugating.

Reduction is one of the most common high-level structures in advanced mathematics.

Preferred JSON fields:

- `claim`: the current claim (P).
- `reduced_to`: the reduced goal (Q).
- `proof_of_reduction`: proof that solving Q is enough to prove P.
- `proof`: proof of the reduced goal Q.

Do not split this into generic `reduction_steps` and `result_used` fields; named
theorems/results used in the reduction should appear inside `proof_of_reduction`
or `proof`.

---

## 18. Diagram chase

Common in algebra, topology, homological algebra, and category theory.

You prove an element has a desired property by following it through maps in a commutative diagram.

Typical steps:

1. start with an element in one object;
2. apply maps around the diagram;
3. use commutativity and exactness;
4. construct or identify the required element.

---

## 19. Epsilon-delta proof

A special but very important proof structure in analysis.

To prove

[
\lim_{x \to a} f(x) = L,
]

you show:

[
\forall \varepsilon > 0,; \exists \delta > 0,; 0 < |x-a| < \delta \implies |f(x)-L| < \varepsilon.
]

The structure is:

1. let (\varepsilon > 0);
2. choose (\delta) appropriately;
3. verify the implication.

---

## 20. Proof by generic element

To prove two sets are equal, prove mutual inclusion.

[
A = B
]

by proving:

[
A \subseteq B
]

and

[
B \subseteq A.
]

Each inclusion is usually proved by taking a generic element:

> Let (x \in A). Then show (x \in B).

This is one of the standard proof structures in set theory, algebra, topology, and analysis.

---

## 21. Local-to-global proof

You prove a global statement by proving compatible local statements and then gluing them.

Common in topology, geometry, sheaf theory, manifolds, algebraic geometry, PDEs.

Structure:

1. cover the object by local pieces;
2. prove the result on each piece;
3. show the local results agree on overlaps;
4. glue them to obtain the global result.

---

## 22. Maximal/minimal object argument

You choose an object maximal or minimal with respect to some ordering, then show it has the desired property.

Examples:

* maximal linearly independent set;
* maximal ideal;
* shortest path;
* minimal counterexample;
* maximal chain via Zorn’s lemma.

Structure:

1. choose an extremal object;
2. prove that if it failed the desired property, one could improve it;
3. contradict maximality/minimality.

---

## 23. Compactness argument

Common in topology, analysis, logic, and model theory.

Typical topological form:

1. express a global condition using an open cover or family of closed sets;
2. use compactness to pass from infinitely many conditions to finitely many;
3. prove the desired conclusion from the finite subcover or finite intersection property.

In logic, compactness often means reducing satisfiability of an infinite theory to satisfiability of all finite fragments.

---

## 24. Density argument

To prove a statement for all elements of a space, prove it first on a dense subset and then extend by continuity.

Structure:

1. prove the statement for (x) in a dense subset (D);
2. approximate arbitrary (x) by elements of (D);
3. use continuity, boundedness, or closure to pass to the limit.

Common in functional analysis, measure theory, PDEs, and topology.

---

## 25. Approximation argument

Related to density, but broader.

Structure:

1. approximate a complicated object by simpler objects;
2. prove the result for the simpler objects;
3. control the error;
4. pass to the limit.

Examples:

* approximate measurable functions by simple functions;
* approximate continuous functions by polynomials;
* approximate rough functions by smooth functions.

---

## 26. Indirect proof using a universal property

Common in algebra and category theory.

Instead of constructing an object explicitly, show it satisfies the defining universal property.

Example:

To show two products (A \times B) and (P) are isomorphic, show (P) also satisfies the universal property of the product.

Structure:

1. identify the relevant universal property;
2. show the object satisfies it;
3. invoke uniqueness up to unique isomorphism.

---

## 27. Algorithmic proof

You prove a statement by giving an algorithm and proving it terminates and is correct.

Structure:

1. define the algorithm;
2. prove termination;
3. prove partial correctness;
4. conclude total correctness.

This is common in discrete mathematics, logic, and computer science.

---

## 28. Probabilistic proof

You prove existence by showing a randomly chosen object has positive probability of satisfying the desired property.

Structure:

1. define a probability space;
2. estimate the probability of failure;
3. show the probability of success is positive;
4. conclude existence.

Example:

> If (\Pr(\text{good object}) > 0), then at least one good object exists.

---

## 29. Genericity or “almost everywhere” proof

Common in measure theory, topology, algebraic geometry, and dynamical systems.

You prove that the bad set is small:

* measure zero;
* meagre;
* lower-dimensional;
* contained in a proper algebraic subset.

Then conclude the desired property holds generically or almost everywhere.

---

## 30. Diagrammatic or geometric proof

A proof where the main reasoning comes from a geometric construction, diagram, or visual invariant.

Examples include:

* Euclidean geometry proofs;
* knot diagrams;
* commutative diagrams;
* convexity diagrams;
* graph-theoretic drawings.

The proof still needs a logical justification, but the structure is guided by the diagram.

---

# A compact taxonomy

At a high level, many proof structures fall into these families:

| Goal type                              | Common proof structure                               |
| -------------------------------------- | ---------------------------------------------------- |
| Prove (P \implies Q)                   | direct proof, contrapositive, contradiction          |
| Prove (P \lor Q)                       | prove one side, or split cases from hypotheses       |
| Prove (P \land Q)                      | prove both parts separately                          |
| Prove (\forall x,;P(x))                | take arbitrary (x), prove (P(x))                     |
| Prove (\exists x,;P(x))                | construct witness, or use non-constructive existence |
| Prove (\exists!x,;P(x))                | existence plus uniqueness                            |
| Prove (P \iff Q)                       | prove both implications                              |
| Prove statement for all (n)            | induction, strong induction, minimal counterexample  |
| Prove equality of sets                 | prove mutual inclusion                               |
| Prove impossibility                    | contradiction, invariant, parity, descent            |
| Prove finite combinatorial identity    | double counting, bijection, generating functions     |
| Prove global statement from local data | compactness, gluing, local-to-global                 |
| Prove analytic limit statement         | epsilon-delta, approximation, density                |

The most reusable core structures are: **direct proof, contradiction, contrapositive, cases, induction, construction, uniqueness, equivalence, reduction, and invariant arguments**.
