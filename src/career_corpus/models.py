"""Core data models."""

from dataclasses import dataclass
from pathlib import Path

from career_corpus.metadata import DocumentMetadata


@dataclass(slots=True)
class Paragraph:
    """A single paragraph extracted from a document."""

    number: int
    text: str


@dataclass(slots=True)
class DocumentRecord:
    """A document loaded into the corpus."""

    name: str
    path: Path
    sha256: str
    metadata: DocumentMetadata
    paragraphs: list[Paragraph]

    @property
    def paragraph_count(self) -> int:
        return len(self.paragraphs)