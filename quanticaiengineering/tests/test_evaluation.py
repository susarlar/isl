"""
Tests for the evaluation module.

No external API calls needed - evaluation functions are purely algorithmic.
"""

from app.evaluation import (
    evaluate_groundedness,
    evaluate_citation_accuracy,
    evaluate_answer_relevance,
    compute_latency_stats,
    _extract_inline_citations,
)


# ---------------------------------------------------------------------------
# Groundedness
# ---------------------------------------------------------------------------


class TestGroundedness:
    def test_fully_grounded(self):
        answer = "Employees receive 20 days of paid time off per year."
        context = [
            "Employees receive 20 days of paid time off per year, accrued monthly."
        ]
        score = evaluate_groundedness(answer, context)
        assert score >= 0.8

    def test_not_grounded(self):
        answer = "Employees receive unlimited vacation days and free snacks."
        context = ["The expense reimbursement limit is $500 per trip."]
        score = evaluate_groundedness(answer, context)
        assert score < 0.5

    def test_empty_answer(self):
        assert evaluate_groundedness("", ["some context"]) == 0.0

    def test_empty_context(self):
        assert evaluate_groundedness("some answer", []) == 0.0

    def test_partial_grounding(self):
        answer = "Employees get 20 PTO days. They also get free lunches every day."
        context = ["Employees are entitled to 20 days of paid time off per year."]
        score = evaluate_groundedness(answer, context)
        # First sentence grounded, second not — expect partial score
        assert 0.2 < score < 1.0


# ---------------------------------------------------------------------------
# Citation Accuracy
# ---------------------------------------------------------------------------


class TestCitationAccuracy:
    def test_perfect_citation(self):
        retrieved = ["leave_and_time_off.md", "remote_work_policy.md"]
        cited = ["leave_and_time_off.md"]
        score = evaluate_citation_accuracy("", retrieved, cited)
        assert score == 1.0

    def test_wrong_citation(self):
        retrieved = ["leave_and_time_off.md"]
        cited = ["nonexistent_policy.md"]
        score = evaluate_citation_accuracy("", retrieved, cited)
        assert score == 0.0

    def test_mixed_citations(self):
        retrieved = ["leave_and_time_off.md", "remote_work_policy.md"]
        cited = ["leave_and_time_off.md", "made_up.md"]
        score = evaluate_citation_accuracy("", retrieved, cited)
        assert score == 0.5

    def test_no_citations(self):
        score = evaluate_citation_accuracy("no citations here", ["policy.md"], [])
        assert score == 0.0

    def test_inline_citation_extraction(self):
        answer = "See [Source: remote_work_policy.md] for details."
        retrieved = ["remote_work_policy.md"]
        score = evaluate_citation_accuracy(answer, retrieved, [])
        # Should extract inline citation and find it in retrieved set
        assert score == 1.0


# ---------------------------------------------------------------------------
# Relevance
# ---------------------------------------------------------------------------


class TestRelevance:
    def test_relevant_answer(self):
        answer = (
            "Employees receive 20 days of PTO per year, accruing 1.67 days monthly."
        )
        question = "How many PTO days do employees get?"
        keywords = ["20", "days", "PTO", "annual"]
        score = evaluate_answer_relevance(answer, question, keywords)
        assert score >= 0.5

    def test_empty_answer(self):
        score = evaluate_answer_relevance("", "What is PTO?", ["PTO"])
        assert score == 0.0

    def test_no_gold_keywords(self):
        answer = "The remote work policy requires manager approval."
        question = "What is the remote work policy?"
        score = evaluate_answer_relevance(answer, question, [])
        assert 0.0 <= score <= 1.0

    def test_short_answer_penalty(self):
        score_short = evaluate_answer_relevance("Yes.", "What is the PTO policy?", [])
        score_long = evaluate_answer_relevance(
            "The PTO policy entitles employees to 20 days of paid time off per year, "
            "accrued on a monthly basis starting from the first day of employment.",
            "What is the PTO policy?",
            [],
        )
        assert score_long > score_short


# ---------------------------------------------------------------------------
# Latency stats
# ---------------------------------------------------------------------------


class TestLatencyStats:
    def test_basic(self):
        import pytest

        latencies = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        stats = compute_latency_stats(latencies)
        assert stats["p50_ms"] == pytest.approx(550.0)
        assert stats["p95_ms"] == pytest.approx(955.0)
        assert stats["mean_ms"] == pytest.approx(550.0)

    def test_empty(self):
        stats = compute_latency_stats([])
        assert stats["p50_ms"] == 0.0
        assert stats["p95_ms"] == 0.0

    def test_single(self):
        stats = compute_latency_stats([250.0])
        assert stats["p50_ms"] == 250.0
        assert stats["p95_ms"] == 250.0


# ---------------------------------------------------------------------------
# Inline citation extraction
# ---------------------------------------------------------------------------


class TestInlineCitationExtraction:
    def test_extract_single(self):
        text = "According to [Source: remote_work_policy.md], remote work requires approval."
        result = _extract_inline_citations(text)
        assert result == ["remote_work_policy.md"]

    def test_extract_multiple(self):
        text = (
            "[Source: leave_and_time_off.md] covers PTO. "
            "[Source: expense_reimbursement_policy.md] covers expenses."
        )
        result = _extract_inline_citations(text)
        assert len(result) == 2

    def test_no_citations(self):
        result = _extract_inline_citations("This answer has no citations.")
        assert result == []
