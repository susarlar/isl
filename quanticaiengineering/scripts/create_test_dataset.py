"""
Create Test Dataset for RAG Evaluation
=======================================

Generates a curated set of 25 questions covering all policy topics.
Saves to data/test_queries.json.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import TEST_DATASET_PATH

# fmt: off
QUESTIONS = [
    # ---------- Leave & Time Off ----------
    {
        "question_id": "leave_001",
        "question": "How many days of paid time off do full-time employees receive per year?",
        "expected_sources": ["leave_and_time_off.md"],
        "gold_answer_keywords": ["PTO", "days", "annual", "accrual"],
        "category": "leave",
    },
    {
        "question_id": "leave_002",
        "question": "What is the parental leave policy for new parents?",
        "expected_sources": ["leave_and_time_off.md"],
        "gold_answer_keywords": ["parental", "maternity", "paternity", "weeks"],
        "category": "leave",
    },
    {
        "question_id": "leave_003",
        "question": "How do I request sick leave and how many sick days am I entitled to?",
        "expected_sources": ["leave_and_time_off.md"],
        "gold_answer_keywords": ["sick", "days", "request", "notify"],
        "category": "leave",
    },
    {
        "question_id": "leave_004",
        "question": "What are the company-observed holidays?",
        "expected_sources": ["leave_and_time_off.md"],
        "gold_answer_keywords": ["holiday", "observed", "federal"],
        "category": "leave",
    },
    # ---------- Remote Work ----------
    {
        "question_id": "remote_001",
        "question": "What are the eligibility requirements for remote work?",
        "expected_sources": ["remote_work_policy.md"],
        "gold_answer_keywords": ["eligible", "remote", "criteria", "approval"],
        "category": "remote_work",
    },
    {
        "question_id": "remote_002",
        "question": "How many days per week can employees work from home?",
        "expected_sources": ["remote_work_policy.md"],
        "gold_answer_keywords": ["days", "week", "home", "office"],
        "category": "remote_work",
    },
    {
        "question_id": "remote_003",
        "question": "What equipment does the company provide for remote workers?",
        "expected_sources": ["remote_work_policy.md", "equipment_it_usage_policy.md"],
        "gold_answer_keywords": ["laptop", "equipment", "provide", "setup"],
        "category": "remote_work",
    },
    # ---------- Expenses ----------
    {
        "question_id": "expense_001",
        "question": "What is the daily meal allowance when traveling for business?",
        "expected_sources": ["expense_reimbursement_policy.md"],
        "gold_answer_keywords": ["meal", "per diem", "allowance", "travel"],
        "category": "expenses",
    },
    {
        "question_id": "expense_002",
        "question": "How do I submit an expense report and what is the deadline?",
        "expected_sources": ["expense_reimbursement_policy.md"],
        "gold_answer_keywords": ["submit", "expense", "report", "deadline", "receipt"],
        "category": "expenses",
    },
    {
        "question_id": "expense_003",
        "question": "What expenses are not reimbursable?",
        "expected_sources": ["expense_reimbursement_policy.md"],
        "gold_answer_keywords": ["not reimbursable", "excluded", "personal"],
        "category": "expenses",
    },
    # ---------- Information Security ----------
    {
        "question_id": "security_001",
        "question": "What are the password requirements for company systems?",
        "expected_sources": ["information_security_policy.md"],
        "gold_answer_keywords": ["password", "length", "characters", "uppercase"],
        "category": "security",
    },
    {
        "question_id": "security_002",
        "question": "How should I report a security incident or data breach?",
        "expected_sources": ["information_security_policy.md"],
        "gold_answer_keywords": ["report", "incident", "security", "notify", "breach"],
        "category": "security",
    },
    {
        "question_id": "security_003",
        "question": "What is the policy on using personal devices for work?",
        "expected_sources": ["information_security_policy.md", "equipment_it_usage_policy.md"],
        "gold_answer_keywords": ["personal device", "BYOD", "approved", "MDM"],
        "category": "security",
    },
    # ---------- Professional Development ----------
    {
        "question_id": "prodev_001",
        "question": "What is the annual professional development budget per employee?",
        "expected_sources": ["professional_development_policy.md"],
        "gold_answer_keywords": ["budget", "annual", "development", "training"],
        "category": "professional_development",
    },
    {
        "question_id": "prodev_002",
        "question": "Are online courses and certifications covered by the professional development budget?",
        "expected_sources": ["professional_development_policy.md"],
        "gold_answer_keywords": ["course", "certification", "online", "eligible"],
        "category": "professional_development",
    },
    # ---------- Social Media ----------
    {
        "question_id": "social_001",
        "question": "Can I post about my work on personal social media accounts?",
        "expected_sources": ["social_media_policy.md"],
        "gold_answer_keywords": ["social media", "personal", "post", "confidential"],
        "category": "social_media",
    },
    # ---------- Email & Communication ----------
    {
        "question_id": "email_001",
        "question": "What is the expected response time for business emails?",
        "expected_sources": ["email_communication_policy.md"],
        "gold_answer_keywords": ["response time", "email", "business", "hours"],
        "category": "communication",
    },
    # ---------- Workplace Safety ----------
    {
        "question_id": "safety_001",
        "question": "What should I do if I witness a workplace accident?",
        "expected_sources": ["workplace_safety_policy.md"],
        "gold_answer_keywords": ["accident", "report", "injury", "emergency"],
        "category": "safety",
    },
    # ---------- Employee Handbook ----------
    {
        "question_id": "handbook_001",
        "question": "What is the performance review cycle at the company?",
        "expected_sources": ["employee_handbook.md"],
        "gold_answer_keywords": ["performance", "review", "annual", "cycle"],
        "category": "hr",
    },
    {
        "question_id": "handbook_002",
        "question": "What is the dress code policy?",
        "expected_sources": ["employee_handbook.md"],
        "gold_answer_keywords": ["dress", "attire", "professional", "casual"],
        "category": "hr",
    },
    # ---------- IT & Equipment ----------
    {
        "question_id": "it_001",
        "question": "What software can I install on my company laptop?",
        "expected_sources": ["equipment_it_usage_policy.md"],
        "gold_answer_keywords": ["software", "approved", "install", "IT"],
        "category": "it",
    },
    # ---------- Data Privacy ----------
    {
        "question_id": "privacy_001",
        "question": "How is employee personal data protected and used?",
        "expected_sources": ["data_privacy_policy.md"],
        "gold_answer_keywords": ["personal data", "privacy", "GDPR", "stored"],
        "category": "privacy",
    },
    {
        "question_id": "privacy_002",
        "question": "Who can I contact regarding data privacy concerns?",
        "expected_sources": ["data_privacy_policy.md"],
        "gold_answer_keywords": ["contact", "privacy", "officer", "DPO"],
        "category": "privacy",
    },
    # ---------- Out-of-corpus (tests refusal guardrail) ----------
    {
        "question_id": "ooc_001",
        "question": "What is the capital of France?",
        "expected_sources": [],
        "gold_answer_keywords": ["only answer", "policy", "not covered"],
        "category": "out_of_corpus",
    },
    {
        "question_id": "ooc_002",
        "question": "Can you help me write a Python script to scrape websites?",
        "expected_sources": [],
        "gold_answer_keywords": ["only answer", "policy", "not covered"],
        "category": "out_of_corpus",
    },
]
# fmt: on


def main():
    output_path = Path(TEST_DATASET_PATH)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(QUESTIONS, f, indent=2, ensure_ascii=False)

    print(f"✓ Created test dataset with {len(QUESTIONS)} questions")
    print(f"  Saved to: {output_path}")

    categories = {}
    for q in QUESTIONS:
        categories.setdefault(q["category"], 0)
        categories[q["category"]] += 1

    print("\nBreakdown by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
