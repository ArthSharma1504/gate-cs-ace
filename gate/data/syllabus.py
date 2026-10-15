"""GATE 2027 CS syllabus (IIT Madras, revised) with approximate mark weightage.

Official split: GA 15 marks, Engineering Mathematics 13 marks, core subjects 72 marks.
Per-subject core weights below are approximate, based on the pattern of recent papers,
and are only used to prioritise study time.
"""

EXAM_DATES = ["2027-02-06", "2027-02-07", "2027-02-13", "2027-02-14", "2027-02-20", "2027-02-21"]
OFFICIAL_SITE = "https://gate2027.iitm.ac.in"
SYLLABUS_PDF = "https://gate2027.iitm.ac.in/static/doc/GATE2027_Syllabus/CS_GATE2027_Syllabus.pdf"

SYLLABUS = {
    "General Aptitude": {
        "short": "GA",
        "weight": 15,
        "topics": [
            "Verbal: grammar, vocabulary, sentence completion",
            "Verbal: reading comprehension & critical reasoning",
            "Quantitative: percentages, ratios, time & work, speed",
            "Quantitative: permutations, probability, number series",
            "Analytical: logical deduction, syllogisms, puzzles",
            "Spatial: rotations, patterns, paper folding",
            "Data interpretation: tables, graphs, charts",
        ],
    },
    "Engineering Mathematics": {
        "short": "EM",
        "weight": 13,
        "topics": [
            "Propositional & first-order logic",
            "Sets, relations, functions",
            "Partial orders & lattices",
            "Monoids & groups",
            "Graphs: connectivity, matching, colouring",
            "Combinatorics: counting, recurrences, generating functions",
            "Matrices, determinants, linear systems",
            "Eigenvalues & eigenvectors, LU decomposition",
            "Calculus: limits, continuity, differentiability",
            "Calculus: maxima/minima, mean value theorem, integration",
            "Random variables & distributions (uniform, normal, exponential, Poisson, binomial)",
            "Mean, median, mode, standard deviation",
            "Conditional probability & Bayes' theorem",
        ],
    },
    "Digital Logic": {
        "short": "DL",
        "weight": 5,
        "topics": [
            "Boolean algebra",
            "Minimisation: K-maps, tabular method",
            "Combinational circuits (MUX, decoder, adders)",
            "Sequential circuits (flip-flops, counters, registers)",
            "Number representation: fixed & floating point (IEEE 754)",
            "Computer arithmetic",
        ],
    },
    "Computer Organization & Architecture": {
        "short": "COA",
        "weight": 9,
        "topics": [
            "Instruction set & addressing modes",
            "ALU design",
            "Control unit: hardwired & microprogrammed",
            "Memory interfacing & hierarchy",
            "Cache mapping & performance",
            "I/O interface: interrupts & DMA",
            "Instruction pipelining & hazards",
        ],
    },
    "Programming & Data Structures": {
        "short": "PDS",
        "weight": 11,
        "topics": [
            "Programming in C (pointers, scope, storage classes)",
            "Recursion",
            "Arrays, stacks, queues",
            "Linked lists",
            "Trees & binary search trees",
            "Binary heaps",
            "Graphs (representation)",
        ],
    },
    "Algorithms": {
        "short": "ALGO",
        "weight": 9,
        "topics": [
            "Asymptotic analysis & recurrences",
            "Searching & sorting",
            "Hashing",
            "Greedy algorithms",
            "Dynamic programming",
            "Divide & conquer",
            "Graph traversals (BFS, DFS)",
            "Minimum spanning trees",
            "Shortest paths",
        ],
    },
    "Theory of Computation": {
        "short": "TOC",
        "weight": 8,
        "topics": [
            "Regular expressions & finite automata",
            "Regular languages & pumping lemma",
            "Context-free grammars & PDA",
            "Context-free languages & closure properties",
            "Turing machines",
            "Decidability & undecidability",
        ],
    },
    "Compiler Design": {
        "short": "CD",
        "weight": 5,
        "topics": [
            "Lexical analysis",
            "Parsing (LL, LR, FIRST/FOLLOW)",
            "Syntax-directed translation",
            "Runtime environments",
            "Intermediate code generation",
            "Local optimisation & data-flow analysis (liveness, constant propagation, CSE)",
        ],
    },
    "Operating System": {
        "short": "OS",
        "weight": 9,
        "topics": [
            "System calls, processes, threads, IPC",
            "Concurrency & synchronisation",
            "Deadlock",
            "CPU & I/O scheduling",
            "Memory management & virtual memory",
            "File systems",
        ],
    },
    "Databases": {
        "short": "DBMS",
        "weight": 8,
        "topics": [
            "ER model",
            "Relational algebra & tuple calculus",
            "SQL",
            "Integrity constraints & normal forms",
            "File organisation & indexing (B / B+ trees)",
            "Transactions & concurrency control",
        ],
    },
    "Computer Networks": {
        "short": "CN",
        "weight": 8,
        "topics": [
            "Layering principles",
            "Switching & performance metrics",
            "Data link: error detection, MAC, Ethernet",
            "Routing: distance vector & link state",
            "IPv4: fragmentation, CIDR, NAT",
            "TCP: flow & congestion control, sockets",
            "DNS & HTTP",
        ],
    },
}

SUBJECTS = list(SYLLABUS.keys())
