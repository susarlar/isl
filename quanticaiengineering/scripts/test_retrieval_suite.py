"""
Test retrieval quality for the 30-question audit suite.

For each test question, runs the full hybrid retrieval pipeline and grades
whether the retrieved chunks contain the concepts/facts the LLM would need
to produce a correct answer. Prints a scorecard and highlights failures.

This is a RETRIEVAL test, not an LLM test — we're measuring whether the
right content reaches the model's context, not whether the model then
synthesizes it well. Retrieval failures are the most common root cause
of bad answers; LLM synthesis failures are diagnosed separately by
actually calling the API.

Usage:
    APP_ENV=test python scripts/test_retrieval_suite.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.embeddings import EmbeddingGenerator
from app.vector_store import FAISSVectorStore
from app.rag_system import IsekaiRAGSystem
from config import VECTOR_STORE_PATH, EMBEDDING_MODEL, TOP_K_DOCUMENTS


# Each test is:
#   id, question, required_concepts, forbidden_concepts, notes
# required_concepts: list of lowercase substrings — at least one chunk in top-K
#   must contain each of these. Missing = retrieval gap.
# forbidden_concepts: list of lowercase substrings that SHOULD NOT appear in
#   top-K (e.g., "stacks multiplicatively" is a hallucination trigger).
TESTS = [
    # ============================================================
    # Category A — Smoke tests
    # ============================================================
    (
        "A1",
        "What is Fellow Power? Explain the formula.",
        ["base", "aptitude", "level multiplier", "additive", "σ"],
        [],
        "Core formula should be retrievable",
    ),
    (
        "A2",
        "Tell me about Amaterasu",
        ["amaterasu", "empyrean sound", "inspiring", "120"],
        [],
        "Named entity with keyword boost",
    ),
    (
        "A3",
        "What typings are in the game?",
        ["brave", "diligent", "unfettered", "inspiring", "informed"],
        ["healer"],
        "5 typings, no Healer",
    ),
    (
        "A4",
        "What fellows do you know?",
        ["amaterasu", "sunna", "leon", "all fellows by name"],
        [],
        "Master index should be top result",
    ),
    (
        "A5",
        "How does awakening work?",
        ["4", "5", "6", "stars", "stones", "aptitude slot"],
        [],
        "Awakening gates + aptitude slots",
    ),
    # ============================================================
    # Category B — Named-entity + typing-scoped retrieval
    # ============================================================
    (
        "B6",
        "How do I maximize fellow power for Sunna?",
        [
            "sunna",
            "fish",
            "family",
            "stella",
            "aptitude",
            "artifact",
            "awakening",
            "building",
        ],
        [],
        "Power optimization with domain expansion — needs ALL domains covered",
    ),
    (
        "B7",
        "i am unfettered main with fishing levels over 1000 in unfettered ponds. what should be my fishing strategy?",
        [
            "unfettered",
            "sea angel",
            "drakenberg monster",
            "goddess sponge",
            "spot rotation",
        ],
        [],
        "Unfettered fish table must be retrieved",
    ),
    (
        "B8",
        "Tell me about Beelzebub",
        ["beelzebub", "unfettered", "empyrean sound"],
        [],
        "Non-top-tier fellow retrieval",
    ),
    (
        "B9",
        "Compare Leon and Heracles for a Brave main",
        ["leon", "heracles", "empyrean sound", "brave", "family"],
        [],
        "Equivalence rule + family count knowledge",
    ),
    (
        "B10",
        "Belzebub main carry strategy",
        ["beelzebub", "unfettered"],
        [],
        "Typo: 'Belzebub' should still retrieve Beelzebub chunks",
    ),
    # ============================================================
    # Category C — Anti-hallucination guardrails
    # ============================================================
    (
        "C11",
        "How should I push Stella on Fifi?",
        ["fifi", "n ", "hard rules", "never"],
        [],
        "Must surface Rarity Capability Matrix / hard rules content",
    ),
    (
        "C12",
        "What's the best Informed main?",
        ["aegle", "neptune", "not recommend"],
        [],
        "Neptune anti-recommendation must be visible",
    ),
    (
        "C13",
        "Should I switch from Sunna to Master Tongxuan if I'm already invested?",
        ["sunna", "master tongxuan", "family"],
        [],
        "Equivalence + new Family Stella nuance — Tongxuan has better family coverage",
    ),
    (
        "C14",
        "How does Advanced Blessing compound with other multipliers?",
        ["additive", "advanced blessing", "σ"],
        ["stacks multiplicatively"],
        "Must retrieve additive-math content. 'compound exponentially' is OK in blessing-cost context",
    ),
    (
        "C15",
        "What antique should I max in the museum?",
        [
            "oyster trap",
            "narwhal",
            "sledge",
            "bear-eared seal",
            "mammoth",
        ],
        [],
        "Must retrieve the Quick Answer section",
    ),
    # ============================================================
    # Category D — Mechanical depth
    # ============================================================
    (
        "D16",
        "Explain the aptitude slot system on a UR fellow",
        [
            "supreme talent",
            "slot",
            "insight",
            "limit break",
            "alraune",
            "proficiency",
        ],
        [],
        "New aptitude slot system from skill-pearls.md rewrite",
    ),
    (
        "D17",
        "What's the difference between Museum gold and Museum coins?",
        [
            "museum",
            "gold",
            "coins",
            "bronze",
            "silver",
            "museum card",
        ],
        [],
        "Two-economy separation",
    ),
    (
        "D18",
        "What is Bond and how does it work?",
        ["bond", "intimacy", "blessing power", "student"],
        [],
        "Bond stat determines student rarity",
    ),
    (
        "D19",
        "I got Acquaint Stones. Who should I awaken?",
        ["awakening", "aegle", "mio", "mulberry"],
        ["neptune as main"],
        "Awakening priority list without Neptune",
    ),
    (
        "D20",
        "What should I spend my crystals on?",
        ["crystal", "white pearl", "black pearl", "event"],
        [],
        "New crystal economy section",
    ),
    # ============================================================
    # Category E — NEW additional tests (generated this pass)
    # ============================================================
    (
        "E21",
        "Best Diligent main between Sunna and Master Tongxuan?",
        [
            "sunna",
            "master tongxuan",
            "cranelia",
            "wadjetta",
            "family",
        ],
        [],
        "Should retrieve the new Family Stella comparison",
    ),
    (
        "E22",
        "Is Beelzebub a good Unfettered main?",
        ["beelzebub", "unfettered", "120", "empyrean sound"],
        [],
        "Should reflect her top-tier framing",
    ),
    (
        "E23",
        "Does the aptitude cap on Supreme Talent go beyond 900?",
        [
            "supreme talent",
            "cap",
            "stella",
            "awakening",
        ],
        [],
        "New 'caps are not hard ceilings' content",
    ),
    (
        "E24",
        "How much Skill Pearl aptitude can a fully invested UR carry actually reach?",
        ["20,965", "aptitude", "stella", "awakening", "costume"],
        [],
        "Endgame ceiling + slot unlock mechanics",
    ),
    (
        "E25",
        "What Family Stella do I get on Master Tongxuan?",
        [
            "master tongxuan",
            "cranelia",
            "wadjetta",
            "emiru",
            "pan pan",
        ],
        [],
        "Master Tongxuan family list",
    ),
    (
        "E26",
        "How do I get more Acquaint Stones?",
        [
            "acquaint",
            "fragment",
            "synthesize",
            "event",
            "fountain",
        ],
        [],
        "Acquaint Stone sourcing",
    ),
    (
        "E27",
        "What fish should I prioritize if I main Inspiring?",
        [
            "axolotl",
            "barreleye",
            "megakarp",
            "ocean",
        ],
        [],
        "Inspiring fish priority",
    ),
    (
        "E28",
        "Should I recycle a Magic Lamp for a new artifact?",
        ["artifact", "magic lamp", "awakening", "materia"],
        [],
        "Artifact investment strategy",
    ),
    (
        "E29",
        "How many fragments does Stella Lv 11 need on Empyrean Sound?",
        ["empyrean sound", "11", "100", "frag"],
        [],
        "Stella level cost data",
    ),
    (
        "E30",
        "What's a custom slot family and how do I use it?",
        ["lancelot", "hestia", "hanamiya rica", "custom"],
        [],
        "Custom slot family mechanic",
    ),
    # ============================================================
    # Category F — Mechanic Deep Dives
    # ============================================================
    (
        "F31",
        "What's the difference between normal and gold crown fish?",
        ["gold crown", "normal", "variant", "skill"],
        [],
        "Gold Crown variant mechanic (not a 'next level')",
    ),
    (
        "F32",
        "What does a limit break give my fellow?",
        ["limit break", "aptitude", "level cap"],
        [],
        "Limit break is flat aptitude + level cap raise, NOT a multiplier",
    ),
    (
        "F33",
        "Explain the Resonance Power mechanic",
        ["resonance", "top-tier", "final"],
        [],
        "Resonance Power is a final-multiplier top-tier mechanic",
    ),
    (
        "F34",
        "What's the difference between Magic Ore and Breakthrough Materia?",
        ["magic ore", "breakthrough", "materia", "10"],
        [],
        "Breakthrough Materia gates past Lv 10, Magic Ore is the leveling currency",
    ),
    (
        "F35",
        "How do Reforge Oils work?",
        ["reforge", "oil", "reroll", "skill"],
        [],
        "Reforge Oils reroll artifact skill slots",
    ),
    # ============================================================
    # Category G — Rare / Specific Fellows
    # ============================================================
    (
        "G36",
        "Can I awaken my SR fellow Fawna?",
        ["fawna", "sr", "awaken", "ssr"],
        [],
        "SR fellows cannot be awakened — Rarity Capability Matrix",
    ),
    (
        "G37",
        "Tell me about Beryl",
        ["beryl", "brave", "ur+"],
        [],
        "Beryl is UR+ Brave",
    ),
    (
        "G38",
        "Who is Gabrael?",
        ["gabrael", "uncrowned", "informed"],
        [],
        "Gabrael is UR+ Informed in Uncrowned group",
    ),
    (
        "G39",
        "How does Lokia upgrade from SSR to UR?",
        ["lokia", "upgrade", "empyrean sound"],
        [],
        "Lokia is SSR Diligent upgradeable to UR Empyrean Sound",
    ),
    (
        "G40",
        "List the Dragon Maid collab fellows",
        ["dragon maid", "tohru", "kanna", "fafnir", "elma"],
        [],
        "Dragon Maid collab roster",
    ),
    # ============================================================
    # Category H — Account State / Multi-Part Queries
    # ============================================================
    (
        "H41",
        "I'm a new Diligent main at level 45. Give me my first action plan.",
        ["diligent", "master tongxuan", "family", "fish", "stella"],
        [],
        "Comprehensive Diligent main guidance",
    ),
    (
        "H42",
        "I have Skill Pearls saved up. Where should I spend them?",
        ["skill pearl", "supreme talent", "main carry"],
        [],
        "Skill pearl allocation priority",
    ),
    (
        "H43",
        "What do I need to reach 6-star awakening on my main carry?",
        ["6", "star", "acquaint", "gate"],
        [],
        "6-star gate requirements",
    ),
    (
        "H44",
        "How do I fill the 4-star awakening gate?",
        ["4", "star", "15", "sub-fellow"],
        [],
        "4-star gate requires 15 3-star sub-fellows",
    ),
    (
        "H45",
        "The Museum is an Informed building — which fellows should operate it?",
        ["museum", "informed", "cimitir", "aegle"],
        [],
        "Museum building is Informed-typed; Aegle is recommended",
    ),
    # ============================================================
    # Category I — Meta / Negative / Tricky
    # ============================================================
    (
        "I46",
        "What should I NOT spend crystals on?",
        ["crystal", "dates", "not"],
        [],
        "Crystal negative advice — don't spend on dates",
    ),
    (
        "I47",
        "Which events give the best rewards?",
        ["cloud kingdom", "olympics", "penglai", "rewards"],
        [],
        "Event ranking — Olympics and Penglai are top",
    ),
    (
        "I48",
        "How does Siege Warfare work?",
        ["siege", "team", "1%", "match chain"],
        [],
        "Siege mechanic — 1% loss per win in match chain",
    ),
    (
        "I49",
        "What's the difference between Fellow Blessing and Advanced Blessing?",
        ["fellow blessing", "advanced blessing", "flat", "%"],
        [],
        "Fellow Blessing is flat, Advanced Blessing is %",
    ),
    (
        "I50",
        "Does this game have PvP? Explain siege and trade post battles.",
        ["siege", "trade post"],
        [],
        "Closest to PvP are siege and trade post negotiation",
    ),
]


def grade_retrieval(rag, question):
    """Run retrieval and return (results, retrieval_time_ms)."""
    results, retrieval_time = rag._retrieve(question, k=TOP_K_DOCUMENTS)
    return results, retrieval_time


def check_concepts(results, concepts):
    """
    For each required concept, check whether at least one chunk contains it.
    Returns {concept: bool_found}.
    """
    joined = "\n".join(c.content.lower() for c, _ in results)
    return {c: (c in joined) for c in concepts}


def check_forbidden(results, forbidden):
    """Return forbidden concepts that DO appear (should be empty)."""
    joined = "\n".join(c.content.lower() for c, _ in results)
    return [f for f in forbidden if f in joined]


def grade_question(rag, test):
    test_id, question, required, forbidden, notes = test
    results, _ = grade_retrieval(rag, question)

    required_status = check_concepts(results, required)
    forbidden_hits = check_forbidden(results, forbidden)

    required_missing = [c for c, found in required_status.items() if not found]

    # Grade: pass if all required found AND no forbidden hits
    passed = len(required_missing) == 0 and len(forbidden_hits) == 0

    return {
        "id": test_id,
        "question": question,
        "notes": notes,
        "passed": passed,
        "required_missing": required_missing,
        "forbidden_hits": forbidden_hits,
        "top_chunks": [
            (c.metadata.get("filename", "?"), c.metadata.get("heading", "") or "-")
            for c, _ in results[:5]
        ],
    }


def main():
    print("=" * 80)
    print("RETRIEVAL TEST SUITE — Isekai Fellow Power Advisor")
    print("=" * 80)
    print()
    print("Loading RAG components...")

    eg = EmbeddingGenerator(model_name=EMBEDDING_MODEL)
    vs = FAISSVectorStore(embedding_dimension=eg.embedding_dimension)
    vs.load(str(VECTOR_STORE_PATH))

    class Stub:
        pass

    rag = Stub()
    rag.embedding_generator = eg
    rag.vector_store = vs
    rag._retrieve = IsekaiRAGSystem._retrieve.__get__(rag, Stub)
    rag._KEYWORD_ENTITIES = IsekaiRAGSystem._KEYWORD_ENTITIES
    rag._KEYWORD_ALIASES = IsekaiRAGSystem._KEYWORD_ALIASES
    rag._KEYWORD_DOMAIN_PHRASES = IsekaiRAGSystem._KEYWORD_DOMAIN_PHRASES
    rag._POWER_QUERY_TRIGGERS = IsekaiRAGSystem._POWER_QUERY_TRIGGERS
    rag._POWER_DOMAIN_SUBQUERIES = IsekaiRAGSystem._POWER_DOMAIN_SUBQUERIES

    print(f"Loaded {len(vs.chunks)} chunks")
    print(f"TOP_K: {TOP_K_DOCUMENTS}")
    print()

    results = []
    for test in TESTS:
        r = grade_question(rag, test)
        results.append(r)

    # Print scorecard
    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)
    print("=" * 80)
    print(f"SCORECARD: {passed_count}/{total} passed")
    print("=" * 80)
    print()

    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"[{status}] {r['id']}: {r['question'][:70]}")
        if r["required_missing"]:
            print(f"       Missing required concepts: {r['required_missing']}")
        if r["forbidden_hits"]:
            print(f"       FORBIDDEN hits: {r['forbidden_hits']}")
        if not r["passed"]:
            print(f"       Top 5 retrieved:")
            for fn, h in r["top_chunks"]:
                print(f"         - {fn} :: {h[:50]}")
        print()

    # Failures summary
    failures = [r for r in results if not r["passed"]]
    if failures:
        print("=" * 80)
        print(f"FAILURES: {len(failures)}")
        print("=" * 80)
        for f in failures:
            print(f"  {f['id']}: {f['notes']}")

    return passed_count, total, failures


if __name__ == "__main__":
    passed, total, failures = main()
    sys.exit(0 if len(failures) == 0 else 1)
