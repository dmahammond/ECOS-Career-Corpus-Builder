"""Corpus builder."""

from pathlib import Path

from career_corpus.hashing import sha256_file
from career_corpus.loader import list_documents
from career_corpus.metadata import get_document_metadata
from career_corpus.models import DocumentRecord, Paragraph
from career_corpus.reader import read_document


def build_corpus(folder: str) -> list[DocumentRecord]:
    """Build an in-memory corpus from all Word documents."""

    folder_path = Path(folder)

    corpus: list[DocumentRecord] = []

    for file in list_documents(str(folder_path)):

        metadata = get_document_metadata(file)

        paragraphs = [
            Paragraph(number=index + 1, text=text)
            for index, text in enumerate(read_document(file))
        ]

        corpus.append(
            DocumentRecord(
                name=file.name,
                path=file,
                sha256=sha256_file(file),
                metadata=metadata,
                paragraphs=paragraphs,
            )
        )

    return corpus