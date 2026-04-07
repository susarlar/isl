"""
Tests for document chunking utilities.

Uses synthetic markdown content — no file system access needed.
"""

import sys
from pathlib import Path

# APP_ENV=test is set in conftest.py before config import
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.chunking import DocumentChunker, Chunk
from app.document_loader import Document


def _make_document(content: str, filename: str = "test.md") -> Document:
    return Document(
        content=content,
        source=filename,
        doc_type="md",
        metadata={"filename": filename, "title": "Test Document"},
    )


SAMPLE_MD = """# Employee Handbook

## Section 1: Introduction

Welcome to Quantic AI Engineering. This handbook outlines our policies and procedures.
All employees are expected to read and understand these guidelines carefully.

## Section 2: Leave Policy

Employees receive 20 days of paid time off per year. Sick leave is separate and
provides an additional 10 days per year for illness or medical appointments.

### Subsection 2.1: PTO Accrual

PTO accrues at a rate of 1.67 days per month starting from the first day of employment.
Unused PTO may be carried over up to a maximum of 10 days per year.

## Section 3: Remote Work

Employees may work remotely up to 3 days per week after completing 6 months of service.
A formal request must be submitted to the direct manager for approval.
"""


class TestDocumentChunker:
    def test_creates_chunks(self):
        chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        doc = _make_document(SAMPLE_MD)
        chunks = chunker.chunk_document(doc, strategy="hybrid")
        assert len(chunks) > 0

    def test_chunks_are_chunk_objects(self):
        chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        doc = _make_document(SAMPLE_MD)
        chunks = chunker.chunk_document(doc, strategy="hybrid")
        for chunk in chunks:
            assert isinstance(chunk, Chunk)
            assert chunk.content
            assert chunk.chunk_id
            assert "filename" in chunk.metadata

    def test_chunk_ids_are_unique(self):
        chunker = DocumentChunker(chunk_size=300, chunk_overlap=50)
        doc = _make_document(SAMPLE_MD)
        chunks = chunker.chunk_document(doc, strategy="token")
        ids = [c.chunk_id for c in chunks]
        assert len(ids) == len(set(ids)), "Chunk IDs should be unique"

    def test_metadata_filename(self):
        chunker = DocumentChunker(chunk_size=500, chunk_overlap=50)
        doc = _make_document(SAMPLE_MD, filename="employee_handbook.md")
        chunks = chunker.chunk_document(doc, strategy="hybrid")
        for chunk in chunks:
            assert chunk.metadata["filename"] == "employee_handbook.md"

    def test_heading_strategy(self):
        chunker = DocumentChunker(chunk_size=1000, chunk_overlap=100)
        doc = _make_document(SAMPLE_MD)
        chunks = chunker.chunk_document(doc, strategy="heading")
        assert len(chunks) >= 1

    def test_token_strategy(self):
        chunker = DocumentChunker(chunk_size=300, chunk_overlap=50)
        doc = _make_document(SAMPLE_MD)
        chunks = chunker.chunk_document(doc, strategy="token")
        assert len(chunks) >= 1

    def test_reproducibility_with_fixed_seed(self):
        chunker1 = DocumentChunker(chunk_size=300, chunk_overlap=50, seed=42)
        chunker2 = DocumentChunker(chunk_size=300, chunk_overlap=50, seed=42)
        doc = _make_document(SAMPLE_MD)
        chunks1 = chunker1.chunk_document(doc, strategy="token")
        chunks2 = chunker2.chunk_document(doc, strategy="token")
        assert [c.content for c in chunks1] == [c.content for c in chunks2]

    def test_invalid_strategy_raises(self):
        import pytest

        chunker = DocumentChunker()
        doc = _make_document(SAMPLE_MD)
        with pytest.raises(ValueError):
            chunker.chunk_document(doc, strategy="invalid_strategy")
