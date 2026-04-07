"""
Configuration module for Policy Corpus RAG application.

This module centralizes all configuration settings and ensures
reproducibility through fixed random seeds.
"""

import os
import random
from pathlib import Path
from typing import Optional

import numpy as np

# Try to import torch, but make it optional
try:
    import torch

    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    torch = None

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Paths
# =============
PROJECT_ROOT = Path(__file__).parent
POLICIES_DIR = PROJECT_ROOT / "knowledge"
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
VECTOR_STORE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Reproducibility Seeds
# =====================
# Fixed seeds for deterministic behavior
RANDOM_SEED = int(os.getenv("RANDOM_SEED", "42"))
EMBEDDING_SEED = int(os.getenv("EMBEDDING_SEED", "42"))
EVAL_SEED = int(os.getenv("EVAL_SEED", "42"))
NUMPY_SEED = int(os.getenv("NUMPY_SEED", "42"))
TORCH_SEED = int(os.getenv("TORCH_SEED", "42"))


def set_seeds(seed: Optional[int] = None) -> None:
    """
    Set all random seeds for reproducibility.

    Args:
        seed: Random seed to use. If None, uses RANDOM_SEED from config.
    """
    if seed is None:
        seed = RANDOM_SEED

    # Python random
    random.seed(seed)

    # NumPy
    np.random.seed(seed)

    # PyTorch (optional)
    if TORCH_AVAILABLE and torch is not None:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)

        # Make PyTorch operations deterministic
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    # Set environment variable for hash seed (Python 3.3+)
    os.environ["PYTHONHASHSEED"] = str(seed)


# Initialize seeds on import
set_seeds()

# Groq Configuration
# ==================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY and os.getenv("APP_ENV") != "test":
    raise ValueError(
        "GROQ_API_KEY not found in environment variables. "
        "Please set it in your .env file or environment."
    )

GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.1"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
TOP_P = float(os.getenv("TOP_P", "0.9"))

# Groq model options with characteristics
GROQ_MODELS = {
    "llama-3.3-70b-versatile": {
        "context_window": 128000,
        "description": "Best balance of speed and quality (recommended)",
        "recommended_for": "general_use",
    },
    "llama-3.1-70b-versatile": {
        "context_window": 32768,
        "description": "Legacy — may be deprecated",
        "recommended_for": "general_use",
    },
    "llama-3.1-8b-instant": {
        "context_window": 131072,
        "description": "Fastest, good quality",
        "recommended_for": "high_throughput",
    },
    "llama3-70b-8192": {
        "context_window": 8192,
        "description": "Llama 3 70B",
        "recommended_for": "general_use",
    },
    "gemma2-9b-it": {
        "context_window": 8192,
        "description": "Gemma 2 9B instruction-tuned",
        "recommended_for": "fast_responses",
    },
    "mixtral-8x7b-32768": {
        "context_window": 32768,
        "description": "Large context window",
        "recommended_for": "long_documents",
    },
}

# Embedding Configuration
# =======================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "384"))

# Supported embedding models (local via sentence-transformers)
EMBEDDING_MODELS = {
    "all-MiniLM-L6-v2": {
        "dimension": 384,
        "speed": "fast",
        "quality": "good",
        "provider": "sentence-transformers",
    },
}

# Document Processing Configuration
# ==================================
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "300"))
MAX_CHUNKS_PER_DOC = int(os.getenv("MAX_CHUNKS_PER_DOC", "100"))

# Supported document types
SUPPORTED_EXTENSIONS = [".md", ".txt", ".pdf", ".html"]

# Retrieval Configuration
# =======================
TOP_K_DOCUMENTS = int(os.getenv("TOP_K_DOCUMENTS", "10"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
RERANK_ENABLED = os.getenv("RERANK_ENABLED", "false").lower() == "true"

# Vector Store Configuration
# ===========================
VECTOR_STORE_PATH = Path(os.getenv("VECTOR_STORE_PATH", str(VECTOR_STORE_DIR)))
INDEX_TYPE = os.getenv("INDEX_TYPE", "FLAT")

# FAISS index types
FAISS_INDEX_TYPES = {
    "FLAT": "Exact search, slower but most accurate",
    "IVF": "Inverted file index, faster for large datasets",
    "HNSW": "Hierarchical navigable small world, good balance",
}

# Cache Configuration
# ===================
ENABLE_CACHE = os.getenv("ENABLE_CACHE", "true").lower() == "true"
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "3600"))
CACHE_MAX_SIZE = int(os.getenv("CACHE_MAX_SIZE", "1000"))

# Application Settings
# ====================
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# API Settings
# ============
API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))

# Evaluation Settings
# ===================
TEST_DATASET_PATH = Path(
    os.getenv("TEST_DATASET_PATH", str(DATA_DIR / "test_queries.json"))
)
EVALUATION_OUTPUT_PATH = Path(
    os.getenv("EVALUATION_OUTPUT_PATH", str(DATA_DIR / "evaluation_results.json"))
)
EVALUATION_SAMPLE_SIZE = int(os.getenv("EVALUATION_SAMPLE_SIZE", "200"))

# Monitoring and Logging
# ======================
ENABLE_METRICS = os.getenv("ENABLE_METRICS", "true").lower() == "true"
METRICS_PORT = int(os.getenv("METRICS_PORT", "9090"))
LOG_FILE = Path(os.getenv("LOG_FILE", str(LOGS_DIR / "app.log")))
LOG_ROTATION = os.getenv("LOG_ROTATION", "daily")

# Performance Settings
# ====================
MAX_CONCURRENT_REQUESTS = int(os.getenv("MAX_CONCURRENT_REQUESTS", "50"))
REQUEST_TIMEOUT_SECONDS = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "32"))

# Development Settings
# ====================
HOT_RELOAD = os.getenv("HOT_RELOAD", "true").lower() == "true"
ENABLE_PROFILING = os.getenv("ENABLE_PROFILING", "false").lower() == "true"

# Evaluation Metrics Thresholds
# ==============================
# From EVALUATION_METRICS.md

# Information Quality Thresholds
GROUNDEDNESS_TARGET = 0.95
GROUNDEDNESS_THRESHOLD = 0.90
CITATION_ACCURACY_TARGET = 0.98
CITATION_ACCURACY_THRESHOLD = 0.95
ANSWER_RELEVANCE_TARGET = 4.2
ANSWER_RELEVANCE_THRESHOLD = 3.5

# System Performance Thresholds
LATENCY_P95_TARGET_MS = 3000
LATENCY_P95_THRESHOLD_MS = 5000
ERROR_RATE_TARGET = 0.005
ERROR_RATE_THRESHOLD = 0.02
UPTIME_TARGET = 0.999

# User Experience Thresholds
USER_SATISFACTION_TARGET = 0.85
USER_SATISFACTION_THRESHOLD = 0.75

# Prompt Templates
# ================

SYSTEM_PROMPT = """You are the Isekai Slow Life Fellow Power Advisor for advanced players (level 45+).
Your role is to help players optimize Fellow Power, resource allocation, and game strategy.

Guidelines:
- Base your answers ONLY on the provided game knowledge documents
- Include specific numbers, formulas, and breakpoints
- Assume the player is advanced — skip basic explanations
- Emphasize multiplier stacking and single-carry meta
- Format citations as [Source: document_name.md]
"""

QUERY_PROMPT_TEMPLATE = """Based on the following game knowledge, answer the player's question.

Game Knowledge:
{context}

Player Question: {question}

Instructions:
1. Answer with specific numbers and calculations
2. Include citations in format [Source: document.md]
3. If the answer is not in the documents, state that clearly
4. Focus on advanced optimization, not basics

Answer:"""

# Validation
# ==========


def validate_config() -> None:
    """Validate configuration settings."""
    errors = []

    # Check required paths exist
    if not POLICIES_DIR.exists():
        errors.append(f"Policies directory not found: {POLICIES_DIR}")

    # Check Groq API key
    if not GROQ_API_KEY and APP_ENV != "test":
        errors.append("GROQ_API_KEY not set")

    # Check model availability (warn only — Groq adds new models regularly)
    if GROQ_MODEL not in GROQ_MODELS:
        print(f"Warning: GROQ_MODEL '{GROQ_MODEL}' not in known models list — proceeding anyway.")

    # Check embedding model
    if EMBEDDING_MODEL not in EMBEDDING_MODELS:
        print(f"Warning: Unknown embedding model: {EMBEDDING_MODEL}")

    # Check chunk settings
    if CHUNK_OVERLAP >= CHUNK_SIZE:
        errors.append("CHUNK_OVERLAP must be less than CHUNK_SIZE")

    if errors:
        raise ValueError(
            f"Configuration errors:\n" + "\n".join(f"- {e}" for e in errors)
        )


# Run validation on import (except in test environment)
if APP_ENV != "test":
    validate_config()


# Configuration Info Display
# ==========================


def display_config() -> None:
    """Display current configuration (for debugging)."""
    print("=" * 60)
    print("Policy Corpus RAG - Configuration")
    print("=" * 60)
    print(f"Environment: {APP_ENV}")
    print(f"Debug Mode: {DEBUG}")
    print(f"\nGroq Configuration:")
    print(f"  Model: {GROQ_MODEL}")
    print(f"  Temperature: {TEMPERATURE}")
    print(f"  Max Tokens: {MAX_TOKENS}")
    print(f"\nEmbedding Configuration:")
    print(f"  Model: {EMBEDDING_MODEL}")
    print(f"  Dimension: {EMBEDDING_DIMENSION}")
    print(f"\nChunking Configuration:")
    print(f"  Chunk Size: {CHUNK_SIZE}")
    print(f"  Overlap: {CHUNK_OVERLAP}")
    print(f"\nRetrieval Configuration:")
    print(f"  Top-K Documents: {TOP_K_DOCUMENTS}")
    print(f"  Similarity Threshold: {SIMILARITY_THRESHOLD}")
    print(f"\nReproducibility:")
    print(f"  Random Seed: {RANDOM_SEED}")
    print(f"  Embedding Seed: {EMBEDDING_SEED}")
    print(f"  Evaluation Seed: {EVAL_SEED}")
    print("=" * 60)


if __name__ == "__main__":
    display_config()
