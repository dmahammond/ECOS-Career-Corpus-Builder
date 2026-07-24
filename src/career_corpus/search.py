"""Corpus search."""

import sqlite3
from dataclasses import dataclass

from career_corpus.knowledge import KnowledgeArtifact


@dataclass(slots=True)
class SearchResult:
    """A paragraph returned from the corpus."""

    document: str
    paragraph: int
    text: str


def search_corpus(
    connection: sqlite3.Connection,
    query: str,
    limit: int = 25,
) -> list[SearchResult]:
    """Search paragraph text."""

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            d.name,
            p.paragraph_number,
            p.paragraph_text
        FROM paragraphs p
        JOIN documents d
            ON p.document_id = d.id
        WHERE p.paragraph_text LIKE ?
        ORDER BY
            d.name,
            p.paragraph_number
        LIMIT ?
        """,
        (
            f"%{query}%",
            limit,
        ),
    )

    return [
        SearchResult(
            document=row[0],
            paragraph=row[1],
            text=row[2],
        )
        for row in cursor.fetchall()
    ]


def search_evidence(
    artifact: KnowledgeArtifact,
    query: str,
    limit: int = 25,
) -> None:
    """
    Search classified evidence contained in the knowledge artifact.
    """

    query = query.lower()

    matches = [
        item
        for item in artifact.evidence
        if query in item.evidence.text.lower()
    ]

    matches.sort(
        key=lambda item: (
            item.evidence_score,
            item.achievement_score,
        ),
        reverse=True,
    )

    print("=" * 60)
    print(f"Search Results: {query}")
    print("=" * 60)
    print()

    if not matches:
        print("No matching evidence found.")
        return

    for index, item in enumerate(matches[:limit], start=1):

        evidence = item.evidence

        print(f"{index}. Score: {item.evidence_score}")
        print(f"   Category : {item.category}")
        print(f"   Document : {evidence.document}")
        print(f"   Paragraph: {evidence.paragraph}")
        print()
        print(evidence.text)
        print("-" * 60)