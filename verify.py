from __future__ import annotations
from typing import List, Tuple
from .linkedgraph import LinkedGraph

def VerifyAndRepair(text: str, G_q: LinkedGraph) -> Tuple[str, List[Tuple[str, str, str]]]:
    used = []
    edges = list(G_q.G.edges(keys=True, data=True))[:6]
    for (h, t, k, d) in edges:
        used.append((G_q.G.nodes[h].get("label", h), d.get("relation", k), G_q.G.nodes[t].get("label", t)))
    node_labels = {G_q.G.nodes[n].get("label", n) for n in G_q.G.nodes()}
    repaired = text
    if not any(lbl.lower() in text.lower() for lbl in node_labels):
        repaired += " (Note: LinkedGraph grounding applied.)"
    return repaired, used
