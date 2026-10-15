"""Built-in lessons for every topic of the GATE 2027 CS syllabus, keyed by (subject, topic)."""
from urllib.parse import quote_plus

from gate.data.lessons_a import LESSONS as _A
from gate.data.lessons_b import LESSONS as _B
from gate.data.lessons_c import LESSONS as _C

LESSONS = {**_A, **_B, **_C}


def video_search_url(subject: str, topic: str) -> str:
    """YouTube search for free lectures (NPTEL / GATE) on this topic."""
    short = topic.split("(")[0].strip()
    return "https://www.youtube.com/results?search_query=" + quote_plus(f"{short} {subject} GATE CSE lecture")


def nptel_search_url(subject: str, topic: str) -> str:
    """YouTube search restricted by keyword to NPTEL (IIT/IISc) lectures."""
    short = topic.split("(")[0].split(":")[-1].strip()
    return "https://www.youtube.com/results?search_query=" + quote_plus(f"NPTEL {subject} {short}")
