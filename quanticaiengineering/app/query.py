"""
Query Interface Module
======================

Interactive CLI for querying the Policy RAG system.

Usage:
    python app/query.py
    python app/query.py "What is the remote work policy?"
    python app/query.py --stream "How much PTO do I get?"
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional
import time

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.rag_system import PolicyRAGSystem
from app.prompts import EXAMPLE_QUERIES
from config import TOP_K_DOCUMENTS


class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def print_header():
    """Print welcome header."""
    print()
    print("=" * 70)
    print(f"{Colors.BOLD}Quantic AI Engineering - Policy Assistant{Colors.ENDC}")
    print("=" * 70)
    print("Ask questions about company policies and procedures.")
    print("Type 'exit', 'quit', or 'q' to exit.")
    print("Type 'help' for example questions.")
    print("=" * 70)
    print()


def print_help():
    """Print help information."""
    print()
    print(f"{Colors.BOLD}Example Questions:{Colors.ENDC}")
    print("-" * 70)
    for i, query in enumerate(EXAMPLE_QUERIES[:5], 1):
        print(f"{i}. {query}")
    print()
    print(f"{Colors.BOLD}Commands:{Colors.ENDC}")
    print("  help    - Show this help message")
    print("  stats   - Show system statistics")
    print("  clear   - Clear screen")
    print("  exit    - Exit the program")
    print()


def print_stats(rag: PolicyRAGSystem):
    """Print system statistics."""
    print()
    print(f"{Colors.BOLD}System Statistics:{Colors.ENDC}")
    print("-" * 70)

    stats = rag.get_stats()

    print(f"Model: {stats['model']}")
    print(f"Top-K Retrieval: {stats['top_k']}")
    print(f"Re-ranking: {'Enabled' if stats['reranking_enabled'] else 'Disabled'}")
    print(f"Temperature: {stats['temperature']}")
    print(f"Max Tokens: {stats['max_tokens']}")
    print(f"\nEmbedding Model: {stats['embedding_model']}")
    print(f"Embedding Dimension: {stats['embedding_dimension']}")
    print(f"\nTotal Documents: {stats['vector_store']['total_chunks']} chunks")
    print(f"Unique Sources: {stats['vector_store']['unique_sources']}")
    print()


def print_result(result: dict, show_metadata: bool = False):
    """Print query result."""
    print()
    print(f"{Colors.BOLD}Answer:{Colors.ENDC}")
    print("-" * 70)
    print(result["answer"])

    # Print sources
    if result["sources"]:
        print()
        print(f"{Colors.BOLD}Sources:{Colors.ENDC}")
        print("-" * 70)
        for i, source in enumerate(result["sources"], 1):
            confidence_color = (
                Colors.OKGREEN if source["score"] > 0.7 else Colors.WARNING
            )
            print(f"{i}. {source['title']}")
            print(f"   File: {source['filename']}")
            print(f"   {confidence_color}Relevance: {source['score']:.4f}{Colors.ENDC}")

    # Print metrics
    print()
    print(f"{Colors.BOLD}Metrics:{Colors.ENDC}")
    print("-" * 70)

    # Confidence indicator
    confidence = result["confidence"]
    if confidence > 0.8:
        conf_color = Colors.OKGREEN
        conf_label = "High"
    elif confidence > 0.6:
        conf_color = Colors.WARNING
        conf_label = "Medium"
    else:
        conf_color = Colors.FAIL
        conf_label = "Low"

    print(f"Confidence: {conf_color}{conf_label} ({confidence:.4f}){Colors.ENDC}")
    print(f"Retrieval Time: {result['retrieval_time']:.3f}s")
    print(f"Generation Time: {result['generation_time']:.3f}s")
    print(f"Total Time: {result['total_time']:.3f}s")

    if not result["is_valid"] and not result["is_refusal"]:
        print(
            f"{Colors.WARNING}⚠ Warning: Answer may not meet quality standards{Colors.ENDC}"
        )

    # Show detailed metadata if requested
    if show_metadata and "metadata" in result:
        print()
        print(f"{Colors.BOLD}Retrieved Chunks:{Colors.ENDC}")
        print("-" * 70)
        for i, chunk in enumerate(result["metadata"]["retrieved_chunks"], 1):
            print(f"\n{i}. {chunk['chunk_id']} (score: {chunk['score']:.4f})")
            print(f"   Source: {chunk['source']}")
            if chunk["heading"]:
                print(f"   Section: {chunk['heading']}")
            print(f"   Preview: {chunk['preview']}")

    print()


def stream_result(rag: PolicyRAGSystem, question: str, top_k: int):
    """Print streaming result."""
    print()
    print(f"{Colors.BOLD}Answer:{Colors.ENDC}")
    print("-" * 70)

    try:
        for chunk in rag.stream_query(question, top_k):
            print(chunk, end="", flush=True)
        print()  # New line at end
    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")


def interactive_mode(rag: PolicyRAGSystem, top_k: int, show_metadata: bool):
    """Run interactive query mode."""
    print_header()

    while True:
        try:
            # Get user input
            question = input(f"{Colors.OKBLUE}Question:{Colors.ENDC} ").strip()

            if not question:
                continue

            # Handle commands
            question_lower = question.lower()

            if question_lower in ["exit", "quit", "q"]:
                print(f"\n{Colors.OKGREEN}Goodbye!{Colors.ENDC}\n")
                break

            elif question_lower == "help":
                print_help()
                continue

            elif question_lower == "stats":
                print_stats(rag)
                continue

            elif question_lower == "clear":
                os.system("cls" if os.name == "nt" else "clear")
                print_header()
                continue

            # Process query
            result = rag.query(question, top_k=top_k, return_metadata=show_metadata)
            print_result(result, show_metadata)

        except KeyboardInterrupt:
            print(
                f"\n\n{Colors.WARNING}Interrupted. Type 'exit' to quit.{Colors.ENDC}\n"
            )
        except Exception as e:
            print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}\n")


def single_query_mode(
    rag: PolicyRAGSystem, question: str, top_k: int, stream: bool, show_metadata: bool
):
    """Process a single query."""
    if stream:
        stream_result(rag, question, top_k)
    else:
        result = rag.query(question, top_k=top_k, return_metadata=show_metadata)
        print_result(result, show_metadata)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Query the Policy RAG system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python app/query.py
  python app/query.py "What is the remote work policy?"
  python app/query.py --stream "How much PTO do I get?"
  python app/query.py --top-k 10 --verbose "Security requirements?"
        """,
    )

    parser.add_argument(
        "question", nargs="?", help="Question to ask (omit for interactive mode)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=TOP_K_DOCUMENTS,
        help=f"Number of chunks to retrieve (default: {TOP_K_DOCUMENTS})",
    )
    parser.add_argument("--stream", action="store_true", help="Stream the response")
    parser.add_argument("--verbose", action="store_true", help="Show detailed metadata")
    parser.add_argument("--no-rerank", action="store_true", help="Disable re-ranking")
    parser.add_argument(
        "--model",
        default=None,
        help="Override the model (e.g., llama-3.1-70b-versatile)",
    )

    args = parser.parse_args()

    # Initialize RAG system
    try:
        print(f"{Colors.OKCYAN}Initializing RAG system...{Colors.ENDC}")

        rag = PolicyRAGSystem(
            top_k=args.top_k,
            enable_reranking=not args.no_rerank,
            model_name=args.model if args.model else None,
        )

        print(f"{Colors.OKGREEN}✓ System ready!{Colors.ENDC}")

        # Run in appropriate mode
        if args.question:
            # Single query mode
            single_query_mode(rag, args.question, args.top_k, args.stream, args.verbose)
        else:
            # Interactive mode
            interactive_mode(rag, args.top_k, args.verbose)

    except FileNotFoundError as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        print(f"\n{Colors.WARNING}Please build the vector database first:{Colors.ENDC}")
        print("  python scripts/build_vector_db.py")
        print()
        sys.exit(1)

    except Exception as e:
        print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
