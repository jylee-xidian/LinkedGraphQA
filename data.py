from __future__ import annotations
import json
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class QAItem:
    question_id: str
    question: str
    domain: str
    entities: List[Dict[str, str]]
    answer_text: str

def load_compmix_like(path: str) -> List[QAItem]:
    items: List[QAItem] = []
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    for rec in raw:
        qid = str(rec.get("question_id", ""))
        q = rec.get("question", "").strip()
        dom = rec.get("domain", "unknown")
        ents = rec.get("entities", [])
        ans = rec.get("answer_text") or (rec.get("answers", [{}])[0].get("label") if rec.get("answers") else "")
        items.append(QAItem(qid, q, dom, ents, ans))
    return items
