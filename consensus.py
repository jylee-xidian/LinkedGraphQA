from __future__ import annotations
from typing import List

def normalize(s: str) -> str:
    return " ".join(s.lower().strip().split())

def ConsensusScore(cands: List[str], anchor: str, thr_sem: float = 0.82) -> float:
    if not cands: return 0.0
    norm = [normalize(c) for c in cands]
    a = normalize(anchor)
    exact = sum(1 for c in norm if c == a) - 1
    a_set = set(a.split())
    sem = sum(1 for c in norm if len(a_set & set(c.split())) / max(1, len(a_set)) >= 0.6) - 1
    n = max(1, len(cands) - 1)
    return 0.5 * exact/n + 0.5 * sem/n
