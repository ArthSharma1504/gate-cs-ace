"""High-yield revision sheets: formulas, facts and common traps per subject."""

NOTES = {
    "General Aptitude": """
**Exam shape:** 10 questions, 15 marks (5 × 1-mark, 5 × 2-mark). The easiest 15 marks in the paper — never skip GA practice.

**Quantitative**
- Percentage change in consumption to keep spend fixed after a price rise of r%: r/(100 + r) × 100.
- Successive changes a% and b%: a + b + ab/100.
- Time & work: add rates (1/days), not days. Pipes that empty a tank have negative rates.
- Relative speed: same direction subtract, opposite direction add. A train crossing a platform covers train + platform length.
- Average of an arithmetic progression = middle term = (first + last)/2.
- Clock angle at H:M = |30H − 5.5M|. Hands overlap every 720/11 minutes.
- Arrangements with repeats: n!/(p!q!…). Circular arrangements: (n − 1)!.
- nCr = n!/(r!(n − r)!). "At least one" problems → 1 − P(none).

**Verbal**
- *Neither/either…nor/or*: verb agrees with the nearer subject.
- Collective nouns usually take singular verbs; "a number of" takes plural, "the number of" singular.
- Read every option in sentence-completion questions; GATE likes near-synonyms with different connotations.

**Analytical**
- Syllogisms: draw Venn diagrams and look for a counter-example. "Some A are B" never forces anything about a third set.
- Data interpretation: compute ratios before absolute values; units in table headers are a frequent trap.
""",
    "Engineering Mathematics": """
**Weight:** 13 marks, officially.

**Discrete maths**
- Relations on an n-element set: total 2^(n²); reflexive 2^(n² − n); symmetric 2^(n(n+1)/2); antisymmetric 2^n · 3^(n(n−1)/2).
- Functions from A (m) to B (n): n^m. Injective: n!/(n − m)! for m ≤ n. Bijections between n-sets: n!.
- Surjections from m onto n: Σ (−1)^k C(n, k)(n − k)^m.
- Partial order = reflexive + antisymmetric + transitive. Lattice: every pair has a lub and glb.
- Group: closure, associativity, identity, inverses. Order of a subgroup divides the group order (Lagrange). Every group of prime order is cyclic.
- Handshake lemma: Σ deg(v) = 2|E|. A tree with n vertices has n − 1 edges.
- Euler circuit ⇔ connected and every vertex has even degree. Planar: |E| ≤ 3|V| − 6, and v − e + f = 2.
- Chromatic number: bipartite = 2, odd cycle = 3, Kₙ = n.
- Linear recurrence with distinct roots r₁, r₂: aₙ = A·r₁ⁿ + B·r₂ⁿ. Repeated root r: (A + Bn)rⁿ.
- Derangements: Dₙ = n! Σ (−1)^k / k!. D₃ = 2, D₄ = 9, D₅ = 44.

**Linear algebra**
- Σ eigenvalues = trace; Π eigenvalues = determinant. Triangular matrix → eigenvalues are the diagonal.
- A x = b: unique solution ⇔ det A ≠ 0 ⇔ rank A = n. Consistent ⇔ rank A = rank [A|b].
- Eigenvalues of Aᵏ are λᵏ; of A⁻¹ are 1/λ. Symmetric matrices have real eigenvalues.

**Calculus**
- L'Hôpital for 0/0 or ∞/∞. lim sin x / x = 1.
- Critical points: f′ = 0. f″ < 0 → local max. Always check the interval endpoints.
- ∫ x eˣ dx = (x − 1)eˣ. Integration by parts: ∫u dv = uv − ∫v du.

**Probability & statistics**
- Bayes: P(A|B) = P(B|A)P(A) / P(B).
- Binomial: mean np, variance np(1 − p). Poisson(λ): mean = variance = λ, P(0) = e^(−λ).
- Exponential(mean μ): P(X > x) = e^(−x/μ), memoryless. Uniform(a, b): mean (a + b)/2, variance (b − a)²/12.
- Var(X) = E[X²] − (E[X])². Fair die: mean 3.5, variance 35/12.
""",
    "Digital Logic": """
- NAND and NOR are each universal.
- n variables → 2^(2ⁿ) Boolean functions. Self-dual functions: 2^(2^(n−1)).
- K-map: group in powers of two, wrap edges, use don't-cares only if they enlarge a group.
- Consensus theorem: AB + A′C + BC = AB + A′C.
- 2ⁿ:1 MUX from 2:1 MUXes needs 2ⁿ − 1 of them. A 2ⁿ:1 MUX can implement any function of n + 1 variables.
- Ripple-carry adder delay grows linearly with n; carry-lookahead reduces it to logarithmic.
- Flip-flops: SR (S = R = 1 invalid), JK (11 toggles), D (Q⁺ = D), T (Q⁺ = T ⊕ Q).
- Counters: ring counter n states, Johnson counter 2n states, n-bit binary counter 2ⁿ states.
- Two's complement range: −2^(n−1) … 2^(n−1) − 1. Overflow when two operands of the same sign give a result of the other sign.
- IEEE 754 single: 1 sign, 8 exponent (bias 127), 23 fraction. Double: 1, 11 (bias 1023), 52.
- Exponent all 1s: ∞ (fraction 0) or NaN. Exponent all 0s: zero or denormal (no hidden 1).
""",
    "Computer Organization & Architecture": """
- CPU time = instructions × CPI × clock period.
- Pipeline (k stages, n instructions, no stalls): (k + n − 1) cycles. Ideal speedup → k.
- With stalls: CPI = 1 + stall cycles per instruction. Speedup = k / (1 + stalls per instruction) when stages are balanced.
- Pipeline clock = slowest stage + latch delay.
- Hazards: structural, data (RAW true, WAR anti, WAW output), control. Forwarding fixes most RAW hazards except load-use.
- Cache address split: tag | index | offset. Offset = log₂(block). Index = log₂(sets). Sets = lines / associativity.
- Fully associative: no index bits. Direct mapped: associativity 1.
- Hierarchical access: T = h·t_c + (1 − h)(t_c + t_m). Simultaneous access: T = h·t_c + (1 − h)·t_m.
- Write-through vs write-back (dirty bit). Write-allocate usually pairs with write-back.
- Miss types: compulsory, capacity, conflict (the three Cs).
- Interrupt-driven I/O vs DMA. DMA modes: burst, cycle stealing, transparent.
- Microprogrammed control is flexible but slower; hardwired is fast but rigid. Horizontal microcode = wide control words, little decoding.
""",
    "Programming & Data Structures": """
- C passes everything by value; pointers simulate pass-by-reference.
- `static` locals keep their value between calls and are initialised once.
- `a[i]` ≡ `*(a + i)`; `sizeof(array)` inside the declaring scope is the full array size, but in a function parameter it is a pointer.
- `x++` returns the old value; avoid expressions that modify a variable twice between sequence points (undefined behaviour).
- Naive Fibonacci recursion makes 2·F(n+1) − 1 calls (with F(1) = F(2) = 1).
- Stack: LIFO, used for recursion, expression evaluation and balancing brackets. Queue: FIFO, used in BFS.
- Circular queue of size n (one slot kept empty) holds n − 1 items.
- Binary tree of height h (root = 0): at most 2^(h+1) − 1 nodes. n nodes → minimum height ⌊log₂ n⌋.
- Full binary tree: leaves = internal nodes + 1. In any binary tree, n₀ = n₂ + 1.
- Number of distinct binary trees / BSTs on n keys: Catalan number C(2n, n)/(n + 1).
- Inorder of a BST is sorted. Preorder + inorder (or postorder + inorder) identifies a binary tree uniquely.
- Binary heap: insert O(log n), extract O(log n), build O(n). Array indices (0-based): children 2i + 1, 2i + 2.
- Adjacency matrix: Θ(V²) space; adjacency list: Θ(V + E).
""",
    "Algorithms": """
**Master theorem** for T(n) = aT(n/b) + f(n), compare f(n) with n^(log_b a):
1. Smaller polynomially → Θ(n^(log_b a)).
2. Equal, f = Θ(n^(log_b a) · logᵏ n) → Θ(n^(log_b a) · log^(k+1) n).
3. Larger (with regularity) → Θ(f(n)).

**Sorting**
| Algorithm | Best | Average | Worst | Stable | In place |
|---|---|---|---|---|---|
| Insertion | n | n² | n² | yes | yes |
| Merge | n log n | n log n | n log n | yes | no |
| Quick | n log n | n log n | n² | no | yes |
| Heap | n log n | n log n | n log n | no | yes |
| Counting/Radix | n + k | n + k | n + k | yes | no |

- Comparison sorting lower bound: Ω(n log n). Binary search: ⌊log₂ n⌋ + 1 comparisons worst case.
- Hashing with chaining: expected O(1 + α). Linear probing suffers primary clustering.
- BFS/DFS: O(V + E) with lists. BFS gives shortest paths in unweighted graphs.
- Dijkstra: O((V + E) log V) with a binary heap; fails with negative edges. Bellman-Ford: O(VE), detects negative cycles.
- Floyd-Warshall O(V³). Prim O(E log V), Kruskal O(E log E).
- MST with distinct weights is unique. The lightest edge across any cut is in some MST.
- DP classics: LCS O(mn), 0/1 knapsack O(nW), matrix chain O(n³), edit distance O(mn).
- Greedy classics: activity selection, Huffman, fractional knapsack, Kruskal/Prim, Dijkstra.
""",
    "Theory of Computation": """
- Chomsky hierarchy: Regular ⊂ DCFL ⊂ CFL ⊂ CSL ⊂ Recursive ⊂ RE.
- DFA = NFA = ε-NFA = regular expression in power. NFA with n states → DFA with ≤ 2ⁿ states.
- Minimal DFA states = number of Myhill–Nerode equivalence classes.
- Strings ending with a fixed string of length k: k + 1 states. "Count mod m" languages: m states.
- Regular: closed under union, intersection, complement, concatenation, star, reversal, homomorphism.
- CFL: closed under union, concatenation, star, reversal; **not** intersection or complement. CFL ∩ regular is CFL.
- DCFL: closed under complement, **not** union or intersection.
- Non-regular classics: aⁿbⁿ, palindromes, ww, a^(prime). Non-CFL classics: aⁿbⁿcⁿ, ww, a^(n²).
- wwᴿ is CFL but not DCFL; wcwᴿ is DCFL.
- Recursive languages are closed under complement; RE languages are not. L and L̄ both RE → L recursive.
- Undecidable: halting, emptiness/equivalence/regularity of TMs, CFG ambiguity, CFG equivalence, whether a CFG generates all strings.
- Rice's theorem: every non-trivial property of the language of a TM is undecidable.
- Decidable: DFA emptiness/equivalence, CFG membership and emptiness, finiteness of a CFL.
""",
    "Compiler Design": """
- Phases: lexical → syntax → semantic → intermediate code → optimisation → code generation.
- Tokens: keywords, identifiers, operators, constants, punctuation. A string literal is a single token. Comments and whitespace are discarded.
- FIRST(X): terminals that can begin X (plus ε if X ⇒* ε). FOLLOW(A): terminals that can appear right after A; $ ∈ FOLLOW(start).
- LL(1) needs no left recursion and no common prefixes (left-factor). Ambiguous grammars are never LL(1) or LR(k).
- Power: LL(1) ⊂ LR(1); SLR(1) ⊂ LALR(1) ⊂ LR(1). LALR has the same number of states as SLR (LR(0) items).
- Merging LR(1) states into LALR can introduce reduce–reduce conflicts, never new shift–reduce conflicts.
- S-attributed SDD: only synthesised attributes, evaluated bottom-up. L-attributed: inherited attributes from parent/left siblings only.
- Activation records live on the stack: return address, parameters, locals, control/access links.
- Three-address code forms: quadruples, triples, indirect triples. SSA: each variable assigned once.
- Basic block: single entry at the leader, single exit. Leaders: first statement, branch targets, statements after branches.
- Liveness is a backward analysis: in[B] = use[B] ∪ (out[B] − def[B]). Reaching definitions and available expressions are forward.
""",
    "Operating System": """
- fork() n times in sequence → 2ⁿ processes (2ⁿ − 1 children). Threads share code, heap, globals and files; each has its own stack and registers.
- Turnaround = completion − arrival. Waiting = turnaround − burst. Response = first run − arrival.
- SJF/SRTF minimise average waiting time. Round robin: smaller quantum → more context switches; huge quantum → FCFS.
- Critical-section solution needs mutual exclusion, progress and bounded waiting. Peterson's solution satisfies all three for two processes.
- Semaphores: P/wait decrements (blocks if negative), V/signal increments.
- Deadlock conditions: mutual exclusion, hold & wait, no preemption, circular wait. Banker's algorithm avoids deadlock.
- With n processes each needing at most k instances, deadlock is impossible if resources ≥ n(k − 1) + 1.
- Paging: page table size = (virtual address space / page size) × PTE size. Offset bits = log₂ page size.
- EMAT with TLB: h(t_tlb + t_m) + (1 − h)(t_tlb + (levels + 1)·t_m).
- Page replacement: OPT is optimal; LRU and OPT are stack algorithms (no Belady's anomaly); FIFO can suffer Belady's anomaly.
- Thrashing: too little memory per process → page-fault storm. Working-set model prevents it.
- Disk: SSTF can starve requests; SCAN/C-SCAN are fairer. Access time = seek + rotational latency + transfer.
- Inode max file size = (direct + p + p² + p³) × block size, where p = block size / pointer size.
""",
    "Databases": """
- Superkey: determines all attributes. Candidate key: minimal superkey. Attributes on no right-hand side belong to every key.
- Attribute closure X⁺ finds what X determines. Use it to test keys and FD implication.
- 1NF: atomic values. 2NF: no partial dependency on a key. 3NF: for X → A, X is a superkey or A is prime. BCNF: every determinant is a superkey.
- 3NF decomposition can always be lossless and dependency-preserving; BCNF always lossless but not always dependency-preserving.
- Lossless join of R₁, R₂: R₁ ∩ R₂ → R₁ or R₁ ∩ R₂ → R₂.
- Relational algebra: σ select, π project (removes duplicates), ⋈ join, ÷ division ("for all").
- SQL: WHERE filters rows, HAVING filters groups. COUNT(col) ignores NULLs; COUNT(*) does not. NULL = NULL is unknown.
- B+ tree: all data in leaves, leaves linked. Internal order p: p·P + (p − 1)·K ≤ block size.
- Conflict serializability: build the precedence graph; acyclic ⇔ conflict serializable. View serializable ⊇ conflict serializable.
- Recoverable: commit only after the transactions you read from commit. Cascadeless: read only committed data.
- 2PL ⇒ conflict serializable (can deadlock). Strict 2PL ⇒ also cascadeless. Timestamp ordering is deadlock-free.
""",
    "Computer Networks": """
- Transmission delay = L / B. Propagation delay = distance / speed. a = Tp / Tt.
- Stop-and-wait efficiency = 1 / (1 + 2a). Sliding window efficiency = min(1, W / (1 + 2a)).
- Go-Back-N window ≤ 2ᵏ − 1; Selective Repeat window ≤ 2^(k−1).
- CRC: append (degree of generator) zeros, divide using XOR, append the remainder. Detects all burst errors of length ≤ degree.
- Pure ALOHA max throughput 1/(2e) ≈ 18.4%; slotted ALOHA 1/e ≈ 36.8%.
- CSMA/CD: minimum frame size L ≥ 2 · Tp · B. Ethernet minimum frame 64 bytes.
- CIDR /n block: 2^(32 − n) addresses, 2^(32 − n) − 2 usable hosts.
- Fragmentation: fragment data sizes must be multiples of 8 (except the last). Offset field = byte offset / 8. MF = 1 on all but the last fragment.
- Distance vector (Bellman-Ford, count-to-infinity, split horizon helps). Link state (Dijkstra, flooding of LSAs).
- TCP: slow start doubles cwnd each RTT until ssthresh, then +1 MSS per RTT. Timeout → ssthresh = cwnd/2, cwnd = 1. Three duplicate ACKs (Reno) → fast recovery, cwnd = ssthresh.
- TCP header 20–60 bytes; UDP header 8 bytes; IPv4 header 20–60 bytes.
- Ports: HTTP 80, HTTPS 443, DNS 53 (UDP), SMTP 25, FTP 20/21, DHCP 67/68.
- HTTP/1.1 persistent connections by default. DNS can be iterative or recursive.
""",
}
