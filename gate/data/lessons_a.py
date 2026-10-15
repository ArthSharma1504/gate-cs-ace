"""Built-in lessons: General Aptitude and Engineering Mathematics."""

GA = "General Aptitude"
EM = "Engineering Mathematics"

LESSONS = {
    # ================================================================ GA
    (GA, "Verbal: grammar, vocabulary, sentence completion"): """
### The idea
GATE verbal questions test everyday grammar and precise word meaning, not rare vocabulary. Most questions are
fill-in-the-blank or "pick the correct sentence".

**Rules that cover most questions**
- **Subject–verb agreement:** find the real subject. "The list of items *is* on the desk" (subject = list).
- **Either/neither … or/nor:** the verb follows the nearer subject. "Neither the teacher nor the *students were* late."
- **Collective nouns** (team, committee) usually take a singular verb.
- **"One of the + plural noun"** takes a singular verb: "One of the books *is* missing."
- **Tense consistency:** don't switch tense in one sentence without a reason.
- **Prepositions that GATE likes:** *comply with, independent of, different from, superior to, prefer A to B*.

### Worked example
*"Each of the candidates ___ given an admit card."* (a) were (b) are (c) was (d) have been
"Each" is singular → **was**.

### Exam traps
- Options that are *near-synonyms* with different tone (e.g. *frugal* vs *stingy*). Read the whole sentence for tone.
- Don't pick an option because it "sounds fancy". Plain, grammatical English wins.
""",
    (GA, "Verbal: reading comprehension & critical reasoning"): """
### The idea
You get a short passage and must pick what it **implies**, **assumes** or what **can be inferred**. The answer must be
supported by the passage alone — not by your general knowledge.

**Question types**
- *Inference:* what must be true given the passage.
- *Assumption:* an unstated idea the argument needs to work.
- *Main idea:* the one option that covers the whole passage, not just one line.

### Worked example
Passage: "Cities that expanded metro lines saw a fall in road accidents."
Which can be inferred? (a) Metros cause fewer accidents (b) Accidents fell in some cities with metro expansion
(c) All cities should build metros (d) Road safety laws failed
Only **(b)** restates what is supported. (a) claims causation, (c) is a recommendation, (d) is not mentioned.

### Exam traps
- **Extreme words** (always, never, all, only) are usually wrong.
- Correlation is not causation — options claiming "X causes Y" are rarely supported.
""",
    (GA, "Quantitative: percentages, ratios, time & work, speed"): """
### The idea
Arithmetic questions reward a few reusable formulas and careful units.

**Percentages**
- Successive changes of a% and b%: net = a + b + ab/100.
- Price up r% → to keep spending fixed, cut consumption by r/(100 + r) × 100 %.

**Time & work**
- Convert to **rates**: a person who finishes in d days does 1/d per day. Add rates, then invert.

**Speed**
- Distance = speed × time. Same direction: subtract speeds. Opposite: add.
- Train crossing a pole covers its own length; crossing a platform covers train + platform.
- 1 km/h = 5/18 m/s.

### Worked example
A pipe fills a tank in 6 h; a leak empties it in 9 h. Both open: rate = 1/6 − 1/9 = 1/18 → **18 hours**.

### Exam traps
- Mixing km/h and m/s.
- Averaging speeds: for equal distances, average speed = 2xy/(x + y), **not** (x + y)/2.
""",
    (GA, "Quantitative: permutations, probability, number series"): """
### The idea
- **Arrangements** (order matters): nPr = n!/(n − r)!. With repeated letters: n!/(p!·q!…).
- **Selections** (order doesn't matter): nCr = n!/(r!(n − r)!).
- **Circular arrangement** of n people: (n − 1)!.
- **Probability** = favourable / total equally likely outcomes. "At least one" → 1 − P(none).
- **Series:** check differences, then second differences, then ratios, then patterns like n², n(n+1), primes.

### Worked example
Probability of at least one head in 3 coin tosses = 1 − (1/2)³ = **7/8**.

### Exam traps
- Forgetting to divide by repeats (e.g. arrangements of BANANA = 6!/(3!·2!) = 60).
- Treating dependent events as independent (drawing without replacement).
""",
    (GA, "Analytical: logical deduction, syllogisms, puzzles"): """
### The idea
**Syllogisms:** draw Venn diagrams. A conclusion "must follow" only if it is true in **every** possible drawing.

- "All A are B" → circle A inside B.
- "Some A are B" → circles overlap (at least partly).
- "No A is B" → circles apart.

**Arrangement puzzles:** write every clue as a constraint, fix the most restrictive clue first, then fill the rest.

### Worked example
All cats are animals. Some animals are pets. Does "some cats are pets" follow?
Draw pets overlapping animals but outside cats → still consistent. So it does **not** follow.

### Exam traps
- Reading "some" as "some but not all". In logic, "some" allows "all".
- Using real-world knowledge instead of the given statements.
""",
    (GA, "Spatial: rotations, patterns, paper folding"): """
### The idea
Spatial questions show shapes that are rotated, mirrored, folded or arranged in a pattern.

- **Rotation** keeps handedness: a clockwise arrangement stays clockwise. **Mirror image** reverses it.
- **Paper folding with a hole punch:** unfold one fold at a time; each unfold mirrors the holes across that fold line.
- **Cube nets:** faces opposite each other never share an edge in the net; in a straight strip of faces, alternate faces are opposite.

### Worked example
A square is folded in half vertically, then a hole is punched near the right edge. Unfolded, there are **2** holes,
mirror images across the fold.

### Exam traps
- Confusing rotation with reflection — check whether a small marker (dot, arrow) flipped sides.
- Counting the number of folds instead of tracing them: n folds → up to 2ⁿ holes.
""",
    (GA, "Data interpretation: tables, graphs, charts"): """
### The idea
Read the chart's **units and labels** first, then compute only what the question asks.

- Percentage change = (new − old)/old × 100.
- Share of total = part/total × 100.
- **Ratio questions:** simplify early; approximate when options are far apart.

### Worked example
Sales went 120 → 150. Growth = 30/120 = **25%** (not 30/150 = 20%).

### Exam traps
- Units in the legend ("in thousands", "in ₹ crore").
- Using the wrong base year for percentage change.
- Pie charts: angles are out of 360°, not 100.
""",
    # ================================================================ EM
    (EM, "Propositional & first-order logic"): """
### The idea
**Propositional logic** combines true/false statements with ¬ (not), ∧ (and), ∨ (or), → (implies), ↔ (iff).

- p → q is false **only** when p is true and q is false.
- p → q ≡ ¬p ∨ q ≡ ¬q → ¬p (contrapositive). Converse (q → p) is **not** equivalent.
- De Morgan: ¬(p ∧ q) ≡ ¬p ∨ ¬q.
- **Tautology:** true in every row. **Contradiction:** false in every row.

**First-order logic** adds ∀ (for all) and ∃ (there exists).
- ¬∀x P(x) ≡ ∃x ¬P(x);  ¬∃x P(x) ≡ ∀x ¬P(x).
- ∀x ∀y and ∃x ∃y can swap; **∀x ∃y is not the same as ∃y ∀x**.
- "Every student loves some course": ∀s ∃c Loves(s, c).

### Worked example
Is (p ∧ (p → q)) → q a tautology? If the left side is true, p is true and p → q is true, so q must be true.
Yes — this is *modus ponens*.

### Exam traps
- ∃y ∀x P(x, y) → ∀x ∃y P(x, y) is valid; the reverse is not.
- "Only if": "p only if q" means p → q.
""",
    (EM, "Sets, relations, functions"): """
### The idea
A **relation** on set A is a subset of A × A. Properties:
- Reflexive: every (a, a) present. Symmetric: (a, b) ⇒ (b, a). Antisymmetric: (a, b) and (b, a) ⇒ a = b.
- Transitive: (a, b), (b, c) ⇒ (a, c). **Equivalence relation** = reflexive + symmetric + transitive.

**Counting on an n-element set**
- All relations: 2^(n²). Reflexive: 2^(n² − n). Symmetric: 2^(n(n+1)/2).
- Equivalence relations on n elements = number of partitions (Bell number): B₃ = 5, B₄ = 15.

**Functions f: A → B** (|A| = m, |B| = n)
- Total functions nᵐ. One-one: n!/(n − m)! (m ≤ n). Onto: Σₖ (−1)ᵏ C(n, k)(n − k)ᵐ.

### Worked example
Onto functions from a 4-element set to a 2-element set = 2⁴ − 2 = **14** (remove the two constant functions).

### Exam traps
- An empty relation is symmetric and transitive but not reflexive (on a non-empty set).
- Antisymmetric ≠ "not symmetric". A relation can be both symmetric and antisymmetric (e.g. the identity).
""",
    (EM, "Partial orders & lattices"): """
### The idea
A **partial order** (poset) is reflexive, antisymmetric and transitive — e.g. ⊆ on sets, divisibility on integers.
Draw it as a **Hasse diagram** (omit self-loops and implied edges; smaller elements lower).

- **Lattice:** every pair has a least upper bound (join, ∨) and greatest lower bound (meet, ∧).
- **Bounded:** has a top (1) and bottom (0).
- **Complement** of a: an element b with a ∨ b = 1 and a ∧ b = 0.
- **Distributive** lattices have at most one complement per element. A **Boolean algebra** is complemented and distributive.

### Worked example
Divisors of 30 under divisibility: {1, 2, 3, 5, 6, 10, 15, 30}. Join = lcm, meet = gcd. 30 = 2·3·5 is square-free,
so every element has a complement (complement of 6 is 5) → it's a **Boolean algebra** (isomorphic to subsets of a 3-set).

### Exam traps
- Divisors of n form a Boolean algebra **only** when n is square-free.
- The pentagon N₅ and diamond M₃ are the classic non-distributive lattices.
""",
    (EM, "Monoids & groups"): """
### The idea
For a set with an operation ∗:
- **Semigroup:** closed + associative. **Monoid:** + identity. **Group:** + every element has an inverse.
- **Abelian:** also commutative.

**Key theorems**
- Lagrange: the order of a subgroup divides the order of the group.
- Every group of prime order p is cyclic (and abelian).
- In a cyclic group of order n, there are φ(n) generators.
- If every element satisfies a² = e, the group is abelian.

### Worked example
(ℤ₁₀, + mod 10) is cyclic. Generators = numbers coprime to 10 = {1, 3, 7, 9} → φ(10) = **4**.

### Exam traps
- (ℤ, −) is not even associative. (ℕ, +) has no inverses.
- {1, −1, i, −i} under multiplication is a cyclic group of order 4 (generator i).
""",
    (EM, "Graphs: connectivity, matching, colouring"): """
### The idea
- **Handshake:** Σ degree = 2|E| → the number of odd-degree vertices is even.
- **Trees:** n vertices, n − 1 edges, connected and acyclic.
- **Connectivity:** a graph with n vertices and more than (n−1)(n−2)/2 edges must be connected.
- **Euler circuit:** connected + all degrees even. **Euler path:** exactly 0 or 2 odd vertices.
- **Planar:** v − e + f = 2; simple planar graph has e ≤ 3v − 6 (e ≤ 2v − 4 if no triangles). K₅ and K₃,₃ are not planar.
- **Colouring:** χ(Kₙ) = n, bipartite (with ≥1 edge) = 2, odd cycle = 3, any planar graph ≤ 4.
- **Matching:** a set of edges with no shared vertex. Perfect matching covers all vertices (needs even n).

### Worked example
Can a simple graph have degrees (3, 3, 3, 1)? Sum = 10 → 5 edges. Each degree-3 vertex connects to all 3 others,
so vertex 4 would have degree 3, not 1. **Not graphical.** (Use Havel–Hakimi to check systematically.)

### Exam traps
- Kₙ has n(n−1)/2 edges; number of perfect matchings in K₂ₙ is (2n − 1)!! = 1·3·5·…·(2n − 1).
- χ of a bipartite graph is 2 only if it has at least one edge.
""",
    (EM, "Combinatorics: counting, recurrences, generating functions"): """
### The idea
- **Stars and bars:** non-negative integer solutions of x₁ + … + xₖ = n is C(n + k − 1, k − 1).
- **Inclusion–exclusion:** |A ∪ B ∪ C| = Σ|A| − Σ|A ∩ B| + |A ∩ B ∩ C|.
- **Pigeonhole:** n + 1 items in n boxes → some box has ≥ 2.
- **Linear recurrences:** for aₙ = c₁aₙ₋₁ + c₂aₙ₋₂, solve r² = c₁r + c₂.
  Distinct roots → A·r₁ⁿ + B·r₂ⁿ; repeated root r → (A + Bn)rⁿ.
- **Generating functions:** 1/(1 − x) = Σ xⁿ; 1/(1 − x)ᵏ has coefficient C(n + k − 1, k − 1).
- **Catalan numbers** Cₙ = C(2n, n)/(n + 1): 1, 1, 2, 5, 14, 42 — counts BSTs, balanced parentheses, triangulations.

### Worked example
Binary strings of length n with no two consecutive 1s: aₙ = aₙ₋₁ + aₙ₋₂, a₁ = 2, a₂ = 3 → a₅ = **13**.

### Exam traps
- Derangements: Dₙ = (n − 1)(Dₙ₋₁ + Dₙ₋₂); D₄ = 9.
- Positive vs non-negative solutions: for xᵢ ≥ 1 use C(n − 1, k − 1).
""",
    (EM, "Matrices, determinants, linear systems"): """
### The idea
- det(AB) = det A · det B; det(Aᵀ) = det A; det(kA) = kⁿ det A for n × n.
- Swapping two rows flips the sign; adding a multiple of one row to another doesn't change det.
- **Rank** = number of non-zero rows after row reduction.
- For Ax = b with n unknowns:
  - rank A ≠ rank [A|b] → **no solution**
  - rank A = rank [A|b] = n → **unique**
  - rank A = rank [A|b] < n → **infinitely many**
- Homogeneous Ax = 0 always has x = 0; it has non-trivial solutions iff det A = 0.

### Worked example
x + y = 2, 2x + 2y = k. Rank A = 1. If k = 4, rank [A|b] = 1 → infinite solutions; otherwise none.

### Exam traps
- A matrix with two equal or proportional rows has det 0.
- For a 3 × 3 skew-symmetric matrix, det = 0 always (odd order).
""",
    (EM, "Eigenvalues & eigenvectors, LU decomposition"): """
### The idea
Av = λv for a non-zero v. Find λ from det(A − λI) = 0.

- Σλ = trace, Πλ = det. Triangular/diagonal matrix: eigenvalues = diagonal entries.
- Aᵏ has λᵏ; A⁻¹ has 1/λ; A + cI has λ + c.
- Real symmetric matrices: real eigenvalues, orthogonal eigenvectors.
- Distinct eigenvalues → eigenvectors linearly independent → diagonalizable.
- **Cayley–Hamilton:** every matrix satisfies its own characteristic equation.

**LU decomposition:** A = LU with L lower-triangular (1s on diagonal, Doolittle) and U upper-triangular.
Solve Ax = b by Ly = b (forward) then Ux = y (backward).

### Worked example
A = [[2, 1], [1, 2]]: trace 4, det 3 → λ² − 4λ + 3 = 0 → λ = **1, 3**.

### Exam traps
- Eigenvalues of A and Aᵀ are equal; eigenvectors usually aren't.
- A singular matrix has 0 as an eigenvalue.
""",
    (EM, "Calculus: limits, continuity, differentiability"): """
### The idea
- Standard limits: sin x / x → 1, (1 + x)^(1/x) → e, (eˣ − 1)/x → 1 as x → 0.
- **L'Hôpital:** for 0/0 or ∞/∞, differentiate top and bottom.
- **Continuity at a:** limit from left = limit from right = f(a).
- **Differentiable ⇒ continuous**, not the other way: |x| is continuous but not differentiable at 0.

### Worked example
lim(x→0) (1 − cos x)/x² = lim sin x/(2x) = **1/2** (L'Hôpital once).

### Exam traps
- Check one-sided limits for |x|, floor and piecewise functions.
- ∞ − ∞ and 1^∞ need rewriting before L'Hôpital.
""",
    (EM, "Calculus: maxima/minima, mean value theorem, integration"): """
### The idea
- Critical points: f′(x) = 0 (or undefined). f″ > 0 → local min, f″ < 0 → local max.
- **Global max/min on [a, b]:** compare f at critical points **and** at a, b.
- **Rolle:** f(a) = f(b) ⇒ some c with f′(c) = 0. **MVT:** f′(c) = (f(b) − f(a))/(b − a).
- **Integration:** by parts ∫u dv = uv − ∫v du; ∫₀^a f(x)dx = ∫₀^a f(a − x)dx;
  odd function over [−a, a] integrates to 0.

### Worked example
MVT for f(x) = x² on [1, 3]: (9 − 1)/2 = 4 = 2c → **c = 2**.

### Exam traps
- Forgetting the endpoints when asked for the global maximum.
- Improper integrals: ∫₁^∞ 1/xᵖ converges only for p > 1.
""",
    (EM, "Random variables & distributions (uniform, normal, exponential, Poisson, binomial)"): """
### The idea
| Distribution | Mean | Variance | Use |
|---|---|---|---|
| Binomial(n, p) | np | np(1 − p) | successes in n trials |
| Poisson(λ) | λ | λ | count of rare events; P(k) = e^(−λ) λᵏ/k! |
| Uniform(a, b) | (a + b)/2 | (b − a)²/12 | equally likely values |
| Exponential(rate λ) | 1/λ | 1/λ² | waiting time; P(X > x) = e^(−λx), memoryless |
| Normal(μ, σ²) | μ | σ² | 68–95–99.7% within 1, 2, 3 σ |

- E[aX + b] = aE[X] + b; Var(aX + b) = a² Var(X).
- Independent X, Y: Var(X + Y) = Var X + Var Y.

### Worked example
Calls arrive at 3 per hour (Poisson). P(no call in an hour) = e^(−3) ≈ **0.0498**.

### Exam traps
- Exponential "mean 5" means rate 1/5.
- For continuous variables, P(X = a) = 0.
""",
    (EM, "Mean, median, mode, standard deviation"): """
### The idea
- **Mean** = Σx/n; **median** = middle value of sorted data (average of the two middle ones if n is even);
  **mode** = most frequent value.
- **Variance** = average of (x − mean)² = E[X²] − (E[X])². SD = √variance.
- Adding a constant shifts mean/median/mode but leaves SD unchanged; multiplying by k scales SD by |k|.

### Worked example
Data 2, 4, 4, 4, 5, 5, 7, 9: mean = 40/8 = 5; squared deviations sum = 9+1+1+1+0+0+4+16 = 32;
population variance = 4 → **SD = 2**.

### Exam traps
- Population variance divides by n; sample variance divides by n − 1. GATE usually states which.
""",
    (EM, "Conditional probability & Bayes' theorem"): """
### The idea
- P(A | B) = P(A ∩ B)/P(B).
- **Total probability:** P(B) = Σ P(B | Aᵢ) P(Aᵢ) over a partition.
- **Bayes:** P(Aᵢ | B) = P(B | Aᵢ) P(Aᵢ) / P(B).
- Independent ⇔ P(A ∩ B) = P(A) P(B).

### Worked example
Box 1: 3 red, 2 blue. Box 2: 1 red, 4 blue. Pick a box at random, draw red. P(box 1)?
P(red) = ½·⅗ + ½·⅕ = ⅖. P(box 1 | red) = (½·⅗)/(⅖) = **¾**.

### Exam traps
- Mutually exclusive events (with non-zero probability) are **not** independent.
- Low base rates make most positive test results false positives — always weight by the prior.
""",
}
