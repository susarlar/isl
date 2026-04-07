"""
Evaluation Pipeline for Policy RAG System
==========================================

Usage:
  python scripts/evaluate.py
  python scripts/evaluate.py --test-file data/test_queries.json
  python scripts/evaluate.py --top-k 3
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment before importing config so validation is skipped
import os

os.environ.setdefault("APP_ENV", "production")

from config import TEST_DATASET_PATH, EVALUATION_OUTPUT_PATH
from app.rag_system import PolicyRAGSystem
from app.evaluation import EvalQuestion, run_evaluation, save_results, print_summary


def load_questions(path: Path) -> list[EvalQuestion]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [
        EvalQuestion(
            question_id=q["question_id"],
            question=q["question"],
            expected_sources=q.get("expected_sources", []),
            gold_answer_keywords=q.get("gold_answer_keywords", []),
            category=q.get("category", "general"),
        )
        for q in raw
    ]


def main():
    parser = argparse.ArgumentParser(description="Evaluate the Policy RAG system")
    parser.add_argument(
        "--test-file",
        type=Path,
        default=TEST_DATASET_PATH,
        help="Path to test queries JSON (default: data/test_queries.json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=EVALUATION_OUTPUT_PATH,
        help="Path to save evaluation results",
    )
    parser.add_argument(
        "--top-k", type=int, default=5, help="Number of chunks to retrieve per query"
    )
    parser.add_argument(
        "--category",
        type=str,
        default=None,
        help="Filter questions by category (e.g. leave, security)",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress per-question output"
    )
    args = parser.parse_args()

    # Create test dataset if it doesn't exist
    if not args.test_file.exists():
        print(f"Test file not found at {args.test_file}. Creating default dataset...")
        from scripts.create_test_dataset import QUESTIONS

        args.test_file.parent.mkdir(parents=True, exist_ok=True)
        with open(args.test_file, "w") as f:
            json.dump(QUESTIONS, f, indent=2)
        print(f"✓ Created {len(QUESTIONS)} test questions")

    questions = load_questions(args.test_file)

    if args.category:
        questions = [q for q in questions if q.category == args.category]
        print(f"Filtered to {len(questions)} questions in category: {args.category}")

    if not questions:
        print("No questions to evaluate. Exiting.")
        sys.exit(1)

    print(f"\nEvaluating {len(questions)} questions (top_k={args.top_k})...")
    print("-" * 65)

    # Initialize RAG system
    try:
        rag = PolicyRAGSystem()
    except FileNotFoundError as e:
        print(f"\n✗ {e}")
        print("Run: python scripts/build_vector_db.py")
        sys.exit(1)

    # Run evaluation
    summary = run_evaluation(
        rag_system=rag,
        questions=questions,
        top_k=args.top_k,
        verbose=not args.quiet,
    )

    # Print results
    print_summary(summary)

    # Save results
    save_results(summary, args.output)
    print(f"Results saved to: {args.output}")

    # Exit with non-zero if metrics are very poor
    if summary.error_rate > 0.5:
        sys.exit(1)


if __name__ == "__main__":
    main()
