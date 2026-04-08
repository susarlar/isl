"""
Document Chunking Module
========================

Chunks documents using multiple strategies:
1. Semantic chunking by headings (for markdown documents)
2. Token-based chunking with overlap (for all documents)
3. Hybrid approach combining both methods

Uses fixed random seeds for reproducible chunking.
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import logging

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.document_loader import Document
from config import CHUNK_SIZE, CHUNK_OVERLAP, RANDOM_SEED, set_seeds

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a document chunk with metadata."""

    content: str
    source: str
    chunk_id: str
    chunk_index: int
    chunk_type: str  # 'heading', 'token', 'hybrid'
    metadata: Dict[str, any]

    def __len__(self):
        return len(self.content)


class DocumentChunker:
    """Chunks documents using various strategies."""

    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        seed: int = RANDOM_SEED,
    ):
        """
        Initialize the document chunker.

        Args:
            chunk_size: Target chunk size in characters
            chunk_overlap: Overlap between chunks in characters
            seed: Random seed for reproducibility
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.seed = seed

        # Set seeds for reproducibility
        set_seeds(seed)

        logger.info(
            f"Initialized chunker: size={chunk_size}, overlap={chunk_overlap}, seed={seed}"
        )

    def chunk_documents(
        self, documents: List[Document], strategy: str = "hybrid"
    ) -> List[Chunk]:
        """
        Chunk a list of documents.

        Args:
            documents: List of Document objects
            strategy: Chunking strategy ('heading', 'token', 'hybrid')

        Returns:
            List of Chunk objects
        """
        all_chunks = []

        for doc in documents:
            doc_chunks = self.chunk_document(doc, strategy)
            all_chunks.extend(doc_chunks)
            logger.info(
                f"  {Path(doc.source).name}: {len(doc_chunks)} chunks "
                f"(avg {len(doc) // len(doc_chunks) if doc_chunks else 0} chars/chunk)"
            )

        logger.info(f"\nTotal chunks created: {len(all_chunks)}")
        return all_chunks

    def chunk_document(
        self, document: Document, strategy: str = "hybrid"
    ) -> List[Chunk]:
        """
        Chunk a single document.

        Args:
            document: Document to chunk
            strategy: Chunking strategy

        Returns:
            List of Chunk objects
        """
        if strategy == "heading":
            return self._chunk_by_headings(document)
        elif strategy == "token":
            return self._chunk_by_tokens(document)
        elif strategy == "hybrid":
            return self._chunk_hybrid(document)
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")

    def _chunk_by_headings(self, document: Document) -> List[Chunk]:
        """
        Chunk document by markdown headings.

        Splits on ## and ### level headings, keeping heading with content.
        Falls back to token-based chunking if no headings found.

        Post-processes the output to merge any "heading-only" chunks (where
        the content is just a heading line with no body text) into the next
        chunk. This prevents useless stub chunks like "## Diligent Fellows"
        from polluting the vector store.
        """
        content = document.content

        # Find all markdown headings (## and ###)
        heading_pattern = r"^(#{2,3})\s+(.+)$"
        matches = list(re.finditer(heading_pattern, content, re.MULTILINE))

        if not matches:
            logger.debug(
                f"No headings found in {Path(document.source).name}, using token chunking"
            )
            return self._chunk_by_tokens(document)

        # First pass: extract raw sections (heading + body up to next heading)
        raw_sections = []
        for i, match in enumerate(matches):
            start_pos = match.start()
            if i < len(matches) - 1:
                end_pos = matches[i + 1].start()
            else:
                end_pos = len(content)
            section_content = content[start_pos:end_pos].strip()
            raw_sections.append(section_content)

        # Second pass: merge "heading-only" sections (body < min_body_chars)
        # forward into the next section. This handles the common pattern:
        #   ## Parent Heading
        #   ### Child Heading 1
        #   | table content |
        #   ### Child Heading 2
        #   | more table content |
        # where the Parent Heading would otherwise become a useless stub chunk.
        min_body_chars = 40  # anything shorter than this is "heading only"
        merged_sections = []
        carry = ""
        for section in raw_sections:
            # Calculate the "body" by removing the heading line
            lines = section.split("\n", 1)
            body = lines[1].strip() if len(lines) > 1 else ""

            if len(body) < min_body_chars:
                # Heading-only: accumulate and prepend to next section
                carry = (carry + "\n\n" + section).strip() if carry else section
            else:
                # Real content: prepend any accumulated heading context
                merged = (carry + "\n\n" + section).strip() if carry else section
                merged_sections.append(merged)
                carry = ""

        # If there's leftover carry (document ends with only headings), emit it
        # as its own chunk rather than losing it entirely.
        if carry and not merged_sections:
            merged_sections.append(carry)
        elif carry:
            # Append leftover to the final section rather than creating a stub
            merged_sections[-1] = merged_sections[-1] + "\n\n" + carry

        # Third pass: create Chunk objects, splitting oversized sections
        chunks = []
        for i, section_content in enumerate(merged_sections):
            if len(section_content) > self.chunk_size * 1.5:
                sub_chunks = self._split_large_section(section_content, document, i)
                chunks.extend(sub_chunks)
            else:
                chunk = self._create_chunk(
                    content=section_content,
                    document=document,
                    chunk_index=i,
                    chunk_type="heading",
                )
                chunks.append(chunk)

        return chunks

    def _chunk_by_tokens(self, document: Document) -> List[Chunk]:
        """
        Chunk document using token-based approach with overlap.

        Uses character-based approximation (1 token ≈ 4 characters).
        """
        content = document.content
        chunks = []

        start = 0
        chunk_index = 0

        while start < len(content):
            # Calculate end position
            end = start + self.chunk_size

            # If not at the end, try to break at a sentence or paragraph boundary
            if end < len(content):
                # Look for paragraph break first
                para_break = content.rfind("\n\n", start, end)
                if para_break > start + self.chunk_size // 2:
                    end = para_break + 2
                else:
                    # Look for sentence break
                    sentence_break = max(
                        content.rfind(". ", start, end),
                        content.rfind("! ", start, end),
                        content.rfind("? ", start, end),
                    )
                    if sentence_break > start + self.chunk_size // 2:
                        end = sentence_break + 2

            # Extract chunk
            chunk_content = content[start:end].strip()

            if chunk_content:
                chunk = self._create_chunk(
                    content=chunk_content,
                    document=document,
                    chunk_index=chunk_index,
                    chunk_type="token",
                )
                chunks.append(chunk)
                chunk_index += 1

            # Move start position with overlap
            start = end - self.chunk_overlap

            # Ensure we make progress
            if start <= chunks[-1].metadata["start_char"] if chunks else 0:
                start = end

        return chunks

    def _chunk_hybrid(self, document: Document) -> List[Chunk]:
        """
        Hybrid chunking: use headings where available, token-based otherwise.

        This is the recommended default strategy.
        """
        content = document.content

        # Check if document has meaningful structure
        heading_pattern = r"^#{2,3}\s+.+$"
        headings = re.findall(heading_pattern, content, re.MULTILINE)

        # If document has good structure (multiple headings), use heading-based
        if len(headings) >= 3:
            return self._chunk_by_headings(document)
        else:
            return self._chunk_by_tokens(document)

    def _split_large_section(
        self, section_content: str, document: Document, base_index: int
    ) -> List[Chunk]:
        """Split a large section into smaller chunks."""
        chunks = []
        start = 0
        sub_index = 0

        while start < len(section_content):
            end = start + self.chunk_size

            # Try to break at paragraph or sentence
            if end < len(section_content):
                para_break = section_content.rfind("\n\n", start, end)
                if para_break > start + self.chunk_size // 2:
                    end = para_break + 2
                else:
                    sentence_break = max(
                        section_content.rfind(". ", start, end),
                        section_content.rfind("! ", start, end),
                        section_content.rfind("? ", start, end),
                    )
                    if sentence_break > start + self.chunk_size // 2:
                        end = sentence_break + 2

            chunk_content = section_content[start:end].strip()

            if chunk_content:
                chunk = self._create_chunk(
                    content=chunk_content,
                    document=document,
                    chunk_index=base_index * 100 + sub_index,  # Unique indexing
                    chunk_type="heading-split",
                )
                chunks.append(chunk)
                sub_index += 1

            start = end - self.chunk_overlap

        return chunks

    def _create_chunk(
        self, content: str, document: Document, chunk_index: int, chunk_type: str
    ) -> Chunk:
        """Create a Chunk object with metadata."""
        # Generate unique chunk ID
        source_name = Path(document.source).stem
        chunk_id = f"{source_name}_chunk_{chunk_index:04d}"

        # Find chunk position in original document
        start_char = document.content.find(content[:100])  # Find by first 100 chars

        # Extract heading if present
        heading_match = re.match(r"^(#{2,3})\s+(.+)$", content, re.MULTILINE)
        heading = heading_match.group(2) if heading_match else None

        metadata = {
            **document.metadata,  # Inherit document metadata
            "chunk_id": chunk_id,
            "chunk_index": chunk_index,
            "chunk_type": chunk_type,
            "chunk_size": len(content),
            "start_char": max(0, start_char),
            "heading": heading,
            "doc_title": document.metadata.get("title", ""),
        }

        return Chunk(
            content=content,
            source=document.source,
            chunk_id=chunk_id,
            chunk_index=chunk_index,
            chunk_type=chunk_type,
            metadata=metadata,
        )


def chunk_documents(
    documents: List[Document],
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
    strategy: str = "hybrid",
    seed: int = RANDOM_SEED,
) -> List[Chunk]:
    """
    Convenience function to chunk documents.

    Args:
        documents: List of Document objects
        chunk_size: Target chunk size in characters
        chunk_overlap: Overlap between chunks in characters
        strategy: Chunking strategy ('heading', 'token', 'hybrid')
        seed: Random seed for reproducibility

    Returns:
        List of Chunk objects
    """
    chunker = DocumentChunker(chunk_size, chunk_overlap, seed)
    return chunker.chunk_documents(documents, strategy)


if __name__ == "__main__":
    # Test the document chunker
    from app.document_loader import load_documents

    print("=" * 60)
    print("Document Chunker Test")
    print("=" * 60)
    print()

    # Load documents
    print("Loading documents...")
    documents = load_documents()
    print(f"✓ Loaded {len(documents)} documents\n")

    # Test different strategies
    strategies = ["heading", "token", "hybrid"]

    for strategy in strategies:
        print(f"\nTesting strategy: {strategy.upper()}")
        print("-" * 60)

        chunks = chunk_documents(documents, strategy=strategy)

        # Statistics
        total_chars = sum(len(c) for c in chunks)
        avg_size = total_chars // len(chunks) if chunks else 0
        min_size = min(len(c) for c in chunks) if chunks else 0
        max_size = max(len(c) for c in chunks) if chunks else 0

        print(f"Total chunks: {len(chunks)}")
        print(f"Avg chunk size: {avg_size:,} characters")
        print(f"Min/Max: {min_size}/{max_size} characters")

        # Show first chunk as example
        if chunks:
            print(f"\nExample chunk ({chunks[0].chunk_id}):")
            print(f"  Type: {chunks[0].chunk_type}")
            print(f"  Size: {len(chunks[0])} characters")
            print(f"  Heading: {chunks[0].metadata.get('heading', 'N/A')}")
            print(f"  Preview: {chunks[0].content[:200]}...")

    print("\n" + "=" * 60)
    print("Chunking test complete!")
    print("=" * 60)
