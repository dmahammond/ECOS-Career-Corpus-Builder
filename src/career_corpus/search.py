"""Corpus search."""

import sqlite3
from dataclasses import dataclass


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