"""
Build Vector Database Script
=============================

Orchestrates the complete document ingestion pipeline:
1. Load documents from policies/ directory
2. Chunk documents using hybrid strategy
3. Generate embeddings using sentence-transformers
4. Store in FAISS vector database
5. Save index to disk

Run this script to build the vector database before querying.
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.document_loader import load_documents
from app.chunking import chunk_documents
from app.embeddings import EmbeddingGenerator
from app.vector_store import FAISSVectorStore
from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_MODEL,
    EMBEDDING_SEED,
    VECTOR_STORE_PATH,
    set_seeds,
)

import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def build_vector_database(
    documents_path: str = "knowledge",
    output_path: str = str(VECTOR_STORE_PATH),
    chunk_strategy: str = "hybrid",
    store_type: str = "faiss",
    save_stats: bool = True,
):
    """
    Build the complete vector database.

    Args:
        documents_path: Path to documents directory
        output_path: Path to save vector database
        chunk_strategy: Chunking strategy ('heading', 'token', 'hybrid')
        store_type: Vector store type ('faiss' or 'chroma')
        save_stats: Whether to save build statistics
    """
    print()
    print("=" * 70)
    print(" BUILDING VECTOR DATABASE FOR ISEKAI FELLOW POWER ADVISOR")
    print("=" * 70)
    print()

    start_time = time.time()
    stats = {
        "build_timestamp": datetime.now().isoformat(),
        "config": {
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "chunk_strategy": chunk_strategy,
            "embedding_model": EMBEDDING_MODEL,
            "embedding_seed": EMBEDDING_SEED,
            "store_type": store_type,
        },
    }

    # Set seeds for reproducibility
    logger.info("Setting random seeds for reproducibility...")
    set_seeds()

    # Step 1: Load documents
    print("\n" + "─" * 70)
    print("STEP 1: Loading Documents")
    print("─" * 70)
    logger.info(f"Loading documents from: {documents_path}")

    try:
        documents = load_documents(documents_path)
        stats["documents_loaded"] = len(documents)
        stats["total_chars"] = sum(len(doc.content) for doc in documents)
        stats["total_words"] = sum(doc.metadata["word_count"] for doc in documents)

        print(f"\n✓ Loaded {len(documents)} documents")
        print(
            f"  Total: {stats['total_chars']:,} characters, {stats['total_words']:,} words"
        )

        if len(documents) == 0:
            raise ValueError("No documents found!")

    except Exception as e:
        logger.error(f"Failed to load documents: {e}")
        raise

    # Step 2: Chunk documents
    print("\n" + "─" * 70)
    print("STEP 2: Chunking Documents")
    print("─" * 70)
    logger.info(f"Chunking with strategy: {chunk_strategy}")

    try:
        chunk_start = time.time()
        chunks = chunk_documents(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            strategy=chunk_strategy,
        )
        chunk_time = time.time() - chunk_start

        stats["chunks_created"] = len(chunks)
        stats["chunking_time_seconds"] = round(chunk_time, 2)
        stats["avg_chunk_size"] = (
            sum(len(c) for c in chunks) // len(chunks) if chunks else 0
        )
        stats["chunk_size_range"] = {
            "min": min(len(c) for c in chunks) if chunks else 0,
            "max": max(len(c) for c in chunks) if chunks else 0,
        }

        print(f"\n✓ Created {len(chunks)} chunks in {chunk_time:.2f}s")
        print(f"  Average chunk size: {stats['avg_chunk_size']:,} characters")
        print(
            f"  Size range: {stats['chunk_size_range']['min']}-{stats['chunk_size_range']['max']} characters"
        )

        if len(chunks) == 0:
            raise ValueError("No chunks created!")

    except Exception as e:
        logger.error(f"Failed to chunk documents: {e}")
        raise

    # Step 3: Generate embeddings
    print("\n" + "─" * 70)
    print("STEP 3: Generating Embeddings")
    print("─" * 70)
    logger.info(f"Using model: {EMBEDDING_MODEL}")

    try:
        embed_start = time.time()

        # Initialize embedding generator
        generator = EmbeddingGenerator(model_name=EMBEDDING_MODEL, seed=EMBEDDING_SEED)

        # Generate embeddings with progress bar
        embeddings = generator.embed_chunks(chunks, batch_size=32, show_progress=True)

        embed_time = time.time() - embed_start

        stats["embeddings_generated"] = len(embeddings)
        stats["embedding_dimension"] = generator.embedding_dimension
        stats["embedding_time_seconds"] = round(embed_time, 2)
        stats["embeddings_per_second"] = round(len(embeddings) / embed_time, 2)

        print(f"\n✓ Generated {len(embeddings)} embeddings in {embed_time:.2f}s")
        print(f"  Dimension: {generator.embedding_dimension}")
        print(f"  Speed: {stats['embeddings_per_second']:.2f} embeddings/second")

    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        raise

    # Step 4: Build vector store
    print("\n" + "─" * 70)
    print("STEP 4: Building Vector Store")
    print("─" * 70)
    logger.info(f"Creating {store_type.upper()} index...")

    try:
        store_start = time.time()

        if store_type.lower() == "faiss":
            vector_store = FAISSVectorStore(
                embedding_dimension=generator.embedding_dimension,
                index_type="Flat",
                metric="cosine",
            )
        elif store_type.lower() == "chroma":
            from app.vector_store import ChromaVectorStore

            vector_store = ChromaVectorStore(
                collection_name="policy_docs", persist_directory=output_path
            )
        else:
            raise ValueError(f"Unknown store type: {store_type}")

        # Add embeddings to store
        vector_store.add_embeddings(embeddings, chunks)

        store_time = time.time() - store_start
        stats["indexing_time_seconds"] = round(store_time, 2)

        print(f"\n✓ Built {store_type.upper()} index in {store_time:.2f}s")

    except Exception as e:
        logger.error(f"Failed to build vector store: {e}")
        raise

    # Step 5: Save to disk
    print("\n" + "─" * 70)
    print("STEP 5: Saving to Disk")
    print("─" * 70)
    logger.info(f"Saving to: {output_path}")

    try:
        save_start = time.time()

        if store_type.lower() == "faiss":
            vector_store.save(output_path)
        else:
            vector_store.save()

        save_time = time.time() - save_start
        stats["save_time_seconds"] = round(save_time, 2)

        # Get final stats
        store_stats = vector_store.get_stats()
        stats["vector_store"] = store_stats

        print(f"\n✓ Saved vector database in {save_time:.2f}s")
        print(f"  Location: {output_path}")

    except Exception as e:
        logger.error(f"Failed to save vector store: {e}")
        raise

    # Calculate total time
    total_time = time.time() - start_time
    stats["total_time_seconds"] = round(total_time, 2)

    # Print summary
    print("\n" + "=" * 70)
    print(" BUILD SUMMARY")
    print("=" * 70)
    print(f"\n  Documents Processed:  {stats['documents_loaded']}")
    print(f"  Chunks Created:       {stats['chunks_created']}")
    print(f"  Embeddings Generated: {stats['embeddings_generated']}")
    print(f"  Embedding Dimension:  {stats['embedding_dimension']}")
    print(f"\n  Chunking Time:    {stats['chunking_time_seconds']}s")
    print(f"  Embedding Time:   {stats['embedding_time_seconds']}s")
    print(f"  Indexing Time:    {stats['indexing_time_seconds']}s")
    print(f"  Save Time:        {stats['save_time_seconds']}s")
    print(f"  ───────────────────────────")
    print(f"  Total Time:       {stats['total_time_seconds']}s")
    print()

    # Save statistics
    if save_stats:
        stats_file = Path(output_path) / "build_stats.json"
        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)
        print(f"✓ Saved build statistics to: {stats_file}")

    print("\n" + "=" * 70)
    print(" ✓ VECTOR DATABASE BUILD COMPLETE!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Test the database: python app/vector_store.py")
    print("  2. Start querying: python app/query.py")
    print("  3. Run evaluation: python scripts/evaluate.py")
    print()

    return vector_store, stats


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build vector database for Isekai Fellow Power Advisor"
    )
    parser.add_argument(
        "--documents",
        default="knowledge",
        help="Path to documents directory (default: knowledge)",
    )
    parser.add_argument(
        "--output",
        default=str(VECTOR_STORE_PATH),
        help=f"Path to save vector database (default: {VECTOR_STORE_PATH})",
    )
    parser.add_argument(
        "--strategy",
        choices=["heading", "token", "hybrid"],
        default="hybrid",
        help="Chunking strategy (default: hybrid)",
    )
    parser.add_argument(
        "--store",
        choices=["faiss", "chroma"],
        default="faiss",
        help="Vector store type (default: faiss)",
    )
    parser.add_argument(
        "--no-stats", action="store_true", help="Don't save build statistics"
    )

    args = parser.parse_args()

    try:
        vector_store, stats = build_vector_database(
            documents_path=args.documents,
            output_path=args.output,
            chunk_strategy=args.strategy,
            store_type=args.store,
            save_stats=not args.no_stats,
        )
    except Exception as e:
        logger.error(f"Build failed: {e}")
        sys.exit(1)
