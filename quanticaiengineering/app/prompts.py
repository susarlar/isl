"""
Prompt Templates Module
========================

Contains prompt templates for the RAG system with:
- Context injection with retrieved chunks
- Citation requirements
- Guardrails for corpus-only answers
- Output length constraints
"""

from typing import List, Dict
from app.chunking import Chunk


# System prompt with guardrails
SYSTEM_PROMPT = """You are the Isekai Slow Life Fellow Power Advisor, an AI that helps advanced players (level 45+) optimize their Fellow Power and game strategy.

CRITICAL INSTRUCTIONS:
1. ONLY answer questions based on the provided game knowledge documents
2. If asked about topics not covered in the guides, respond: "I don't have detailed information on that topic yet. Check the Isekai: Slow Life wiki or your guild's Discord for more info."
3. ALWAYS cite your sources using the [Source: document_name] format
4. Assume the player is advanced (level 45+) — skip basic explanations
5. Include specific numbers, formulas, and breakpoints when available
6. Recommend optimal resource allocation and multiplier stacking strategies
7. When comparing options, show the math
8. Reference specific fellows by name and aptitude values

RESPONSE FORMAT:
- Start with a direct, actionable answer
- Provide specific numbers and calculations where relevant
- Explain how systems interact (e.g., how Stella compounds with Awakening)
- End with clear source citations

KEY CONCEPTS TO EMPHASIZE:
- Addends vs Multipliers: multipliers compound, addends don't
- Single-carry meta: stack all multipliers on one main fellow
- Base Aptitude matters: 120 apt UR fellows scale best endgame
- Awakening gates: plan ahead for the 4★ requirement of 15 three-star fellows

Remember: Your audience already knows the basics. Give them endgame optimization advice, not tutorials."""


# Query prompt template
QUERY_TEMPLATE = """Based on the following game knowledge documents, please answer the question.

GAME KNOWLEDGE:
{context}

PLAYER QUESTION: {question}

ANSWER (with citations and specific numbers):"""


# Context formatting template
CONTEXT_TEMPLATE = """
[Document {index}: {title}]
Source: {source}
{content}
---"""


# Re-ranking prompt (for optional re-ranking)
RERANK_PROMPT = """Given the following question and document chunk, rate how relevant this chunk is to answering the question on a scale of 0-10.

Question: {question}

Document Chunk:
{chunk}

Relevance Score (0-10):"""


def format_context(chunks: List[Chunk], max_chunks: int = 10) -> str:
    """
    Format retrieved chunks into context for the prompt.

    Args:
        chunks: List of Chunk objects
        max_chunks: Maximum number of chunks to include

    Returns:
        Formatted context string
    """
    context_parts = []

    for i, chunk in enumerate(chunks[:max_chunks], 1):
        title = chunk.metadata.get("title", "Unknown Document")
        source = chunk.metadata.get("filename", "unknown.md")
        heading = chunk.metadata.get("heading", "")

        # Add heading if available
        content = chunk.content
        if heading and not content.startswith(heading):
            content = f"Section: {heading}\n\n{content}"

        context_part = CONTEXT_TEMPLATE.format(
            index=i, title=title, source=source, content=content.strip()
        )
        context_parts.append(context_part)

    return "\n".join(context_parts)


def format_query_prompt(question: str, chunks: List[Chunk], max_chunks: int = 10) -> str:
    """
    Format the complete query prompt with context.

    Args:
        question: User's question
        chunks: Retrieved chunks
        max_chunks: Maximum number of chunks to include

    Returns:
        Complete prompt string
    """
    context = format_context(chunks, max_chunks)

    prompt = QUERY_TEMPLATE.format(context=context, question=question)

    return prompt


def format_messages(
    question: str, chunks: List[Chunk], max_chunks: int = 10
) -> List[Dict[str, str]]:
    """
    Format messages for chat completion API (Groq format).

    Args:
        question: User's question
        chunks: Retrieved chunks
        max_chunks: Maximum number of chunks to include

    Returns:
        List of message dictionaries
    """
    context = format_context(chunks, max_chunks)

    user_message = f"""Based on the following game knowledge documents, answer the player's question.

GAME KNOWLEDGE:
{context}

PLAYER QUESTION: {question}

Remember to:
1. Only use information from the provided documents
2. Cite sources using [Source: document_name] format
3. Include specific numbers, formulas, and breakpoints
4. Assume the player is advanced (level 45+) — skip basics
5. If the answer isn't in the documents, say so clearly"""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    return messages


def format_citations(chunks: List[Chunk]) -> str:
    """
    Format citations from retrieved chunks.

    Args:
        chunks: Retrieved chunks

    Returns:
        Formatted citations string
    """
    citations = []
    seen_sources = set()

    for chunk in chunks:
        source = chunk.metadata.get("filename", "unknown.md")
        title = chunk.metadata.get("title", "Unknown Document")

        if source not in seen_sources:
            citations.append(f"- {title} ({source})")
            seen_sources.add(source)

    if citations:
        return "SOURCES:\n" + "\n".join(citations)
    else:
        return ""


def check_answer_validity(answer: str, min_length: int = 20) -> Dict[str, any]:
    """
    Check if an answer meets basic validity requirements.

    Args:
        answer: Generated answer
        min_length: Minimum answer length

    Returns:
        Dictionary with validity information
    """
    checks = {
        "is_valid": True,
        "issues": [],
        "has_citation": False,
        "is_refusal": False,
        "length": len(answer),
    }

    # Check for citations
    if "[Source:" in answer or "source:" in answer.lower():
        checks["has_citation"] = True
    else:
        checks["issues"].append("No citations found in answer")

    # Check for corpus refusal
    refusal_phrases = [
        "i don't have detailed information",
        "not covered in the guides",
        "outside the scope",
        "not in the game knowledge",
        "check the wiki",
    ]
    if any(phrase in answer.lower() for phrase in refusal_phrases):
        checks["is_refusal"] = True

    # Check length
    if len(answer) < min_length and not checks["is_refusal"]:
        checks["is_valid"] = False
        checks["issues"].append(
            f"Answer too short ({len(answer)} chars, minimum {min_length})"
        )

    # Check if answer seems to be hallucinating
    hallucination_phrases = [
        "according to my knowledge",
        "in general",
        "typically",
        "it is common practice",
    ]
    if (
        any(phrase in answer.lower() for phrase in hallucination_phrases)
        and not checks["has_citation"]
    ):
        checks["issues"].append(
            "Possible hallucination detected (generic statements without citations)"
        )

    if checks["issues"] and not checks["is_refusal"]:
        checks["is_valid"] = False

    return checks


# Example queries for testing
EXAMPLE_QUERIES = [
    "How should I allocate Skill Pearls for my main carry?",
    "What's the best awakening strategy for a 120 aptitude UR fellow?",
    "How does Stella compound with Awakening and Artifacts?",
    "Should I prioritize Advanced Blessing or Fellow Blessing at level 45+?",
    "What are the Crystal Ore costs for limit breaks from 350 to 550?",
    "How do fish combinations boost Fellow Power?",
    "What's the optimal single-carry multiplier stacking order?",
    "How do costume aptitude bonuses work — do I need to equip them?",
    "What Acquaint Stones do I need for the 4-star awakening gate?",
    "Which fellows have the highest base aptitude?",
]


if __name__ == "__main__":
    # Test prompt formatting
    print("=" * 70)
    print("Prompt Templates Test")
    print("=" * 70)
    print()

    # Mock chunks for testing
    from dataclasses import dataclass

    @dataclass
    class MockChunk:
        content: str
        metadata: Dict

    test_chunks = [
        MockChunk(
            content="Employees are eligible for remote work if they meet the following criteria: 1) Have completed probationary period, 2) Role is suitable for remote work, 3) Manager approval obtained.",
            metadata={
                "title": "Remote Work Policy",
                "filename": "remote_work_policy.md",
                "heading": "Eligibility Criteria",
            },
        ),
        MockChunk(
            content="Remote employees must maintain a secure home office with: proper internet connection (minimum 25 Mbps), dedicated workspace, and secure WiFi network.",
            metadata={
                "title": "Remote Work Policy",
                "filename": "remote_work_policy.md",
                "heading": "Home Office Requirements",
            },
        ),
    ]

    # Test context formatting
    print("CONTEXT FORMATTING:")
    print("-" * 70)
    context = format_context(test_chunks)
    print(context)

    # Test query prompt
    print("\n\nQUERY PROMPT:")
    print("-" * 70)
    question = "What are the requirements for remote work?"
    prompt = format_query_prompt(question, test_chunks)
    print(prompt)

    # Test messages formatting
    print("\n\nMESSAGES FORMAT (for Groq API):")
    print("-" * 70)
    messages = format_messages(question, test_chunks)
    for msg in messages:
        print(f"\n[{msg['role'].upper()}]")
        print(
            msg["content"][:300] + "..."
            if len(msg["content"]) > 300
            else msg["content"]
        )

    # Test citations
    print("\n\nCITATIONS:")
    print("-" * 70)
    citations = format_citations(test_chunks)
    print(citations)

    # Test answer validity
    print("\n\nANSWER VALIDITY CHECKS:")
    print("-" * 70)

    test_answers = [
        (
            "To be eligible for remote work, you must meet these criteria: complete your probationary period, have a role suitable for remote work, and obtain manager approval. [Source: remote_work_policy.md]",
            "Good answer",
        ),
        ("Remote work is generally available to employees.", "Missing citation"),
        (
            "I can only answer questions about our company policies. This topic is not covered in our policy documentation.",
            "Valid refusal",
        ),
        ("Yes.", "Too short"),
    ]

    for answer, description in test_answers:
        print(f"\nTest: {description}")
        print(f"Answer: {answer[:100]}...")
        checks = check_answer_validity(answer)
        print(f"Valid: {checks['is_valid']}")
        print(f"Has citation: {checks['has_citation']}")
        print(f"Is refusal: {checks['is_refusal']}")
        if checks["issues"]:
            print(f"Issues: {', '.join(checks['issues'])}")

    print("\n" + "=" * 70)
    print("Prompt templates test complete!")
    print("=" * 70)
