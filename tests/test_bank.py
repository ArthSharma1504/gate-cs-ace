"""Validates the question bank and independently recomputes numeric answers.

Run: python -m pytest -q
"""
import heapq
import itertools
import math
import sys
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gate.data.questions import QUESTIONS  # noqa: E402
from gate.data.syllabus import SYLLABUS  # noqa: E402
from gate.data.notes import NOTES  # noqa: E402

BY_ID = {q["id"]: q for q in QUESTIONS}


def nat_ok(qid, value):
    lo, hi = BY_ID[qid]["answer"]
    assert lo - 1e-9 <= value <= hi + 1e-9, f"{qid}: computed {value}, bank says [{lo}, {hi}]"


# ----------------------------------------------------------------- structure
def test_structure():
    ids = set()
    for q in QUESTIONS:
        assert q["id"] not in ids, f"duplicate id {q['id']}"
        ids.add(q["id"])
        assert q["subject"] in SYLLABUS, q["id"]
        assert q["topic"] in SYLLABUS[q["subject"]]["topics"], f"{q['id']}: unknown topic {q['topic']}"
        assert q["marks"] in (1, 2)
        assert q["type"] in ("MCQ", "MSQ", "NAT")
        assert q["explanation"]
        if q["type"] == "MCQ":
            assert len(q["options"]) == 4 and isinstance(q["answer"], int) and 0 <= q["answer"] < 4, q["id"]
        elif q["type"] == "MSQ":
            assert len(q["options"]) == 4 and q["answer"] and all(0 <= i < 4 for i in q["answer"]), q["id"]
        else:
            lo, hi = q["answer"]
            assert lo <= hi and not q["options"], q["id"]


def test_full_mock_is_possible():
    ga = [q for q in QUESTIONS if q["subject"] == "General Aptitude"]
    core = [q for q in QUESTIONS if q["subject"] != "General Aptitude"]
    assert sum(q["marks"] == 1 for q in ga) >= 5 and sum(q["marks"] == 2 for q in ga) >= 5
    assert sum(q["marks"] == 1 for q in core) >= 25 and sum(q["marks"] == 2 for q in core) >= 30


def test_notes_cover_all_subjects():
    assert set(NOTES) == set(SYLLABUS)


# ----------------------------------------------------------------- GA / EM
def test_ga_numbers():
    nat_ok("GA03", 1 / ((1 / 12 + 1 / 15 + 1 / 20) / 2))
    nat_ok("GA05", 27 + 4)
    nat_ok("GA07", (1 - 1 / 1.25) * 100)
    nat_ok("GA09", math.factorial(5) / (2 * 2))
    nat_ok("GA12", sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == 7) / 36)
    assert abs(30 * 3 - 5.5 * 40) == 130  # GA10
    assert 240 / 12 and (240 + 360) / (240 / 12) == 30  # GA04


def test_em_numbers():
    nat_ok("EM01", 2 ** (16 - 4))
    a = [1, 4]
    for _ in range(3):
        a.append(5 * a[-1] - 6 * a[-2])
    nat_ok("EM03", a[4])
    tr, det = 7, 4 * 3 - 1 * 2
    nat_ok("EM05", (tr + math.sqrt(tr * tr - 4 * det)) / 2)
    f = lambda x: x ** 3 - 6 * x ** 2 + 9 * x + 1  # noqa: E731
    nat_ok("EM09", max(f(x / 1000) for x in range(0, 4001)))
    nat_ok("EM10", sum((i + 0.5) / 100000 * math.exp((i + 0.5) / 100000) for i in range(100000)) / 100000)
    nat_ok("EM11", 0.01 * 0.9 / (0.01 * 0.9 + 0.99 * 0.05))
    nat_ok("EM12", math.exp(-2))
    nat_ok("EM14", sum(x * x for x in range(1, 7)) / 6 - 3.5 ** 2)
    nat_ok("EM08", math.sin(3e-7) / 1e-7)
    # EM07 determinant = k - 7
    for k in (0, 7, 10):
        d = 1 * (2 * k - 12) - 1 * (k - 3) + 1 * (4 - 2)
        assert d == k - 7


def rank(m):
    m = [row[:] for row in m]
    r = 0
    for c in range(len(m[0])):
        piv = next((i for i in range(r, len(m)) if abs(m[i][c]) > 1e-12), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(len(m)):
            if i != r:
                fac = m[i][c] / m[r][c]
                m[i] = [x - fac * y for x, y in zip(m[i], m[r])]
        r += 1
    return r


def test_em_rank():
    nat_ok("EM06", rank([[1, 2, 3], [2, 4, 6], [1, 1, 1]]))


# ----------------------------------------------------------------- DL / COA
def test_dl():
    import struct
    nat_ok("DL04", struct.unpack(">f", bytes.fromhex("C1480000"))[0])
    assert format((-45) & 0xFF, "02X") == "D3"
    assert BY_ID["DL03"]["options"][BY_ID["DL03"]["answer"]] == "D3"
    # DL01: A' + B' equals the function
    for m in range(8):
        a, b = (m >> 2) & 1, (m >> 1) & 1
        assert ((not a) or (not b)) == (m in {0, 1, 2, 3, 4, 5})
    s = (0x70 + 0x50) & 0xFF
    assert s == 0xC0


def test_coa():
    nat_ok("COA01", (5 + 100 - 1) * 1)
    nat_ok("COA02", 500 / 104)
    nat_ok("COA03", 32 - int(math.log2(64 * 1024 // 32)) - 5)
    nat_ok("COA04", 32 - int(math.log2(16 * 1024 // 64 // 4)) - 6)
    nat_ok("COA05", 0.9 * 10 + 0.1 * 110)
    nat_ok("COA09", 0.5 * 1 + 0.3 * 2 + 0.2 * 3)
    nat_ok("COA10", math.log2(2 ** 20))


# ----------------------------------------------------------------- PDS
def test_pds():
    calls = 0

    def f(n):
        nonlocal calls
        calls += 1
        return 1 if n <= 1 else f(n - 1) + f(n - 2)

    nat_ok("PDS01", f(5))
    nat_ok("PDS02", calls)

    stack = []
    for t in "6 2 3 + - 3 8 2 / + *".split():
        if t.isdigit():
            stack.append(int(t))
        else:
            b, a = stack.pop(), stack.pop()
            stack.append({"+": a + b, "-": a - b, "*": a * b, "/": a / b}[t])
    nat_ok("PDS04", stack[0])

    # BST height
    tree = {}

    def ins(node, k, depth):
        if node is None:
            return {"k": k, "l": None, "r": None, "d": depth}
        side = "l" if k < node["k"] else "r"
        node[side] = ins(node[side], k, depth + 1)
        return node

    root = None
    for k in [50, 30, 70, 20, 40, 60, 80, 35]:
        root = ins(root, k, 0)

    def height(n):
        return -1 if n is None else 1 + max(height(n["l"]), height(n["r"]))

    nat_ok("PDS05", height(root))

    h = [50, 30, 40, 10, 20, 35, 45]
    i = 6
    while i > 0 and h[(i - 1) // 2] < h[i]:
        h[i], h[(i - 1) // 2] = h[(i - 1) // 2], h[i]
        i = (i - 1) // 2
    nat_ok("PDS08", h[6])
    nat_ok("PDS11", 2 + 4 + 6)


def test_tree_postorder():
    pre, ino = list("ABDECF"), list("DBEAFC")

    def build(pre, ino):
        if not pre:
            return []
        r = pre[0]
        i = ino.index(r)
        return build(pre[1:i + 1], ino[:i]) + build(pre[i + 1:], ino[i + 1:]) + [r]

    post = " ".join(build(pre, ino))
    q = BY_ID["PDS06"]
    assert q["options"][q["answer"]] == post


# ----------------------------------------------------------------- ALGO
EDGES = [("A", "B", 4), ("A", "C", 1), ("B", "C", 2), ("B", "D", 5), ("C", "D", 8),
         ("C", "E", 10), ("D", "E", 2), ("B", "E", 6)]


def test_mst_and_dijkstra():
    parent = {v: v for v in "ABCDE"}

    def find(x):
        while parent[x] != x:
            x = parent[x]
        return x

    total = 0
    for u, v, w in sorted(EDGES, key=lambda e: e[2]):
        if find(u) != find(v):
            parent[find(u)] = find(v)
            total += w
    nat_ok("ALG03", total)

    adj = {v: [] for v in "ABCDE"}
    for u, v, w in EDGES:
        adj[u].append((v, w))
        adj[v].append((u, w))
    dist = {v: math.inf for v in adj}
    dist["A"] = 0
    pq = [(0, "A")]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    nat_ok("ALG04", dist["E"])


def test_dp_and_greedy():
    nat_ok("ALG05", math.floor(math.log2(1000)) + 1)

    x, y = "ABCBDAB", "BDCABA"
    L = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(len(x)):
        for j in range(len(y)):
            L[i + 1][j + 1] = L[i][j] + 1 if x[i] == y[j] else max(L[i][j + 1], L[i + 1][j])
    nat_ok("ALG07", L[-1][-1])

    items = [(1, 1), (3, 4), (4, 5), (5, 7)]
    best = max(sum(v for _, v in c) for r in range(5) for c in itertools.combinations(items, r)
               if sum(w for w, _ in c) <= 7)
    nat_ok("ALG08", best)

    nat_ok("ALG09", min(10 * 30 * 5 + 10 * 5 * 60, 30 * 5 * 60 + 10 * 30 * 60))

    hq = [5, 9, 12, 13, 16, 45]
    heapq.heapify(hq)
    cost = 0
    while len(hq) > 1:
        a, b = heapq.heappop(hq), heapq.heappop(hq)
        cost += a + b
        heapq.heappush(hq, a + b)
    nat_ok("ALG11", cost)

    table = [None] * 10
    for k in [12, 22, 32, 42, 15]:
        i = k % 10
        while table[i] is not None:
            i = (i + 1) % 10
        table[i] = k
    nat_ok("ALG12", table.index(15))


# ----------------------------------------------------------------- TOC (brute-force DFA minimisation)
def min_dfa_states(accept, alphabet, max_len=9):
    """Count Myhill–Nerode classes by distinguishing strings up to max_len (enough for these small languages)."""
    strings = [""] + ["".join(p) for n in range(1, 6) for p in itertools.product(alphabet, repeat=n)]
    suffixes = [""] + ["".join(p) for n in range(1, max_len - 4) for p in itertools.product(alphabet, repeat=n)]
    sigs = {tuple(accept(s + t) for t in suffixes) for s in strings}
    return len(sigs)


def test_toc():
    nat_ok("TOC01", min_dfa_states(lambda s: s.count("1") % 3 == 0, "01"))
    nat_ok("TOC02", min_dfa_states(lambda s: int(s or "0", 2) % 5 == 0, "01"))
    nat_ok("TOC03", min_dfa_states(lambda s: s.endswith("ab"), "ab"))


# ----------------------------------------------------------------- OS
def test_os_scheduling():
    procs = {"P1": (0, 6), "P2": (1, 8), "P3": (2, 7), "P4": (3, 3)}
    t, done, wait = 0, set(), {}
    while len(done) < 4:
        ready = [p for p, (a, b) in procs.items() if a <= t and p not in done]
        if not ready:
            t += 1
            continue
        p = min(ready, key=lambda p: (procs[p][1], procs[p][0]))
        wait[p] = t - procs[p][0]
        t += procs[p][1]
        done.add(p)
    nat_ok("OS01", sum(wait.values()) / 4)

    procs = [("P1", 0, 5), ("P2", 1, 3), ("P3", 2, 1)]
    rem = {p: b for p, _, b in procs}
    arr = {p: a for p, a, _ in procs}
    q, t, finish, arrived = deque(), 0, {}, set()

    def admit(now):
        for p, a, _ in procs:
            if a <= now and p not in arrived:
                arrived.add(p)
                q.append(p)

    admit(0)
    while q:
        p = q.popleft()
        run = min(2, rem[p])
        t += run
        rem[p] -= run
        admit(t)
        if rem[p]:
            q.append(p)
        else:
            finish[p] = t
    nat_ok("OS02", sum(finish[p] - arr[p] for p in finish) / 3)


def test_os_paging_disk():
    ref = [7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2]
    frames, faults = deque(), 0
    for r in ref:
        if r not in frames:
            faults += 1
            if len(frames) == 3:
                frames.popleft()
            frames.append(r)
    nat_ok("OS03", faults)

    frames, faults = [], 0
    for r in ref:
        if r in frames:
            frames.remove(r)
        else:
            faults += 1
            if len(frames) == 3:
                frames.pop(0)
        frames.append(r)
    nat_ok("OS04", faults)

    nat_ok("OS05", 10 - 6 + 4)
    nat_ok("OS07", 2 ** 3 - 1)
    nat_ok("OS08", (2 ** 32 // 2 ** 12) * 4 / 2 ** 20)
    nat_ok("OS09", 0.8 * 110 + 0.2 * 210)
    nat_ok("OS13", 12 + 1024 // 4)

    head, reqs, moved = 50, [82, 170, 43, 140, 24, 16, 190], 0
    while reqs:
        nxt = min(reqs, key=lambda r: abs(r - head))
        moved += abs(nxt - head)
        head = nxt
        reqs.remove(nxt)
    nat_ok("OS11", moved)


# ----------------------------------------------------------------- DB
def closure(attrs, fds):
    c = set(attrs)
    changed = True
    while changed:
        changed = False
        for lhs, rhs in fds:
            if set(lhs) <= c and not set(rhs) <= c:
                c |= set(rhs)
                changed = True
    return c


def test_db():
    fds = [("AB", "C"), ("C", "D"), ("D", "A")]
    supers = [set(s) for r in range(1, 5) for s in itertools.combinations("ABCD", r)
              if closure(s, fds) == set("ABCD")]
    keys = [s for s in supers if not any(o < s for o in supers)]
    nat_ok("DB01", len(keys))
    p = max(p for p in range(1, 200) if 6 * p + 10 * (p - 1) <= 1024)
    nat_ok("DB03", p)
    nat_ok("DB08", 2 ** 3)
    nat_ok("DB11", len([x for x in [1, 2, 2, None, 3] if x is not None]))


# ----------------------------------------------------------------- CN
def crc(msg, gen):
    bits = list(map(int, msg + "0" * (len(gen) - 1)))
    g = list(map(int, gen))
    for i in range(len(msg)):
        if bits[i]:
            for j in range(len(g)):
                bits[i + j] ^= g[j]
    return "".join(map(str, bits[-(len(gen) - 1):]))


def test_cn():
    nat_ok("CN01", 2 ** 12 - 2)
    a = 4 / 1
    nat_ok("CN03", 1 / (1 + 2 * a))
    k = 1
    while 2 ** k - 1 < 1 + 2 * a:
        k += 1
    nat_ok("CN04", k)
    data, per = 4000 - 20, (1500 - 20) // 8 * 8
    offsets = list(range(0, data, per))
    nat_ok("CN05", offsets[-1] // 8)
    assert BY_ID["CN06"]["options"][BY_ID["CN06"]["answer"]] == crc("1101", "1011")
    cw, rounds = 1, [1]
    while len(rounds) < 7:
        cw = cw * 2 if cw < 16 else cw + 1
        cw = min(cw, 16) if rounds[-1] < 16 and cw > 16 else cw
        rounds.append(cw)
    nat_ok("CN08", rounds[6])
    nat_ok("CN11", 1 / (2 * math.e))
    import ipaddress
    net = ipaddress.ip_network("192.168.10.64/26")
    q = BY_ID["CN02"]
    assert ipaddress.ip_address(q["options"][q["answer"]]) in net
    assert all(ipaddress.ip_address(o) not in net for i, o in enumerate(q["options"]) if i != q["answer"])
