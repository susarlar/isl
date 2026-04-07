"""
Document Loader Module
======================

Handles loading and parsing of documents from various formats:
- Markdown (.md)
- Plain text (.txt)
- HTML (.html, .htm)
- PDF (.pdf)

Includes cleaning and preprocessing functionality.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Represents a loaded document with metadata."""

    content: str
    source: str
    doc_type: str
    metadata: Dict[str, any]

    def __len__(self):
        return len(self.content)


class DocumentLoader:
    """Loads and preprocesses documents from various file formats."""

    SUPPORTED_EXTENSIONS = {".md", ".txt", ".html", ".htm", ".pdf"}

    def __init__(self, base_path: str = "knowledge"):
        """
        Initialize the document loader.

        Args:
            base_path: Base directory containing policy documents
        """
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            raise ValueError(f"Base path does not exist: {base_path}")

    def load_all_documents(self) -> List[Document]:
        """
        Load all supported documents from the base path.

        Returns:
            List of Document objects
        """
        documents = []

        for file_path in self.base_path.rglob("*"):
            if (
                file_path.is_file()
                and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS
            ):
                # Skip README files
                if file_path.name.upper() in ["README.MD", "README.TXT"]:
                    logger.info(f"Skipping README: {file_path.name}")
                    continue

                try:
                    doc = self.load_document(str(file_path))
                    if doc and len(doc.content.strip()) > 0:
                        documents.append(doc)
                        logger.info(
                            f"✓ Loaded: {file_path.name} ({len(doc.content):,} chars)"
                        )
                except Exception as e:
                    logger.error(f"✗ Failed to load {file_path.name}: {e}")

        logger.info(
            f"\nLoaded {len(documents)} documents totaling {sum(len(d) for d in documents):,} characters"
        )
        return documents

    def load_document(self, file_path: str) -> Optional[Document]:
        """
        Load a single document.

        Args:
            file_path: Path to the document file

        Returns:
            Document object or None if loading failed
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        if extension not in self.SUPPORTED_EXTENSIONS:
            logger.warning(f"Unsupported file type: {extension}")
            return None

        # Load content based on file type
        if extension in [".md", ".txt"]:
            content = self._load_text_file(file_path)
        elif extension in [".html", ".htm"]:
            content = self._load_html_file(file_path)
        elif extension == ".pdf":
            content = self._load_pdf_file(file_path)
        else:
            return None

        if not content:
            return None

        # Clean content
        content = self._clean_content(content)

        # Extract metadata
        metadata = self._extract_metadata(content, file_path)

        return Document(
            content=content,
            source=str(file_path),
            doc_type=extension[1:],  # Remove the dot
            metadata=metadata,
        )

    def _load_text_file(self, file_path: Path) -> str:
        """Load markdown or text file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encoding
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()

    def _load_html_file(self, file_path: Path) -> str:
        """Load and parse HTML file."""
        try:
            from bs4 import BeautifulSoup

            with open(file_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            soup = BeautifulSoup(html_content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = "\n".join(chunk for chunk in chunks if chunk)

            return text

        except ImportError:
            logger.warning(
                "BeautifulSoup not installed. Install with: pip install beautifulsoup4"
            )
            # Fallback to basic text extraction
            with open(file_path, "r", encoding="utf-8") as f:
                html = f.read()
            # Very basic HTML tag removal
            text = re.sub(r"<[^>]+>", " ", html)
            text = re.sub(r"\s+", " ", text)
            return text.strip()

    def _load_pdf_file(self, file_path: Path) -> str:
        """Load and parse PDF file."""
        try:
            import PyPDF2

            text_content = []
            with open(file_path, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append(text)

            return "\n\n".join(text_content)

        except ImportError:
            logger.warning("PyPDF2 not installed. Install with: pip install PyPDF2")
            return ""
        except Exception as e:
            logger.error(f"Error reading PDF: {e}")
            return ""

    def _clean_content(self, content: str) -> str:
        """
        Clean and normalize document content.

        Args:
            content: Raw document content

        Returns:
            Cleaned content
        """
        # Remove excessive whitespace
        content = re.sub(r"\n{3,}", "\n\n", content)
        content = re.sub(r" {2,}", " ", content)

        # Remove page numbers and common artifacts
        content = re.sub(r"\n\s*\d+\s*\n", "\n", content)

        # Remove markdown links but keep the text
        content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)

        # Normalize quotes
        content = content.replace('"', '"').replace('"', '"')
        content = content.replace(""", "'").replace(""", "'")

        # Remove excessive punctuation
        content = re.sub(r"\.{3,}", "...", content)

        return content.strip()

    def _extract_metadata(self, content: str, file_path: Path) -> Dict[str, any]:
        """
        Extract metadata from document content and filename.

        Args:
            content: Document content
            file_path: Path to the document

        Returns:
            Dictionary of metadata
        """
        metadata = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "file_size": file_path.stat().st_size,
            "word_count": len(content.split()),
            "char_count": len(content),
        }

        # Extract title from markdown
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            metadata["title"] = title_match.group(1).strip()
        else:
            # Use filename as title
            metadata["title"] = file_path.stem.replace("_", " ").title()

        # Extract version if present
        version_match = re.search(r"Version[:\s]+(\d+\.[\d.]+)", content, re.IGNORECASE)
        if version_match:
            metadata["version"] = version_match.group(1)

        # Extract effective date if present
        date_match = re.search(
            r"Effective Date[:\s]+([A-Za-z]+\s+\d{1,2},\s+\d{4})",
            content,
            re.IGNORECASE,
        )
        if date_match:
            metadata["effective_date"] = date_match.group(1)

        # Count sections (markdown headers)
        headers = re.findall(r"^#+\s+.+$", content, re.MULTILINE)
        metadata["section_count"] = len(headers)

        return metadata


def load_documents(base_path: str = "knowledge") -> List[Document]:
    """
    Convenience function to load all documents.

    Args:
        base_path: Base directory containing documents

    Returns:
        List of Document objects
    """
    loader = DocumentLoader(base_path)
    return loader.load_all_documents()


if __name__ == "__main__":
    # Test the document loader
    print("=" * 60)
    print("Document Loader Test")
    print("=" * 60)
    print()

    documents = load_documents()

    print()
    print("Document Summary:")
    print("-" * 60)

    for i, doc in enumerate(documents, 1):
        print(f"\n{i}. {doc.metadata.get('title', 'Untitled')}")
        print(f"   Source: {Path(doc.source).name}")
        print(f"   Type: {doc.doc_type}")
        print(f"   Size: {doc.metadata['char_count']:,} characters")
        print(f"   Words: {doc.metadata['word_count']:,}")
        print(f"   Sections: {doc.metadata['section_count']}")
        if "version" in doc.metadata:
            print(f"   Version: {doc.metadata['version']}")
        if "effective_date" in doc.metadata:
            print(f"   Effective: {doc.metadata['effective_date']}")

    print()
    print("=" * 60)
    print(
        f"Total: {len(documents)} documents, {sum(d.metadata['word_count'] for d in documents):,} words"
    )
    print("=" * 60)
