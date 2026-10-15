"""Built-in lessons: Digital Logic, COA, Programming & Data Structures, Algorithms."""

DL = "Digital Logic"
COA = "Computer Organization & Architecture"
PDS = "Programming & Data Structures"
ALGO = "Algorithms"

LESSONS = {
    # ================================================================ DL
    (DL, "Boolean algebra"): """
### The idea
Boolean algebra works on 0/1 with AND (·), OR (+) and NOT (′).

**Laws you'll use constantly**
- Identity: A + 0 = A, A·1 = A. Null: A + 1 = 1, A·0 = 0. Idempotent: A + A = A.
- Complement: A + A′ = 1, A·A′ = 0. Involution: (A′)′ = A.
- Absorption: A + AB = A, A(A + B) = A.
- **A + A′B = A + B** (very common simplification).
- De Morgan: (A + B)′ = A′B′, (AB)′ = A′ + B′.
- Consensus: AB + A′C + BC = AB + A′C.

**Duality:** swap + ↔ · and 0 ↔ 1 to get another valid identity.
**Functional completeness:** {NAND} alone or {NOR} alone can build every function.

### Worked example
Simplify F = AB + AB′ + A′B = A(B + B′) + A′B = A + A′B = **A + B**.

### Exam traps
- XOR: A ⊕ B = AB′ + A′B; A ⊕ A = 0; A ⊕ 1 = A′. XOR is associative.
- Number of Boolean functions of n variables: 2^(2ⁿ).
""",
    (DL, "Minimisation: K-maps, tabular method"): """
### The idea
A **Karnaugh map** places minterms in Gray-code order so adjacent cells differ in one variable.
Group 1s in rectangles of size 1, 2, 4, 8… (wrapping around edges and corners); each group drops variables.

- **Prime implicant:** a largest possible group. **Essential PI:** covers some 1 that no other PI covers.
- Minimal SOP = all essential PIs + the fewest extra PIs to cover the remaining 1s.
- **Don't cares (X)** may be used as 1 when they enlarge a group, ignored otherwise.
- **Tabular (Quine–McCluskey):** group minterms by number of 1s, repeatedly combine pairs differing in one bit.

### Worked example
F(A,B,C,D) = Σm(0, 2, 8, 10): the four corners → one group of 4 → **F = B′D′**.

### Exam traps
- Corners of a 4-variable map are adjacent.
- A function can have more than one minimal SOP; GATE often asks for the *number* of PIs or EPIs.
""",
    (DL, "Combinational circuits (MUX, decoder, adders)"): """
### The idea
Output depends only on current inputs.

- **MUX 2ⁿ:1** has n select lines and implements any n-variable function directly, or any (n+1)-variable
  function using the extra variable (or its complement, 0, 1) on the data inputs.
- **Decoder n:2ⁿ** outputs one minterm per line; OR the needed outputs to build any function.
- **Half adder:** S = A ⊕ B, C = AB. **Full adder:** S = A ⊕ B ⊕ Cin, Cout = AB + Cin(A ⊕ B).
- **Ripple-carry adder** delay ∝ n; **carry look-ahead** computes Gᵢ = AᵢBᵢ, Pᵢ = Aᵢ ⊕ Bᵢ in parallel.
- Building a 2ⁿ:1 MUX from 2:1 MUXes needs 2ⁿ − 1 of them.

### Worked example
Implement F = A ⊕ B with a 2:1 MUX using A as select: when A = 0 output B, when A = 1 output B′ → inputs **(B, B′)**.

### Exam traps
- Propagation delay questions: count the longest path in gate delays.
- A 4:16 decoder from 2:4 decoders needs 5 (one to enable four others).
""",
    (DL, "Sequential circuits (flip-flops, counters, registers)"): """
### The idea
Output depends on inputs **and** stored state; flip-flops store one bit and change on a clock edge.

| FF | Next state Q⁺ |
|---|---|
| D | D |
| T | T ⊕ Q |
| JK | JQ′ + K′Q (J=K=1 toggles) |
| SR | S + R′Q (S=R=1 not allowed) |

**Counters**
- n-bit binary (ripple or synchronous): 2ⁿ states. Mod-N counter needs ⌈log₂ N⌉ flip-flops.
- Ring counter: n states. Johnson (twisted ring): 2n states.
- Ripple counters are slower (delays add up); synchronous counters clock all FFs together.

### Worked example
A 3-bit synchronous counter with T flip-flops: T₀ = 1, T₁ = Q₀, T₂ = Q₀Q₁ (toggle when all lower bits are 1).

### Exam traps
- Excitation table (what inputs cause a given transition) vs characteristic table (next state) — read which one is asked.
- Max clock frequency = 1 / (FF delay + combinational delay + setup time).
""",
    (DL, "Number representation: fixed & floating point (IEEE 754)"): """
### The idea
**Integers with n bits**
- Unsigned: 0 … 2ⁿ − 1. Sign-magnitude and 1's complement: −(2ⁿ⁻¹ − 1) … 2ⁿ⁻¹ − 1 (two zeros).
- **2's complement:** −2ⁿ⁻¹ … 2ⁿ⁻¹ − 1. Negate = invert all bits + 1. Sign-extend by copying the MSB.

**IEEE 754** value = (−1)ˢ × 1.M × 2^(E − bias)
- Single: 1 sign, 8 exponent (bias 127), 23 mantissa. Double: 1, 11 (bias 1023), 52.
- E = 0: zero or denormal (0.M × 2^(1 − bias)). E all 1s: ∞ (M = 0) or NaN.

### Worked example
Encode −6.5 in single precision: 6.5 = 110.1₂ = 1.101 × 2² → s = 1, E = 129 = 1000 0001, M = 101000…
→ **0xC0D00000**.

### Exam traps
- Hex ↔ binary must be done carefully nibble by nibble.
- Smallest positive normalised single = 2^(−126); largest ≈ (2 − 2^(−23)) × 2^127.
""",
    (DL, "Computer arithmetic"): """
### The idea
- 2's complement addition: add normally, drop the carry out of the MSB.
- **Overflow** happens only when two numbers of the **same sign** give a result of the other sign.
  Equivalently: carry into MSB ≠ carry out of MSB.
- Subtraction A − B = A + (2's complement of B).
- **Booth's algorithm** multiplies signed numbers by scanning bit pairs: 10 → subtract, 01 → add, 00/11 → shift.

### Worked example
4-bit: 0110 (6) + 0101 (5) = 1011 → reads as −5. Two positives gave a negative → **overflow**.

### Exam traps
- Adding a positive and a negative number can never overflow.
- In Booth recoding, runs of 1s become one subtract and one add — count operations by counting 01/10 transitions.
""",
    # ================================================================ COA
    (COA, "Instruction set & addressing modes"): """
### The idea
An instruction = opcode + operand fields. If there are k opcodes, the opcode needs ⌈log₂ k⌉ bits.

**Addressing modes** (EA = effective address)
| Mode | Operand is | Typical use |
|---|---|---|
| Immediate | the constant itself | constants |
| Register | in a register | fast operands |
| Direct | Mem[A] | global variables |
| Indirect | Mem[Mem[A]] | pointers |
| Register indirect | Mem[R] | pointers in registers |
| Indexed / base | Mem[R + d] | arrays, struct fields |
| PC-relative | Mem[PC + d] | branches, position-independent code |
| Auto-increment | Mem[R], then R++ | stepping through arrays |

**Performance:** CPU time = instruction count × CPI × clock period.

### Worked example
A 32-bit instruction has a 6-bit opcode and two 5-bit register fields. Bits left for an immediate = 32 − 6 − 10 = **16**.

### Exam traps
- Count memory references per mode: direct = 1, indirect = 2 (plus instruction fetch if asked).
- Expanding-opcode questions: compute leftover encodings at each level.
""",
    (COA, "ALU design"): """
### The idea
The ALU performs arithmetic (add, subtract, compare) and logic (AND, OR, XOR, shift) on operands chosen by
control signals, and sets **flags**: zero (Z), sign (N), carry (C), overflow (V).

- Subtraction reuses the adder: A − B = A + B′ + 1 (carry-in = 1).
- **Carry look-ahead** speeds addition: Cᵢ₊₁ = Gᵢ + PᵢCᵢ with Gᵢ = AᵢBᵢ, Pᵢ = Aᵢ ⊕ Bᵢ.
- Shifts: logical shift fills with 0; arithmetic right shift copies the sign bit (divides signed numbers by 2).

### Worked example
After computing 5 − 5, the Z flag = 1, N = 0. A conditional "branch if equal" checks Z.

### Exam traps
- Arithmetic right shift of −7 (1001 in 4 bits) gives 1100 = −4 (rounds toward −∞), not −3.
""",
    (COA, "Control unit: hardwired & microprogrammed"): """
### The idea
The control unit produces the control signals for each step of every instruction.

- **Hardwired:** signals from combinational logic + a step counter. Fast, hard to change. Typical in RISC.
- **Microprogrammed:** signals stored as **microinstructions** in a control memory, fetched one by one. Flexible, slower.
  - *Horizontal:* one bit per control signal → wide words, high parallelism, little decoding.
  - *Vertical:* signals encoded into fields → narrow words, needs decoders, less parallelism.

**Sizing:** control memory = (number of microinstructions) × (bits per microinstruction). A next-address field needs
⌈log₂ (control memory words)⌉ bits.

### Worked example
48 control signals grouped into fields of mutually exclusive signals of sizes 7, 9, 15 and 17. Vertical encoding needs
⌈log₂ 8⌉ + ⌈log₂ 10⌉ + ⌈log₂ 16⌉ + ⌈log₂ 18⌉ = 3 + 4 + 4 + 5 = **16 bits** (each field also needs a "none" code).

### Exam traps
- Remember the +1 "no signal" code when encoding a field.
""",
    (COA, "Memory interfacing & hierarchy"): """
### The idea
Registers → cache → main memory → disk: each level is bigger, slower and cheaper per byte. It works because of
**locality** (temporal: reuse soon; spatial: neighbours soon).

- Memory of 2ⁿ addressable words needs n address lines.
- Building a 64K × 16 memory from 16K × 8 chips: (64K/16K) × (16/8) = **8 chips**, plus a 2:4 decoder on the top
  address bits to select a row of chips.
- **Average access time**
  - Hierarchical (check cache, then memory): T = h·t_c + (1 − h)(t_c + t_m)
  - Simultaneous: T = h·t_c + (1 − h)·t_m
- Byte vs word addressable changes the number of address bits.

### Worked example
h = 0.95, t_c = 2 ns, t_m = 50 ns (hierarchical): T = 0.95·2 + 0.05·52 = 1.9 + 2.6 = **4.5 ns**.

### Exam traps
- Read whether the miss penalty already includes the cache lookup.
""",
    (COA, "Cache mapping & performance"): """
### The idea
Address = **tag | index | offset**.
- Offset bits = log₂(block size). Lines = cache size / block size.
- **Direct mapped:** index = log₂(lines). **k-way set associative:** sets = lines / k, index = log₂(sets).
  **Fully associative:** no index.
- Tag = address bits − index − offset. Total tag memory = lines × (tag + valid + dirty… bits).

**Policies**
- Replacement: LRU, FIFO, random (only for associative caches).
- Write-through (every write goes to memory) vs write-back (dirty bit, write on eviction).
- Misses: compulsory, capacity, conflict.

### Worked example
32 KB, 2-way, 64-byte blocks, 32-bit address: lines = 512, sets = 256 → index 8, offset 6, tag **18**.

### Exam traps
- Direct-mapped conflict questions: two addresses with the same index but different tags evict each other.
- For array loops, count misses per block: a 64-byte block holds 16 ints → 1 miss per 16 accesses (row-major).
""",
    (COA, "I/O interface: interrupts & DMA"): """
### The idea
Three ways to move data between a device and memory:
1. **Programmed I/O** — CPU polls the device. Simple, wastes CPU time.
2. **Interrupt-driven** — device interrupts when ready; CPU runs an ISR. Saves polling, still CPU copies each word.
3. **DMA** — a controller moves the whole block; CPU is interrupted once at the end.

**DMA modes:** burst (holds the bus for the whole block), cycle stealing (one word, then gives the bus back),
transparent (only when the CPU isn't using the bus).

**Interrupt handling:** finish current instruction → save PC/state → jump via vector → ISR → restore.
Priority by daisy chaining or a priority encoder.

### Worked example
Device sends 10 KB/s in 1-byte units; each interrupt costs 5 µs. CPU time per second = 10 240 × 5 µs = 51.2 ms
→ **5.12%** of CPU time.

### Exam traps
- In cycle stealing, % CPU blocked = (bus time per word)/(time between words).
""",
    (COA, "Instruction pipelining & hazards"): """
### The idea
Overlap instruction stages (e.g. IF, ID, EX, MEM, WB). Clock = slowest stage + latch delay.

- k stages, n instructions, no stalls: (k + n − 1) cycles.
- With stalls: CPI = 1 + average stall cycles per instruction.
- **Speedup** over non-pipelined = (time per instruction unpipelined) / (CPI × pipeline clock).

**Hazards**
- **Structural:** two stages need the same hardware.
- **Data:** RAW (true dependency), WAR, WAW. **Forwarding** fixes most RAW; a **load followed by use** still stalls 1 cycle.
- **Control:** branches. Penalty = cycles until the branch outcome is known; reduce with prediction or delay slots.

### Worked example
20% of instructions are branches with a 2-cycle penalty, no other stalls: CPI = 1 + 0.2 × 2 = **1.4**.

### Exam traps
- Stage delays 150, 120, 160, 140 ps + 10 ps latch → clock = **170 ps**, not the average.
- Draw the space-time diagram for small dependency questions — it's faster than reasoning in your head.
""",
    # ================================================================ PDS
    (PDS, "Programming in C (pointers, scope, storage classes)"): """
### The idea
- `a[i]` is `*(a + i)`. Pointer arithmetic moves by `sizeof(type)`.
- C is **pass-by-value**: functions get copies. To change a caller's variable, pass its address.
- **Storage classes:** `auto` (default local), `static` (keeps value between calls, initialised once),
  `extern` (defined elsewhere), `register`.
- Scope: a local variable **shadows** a global of the same name inside its block.
- Strings: `char s[] = "hi";` is a modifiable array of 3 bytes; `char *p = "hi";` points to a read-only literal.
- `sizeof` on an array in its own scope gives the full size; on a pointer parameter it gives the pointer size.

### Worked example
```c
int x = 5;
void f() { static int c = 0; c += x; printf("%d ", c); }
int main() { f(); f(); x = 1; f(); }
```
Output: **5 10 11**.

### Exam traps
- `i++ + ++i` and similar are undefined behaviour — GATE avoids them, but watch for `x = x++`.
- `char *p = "abc"; p[0] = 'z';` is undefined (writing to a literal).
- Precedence: `*p++` means `*(p++)`.
""",
    (PDS, "Recursion"): """
### The idea
A recursive function solves a problem using smaller copies of itself. Every call gets its own stack frame
(parameters + locals), so depth matters for space.

**How to trace:** draw the recursion tree, or write the recurrence for the value / number of calls.
- Value recurrences come straight from the code.
- Number of calls: C(n) = 1 + Σ C(subproblems).
- Printing order: code **before** the recursive call prints going down; code **after** prints coming back up.

### Worked example
```c
void p(int n) { if (n == 0) return; printf("%d", n); p(n - 1); printf("%d", n); }
```
p(3) prints **321123**.

### Exam traps
- Static/global variables are shared across all calls; locals are per call.
- Count calls including the base-case calls.
""",
    (PDS, "Arrays, stacks, queues"): """
### The idea
**Arrays:** address of A[i][j] (row-major, base B, element size w, n columns) = B + (i·n + j)·w.
Column-major swaps the roles: B + (j·m + i)·w.

**Stack (LIFO):** push/pop O(1). Uses: function calls, undo, expression evaluation, bracket matching,
infix → postfix (operator stack).

**Queue (FIFO):** enqueue at rear, dequeue at front. Circular array of size n with one slot kept empty holds n − 1 items;
full when (rear + 1) mod n = front.

**Deque:** insert/delete at both ends. **Priority queue:** usually a heap.

### Worked example
Postfix of A + B * C − D: **A B C * + D −**.

### Exam traps
- A stack can simulate a queue with two stacks (amortised O(1)); a queue with two queues can simulate a stack.
- Number of valid stack permutations of 1…n is the Catalan number Cₙ.
""",
    (PDS, "Linked lists"): """
### The idea
Nodes hold data + pointer(s). No random access: reaching the k-th node costs O(k).

| Operation | Singly (head only) | Singly (head + tail) | Doubly |
|---|---|---|---|
| Insert at head | O(1) | O(1) | O(1) |
| Insert at tail | O(n) | O(1) | O(1) with tail |
| Delete given node | O(n) (need previous) | O(n) | O(1) |

- Reverse a singly list in place with three pointers (prev, curr, next).
- Detect a cycle: Floyd's slow/fast pointers.
- Middle element: slow moves 1, fast moves 2.

### Worked example
To delete a node in a singly linked list when you only have a pointer to it (not the last node): copy the next node's
data into it and delete the next node — **O(1)**.

### Exam traps
- Code questions that forget to update `head` when the first node changes.
""",
    (PDS, "Trees & binary search trees"): """
### The idea
**Binary trees**
- Height h (root = 0): max nodes 2^(h+1) − 1; min height for n nodes ⌊log₂ n⌋.
- Leaves n₀ = n₂ + 1 (n₂ = nodes with two children).
- Traversals: preorder (Root L R), inorder (L Root R), postorder (L R Root), level order (BFS).
- Inorder + (pre or post) order determines a binary tree uniquely; pre + post alone doesn't (unless full).

**BST:** left < node < right. Inorder is sorted. Search/insert/delete O(h) — O(log n) balanced, O(n) skewed.
Delete a node with two children: replace with its inorder successor (or predecessor).

**AVL:** heights of subtrees differ by ≤ 1; height O(log n). Min nodes for height h: N(h) = N(h−1) + N(h−2) + 1.

### Worked example
BSTs possible with keys 1, 2, 3: Catalan C₃ = **5**.

### Exam traps
- "Height" may be counted in edges or nodes — read the definition given.
- Preorder of a BST alone determines the BST (sort it to get the inorder).
""",
    (PDS, "Binary heaps"): """
### The idea
A **complete** binary tree stored in an array where every parent ≥ children (max-heap).
0-based index i: children 2i + 1, 2i + 2; parent ⌊(i − 1)/2⌋.

| Operation | Time |
|---|---|
| Find max | O(1) |
| Insert (sift up) | O(log n) |
| Extract max (move last to root, sift down) | O(log n) |
| Build heap from n items (bottom-up heapify) | **O(n)** |
| Heap sort | O(n log n), in place, not stable |

- In a max-heap the minimum is among the leaves (indices ⌊n/2⌋ … n − 1).
- k-th largest: k extractions → O(k log n).

### Worked example
Insert 10, 20, 15, 30 one by one into an empty max-heap: [10] → [20,10] → [20,10,15] → 30 bubbles to the root →
**[30, 20, 15, 10]**.

### Exam traps
- Building by repeated insertion is O(n log n); bottom-up heapify is O(n).
""",
    (PDS, "Graphs (representation)"): """
### The idea
- **Adjacency matrix:** V × V, edge check O(1), space Θ(V²). Good for dense graphs.
- **Adjacency list:** space Θ(V + E), iterate neighbours fast. Good for sparse graphs.
- Undirected graph: each edge appears twice in lists; Σ degree = 2E.
- Directed: in-degree/out-degree; Σ out-degree = E.
- Max edges: undirected simple V(V−1)/2, directed V(V−1).

### Worked example
Aᵏ[i][j] (the adjacency matrix to the power k) counts walks of length k from i to j. Trace(A³)/6 = number of
triangles in an undirected graph.

### Exam traps
- Time complexity of BFS/DFS depends on representation: Θ(V + E) with lists, Θ(V²) with a matrix.
""",
    # ================================================================ ALGO
    (ALGO, "Asymptotic analysis & recurrences"): """
### The idea
- O (upper bound), Ω (lower), Θ (tight). Growth order:
  1 < log n < √n < n < n log n < n² < n³ < 2ⁿ < n! < nⁿ.
- log(n!) = Θ(n log n). Σ 1/i = Θ(log n). Σ i = Θ(n²).

**Master theorem** T(n) = aT(n/b) + f(n), compare f with n^(log_b a):
1. f smaller → Θ(n^(log_b a))
2. f = Θ(n^(log_b a) · logᵏ n) → Θ(n^(log_b a) · log^(k+1) n)
3. f larger (and regular) → Θ(f(n))

Other recurrences: T(n) = T(n − 1) + n → Θ(n²); T(n) = 2T(n − 1) + 1 → Θ(2ⁿ); T(n) = T(√n) + 1 → Θ(log log n).

### Worked example
T(n) = 3T(n/4) + n log n: n^(log₄3) ≈ n^0.79 < n log n → case 3 → **Θ(n log n)**.

### Exam traps
- Compare functions by taking logs: n^(log n) vs 2ⁿ → (log n)² vs n → 2ⁿ grows faster.
- Loops with i *= 2 run log n times; nested loops where inner runs n/i times sum to n log n.
""",
    (ALGO, "Searching & sorting"): """
### The idea
- Linear search O(n); binary search O(log n) on sorted data (⌊log₂ n⌋ + 1 comparisons worst case).
- Insertion sort: O(n²), but O(n) when nearly sorted; number of swaps = number of inversions.
- Merge sort: Θ(n log n) always, stable, O(n) extra space.
- Quick sort: average Θ(n log n); worst Θ(n²) when the pivot is always min/max (e.g. sorted input with first-element pivot).
- Heap sort: Θ(n log n), in place, not stable.
- Counting/radix sort: linear time for small integer ranges.
- Any comparison sort needs Ω(n log n) comparisons. Finding min and max together: ⌈3n/2⌉ − 2 comparisons.

### Worked example
Merging two sorted lists of sizes m and n needs at most **m + n − 1** comparisons.

### Exam traps
- Selection sort makes O(n) swaps — fewest swaps among simple sorts.
- Quick sort's partition is not stable.
""",
    (ALGO, "Hashing"): """
### The idea
A hash function maps keys to table slots; collisions are resolved by:
- **Chaining:** each slot has a list. Load factor α = n/m. Expected search Θ(1 + α).
- **Open addressing** (all keys in the table, α < 1):
  - Linear probing h(k) + i — suffers primary clustering.
  - Quadratic probing h(k) + c₁i + c₂i² — secondary clustering.
  - Double hashing h₁(k) + i·h₂(k) — best spread.
- Expected probes for unsuccessful search (uniform hashing) ≈ 1/(1 − α).

### Worked example
Table size 7, h(k) = k mod 7, linear probing, insert 15, 22, 8: 15 → 1, 22 → 1 taken → 2, 8 → 1, 2 taken → **3**.

### Exam traps
- Deleting in open addressing needs a "deleted" marker, not an empty slot.
- Probability two keys collide with a uniform hash = 1/m.
""",
    (ALGO, "Greedy algorithms"): """
### The idea
Make the best-looking choice at each step and never undo it. Works when the problem has the
**greedy-choice property** and **optimal substructure**.

Classics:
- **Activity selection:** pick the activity that finishes earliest.
- **Fractional knapsack:** take items by value/weight ratio (0/1 knapsack needs DP!).
- **Huffman coding:** repeatedly merge the two least frequent nodes; total bits = sum of all internal node weights.
- **MST** (Prim, Kruskal) and **Dijkstra** are greedy too.
- **Job sequencing with deadlines:** sort by profit, place each job in the latest free slot before its deadline.

### Worked example
Frequencies a 1, b 1, c 2, d 3, e 5: merges 2, 4, 7, 12 → total bits = 2 + 4 + 7 + 12 = **25**.

### Exam traps
- Greedy by value or by weight alone fails for fractional knapsack; use ratio.
""",
    (ALGO, "Dynamic programming"): """
### The idea
Solve each subproblem once and store it. Use DP when subproblems **overlap** and the problem has **optimal
substructure**. Steps: define the state, write the recurrence, fix base cases, choose fill order.

| Problem | Recurrence | Time |
|---|---|---|
| LCS | L[i][j] = L[i−1][j−1] + 1 if match, else max(L[i−1][j], L[i][j−1]) | O(mn) |
| 0/1 knapsack | K[i][w] = max(K[i−1][w], vᵢ + K[i−1][w − wᵢ]) | O(nW) |
| Matrix chain | M[i][j] = min over k of M[i][k] + M[k+1][j] + pᵢ₋₁pₖpⱼ | O(n³) |
| Edit distance | min(insert, delete, replace) | O(mn) |
| Floyd–Warshall | D[i][j] = min(D[i][j], D[i][k] + D[k][j]) | O(V³) |
| Bellman–Ford | relax all edges V − 1 times | O(VE) |

### Worked example
Coin change, coins {1, 3, 4}, amount 6: greedy gives 4+1+1 (3 coins) but DP finds 3+3 → **2 coins**.

### Exam traps
- Matrix chain with n matrices needs a dimension list of length n + 1.
- Knapsack DP is pseudo-polynomial (depends on W's value, not its bit length).
""",
    (ALGO, "Divide & conquer"): """
### The idea
Split the problem, solve the parts recursively, combine. Analyse with a recurrence.

| Algorithm | Recurrence | Time |
|---|---|---|
| Binary search | T(n/2) + 1 | Θ(log n) |
| Merge sort | 2T(n/2) + n | Θ(n log n) |
| Quick sort (balanced) | 2T(n/2) + n | Θ(n log n) |
| Strassen | 7T(n/2) + n² | Θ(n^2.81) |
| Karatsuba multiplication | 3T(n/2) + n | Θ(n^1.585) |
| Max-min of n numbers | 2T(n/2) + 2 | ⌈3n/2⌉ − 2 comparisons |
| Power aⁿ by squaring | T(n/2) + 1 | Θ(log n) |

### Worked example
Counting inversions with merge sort: during merging, when an element from the right half is placed first, it forms an
inversion with **every remaining element** of the left half — total Θ(n log n).

### Exam traps
- Quick sort with median-of-medians pivot is Θ(n log n) worst case but rarely used.
""",
    (ALGO, "Graph traversals (BFS, DFS)"): """
### The idea
- **BFS** (queue): visits by distance; gives shortest paths in **unweighted** graphs. O(V + E).
- **DFS** (stack/recursion): goes deep first; gives discovery/finish times. O(V + E).

**DFS edge types (directed):** tree, back (to an ancestor → **cycle**), forward, cross.
Undirected DFS has only tree and back edges.

**Applications:** cycle detection, **topological sort** (reverse finish order, DAGs only), connected components,
strongly connected components (Kosaraju: DFS twice), bipartiteness (BFS 2-colouring), articulation points.

### Worked example
DAG edges A→B, A→C, B→D, C→D: one topological order is **A, B, C, D** (A, C, B, D is also valid).

### Exam traps
- A DFS tree's height can be V − 1; a BFS tree's depth equals the graph's eccentricity from the source.
- Number of topological orders: count them carefully with branching choices.
""",
    (ALGO, "Minimum spanning trees"): """
### The idea
A spanning tree connecting all V vertices with V − 1 edges and minimum total weight.

- **Kruskal:** sort edges, add the lightest edge that doesn't form a cycle (union–find). O(E log E).
- **Prim:** grow from a vertex, always add the lightest edge leaving the tree. O(E log V) with a heap.
- **Cut property:** the lightest edge crossing any cut is in some MST.
- **Cycle property:** the heaviest edge on any cycle is in no MST (if unique).
- Distinct weights → the MST is unique.

### Worked example
Square A–B 1, B–C 2, C–D 3, D–A 4, diagonal A–C 5: Kruskal picks 1, 2, 3 → weight **6**.

### Exam traps
- Adding a constant to all edge weights doesn't change the MST (it can change shortest paths!).
- An MST does not give shortest paths between vertices.
""",
    (ALGO, "Shortest paths"): """
### The idea
| Algorithm | Graph | Time |
|---|---|---|
| BFS | unweighted | O(V + E) |
| Dijkstra | non-negative weights | O((V + E) log V) with a heap |
| Bellman–Ford | negative edges allowed; detects negative cycles | O(VE) |
| DAG shortest path | topological order + relax | O(V + E) |
| Floyd–Warshall | all pairs | O(V³) |

**Relaxation:** if d[u] + w(u, v) < d[v], set d[v] = d[u] + w(u, v).
Dijkstra fixes the closest unvisited vertex each step — wrong with negative edges.

### Worked example
Source S, edges S→A 4, S→B 1, B→A 2, A→C 1: d(B) = 1, d(A) = min(4, 1 + 2) = 3, d(C) = **4**.

### Exam traps
- Multiplying all weights by a positive constant keeps shortest paths; adding a constant may change them.
""",
}
