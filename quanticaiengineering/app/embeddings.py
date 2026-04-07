"""
Embeddings Module
=================

Generates embeddings using sentence-transformers (all-MiniLM-L6-v2).
Lightweight local model (~22 MB) — no external API calls needed.
"""

import logging
import sys
from pathlib import Path
from typing import List, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.chunking import Chunk
from config import EMBEDDING_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_DEFAULT_MODEL = "all-MiniLM-L6-v2"
_DEFAULT_DIM = 384


class EmbeddingGenerator:
    """Generates embeddings using sentence-transformers locally."""

    def __init__(
        self,
        model_name: str = EMBEDDING_MODEL,
        seed: int = 0,
        device: Optional[str] = None,
    ):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name or _DEFAULT_MODEL
        self.model = SentenceTransformer(self.model_name, device=device or "cpu")
        self.embedding_dimension = self.model.get_sentence_embedding_dimension()
        logger.info(
            "Loaded sentence-transformers model: %s (dim=%d)",
            self.model_name,
            self.embedding_dimension,
        )

    def embed_texts(
        self, texts: List[str], batch_size: int = 32, show_progress: bool = True
    ) -> np.ndarray:
        if not texts:
            return np.array([])

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return embeddings.astype(np.float32)

    def embed_chunks(
        self, chunks: List[Chunk], batch_size: int = 32, show_progress: bool = True
    ) -> np.ndarray:
        return self.embed_texts([c.content for c in chunks], batch_size, show_progress)

    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.model.encode(
            [query], convert_to_numpy=True, normalize_embeddings=True
        )
        return embedding[0].astype(np.float32)

    def get_embedding_dimension(self) -> int:
        return self.embedding_dimension
