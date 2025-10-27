from __future__ import annotations
from typing import Dict, Any
from .data import QAItem
from .linkedgraph import build_linked_graph_for_question
from .gnn_retriever import personalized_pagerank_scores, topk_evidence
from .prompting import BuildPrompt
from .verify import VerifyAndRepair
from .consensus import ConsensusScore

def run_pipeline(item: QAItem, topk: int = 5, verbose: bool = True) -> Dict[str, Any]:
    # 1) LinkedGraph
    G = build_linked_graph_for_question(item.question, item.entities)
    # 2) “GNN”检索（PPR 近似）
    seeds = [e["id"] for e in item.entities] or list(G.G.nodes())[:1]
    scores = personalized_pagerank_scores(G.G, seeds)
    top_nodes = topk_evidence(G.G, scores, k=topk)
    hints = G.to_triplets(top_edges=10)
    # 3) Prompt
    prompt = BuildPrompt(item.question, C="", G_q=G, R_q=hints, step=0)
    # 4) 生成候选（此处用 toy 候选，实际替换为你的 LLM 输出）
    cands = [item.answer_text, item.answer_text + " (variant)", item.answer_text + " (alt)"]
    # 5) 验证与修复
    repaired, used = VerifyAndRepair(cands[0], G)
    # 6) 共识打分
    score = ConsensusScore(cands, cands[0])
    if verbose:
        print("=== Question ===")
        print(item.question)
        print("\n=== LinkedGraph Summary ===")
        print(G.summary())
        print("\nTop nodes:", top_nodes)
        print("\n=== Prompt Preview ===")
        print(prompt[:500], "...")
        print("\n=== Candidate Answers ===")
        for c in cands: print("-", c)
        print("\n=== Repaired Answer ===")
        print(repaired)
        print("\n=== Evidence Used ===")
        for (h, r, t) in used: print(f"({h}) -[{r}]-> ({t})")
        print("\nConsensus Score:", round(score, 3))
    return {
        "question_id": item.question_id,
        "question": item.question,
        "answer_gold": item.answer_text,
        "answer_pred": repaired,
        "consensus": score,
        "top_nodes": top_nodes,
        "evidence": used,
    }
