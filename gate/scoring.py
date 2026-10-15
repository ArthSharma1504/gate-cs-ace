"""GATE answer checking and marking scheme.

MCQ: +marks if correct, −1/3 (1-mark) or −2/3 (2-mark) if wrong.
MSQ and NAT: no negative marking, no partial credit.
"""
from __future__ import annotations


def parse_nat(value) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def is_answered(q: dict, resp) -> bool:
    if q["type"] == "MCQ":
        return resp is not None
    if q["type"] == "MSQ":
        return bool(resp)
    return parse_nat(resp) is not None


def is_correct(q: dict, resp) -> bool:
    if not is_answered(q, resp):
        return False
    if q["type"] == "MCQ":
        return int(resp) == int(q["answer"])
    if q["type"] == "MSQ":
        return set(map(int, resp)) == set(map(int, q["answer"]))
    lo, hi = q["answer"]
    v = parse_nat(resp)
    return lo - 1e-9 <= v <= hi + 1e-9


def marks_for(q: dict, resp) -> float:
    if not is_answered(q, resp):
        return 0.0
    if is_correct(q, resp):
        return float(q["marks"])
    if q["type"] == "MCQ":
        return -q["marks"] / 3
    return 0.0


def answer_text(q: dict) -> str:
    letters = "ABCD"
    if q["type"] == "MCQ":
        i = q["answer"]
        return f"({letters[i]}) {q['options'][i]}"
    if q["type"] == "MSQ":
        return ", ".join(f"({letters[i]}) {q['options'][i]}" for i in sorted(q["answer"]))
    lo, hi = q["answer"]
    return f"{lo:g}" if lo == hi else f"{lo:g} to {hi:g}"


def response_text(q: dict, resp) -> str:
    letters = "ABCD"
    if not is_answered(q, resp):
        return "Not answered"
    if q["type"] == "MCQ":
        return f"({letters[int(resp)]}) {q['options'][int(resp)]}"
    if q["type"] == "MSQ":
        return ", ".join(f"({letters[i]})" for i in sorted(resp))
    return str(resp).strip()
