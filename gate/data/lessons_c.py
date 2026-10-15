"""Built-in lessons: TOC, Compiler Design, OS, Databases, Computer Networks."""

TOC = "Theory of Computation"
CD = "Compiler Design"
OS = "Operating System"
DB = "Databases"
CN = "Computer Networks"

LESSONS = {
    # ================================================================ TOC
    (TOC, "Regular expressions & finite automata"): """
### The idea
A **DFA** has exactly one move per symbol from every state; an **NFA** may have several or none (and ε-moves).
DFA, NFA, ε-NFA and regular expressions all describe exactly the **regular languages**.

- NFA → DFA by subset construction: up to 2ⁿ states.
- **Minimal DFA:** merge equivalent states (table-filling / partition refinement). The number of states equals the
  number of Myhill–Nerode classes — "how many different things must I remember?"
- Quick counts: strings ending in a fixed k-length pattern → k + 1 states (+1 dead state never needed);
  "count of a's mod m" → m states; "length exactly k" → k + 2 (including dead state).
- Regex identities: (a + b)* = (a*b*)*, (ab)*a = a(ba)*, r** = r*, ∅* = ε.

### Worked example
Strings over {a, b} containing `aa` as a substring: states "nothing", "seen a", "seen aa" (accepting, absorbing)
→ **3 states**.

### Exam traps
- Minimal DFA counts usually include the dead (trap) state if it's reachable and needed.
- For "divisible by n" in binary, the minimal DFA has n states only if n is odd; for powers of 2 it's fewer.
""",
    (TOC, "Regular languages & pumping lemma"): """
### The idea
**Closure:** regular languages are closed under union, intersection, complement, difference, concatenation, star,
reversal, homomorphism, inverse homomorphism. Every **finite** language is regular.

**Pumping lemma (to prove NOT regular):** if L is regular, there's p such that every s ∈ L with |s| ≥ p splits as
s = xyz with |xy| ≤ p, |y| ≥ 1, and xyⁱz ∈ L for all i ≥ 0. Pick s cleverly and show some i breaks it.

Non-regular classics: aⁿbⁿ, palindromes, ww, a^(n²), a^(prime), balanced parentheses, equal number of a's and b's.
Regular (surprisingly): aⁿbᵐ, (number of a's) mod 3 = 0, strings with equal numbers of `ab` and `ba` substrings.

### Worked example
Is {aⁿ | n ≥ 0}·{bᵐ | m ≥ 0} regular? It's a*b* → **yes**. Is {aⁿbⁿ | n ≤ 100}? Finite → **yes**.

### Exam traps
- The pumping lemma can only prove *non*-regularity; passing it doesn't prove regularity.
- A subset of a regular language need not be regular (aⁿbⁿ ⊂ a*b*).
""",
    (TOC, "Context-free grammars & PDA"): """
### The idea
A **CFG** has rules A → (string of terminals/variables). A **PDA** is an NFA plus a stack; PDAs accept exactly the CFLs.
**Deterministic** PDAs accept the smaller class of DCFLs (every DCFL has an unambiguous grammar).

- **Ambiguous grammar:** some string has two parse trees (two leftmost derivations). E → E + E | E * E | id is ambiguous.
- **Chomsky Normal Form:** rules A → BC or A → a. A string of length n takes exactly 2n − 1 steps to derive.
- **Membership** for CFGs is decidable (CYK, O(n³)).

### Worked example
Grammar for {aⁿbⁿ | n ≥ 1}: **S → aSb | ab**. PDA: push for each a, pop for each b, accept on empty stack.

### Exam traps
- wwᴿ (even palindromes) is a CFL but **not** a DCFL — the PDA must guess the middle. wcwᴿ is a DCFL.
- Some CFLs are inherently ambiguous (e.g. {aⁱbʲcᵏ | i = j or j = k}).
""",
    (TOC, "Context-free languages & closure properties"): """
### The idea
| Operation | Regular | DCFL | CFL | Recursive | RE |
|---|---|---|---|---|---|
| Union | ✓ | ✗ | ✓ | ✓ | ✓ |
| Intersection | ✓ | ✗ | ✗ | ✓ | ✓ |
| Complement | ✓ | ✓ | ✗ | ✓ | ✗ |
| Concatenation | ✓ | ✗ | ✓ | ✓ | ✓ |
| Kleene star | ✓ | ✗ | ✓ | ✓ | ✓ |
| ∩ with regular | ✓ | ✓ | ✓ | ✓ | ✓ |

**CFL pumping lemma:** s = uvwxy with |vwx| ≤ p, |vx| ≥ 1, uvⁱwxⁱy ∈ L. Non-CFL classics: aⁿbⁿcⁿ, ww, a^(n²),
aⁱbʲcᵏ with i < j < k.

### Worked example
L₁ = {aⁿbⁿcᵐ}, L₂ = {aᵐbⁿcⁿ}: both CFLs, but L₁ ∩ L₂ = {aⁿbⁿcⁿ} is **not** — so CFLs aren't closed under ∩.

### Exam traps
- The complement of a CFL may or may not be a CFL — "not closed" means "not always".
""",
    (TOC, "Turing machines"): """
### The idea
A TM has an infinite tape, a head that moves left/right, and states. It can **accept**, **reject** or **loop forever**.

- **Recursive (decidable):** some TM always halts and answers.
- **Recursively enumerable (RE):** some TM accepts every string in L but may loop on strings not in L.
- Multi-tape, non-deterministic and multi-head TMs are all equivalent in power to the basic TM.
- **Linear bounded automata** (tape limited to the input) accept the context-sensitive languages.
- Hierarchy: Regular ⊂ DCFL ⊂ CFL ⊂ CSL ⊂ Recursive ⊂ RE ⊂ all languages.

### Worked example
If both L and its complement are RE, run both TMs in parallel — one must accept, so L is **recursive**.

### Exam traps
- RE is not closed under complement; recursive is.
- There are uncountably many languages but only countably many TMs → most languages are not RE.
""",
    (TOC, "Decidability & undecidability"): """
### The idea
A problem is **decidable** if a TM always halts with the right yes/no answer.

**Undecidable:** halting problem; whether a TM accepts ε / any string / all strings; whether two TMs (or two CFGs)
are equivalent; whether a CFG is ambiguous; whether a CFG generates Σ*; Post correspondence problem.

**Decidable:** DFA/NFA emptiness, finiteness, equivalence, membership; CFG membership, emptiness, finiteness;
whether a TM halts within k steps.

**Rice's theorem:** any non-trivial property of the *language* of a TM is undecidable
(e.g. "is L(M) regular?", "is L(M) empty?"). Properties of the machine itself (e.g. "has 5 states") aren't covered.

**Reductions:** if A reduces to B and A is undecidable, then B is undecidable.

### Worked example
"Does TM M accept the string 0101?" — non-trivial property of L(M) → **undecidable**.
"Does DFA D accept 0101?" — just run it → **decidable**.

### Exam traps
- Complement of the halting problem is not even RE.
- "Is L(G) = ∅" is decidable for CFGs but "L(G) = Σ*" is not.
""",
    # ================================================================ CD
    (CD, "Lexical analysis"): """
### The idea
The lexer reads characters and groups them into **tokens** (keywords, identifiers, constants, operators, punctuation),
using regular expressions implemented as DFAs. It strips whitespace and comments and fills the symbol table.

- **Maximal munch:** take the longest possible match (`>=` is one token, not `>` and `=`).
- Ties go to the rule listed first (so keywords are listed before the identifier rule).
- Lexical errors: illegal characters, unterminated strings.

### Worked example
`x = a+++b;` → tokens: x, =, a, ++, +, b, ; → **7 tokens** (maximal munch makes `++` first).

### Exam traps
- A whole string literal "…" is one token; so is a character constant 'a'.
- Comments are not tokens; `#include` lines are handled by the preprocessor before lexing.
""",
    (CD, "Parsing (LL, LR, FIRST/FOLLOW)"): """
### The idea
**FIRST(α):** terminals that can start strings derived from α (+ ε if α ⇒* ε).
**FOLLOW(A):** terminals that can appear immediately after A; put \\$ in FOLLOW(start).

**LL(1)** (top-down, predictive): table entry M[A, a] for each a in FIRST(α); if ε ∈ FIRST(α), also for FOLLOW(A).
Grammar is LL(1) iff no table cell has two entries. Needs no left recursion and left-factoring.

**LR parsers** (bottom-up, shift–reduce):
- LR(0) items → **SLR(1)** uses FOLLOW sets for reductions.
- **LR(1)** items carry lookaheads (most powerful, most states).
- **LALR(1)** merges LR(1) states with the same core: same state count as SLR, may add reduce–reduce conflicts.
- Power: SLR(1) ⊂ LALR(1) ⊂ LR(1), and every LL(1) grammar is LR(1). LL(1) and LALR(1) are incomparable
  (some LL(1) grammars are not LALR(1)).
- Operator precedence parsing handles expression grammars directly.

### Worked example
S → aSb | ε. FIRST(S) = {a, ε}, FOLLOW(S) = {b, \\$}. Table: M[S, a] = aSb, M[S, b] = M[S, \\$] = ε → **LL(1)**.

### Exam traps
- An ambiguous grammar is never LL(k) or LR(k).
- Count SLR/LALR states = number of LR(0) item sets.
""",
    (CD, "Syntax-directed translation"): """
### The idea
Attach **attributes** to grammar symbols and **semantic rules** to productions.
- **Synthesised** attribute: computed from children (flows up).
- **Inherited** attribute: computed from parent or left siblings (flows down/across).
- **S-attributed** SDD: only synthesised → evaluate during bottom-up (LR) parsing.
- **L-attributed** SDD: inherited ones depend only on parent and left siblings → evaluate in one left-to-right
  depth-first pass (works with LL parsing). Every S-attributed SDD is L-attributed.
- **SDT:** semantic actions embedded in production bodies `{ … }`; their position decides when they run.

### Worked example
E → E₁ + T { print('+') }, E → T, T → num { print(num.val) }. Input `2 + 3 + 4` prints **2 3 + 4 +** (postfix).

### Exam traps
- Actions in the middle of a production execute after the symbols to their left are processed.
""",
    (CD, "Runtime environments"): """
### The idea
Memory layout: code | static/global data | heap (grows up) | … | stack (grows down).

Each procedure call pushes an **activation record**: return address, actual parameters, saved registers, local
variables, temporaries, **control link** (caller's frame) and **access link** (enclosing scope, for nested procedures).

- **Static allocation** can't support recursion. **Stack allocation** supports recursion.
- Heap holds data that outlives the call (malloc/new).
- **Parameter passing:** by value, by reference, by value-result (copy-in copy-out), by name (re-evaluate each use).
- **Scoping:** static (lexical) — look up where the function is *defined*; dynamic — look up the calling chain.

### Worked example
```
int x = 1;
void g() { print(x); }
void f() { int x = 2; g(); }
f();
```
Static scoping prints **1**; dynamic scoping prints **2**.

### Exam traps
- Call-by-reference vs value-result differ when the same variable is passed twice (aliasing).
""",
    (CD, "Intermediate code generation"): """
### The idea
Compilers translate to a machine-independent form before code generation.

- **Three-address code (TAC):** at most one operator on the right, e.g. `t1 = b * c`.
  Stored as **quadruples** (op, arg1, arg2, result), **triples** (results referred to by position) or **indirect triples**.
- **SSA form:** each variable assigned exactly once; φ-functions merge values at join points.
- **Syntax tree vs DAG:** a DAG shares common subexpressions (one node for repeated `b*c`).
- Control flow: `if a < b goto L1` style jumps; backpatching fills in targets later.

### Worked example
`a = (b + c) * (b + c)` as a DAG has nodes b, c, +, *, = — the `+` node is shared, so TAC needs only
**t1 = b + c; a = t1 * t1**.

### Exam traps
- Count the minimum number of temporaries or DAG nodes carefully: identical leaves are one node.
""",
    (CD, "Local optimisation & data-flow analysis (liveness, constant propagation, CSE)"): """
### The idea
**Basic block:** straight-line code with one entry and one exit. **Leaders:** the first statement, any jump target,
any statement right after a jump.

**Local optimisations:** constant folding (`2*3` → 6), constant propagation, common subexpression elimination,
copy propagation, dead-code elimination, strength reduction (`x*2` → `x+x` or shift), algebraic simplification.

**Data-flow analyses**
| Analysis | Direction | Meet | Equation |
|---|---|---|---|
| Liveness | backward | ∪ | in = use ∪ (out − def) |
| Reaching definitions | forward | ∪ | out = gen ∪ (in − kill) |
| Available expressions | forward | ∩ | out = gen ∪ (in − kill) |
| Constant propagation | forward | meet of lattice values | |

A variable is **live** at a point if its current value may be used later before being redefined.

### Worked example
```
1: x = 4
2: y = x + 2
3: x = 7
4: print(y)
```
After constant propagation + folding, y = 6; `x = 7` is dead (x never used after) → **removable**.

### Exam traps
- Liveness flows backwards: start from the uses at the end.
- Register allocation: the max number of simultaneously live variables gives the registers needed.
""",
    # ================================================================ OS
    (OS, "System calls, processes, threads, IPC"): """
### The idea
- **System call:** user program requests a kernel service (mode switch user → kernel), e.g. read, write, fork.
- **Process states:** new → ready → running → waiting → ready … → terminated.
- **fork()** creates a copy: returns 0 in the child, child's PID in the parent. n sequential forks → 2ⁿ processes.
- **exec()** replaces the process image; **wait()** blocks until a child ends. Zombie = dead child not yet waited on;
  orphan = child whose parent died.
- **Threads** share code, data, heap and files; each has its own stack, registers and PC. User-level threads are
  fast to switch but one blocking call blocks all (in many-to-one); kernel threads avoid this.
- **IPC:** shared memory (fast, needs sync) or message passing (pipes, sockets, queues).

### Worked example
```c
if (fork() && fork()) fork();
```
Parent: both forks return non-zero → third fork. First child: `fork()` = 0 → stops. Second child: stops.
Total processes = **4** (parent, 2 children, 1 from the third fork).

### Exam traps
- `fork() || fork()` short-circuits differently from `&&`. Trace return values carefully.
""",
    (OS, "Concurrency & synchronisation"): """
### The idea
A **race condition** happens when the result depends on the interleaving of threads using shared data.
The code touching shared data is the **critical section (CS)**. A correct solution needs:
1. **Mutual exclusion** — one process in the CS at a time.
2. **Progress** — if no one is in the CS, a waiting process can enter (no indefinite postponement by outsiders).
3. **Bounded waiting** — a limit on how many times others can go first.

Tools:
- **Peterson's algorithm** (2 processes, uses flag[] and turn) — satisfies all three.
- **Test-and-set / compare-and-swap** hardware locks (busy waiting, may not ensure bounded waiting).
- **Semaphores:** wait(S) decrements and blocks if negative; signal(S) increments and wakes one.
  Binary semaphore = mutex. Counting semaphore = pool of k resources.
- **Monitors** with condition variables.

Classic problems: producer–consumer (empty, full, mutex), readers–writers, dining philosophers.

### Worked example
Producer–consumer with buffer size N: `empty = N`, `full = 0`, `mutex = 1`.
Producer: wait(empty); wait(mutex); add; signal(mutex); signal(full). Swapping the two waits can **deadlock**.

### Exam traps
- Order of wait() calls matters; order of signal() calls usually doesn't.
- With a counting semaphore starting at S, after a P's and b V's its value is S − a + b.
""",
    (OS, "Deadlock"): """
### The idea
Deadlock needs all four: **mutual exclusion, hold and wait, no preemption, circular wait**.

Handling:
- **Prevention:** break one condition (e.g. request resources in a fixed global order → no circular wait).
- **Avoidance:** **Banker's algorithm** — grant a request only if the system stays in a *safe state*
  (some order lets every process finish). Need = Max − Allocation.
- **Detection & recovery:** find cycles in the wait-for graph; kill or roll back processes.
- **Ignore** (ostrich approach).

Single-instance resources: a cycle in the resource allocation graph ⇔ deadlock.
Multiple instances: a cycle is necessary but not sufficient.

### Worked example
3 processes each need at most 4 units of a resource. Minimum units to guarantee no deadlock =
3 × (4 − 1) + 1 = **10**.

### Exam traps
- Unsafe state ≠ deadlock; it means deadlock is *possible*.
""",
    (OS, "CPU & I/O scheduling"): """
### The idea
Turnaround = completion − arrival. Waiting = turnaround − burst. Response = first run − arrival.

| Algorithm | Preemptive? | Notes |
|---|---|---|
| FCFS | no | convoy effect |
| SJF | no | optimal average waiting time (if bursts known) |
| SRTF | yes | preemptive SJF; optimal average waiting time |
| Priority | either | starvation → fix with aging |
| Round robin (q) | yes | good response; q too small → overhead, too large → FCFS |
| Multilevel (feedback) queue | yes | different queues/algorithms per class |

**Disk scheduling:** FCFS, SSTF (closest first, can starve), SCAN (elevator to the end), LOOK (turn at last request),
C-SCAN / C-LOOK (one direction, jump back).

### Worked example
FCFS: P1 (0, 5), P2 (1, 3), P3 (2, 1). Completion 5, 8, 9 → turnaround 5, 7, 7 → waiting 0, 4, 6 → average **3.33**.

### Exam traps
- In RR, the convention for a process arriving at the same time one is preempted matters — read the question.
- Count context switches only between different processes if asked.
""",
    (OS, "Memory management & virtual memory"): """
### The idea
**Paging:** logical address = page number | offset. Physical = frame number | offset.
- Page table entries = virtual space / page size. Page table size = entries × PTE size.
- **Multi-level paging** keeps page tables small; each level costs one extra memory access.
- **TLB** caches translations: EMAT = h(t_tlb + t_m) + (1 − h)(t_tlb + (L + 1)t_m) for L-level paging.
- **Inverted page table:** one entry per physical frame.

**Virtual memory:** pages loaded on demand; a **page fault** brings the page from disk.
EAT = (1 − p)·t_m + p·(fault service time).

**Page replacement:** FIFO (Belady's anomaly possible), **Optimal** (evict the page used farthest in future),
**LRU** (evict least recently used). LRU and Optimal never show Belady's anomaly.

**Thrashing:** too many processes, too few frames → constant faulting. **Working set** model prevents it.
**Fragmentation:** paging → internal; contiguous allocation/segmentation → external.

### Worked example
36-bit virtual address, 8 KB pages, 4-byte PTEs: entries = 2^(36 − 13) = 2²³ → table = 2²³ × 4 B = **32 MB**.

### Exam traps
- Mixing up offset bits (from page size) and frame bits (from physical memory size).
""",
    (OS, "File systems"): """
### The idea
**Allocation methods**
- **Contiguous:** fast, simple; external fragmentation, hard to grow.
- **Linked:** no fragmentation; slow random access; FAT keeps the links in a table.
- **Indexed (inode):** direct pointers + single, double, triple indirect blocks.
  Max file size = (D + p + p² + p³) × block size, with p = block size / pointer size.

**Directories:** single-level, two-level, tree, acyclic graph (links). **Hard link** = another name for the same inode;
**soft link** = a file containing a path.

**Free-space:** bit vector, linked list, grouping, counting.

### Worked example
4 KB blocks, 4-byte pointers, 10 direct + 1 single indirect: p = 1024 → max = (10 + 1024) × 4 KB = **4136 KB**.

### Exam traps
- Disk accesses to read block k of a file: count the indirect blocks that must be read first.
""",
    # ================================================================ DB
    (DB, "ER model"): """
### The idea
- **Entity set** (rectangle), **attributes** (ovals: simple, composite, multivalued, derived), **relationship set** (diamond).
- **Cardinality:** 1:1, 1:N, M:N. **Participation:** total (double line) or partial.
- **Weak entity:** no key of its own; identified by its **partial key** + the owner's key via an identifying relationship.

**ER → tables (minimum)**
- Each strong entity → one table.
- M:N relationship → its own table (keys of both sides).
- 1:N relationship → put the "1"-side key into the "N"-side table (no new table).
- 1:1 → merge into one side (with total participation, merge into that side).
- Multivalued attribute → separate table.

### Worked example
Student (M) — Enrols — (N) Course, plus Dept (1) — Has — (N) Student: tables Student (with dept_id), Course, Dept,
Enrols → **4 tables**.

### Exam traps
- Minimum-tables questions: 1:1 with total participation on both sides can collapse to a single table.
""",
    (DB, "Relational algebra & tuple calculus"): """
### The idea
| Operator | Meaning |
|---|---|
| σ_cond(R) | select rows |
| π_attrs(R) | project columns (removes duplicates) |
| R × S | cross product (|R|·|S| rows) |
| R ⋈ S | natural join on common attributes |
| R ∪ S, R − S, R ∩ S | need union-compatible schemas |
| R ÷ S | rows of R related to **all** rows of S |
| ρ | rename |

Outer joins keep unmatched rows (filled with NULL): left, right, full.

**Tuple relational calculus:** {t | P(t)}, e.g. {t | t ∈ Student ∧ t.cgpa > 9}. Safe expressions avoid infinite results.

### Worked example
|R| = 10, |S| = 5, no common attributes → R ⋈ S = R × S → **50 rows**.

### Exam traps
- Natural join with no common attributes is a cross product.
- π removes duplicates in relational algebra, but SQL SELECT doesn't (unless DISTINCT).
""",
    (DB, "SQL"): """
### The idea
Evaluation order: **FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY**.

- WHERE filters rows; HAVING filters groups (can use aggregates).
- Aggregates ignore NULLs (except COUNT(*)). Any comparison with NULL is *unknown*; use IS NULL.
- `IN`, `EXISTS`, `ANY`, `ALL` for subqueries. `NOT IN` with a NULL in the subquery returns no rows.
- Correlated subqueries refer to the outer query and run per outer row.
- `UNION` removes duplicates; `UNION ALL` keeps them.

### Worked example
Departments with average salary above 50 000:
```sql
SELECT dept, AVG(salary) FROM emp GROUP BY dept HAVING AVG(salary) > 50000;
```

### Exam traps
- `x > ALL (empty set)` is true; `x > ANY (empty set)` is false.
- Columns in SELECT must be in GROUP BY or inside an aggregate.
""",
    (DB, "Integrity constraints & normal forms"): """
### The idea
**Keys:** superkey (determines everything), candidate key (minimal superkey), primary key (chosen candidate).
Attributes that never appear on the right side of an FD are in **every** key.
**Closure X⁺:** apply FDs repeatedly to find everything X determines.

**Normal forms**
- **1NF:** atomic values.
- **2NF:** no non-prime attribute depends on *part* of a candidate key.
- **3NF:** for every X → A, X is a superkey **or** A is prime.
- **BCNF:** for every X → A, X is a superkey.

**Decomposition** R → R₁, R₂ is lossless if R₁ ∩ R₂ → R₁ or R₁ ∩ R₂ → R₂.
3NF: lossless and dependency-preserving always possible. BCNF: lossless always, dependency preservation not always.

**Constraints:** entity integrity (PK not NULL), referential integrity (FK matches a PK or is NULL),
ON DELETE CASCADE / SET NULL.

### Worked example
R(A, B, C) with A → B, B → C: key A, B → C is transitive → in **2NF, not 3NF**.

### Exam traps
- A relation with only two attributes is always in BCNF.
- Minimal cover: split right sides, remove extraneous left attributes, remove redundant FDs.
""",
    (DB, "File organisation & indexing (B / B+ trees)"): """
### The idea
- **Blocking factor** = ⌊block size / record size⌋. Blocks needed = ⌈records / bf⌉.
- **Primary index** (on the ordering key field, sparse — one entry per block); **clustering index**
  (ordering non-key field); **secondary index** (dense — one entry per record).
- Binary search over b index blocks costs ⌈log₂ b⌉ + 1 accesses (plus the data block).

**B tree** of order p: every node holds keys and data pointers; nodes (except root) at least half full.
**B+ tree:** data pointers only in leaves, leaves linked for range queries → higher fan-out, fewer levels.
- Internal order p: p·(block pointer) + (p − 1)·(key) ≤ block size.
- Leaf order: p_leaf·(key + record pointer) + (next-leaf pointer) ≤ block size.

### Worked example
Block 512 B, key 9 B, block pointer 6 B, record pointer 7 B. Internal: 6p + 9(p − 1) ≤ 512 → p = **34**.
Leaf: 16p + 6 ≤ 512 → p_leaf = **31**.

### Exam traps
- Minimum keys in a non-root B-tree node of order p: ⌈p/2⌉ − 1.
""",
    (DB, "Transactions & concurrency control"): """
### The idea
**ACID:** atomicity, consistency, isolation, durability.

**Serializability**
- Two operations **conflict** if they're from different transactions, on the same item, and at least one is a write.
- **Conflict serializable** ⇔ the precedence graph (Tᵢ → Tⱼ if Tᵢ's op conflicts with and precedes Tⱼ's) is acyclic.
- **View serializable** is a weaker condition (includes blind writes); testing it is NP-complete.

**Recoverability**
- Recoverable: a transaction commits only after every transaction it read from has committed.
- Cascadeless: read only committed data. Strict: no read or write of uncommitted data.

**Protocols**
- **2PL:** growing phase then shrinking phase → conflict serializable, can deadlock.
- **Strict 2PL:** hold X-locks until commit → also strict schedules.
- **Timestamp ordering:** older transaction wins; no deadlock, possible starvation. **Thomas' write rule** ignores obsolete writes.

### Worked example
S: r1(A) w2(A) w1(A). Edges T1→T2 (r1 before w2) and T2→T1 (w2 before w1) → cycle → **not conflict serializable**.

### Exam traps
- Every conflict-serializable schedule is view-serializable; not the reverse.
- Number of conflict-equivalent serial schedules = number of topological orders of the precedence graph.
""",
    # ================================================================ CN
    (CN, "Layering principles"): """
### The idea
Each layer offers services to the layer above and uses the layer below; peers talk through **protocols**.

| TCP/IP layer | OSI layers | Unit | Examples |
|---|---|---|---|
| Application | 7, 6, 5 | message | HTTP, DNS, SMTP |
| Transport | 4 | segment | TCP, UDP (ports) |
| Network | 3 | packet | IP, ICMP, routing |
| Data link | 2 | frame | Ethernet, Wi-Fi (MAC addresses) |
| Physical | 1 | bits | cables, signals |

Each layer adds a header (**encapsulation**). Devices: hub (L1), switch/bridge (L2), router (L3).

### Worked example
A 100-byte message gets a 20-byte TCP header, 20-byte IP header and 18-byte Ethernet header/trailer →
158 bytes on the wire; header overhead = 58/158 ≈ **36.7%**.

### Exam traps
- Process-to-process delivery = transport layer; host-to-host = network layer; hop-to-hop = data link layer.
""",
    (CN, "Switching & performance metrics"): """
### The idea
- **Circuit switching:** reserve a path first (setup delay), then constant rate.
- **Packet switching (datagram):** each packet routed independently, store-and-forward at every hop.
- **Virtual circuit:** packets follow a pre-set path; per-connection state in routers.

**Delays**
- Transmission Tt = L / B. Propagation Tp = distance / signal speed. Queuing + processing at routers.
- Store-and-forward over k links (equal rates): first packet takes k·Tt + Σ Tp; n packets take (n + k − 1)·Tt + Σ Tp.
- **Bandwidth–delay product** = B × Tp bits "in flight".

**Flow control efficiency** (a = Tp/Tt)
- Stop-and-wait: 1/(1 + 2a). Sliding window W: min(1, W/(1 + 2a)).
- Go-Back-N: W ≤ 2ᵏ − 1. Selective Repeat: W ≤ 2^(k−1).

### Worked example
1 Mbps link, 1000-bit frames, Tp = 10 ms: Tt = 1 ms, a = 10 → stop-and-wait efficiency 1/21 ≈ **4.8%**.

### Exam traps
- Throughput = efficiency × bandwidth.
- Bits vs bytes (× 8) and kilo = 1000 for data rates but often 1024 for sizes.
""",
    (CN, "Data link: error detection, MAC, Ethernet"): """
### The idea
**Error detection**
- Parity detects odd numbers of bit errors.
- **CRC:** append (degree of generator) zeros, divide by the generator with XOR, append the remainder.
  Detects all single-bit, all double-bit (good generator), all odd errors (if (x + 1) is a factor), all bursts ≤ degree.
- Hamming distance d: detects d − 1 errors, corrects ⌊(d − 1)/2⌋.
- Hamming code: parity bits r satisfy 2ʳ ≥ m + r + 1.

**MAC protocols**
- Pure ALOHA max 18.4% (1/2e); slotted ALOHA 36.8% (1/e).
- **CSMA/CD** (classic Ethernet): minimum frame ≥ 2 × Tp × B so a collision is detected while still sending.
  Backoff after n collisions: random k in [0, 2ⁿ − 1] slots.
- Token passing avoids collisions.

**Ethernet:** 48-bit MAC addresses, frame 64–1518 bytes, payload 46–1500 bytes.

### Worked example
10 Mbps, 2 km cable, signal speed 2 × 10⁸ m/s: Tp = 10 µs → min frame = 2 × 10 µs × 10⁷ = **200 bits**.

### Exam traps
- Read whether the question gives round-trip or one-way delay.
""",
    (CN, "Routing: distance vector & link state"): """
### The idea
**Distance vector (e.g. RIP)**
- Each router sends its distance table to neighbours; update with Bellman–Ford: D(x, y) = min over v of c(x, v) + D(v, y).
- Simple but slow to converge; **count-to-infinity** after a link failure. Fixes: split horizon, poison reverse
  (help, but don't fully solve it for loops of 3+ routers).

**Link state (e.g. OSPF)**
- Each router floods its link costs to everyone; every router builds the full map and runs **Dijkstra**.
- Faster convergence, more memory and computation.

### Worked example
A–B cost 1, B–C cost 1. If the A–B link breaks, B may believe C's old route "A via C is 3" and they keep increasing
each other's distance to A — **count to infinity**.

### Exam traps
- Distance vector: a router knows only next hop + distance; link state: full topology.
""",
    (CN, "IPv4: fragmentation, CIDR, NAT"): """
### The idea
**Addressing**
- 32 bits, written as 4 bytes. CIDR a.b.c.d/n: n network bits, 2^(32 − n) addresses, 2^(32 − n) − 2 usable hosts.
- Network address = IP AND mask; broadcast = network with all host bits 1.
- **Subnetting:** borrow host bits; **supernetting/aggregation:** combine contiguous blocks.
- Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16.

**Fragmentation**
- Header 20–60 bytes; total length ≤ 65 535.
- Each fragment's data (except the last) must be a multiple of 8 bytes. **Offset** field = byte offset / 8.
- MF = 1 on every fragment except the last. Reassembly happens only at the destination.

**NAT:** many private hosts share one public IP; the router rewrites addresses and ports and keeps a translation table.

### Worked example
Which subnet is 172.16.45.130/27 in? Block size 32 → 128–159 → network **172.16.45.128**, broadcast 172.16.45.159.

### Exam traps
- Longest-prefix match: the router uses the most specific matching route.
- TTL decrements at every router; checksum is recomputed at each hop.
""",
    (CN, "TCP: flow & congestion control, sockets"): """
### The idea
**TCP** is connection-oriented and reliable: 3-way handshake (SYN, SYN-ACK, ACK), byte sequence numbers,
cumulative ACKs, retransmission on timeout or 3 duplicate ACKs, 4-way close.

- **Flow control:** receiver advertises a window (rwnd). Send window = min(cwnd, rwnd).
- **Congestion control:**
  - Slow start: cwnd doubles each RTT until ssthresh.
  - Congestion avoidance: +1 MSS per RTT.
  - Timeout: ssthresh = cwnd/2, cwnd = 1 MSS.
  - 3 duplicate ACKs (Reno): ssthresh = cwnd/2, cwnd = ssthresh (fast recovery).
- Throughput ≈ window / RTT. Sequence number wrap-around time = 2³² bytes / bandwidth.

**UDP:** connectionless, 8-byte header, no reliability — used by DNS, streaming, games.

**Socket API (server):** socket → bind → listen → accept → recv/send → close. Client: socket → connect → send/recv.

### Worked example
Window 64 KB, RTT 20 ms → max throughput = 65 536 × 8 / 0.02 ≈ **26.2 Mbps**.

### Exam traps
- SYN and FIN each consume one sequence number.
- "Initial window" questions — read whether cwnd starts at 1 or some given MSS.
""",
    (CN, "DNS & HTTP"): """
### The idea
**DNS** maps names to IP addresses, mostly over **UDP port 53**.
- Hierarchy: root → TLD (.com, .in) → authoritative servers. Local resolvers cache answers (TTL).
- **Recursive** query: the server finds the full answer for you. **Iterative:** it refers you to the next server.
- Record types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail), NS (name server).

**HTTP** (TCP port 80; HTTPS 443)
- Request methods: GET, POST, PUT, DELETE, HEAD. Status: 200 OK, 301 moved, 304 not modified, 404, 500.
- HTTP/1.0: non-persistent (one object per TCP connection). HTTP/1.1: persistent by default, pipelining possible.
- Stateless; cookies add state.

### Worked example
Web page with 1 base HTML + 10 images, non-persistent HTTP, no parallel connections:
each object needs 2 RTT (TCP handshake + request) → **22 RTT** (+ transmission times). Persistent: 2 + 10 = 12 RTT.

### Exam traps
- Other common ports: SMTP 25, FTP 20/21, SSH 22, DHCP 67/68 (UDP).
""",
}
