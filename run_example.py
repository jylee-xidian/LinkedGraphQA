from __future__ import annotations
import argparse, json
from lgqa.data import load_compmix_like
from lgqa.pipeline import run_pipeline

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=str, required=True)
    ap.add_argument("--topk", type=int, default=5)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    items = load_compmix_like(args.data)
    results = []
    for it in items:
        out = run_pipeline(it, topk=args.topk, verbose=args.verbose)
        results.append(out)

    print("\n=== Summary ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
