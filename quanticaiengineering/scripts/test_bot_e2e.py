"""
End-to-end bot test: runs questions through the REAL RAG + LLM pipeline.

Requires ANTHROPIC_API_KEY in .env. Uses the same question set as
test_retrieval_suite.py but actually calls the LLM and records full
responses. Outputs a graded scorecard.

Usage:
    python scripts/test_bot_e2e.py              # run all 65
    python scripts/test_bot_e2e.py --quick 10   # run first 10 only
    python scripts/test_bot_e2e.py --category J # run only category J
"""

import json
import sys
import time
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag_system import IsekaiRAGSystem
from scripts.test_retrieval_suite import TESTS


def run_query(rag, question):
    """Run a question through the full RAG pipeline and return the result."""
    t0 = time.time()
    result = rag.query(question=question, return_metadata=False)
    elapsed = round(time.time() - t0, 2)
    return {
        "answer": result.get("answer", ""),
        "sources": [s.get("filename", "") for s in result.get("sources", [])],
        "confidence": round(result.get("confidence", 0), 4),
        "time": elapsed,
    }


def grade_answer(answer_text, required_concepts, forbidden_concepts):
    """
    Grade a bot answer for concept coverage and forbidden phrases.
    Returns (score, issues).
    """
    lower = answer_text.lower()
    issues = []

    # Check required concepts appear in the ANSWER (not just retrieval)
    found = 0
    for concept in required_concepts:
        if concept in lower:
            found += 1
        else:
            issues.append(f"missing: '{concept}'")

    # Check forbidden
    for f in forbidden_concepts:
        if f in lower:
            issues.append(f"FORBIDDEN: '{f}'")

    # Critical failures
    critical = []
    if "stacks multiplicatively" in lower:
        critical.append("CRITICAL: said 'stacks multiplicatively'")
    # Neptune check: only flag if the bot recommends Neptune AS a main carry
    # without warning. Mentioning Neptune in a list comparison is fine.
    neptune_recommending = (
        "neptune" in lower
        and any(phrase in lower for phrase in [
            "recommend neptune", "neptune is the best", "main neptune",
            "choose neptune", "pick neptune", "invest in neptune",
        ])
        and "not recommend" not in lower
        and "do not" not in lower
        and "don't" not in lower
    )
    if neptune_recommending:
        critical.append("CRITICAL: recommending Neptune as main carry without warning")
    if "healer" in lower and "typing" in lower:
        critical.append("CRITICAL: mentioned 'Healer' as a typing")

    coverage = found / max(len(required_concepts), 1)
    return coverage, issues, critical


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", type=int, default=0, help="Run only first N tests")
    parser.add_argument("--category", type=str, default="", help="Run only tests in category (e.g., J)")
    args = parser.parse_args()

    tests = TESTS
    if args.category:
        tests = [t for t in tests if t[0].startswith(args.category)]
    if args.quick:
        tests = tests[:args.quick]

    print("=" * 80)
    print(f"END-TO-END BOT TEST — {len(tests)} questions")
    print("=" * 80)
    print()
    print("Loading RAG system (this takes ~30s for model loading)...")

    rag = IsekaiRAGSystem()
    print(f"RAG ready. Model: {rag.model_name}")
    print()

    results = []
    total_time = 0

    for i, test in enumerate(tests):
        test_id, question, required, forbidden, notes = test
        print(f"[{i+1}/{len(tests)}] {test_id}: {question[:60]}...", end=" ", flush=True)

        try:
            r = run_query(rag, question)
            coverage, issues, critical = grade_answer(r["answer"], required, forbidden)
            total_time += r["time"]

            status = "PASS" if coverage >= 0.5 and not critical else "FAIL"
            print(f"{status} ({r['time']}s, {coverage:.0%} coverage)")

            if issues or critical:
                for issue in critical:
                    print(f"    🚫 {issue}")
                for issue in issues[:3]:
                    print(f"    ⚠️  {issue}")

            results.append({
                "id": test_id,
                "question": question,
                "status": status,
                "coverage": coverage,
                "issues": issues,
                "critical": critical,
                "answer": r["answer"],
                "sources": r["sources"],
                "confidence": r["confidence"],
                "time": r["time"],
            })

        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "id": test_id,
                "question": question,
                "status": "ERROR",
                "coverage": 0,
                "issues": [str(e)],
                "critical": [],
                "answer": "",
                "sources": [],
                "confidence": 0,
                "time": 0,
            })

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    errors = sum(1 for r in results if r["status"] == "ERROR")
    avg_coverage = sum(r["coverage"] for r in results) / max(len(results), 1)
    criticals = [r for r in results if r["critical"]]

    print()
    print("=" * 80)
    print(f"SCORECARD: {passed}/{len(results)} PASS | {failed} FAIL | {errors} ERROR")
    print(f"Average concept coverage: {avg_coverage:.0%}")
    print(f"Total LLM time: {total_time:.1f}s ({total_time/max(len(results),1):.1f}s avg)")
    print("=" * 80)

    if criticals:
        print()
        print("🚫 CRITICAL FAILURES:")
        for r in criticals:
            print(f"  {r['id']}: {r['critical']}")

    if failed > 0:
        print()
        print("FAILURES:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  {r['id']}: {r['question'][:60]}")
                for issue in r["issues"][:3]:
                    print(f"    - {issue}")

    # Save full results to JSON
    output_path = Path(__file__).parent.parent / "data" / "e2e_test_results.json"
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nFull results saved to: {output_path}")

    return passed, len(results), criticals


if __name__ == "__main__":
    passed, total, criticals = main()
    sys.exit(0 if not criticals and passed >= total * 0.8 else 1)
