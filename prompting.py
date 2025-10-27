from __future__ import annotations
from typing import List
from .linkedgraph import LinkedGraph

def BuildPrompt(q_t: str, C: str, G_q: LinkedGraph, R_q: List[str], step: int = 0) -> str:
    triples = "\n".join(G_q.to_triplets(top_edges=20))
    hints = "\n".join(R_q[:8])
    sys_inst = (
        "You are a graph-grounded assistant. Use only verified facts from the LinkedGraph. "
        "If uncertain, state 'uncertain' explicitly."
    )
    body = f"""Question: {q_t}

Context:
{C}

Facts (LinkedGraph):
{triples}

Reasoning Hints:
{hints}

Step {step}: Analyze facts and reason before drafting.
"""
    return sys_inst + "\n\n" + body
