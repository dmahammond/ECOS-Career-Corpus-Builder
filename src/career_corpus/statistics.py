"""Corpus statistics."""

from collections import Counter
from dataclasses import dataclass

from career_corpus.knowledge import KnowledgeArtifact
from career_corpus.models import DocumentRecord


@dataclass(slots=True)
class CorpusStatistics:
    """Summary statistics for a corpus."""

    document_count: int
    paragraph_count: int
    total_file_size: int
    average_paragraphs: float
    largest_document: str
    smallest_document: str


def calculate_statistics(
    corpus: list[DocumentRecord],
) -> CorpusStatistics:
    """Calculate summary statistics for the corpus."""

    if not corpus:
        return CorpusStatistics(
            document_count=0,
            paragraph_count=0,
            total_file_size=0,
            average_paragraphs=0.0,
            largest_document="",
            smallest_document="",
        )

    paragraph_count = sum(
        document.paragraph_count
        for document in corpus
    )

    total_file_size = sum(
        document.metadata.file_size
        for document in corpus
    )

    largest = max(
        corpus,
        key=lambda document: document.metadata.file_size,
    )

    smallest = min(
        corpus,
        key=lambda document: document.metadata.file_size,
    )

    return CorpusStatistics(
        document_count=len(corpus),
        paragraph_count=paragraph_count,
        total_file_size=total_file_size,
        average_paragraphs=paragraph_count / len(corpus),
        largest_document=largest.name,
        smallest_document=smallest.name,
    )


def print_statistics(
    artifact: KnowledgeArtifact,
) -> None:
    """
    Print executive knowledge statistics.

    This function is retained as a compatibility layer for
    the application entry point.
    """

    print(f"Knowledge Evidence: {artifact.evidence_count}")
    print(
        f"Average Evidence Score: "
        f"{artifact.average_evidence_score:.1f}"
    )
    print(
        f"Highest Evidence Score: "
        f"{artifact.highest_evidence_score}"
    )
    print()

    categories = Counter(
        item.category
        for item in artifact.evidence
    )

    print("Evidence Categories")
    print("-" * 30)

    for category in sorted(categories):
        print(f"{category:<28}{categories[category]}")