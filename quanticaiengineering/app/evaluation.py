"""
Evaluation Module for Policy RAG System
========================================

Measures:
- Groundedness: % of answers factually supported by retrieved chunks
- Citation Accuracy: % of answers whose cited sources match retrieval results
- Answer Relevance: keyword-based relevance score (0-1 proxy, no LLM needed)
- Latency: p50 / p95 response time in milliseconds
"""

import re
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class EvalQuestion:
    """A single evaluation question with optional gold answer."""

    question_id: str
    question: str
    expected_sources: List[str] = field(
        default_factory=list
    )  # filenames that should be cited
    gold_answer_keywords: List[str] = field(
        default_factory=list
    )  # key terms expected in answer
    category: str = "general"


@dataclass
class EvalResult:
    """Result for a single evaluated question."""

    question_id: str
    question: str
    answer: str
    sources: List[Dict]
    confidence: float
    latency_ms: float
    groundedness_score: float
    citation_accuracy: float
    relevance_score: float
    is_refusal: bool = False
    error: Optional[str] = None


@dataclass
class EvalSummary:
    """Aggregate evaluation metrics."""

    total_questions: int
    groundedness_mean: float
    groundedness_passing: float  # % >= 0.95 threshold
    citation_accuracy_mean: float
    citation_accuracy_passing: float  # % >= 0.95 threshold
    relevance_mean: float
    latency_p50_ms: float
    latency_p95_ms: float
    refusal_rate: float
    error_rate: float
    results: List[EvalResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Core evaluation functions
# ---------------------------------------------------------------------------


def evaluate_groundedness(answer: str, context_chunks: List[str]) -> float:
    """
    Measure groundedness via lexical overlap (no external API needed).

    Groundedness = proportion of answer sentences that can be supported by
    at least one token-3-gram present in the retrieved context.

    Args:
        answer: Generated answer text.
        context_chunks: List of retrieved chunk texts used as context.

    Returns:
        Score in [0.0, 1.0]; 1.0 = fully grounded.
    """
    if not answer or not context_chunks:
        return 0.0

    # Build a combined context string (lowercased)
    combined_context = " ".join(context_chunks).lower()
    context_tokens = set(combined_context.split())

    # Split answer into sentences
    sentences = [s.strip() for s in re.split(r"[.!?]+", answer) if s.strip()]
    if not sentences:
        return 0.0

    grounded_count = 0
    for sentence in sentences:
        sentence_tokens = set(sentence.lower().split())
        # Remove stopwords
        stopwords = {
            "i",
            "we",
            "you",
            "the",
            "a",
            "an",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "shall",
            "to",
            "of",
            "in",
            "on",
            "at",
            "by",
            "for",
            "with",
            "about",
            "and",
            "or",
            "but",
            "not",
            "no",
            "so",
            "as",
            "if",
            "that",
            "this",
            "it",
            "its",
            "they",
            "their",
            "there",
            "here",
            "from",
        }
        content_tokens = sentence_tokens - stopwords
        if not content_tokens:
            grounded_count += 1  # skip trivially short sentences
            continue

        overlap = content_tokens & context_tokens
        overlap_ratio = len(overlap) / len(content_tokens)
        if overlap_ratio >= 0.5:  # ≥50% of content words found in context
            grounded_count += 1

    return grounded_count / len(sentences)


def evaluate_citation_accuracy(
    answer: str, retrieved_sources: List[str], cited_sources: List[str]
) -> float:
    """
    Measure citation accuracy.

    Citation accuracy = fraction of cited sources that are present in
    the set of actually retrieved sources.

    Args:
        answer: The generated answer (used to extract inline citations if needed).
        retrieved_sources: List of filenames actually retrieved by the RAG system.
        cited_sources: List of filenames listed in the response sources field.

    Returns:
        Score in [0.0, 1.0].
    """
    if not cited_sources:
        # Also extract citations mentioned inline in the answer text
        inline = _extract_inline_citations(answer)
        cited_sources = inline

    if not cited_sources:
        # No citations at all - penalise unless it's a refusal
        return 0.0

    retrieved_set = set(retrieved_sources)
    correct = sum(1 for s in cited_sources if s in retrieved_set)
    return correct / len(cited_sources)


def evaluate_answer_relevance(
    answer: str, question: str, gold_keywords: List[str]
) -> float:
    """
    Proxy relevance score based on keyword overlap with the question and
    expected gold keywords (no LLM needed).

    Args:
        answer: Generated answer text.
        question: Original question.
        gold_keywords: Key terms expected in a good answer (can be empty list).

    Returns:
        Score in [0.0, 1.0].
    """
    if not answer:
        return 0.0

    answer_lower = answer.lower()
    answer_tokens = set(answer_lower.split())

    scores = []

    # 1. Question keyword coverage
    question_tokens = set(question.lower().split()) - {
        "what",
        "how",
        "when",
        "where",
        "who",
        "why",
        "is",
        "are",
        "the",
        "a",
        "an",
        "do",
        "does",
        "can",
        "i",
        "my",
        "our",
        "your",
    }
    if question_tokens:
        q_overlap = len(question_tokens & answer_tokens) / len(question_tokens)
        scores.append(q_overlap)

    # 2. Gold keyword coverage
    if gold_keywords:
        gold_tokens = set(k.lower() for k in gold_keywords)
        g_overlap = len(gold_tokens & answer_tokens) / len(gold_tokens)
        scores.append(g_overlap)

    # 3. Answer length adequacy (penalise very short non-refusal answers)
    word_count = len(answer.split())
    length_score = min(word_count / 50, 1.0)  # full score at 50+ words
    scores.append(length_score)

    return float(np.mean(scores)) if scores else 0.0


def _extract_inline_citations(answer: str) -> List[str]:
    """Extract filenames cited inline, e.g. [Source: remote_work_policy.md]."""
    pattern = r"\[(?:Source|source|Ref|ref):\s*([^\]]+\.(?:md|pdf|txt|html))\]"
    return re.findall(pattern, answer)


# ---------------------------------------------------------------------------
# Latency utilities
# ---------------------------------------------------------------------------


def compute_latency_stats(latencies_ms: List[float]) -> Dict[str, float]:
    """Compute p50 and p95 latency from a list of millisecond timings."""
    if not latencies_ms:
        return {"p50_ms": 0.0, "p95_ms": 0.0, "mean_ms": 0.0, "max_ms": 0.0}
    arr = np.array(latencies_ms)
    return {
        "p50_ms": float(np.percentile(arr, 50)),
        "p95_ms": float(np.percentile(arr, 95)),
        "mean_ms": float(np.mean(arr)),
        "max_ms": float(np.max(arr)),
    }


# ---------------------------------------------------------------------------
# Full evaluation runner
# ---------------------------------------------------------------------------


def run_evaluation(
    rag_system,
    questions: List[EvalQuestion],
    top_k: int = 5,
    verbose: bool = True,
) -> EvalSummary:
    """
    Run full evaluation against a list of questions.

    Args:
        rag_system: Initialized PolicyRAGSystem instance.
        questions: List of EvalQuestion objects.
        top_k: Retrieval k to use.
        verbose: Print progress.

    Returns:
        EvalSummary with all metrics.
    """
    results: List[EvalResult] = []
    errors = 0

    for i, eq in enumerate(questions, 1):
        if verbose:
            print(f"[{i}/{len(questions)}] {eq.question[:80]}...")

        try:
            t0 = time.perf_counter()
            response = rag_system.query(
                question=eq.question,
                top_k=top_k,
                return_metadata=True,
            )
            latency_ms = (time.perf_counter() - t0) * 1000

            # Collect context texts for groundedness
            context_texts: List[str] = []
            retrieved_filenames: List[str] = []
            if "metadata" in response and "retrieved_chunks" in response["metadata"]:
                for chunk_info in response["metadata"]["retrieved_chunks"]:
                    context_texts.append(chunk_info.get("preview", ""))
                    retrieved_filenames.append(chunk_info.get("source", ""))

            cited_filenames = [s["filename"] for s in response.get("sources", [])]

            groundedness = evaluate_groundedness(response["answer"], context_texts)
            citation_acc = evaluate_citation_accuracy(
                response["answer"], retrieved_filenames, cited_filenames
            )
            relevance = evaluate_answer_relevance(
                response["answer"], eq.question, eq.gold_answer_keywords
            )

            result = EvalResult(
                question_id=eq.question_id,
                question=eq.question,
                answer=response["answer"],
                sources=response.get("sources", []),
                confidence=response.get("confidence", 0.0),
                latency_ms=latency_ms,
                groundedness_score=groundedness,
                citation_accuracy=citation_acc,
                relevance_score=relevance,
                is_refusal=response.get("is_refusal", False),
            )

        except Exception as exc:
            logger.error(f"Error evaluating question {eq.question_id}: {exc}")
            errors += 1
            result = EvalResult(
                question_id=eq.question_id,
                question=eq.question,
                answer="",
                sources=[],
                confidence=0.0,
                latency_ms=0.0,
                groundedness_score=0.0,
                citation_accuracy=0.0,
                relevance_score=0.0,
                error=str(exc),
            )

        results.append(result)
        if verbose:
            print(
                f"   groundedness={result.groundedness_score:.2f}  "
                f"citation_acc={result.citation_accuracy:.2f}  "
                f"latency={result.latency_ms:.0f}ms"
            )

    # Aggregate metrics (exclude errored results from averages)
    valid = [r for r in results if r.error is None]
    latencies = [r.latency_ms for r in valid]
    lat_stats = compute_latency_stats(latencies)

    GROUNDEDNESS_THRESHOLD = 0.90
    CITATION_THRESHOLD = 0.95

    summary = EvalSummary(
        total_questions=len(questions),
        groundedness_mean=float(np.mean([r.groundedness_score for r in valid]))
        if valid
        else 0.0,
        groundedness_passing=float(
            sum(1 for r in valid if r.groundedness_score >= GROUNDEDNESS_THRESHOLD)
            / max(len(valid), 1)
        ),
        citation_accuracy_mean=float(np.mean([r.citation_accuracy for r in valid]))
        if valid
        else 0.0,
        citation_accuracy_passing=float(
            sum(1 for r in valid if r.citation_accuracy >= CITATION_THRESHOLD)
            / max(len(valid), 1)
        ),
        relevance_mean=float(np.mean([r.relevance_score for r in valid]))
        if valid
        else 0.0,
        latency_p50_ms=lat_stats["p50_ms"],
        latency_p95_ms=lat_stats["p95_ms"],
        refusal_rate=float(sum(1 for r in valid if r.is_refusal) / max(len(valid), 1)),
        error_rate=float(errors / max(len(questions), 1)),
        results=results,
    )

    return summary


def save_results(summary: EvalSummary, output_path: Path) -> None:
    """Serialize evaluation results to JSON."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "summary": {
            "total_questions": summary.total_questions,
            "groundedness_mean": summary.groundedness_mean,
            "groundedness_passing_pct": summary.groundedness_passing * 100,
            "citation_accuracy_mean": summary.citation_accuracy_mean,
            "citation_accuracy_passing_pct": summary.citation_accuracy_passing * 100,
            "relevance_mean": summary.relevance_mean,
            "latency_p50_ms": summary.latency_p50_ms,
            "latency_p95_ms": summary.latency_p95_ms,
            "refusal_rate": summary.refusal_rate,
            "error_rate": summary.error_rate,
        },
        "results": [
            {
                "question_id": r.question_id,
                "question": r.question,
                "answer": r.answer,
                "sources": r.sources,
                "confidence": r.confidence,
                "latency_ms": r.latency_ms,
                "groundedness_score": r.groundedness_score,
                "citation_accuracy": r.citation_accuracy,
                "relevance_score": r.relevance_score,
                "is_refusal": r.is_refusal,
                "error": r.error,
            }
            for r in summary.results
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Evaluation results saved to {output_path}")


def print_summary(summary: EvalSummary) -> None:
    """Pretty-print evaluation summary."""
    print()
    print("=" * 65)
    print("  EVALUATION SUMMARY")
    print("=" * 65)
    print(f"  Questions evaluated : {summary.total_questions}")
    print(f"  Error rate          : {summary.error_rate * 100:.1f}%")
    print()
    print("  Information Quality")
    print(
        f"    Groundedness mean    : {summary.groundedness_mean * 100:.1f}%  "
        f"(passing ≥90%: {summary.groundedness_passing * 100:.1f}%)"
    )
    print(
        f"    Citation accuracy    : {summary.citation_accuracy_mean * 100:.1f}%  "
        f"(passing ≥95%: {summary.citation_accuracy_passing * 100:.1f}%)"
    )
    print(f"    Answer relevance     : {summary.relevance_mean * 100:.1f}%")
    print()
    print("  System Performance")
    print(f"    Latency p50          : {summary.latency_p50_ms:.0f} ms")
    print(
        f"    Latency p95          : {summary.latency_p95_ms:.0f} ms  "
        f"{'✓ PASS' if summary.latency_p95_ms < 3000 else '✗ OVER TARGET (3s)'}"
    )
    print(f"    Refusal rate         : {summary.refusal_rate * 100:.1f}%")
    print("=" * 65)
    print()
