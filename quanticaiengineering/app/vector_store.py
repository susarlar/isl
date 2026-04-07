"""
Vector Store Module
===================

Manages vector storage and retrieval using FAISS and optionally ChromaDB.

Features:
- FAISS index for fast similarity search
- Optional ChromaDB integration
- Metadata filtering
- Index persistence
- Hybrid search (dense + sparse)
"""

import sys
import os
import pickle
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union
import logging
import numpy as np

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.chunking import Chunk
from config import VECTOR_STORE_PATH, TOP_K_DOCUMENTS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """Vector store using FAISS for similarity search."""

    def __init__(
        self, embedding_dimension: int, index_type: str = "Flat", metric: str = "cosine"
    ):
        """
        Initialize FAISS vector store.

        Args:
            embedding_dimension: Dimension of embeddings
            index_type: Type of FAISS index ('Flat', 'IVF', 'HNSW')
            metric: Distance metric ('cosine', 'l2', 'ip')
        """
        try:
            import faiss
        except ImportError:
            raise ImportError(
                "FAISS not installed. Install with: pip install faiss-cpu (or faiss-gpu)"
            )

        self.embedding_dimension = embedding_dimension
        self.index_type = index_type
        self.metric = metric
        self.faiss = faiss

        # Create index
        self.index = self._create_index()
        self.chunks: List[Chunk] = []
        self.embeddings: Optional[np.ndarray] = None

        logger.info(
            f"Initialized FAISS vector store: "
            f"dim={embedding_dimension}, type={index_type}, metric={metric}"
        )

    def _create_index(self):
        """Create FAISS index based on configuration."""
        if self.metric == "cosine":
            # For cosine similarity, use Inner Product with normalized vectors
            if self.index_type == "Flat":
                index = self.faiss.IndexFlatIP(self.embedding_dimension)
            elif self.index_type == "HNSW":
                index = self.faiss.IndexHNSWFlat(self.embedding_dimension, 32)
            else:
                raise ValueError(
                    f"Unsupported index type for cosine: {self.index_type}"
                )
        elif self.metric == "l2":
            if self.index_type == "Flat":
                index = self.faiss.IndexFlatL2(self.embedding_dimension)
            elif self.index_type == "HNSW":
                index = self.faiss.IndexHNSWFlat(self.embedding_dimension, 32)
            else:
                raise ValueError(f"Unsupported index type for L2: {self.index_type}")
        elif self.metric == "ip":
            # Inner product (dot product)
            if self.index_type == "Flat":
                index = self.faiss.IndexFlatIP(self.embedding_dimension)
            else:
                raise ValueError(f"Unsupported index type for IP: {self.index_type}")
        else:
            raise ValueError(f"Unsupported metric: {self.metric}")

        return index

    def add_embeddings(self, embeddings: np.ndarray, chunks: List[Chunk]):
        """
        Add embeddings and chunks to the index.

        Args:
            embeddings: NumPy array of embeddings (n_samples, embedding_dim)
            chunks: List of corresponding Chunk objects
        """
        if len(embeddings) != len(chunks):
            raise ValueError(
                f"Mismatch: {len(embeddings)} embeddings but {len(chunks)} chunks"
            )

        # Ensure embeddings are float32 (FAISS requirement)
        embeddings = embeddings.astype("float32")

        # For cosine similarity, ensure vectors are normalized
        if self.metric == "cosine":
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / (norms + 1e-10)

        # Add to index
        self.index.add(embeddings)
        self.chunks.extend(chunks)

        if self.embeddings is None:
            self.embeddings = embeddings
        else:
            self.embeddings = np.vstack([self.embeddings, embeddings])

        logger.info(
            f"✓ Added {len(chunks)} chunks to FAISS index (total: {len(self.chunks)})"
        )

    def search(
        self,
        query_embedding: np.ndarray,
        k: int = TOP_K_DOCUMENTS,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Tuple[Chunk, float]]:
        """
        Search for similar chunks.

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            filter_metadata: Optional metadata filters

        Returns:
            List of (Chunk, score) tuples
        """
        if self.index.ntotal == 0:
            logger.warning("Index is empty")
            return []

        # Ensure query is float32 and 2D
        query_embedding = query_embedding.astype("float32").reshape(1, -1)

        # Normalize for cosine similarity
        if self.metric == "cosine":
            norm = np.linalg.norm(query_embedding)
            query_embedding = query_embedding / (norm + 1e-10)

        # Search
        distances, indices = self.index.search(query_embedding, k)

        # Convert to list of (chunk, score) tuples
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):  # Valid index
                chunk = self.chunks[idx]

                # Apply metadata filters if provided
                if filter_metadata:
                    match = all(
                        chunk.metadata.get(key) == value
                        for key, value in filter_metadata.items()
                    )
                    if not match:
                        continue

                # Convert distance to similarity score
                if self.metric == "cosine":
                    score = float(distance)  # Already similarity for IP
                elif self.metric == "l2":
                    score = 1.0 / (1.0 + float(distance))  # Convert to similarity
                else:
                    score = float(distance)

                results.append((chunk, score))

        return results[:k]  # Ensure we return at most k results

    def save(self, save_path: str):
        """
        Save the index and metadata to disk.

        Args:
            save_path: Directory path to save index
        """
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)

        # Save FAISS index
        index_file = save_path / "faiss_index.bin"
        self.faiss.write_index(self.index, str(index_file))

        # Save chunks and metadata
        metadata_file = save_path / "metadata.pkl"
        with open(metadata_file, "wb") as f:
            pickle.dump(
                {
                    "chunks": self.chunks,
                    "embeddings": self.embeddings,
                    "embedding_dimension": self.embedding_dimension,
                    "index_type": self.index_type,
                    "metric": self.metric,
                },
                f,
            )

        logger.info(f"✓ Saved vector store to {save_path}")

    def load(self, load_path: str):
        """
        Load the index and metadata from disk.

        Args:
            load_path: Directory path to load index from
        """
        load_path = Path(load_path)

        # Load FAISS index
        index_file = load_path / "faiss_index.bin"
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found: {index_file}")

        self.index = self.faiss.read_index(str(index_file))

        # Load chunks and metadata
        metadata_file = load_path / "metadata.pkl"
        with open(metadata_file, "rb") as f:
            data = pickle.load(f)
            self.chunks = data["chunks"]
            self.embeddings = data["embeddings"]
            self.embedding_dimension = data["embedding_dimension"]
            self.index_type = data["index_type"]
            self.metric = data["metric"]

        logger.info(
            f"✓ Loaded vector store from {load_path} ({len(self.chunks)} chunks)"
        )

    def get_stats(self) -> Dict:
        """Get statistics about the index."""
        return {
            "total_chunks": len(self.chunks),
            "embedding_dimension": self.embedding_dimension,
            "index_type": self.index_type,
            "metric": self.metric,
            "index_size": self.index.ntotal,
            "unique_sources": len(set(c.source for c in self.chunks)),
            "chunk_types": {
                chunk_type: sum(1 for c in self.chunks if c.chunk_type == chunk_type)
                for chunk_type in set(c.chunk_type for c in self.chunks)
            },
        }


class ChromaVectorStore:
    """Vector store using ChromaDB (optional alternative to FAISS)."""

    def __init__(
        self,
        collection_name: str = "policy_docs",
        persist_directory: str = "./chroma_db",
    ):
        """
        Initialize ChromaDB vector store.

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist ChromaDB
        """
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError:
            raise ImportError(
                "ChromaDB not installed. Install with: pip install chromadb"
            )

        self.collection_name = collection_name
        self.persist_directory = persist_directory

        # Initialize ChromaDB client
        self.client = chromadb.Client(
            Settings(
                chroma_db_impl="duckdb+parquet", persist_directory=persist_directory
            )
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Quantic AI Engineering Policy Documents"},
        )

        logger.info(f"Initialized ChromaDB: {collection_name} in {persist_directory}")

    def add_embeddings(self, embeddings: np.ndarray, chunks: List[Chunk]):
        """Add embeddings and chunks to ChromaDB."""
        if len(embeddings) != len(chunks):
            raise ValueError(
                f"Mismatch: {len(embeddings)} embeddings but {len(chunks)} chunks"
            )

        # Prepare data for ChromaDB
        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.content for chunk in chunks]
        metadatas = [chunk.metadata for chunk in chunks]
        embeddings_list = embeddings.tolist()

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings_list,
            documents=documents,
            metadatas=metadatas,
        )

        logger.info(f"✓ Added {len(chunks)} chunks to ChromaDB")

    def search(
        self,
        query_embedding: np.ndarray,
        k: int = TOP_K_DOCUMENTS,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Tuple[Chunk, float]]:
        """Search ChromaDB for similar chunks."""
        query_embedding_list = query_embedding.tolist()

        # Build where clause for filtering
        where_clause = filter_metadata if filter_metadata else None

        # Query
        results = self.collection.query(
            query_embeddings=[query_embedding_list], n_results=k, where=where_clause
        )

        # Convert results to list of (Chunk, score) tuples
        chunks_with_scores = []

        if results["ids"] and len(results["ids"][0]) > 0:
            for i, chunk_id in enumerate(results["ids"][0]):
                # Reconstruct chunk from results
                chunk = Chunk(
                    content=results["documents"][0][i],
                    source=results["metadatas"][0][i]["file_path"],
                    chunk_id=chunk_id,
                    chunk_index=results["metadatas"][0][i]["chunk_index"],
                    chunk_type=results["metadatas"][0][i]["chunk_type"],
                    metadata=results["metadatas"][0][i],
                )

                # ChromaDB returns distances, convert to similarity
                distance = results["distances"][0][i]
                score = 1.0 / (1.0 + distance)

                chunks_with_scores.append((chunk, score))

        return chunks_with_scores

    def save(self):
        """Persist ChromaDB to disk."""
        self.client.persist()
        logger.info(f"✓ Persisted ChromaDB to {self.persist_directory}")

    def get_stats(self) -> Dict:
        """Get statistics about the collection."""
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "persist_directory": self.persist_directory,
        }


def create_vector_store(
    store_type: str = "faiss", embedding_dimension: int = 384, **kwargs
) -> Union[FAISSVectorStore, ChromaVectorStore]:
    """
    Factory function to create a vector store.

    Args:
        store_type: Type of vector store ('faiss' or 'chroma')
        embedding_dimension: Dimension of embeddings
        **kwargs: Additional arguments for the vector store

    Returns:
        Vector store instance
    """
    if store_type.lower() == "faiss":
        return FAISSVectorStore(embedding_dimension, **kwargs)
    elif store_type.lower() == "chroma":
        return ChromaVectorStore(**kwargs)
    else:
        raise ValueError(f"Unknown vector store type: {store_type}")


if __name__ == "__main__":
    # Test the vector store
    from app.document_loader import load_documents
    from app.chunking import chunk_documents
    from app.embeddings import EmbeddingGenerator

    print("=" * 60)
    print("Vector Store Test")
    print("=" * 60)
    print()

    # Load, chunk, and embed documents
    print("Loading documents...")
    documents = load_documents()
    print(f"✓ Loaded {len(documents)} documents")

    print("\nChunking documents...")
    chunks = chunk_documents(documents[:2], strategy="hybrid")  # Test with 2 docs
    print(f"✓ Created {len(chunks)} chunks")

    print("\nGenerating embeddings...")
    generator = EmbeddingGenerator()
    embeddings = generator.embed_chunks(chunks, show_progress=True)
    print(f"✓ Generated {len(embeddings)} embeddings")

    # Test FAISS
    print("\n" + "=" * 60)
    print("Testing FAISS Vector Store")
    print("=" * 60)

    vector_store = FAISSVectorStore(
        embedding_dimension=generator.embedding_dimension,
        index_type="Flat",
        metric="cosine",
    )

    vector_store.add_embeddings(embeddings, chunks)

    # Test search
    query = "What are the remote work requirements?"
    print(f"\nQuery: '{query}'")
    query_embedding = generator.embed_query(query)

    results = vector_store.search(query_embedding, k=5)

    print(f"\nTop {len(results)} results:")
    print("-" * 60)
    for i, (chunk, score) in enumerate(results, 1):
        print(f"\n{i}. Score: {score:.4f}")
        print(f"   Chunk: {chunk.chunk_id}")
        print(f"   Source: {Path(chunk.source).name}")
        print(f"   Heading: {chunk.metadata.get('heading', 'N/A')}")
        print(f"   Preview: {chunk.content[:150]}...")

    # Test save/load
    print("\n" + "=" * 60)
    print("Testing Save/Load")
    print("=" * 60)

    test_path = "./test_vector_db"
    vector_store.save(test_path)

    # Load into new store
    new_store = FAISSVectorStore(embedding_dimension=generator.embedding_dimension)
    new_store.load(test_path)

    # Verify search still works
    results2 = new_store.search(query_embedding, k=3)
    print(f"\n✓ Loaded store works! Found {len(results2)} results")

    # Show stats
    print("\n" + "=" * 60)
    print("Vector Store Statistics")
    print("=" * 60)
    stats = new_store.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    print()
    print("=" * 60)
    print("Vector store test complete!")
    print("=" * 60)
