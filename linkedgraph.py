from __future__ import annotations
import networkx as nx
from typing import Dict, List

class LinkedGraph:
    def __init__(self):
        self.G = nx.MultiDiGraph()

    def add_entity(self, eid: str, label: str, source: str):
        self.G.add_node(eid, label=label, source=source)

    def add_edge(self, h: str, r: str, t: str, source: str, weight: float = 1.0):
        self.G.add_edge(h, t, key=r, relation=r, source=source, weight=weight)

    def summary(self) -> str:
        return f"Graph |V|={self.G.number_of_nodes()} |E|={self.G.number_of_edges()}"

    def to_triplets(self, top_edges: int = 20) -> List[str]:
        out = []
        for u, v, k, d in list(self.G.edges(keys=True, data=True))[:top_edges]:
            lu = self.G.nodes[u].get("label", u)
            lv = self.G.nodes[v].get("label", v)
            r = d.get("relation", k)
            src = d.get("source", "?")
            out.append(f"({lu}) -[{r}/{src}]-> ({lv})")
        return out

def build_linked_graph_for_question(question: str, seed_entities: List[Dict[str, str]]) -> LinkedGraph:
    lg = LinkedGraph()
    for e in seed_entities:
        lg.add_entity(e["id"], e["label"], source="seed")

    q = question.lower()
    # Case: The Matrix ↔ AI via Simulation Theory
    if "matrix" in q and "ai" in q:
        lg.add_entity("N:sim_theory", "Simulation Theory", source="text")
        lg.add_entity("C:ai", "Artificial Intelligence", source="kg")
        if "Q:matrix" not in lg.G.nodes:
            lg.add_entity("Q:matrix", "The Matrix", source="seed")
        lg.add_edge("Q:matrix", "inspiredBy", "N:sim_theory", source="text")
        lg.add_edge("N:sim_theory", "associatedWith", "C:ai", source="text")

    # Case: Alan Turing ↔ Analytical Engine ↔ Charles Babbage
    if "alan turing" in q and "device" in q:
        lg.add_entity("P:turing", "Alan Turing", source="seed")
        lg.add_entity("D:ae", "Analytical Engine", source="kg")
        lg.add_entity("P:babbage", "Charles Babbage", source="text")
        lg.add_edge("P:turing", "inspiredBy", "D:ae", source="kg")
        lg.add_edge("P:turing", "historicalInfluence", "P:babbage", source="fusion")
        lg.add_edge("P:babbage", "designed", "D:ae", source="text")

    # Light self-loop to keep seeds in graph
    for e in seed_entities:
        lg.add_edge(e["id"], "relatedTo", e["id"], source="seed", weight=0.1)
    return lg
