"""Corpus retrieval."""

import sqlite3
from dataclasses import dataclass


@dataclass(slots=True)
class RetrievedParagraph:
    """A paragraph returned from the corpus."""

    document: str
    paragraph_number: int
    text: str


def get_all_paragraphs(
    connection: sqlite3.Connection,
) -> list[RetrievedParagraph]:
    """Return every paragraph in the corpus."""

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            d.name,
            p.paragraph_number,
            p.paragraph_text
        FROM paragraphs p
        JOIN documents d
            ON d.id = p.document_id
        ORDER BY
            d.name,
            p.paragraph_number
        """
    )

    return [
        RetrievedParagraph(
            document=row[0],
            paragraph_number=row[1],
            text=row[2],
        )
        for row in cursor.fetchall()
    ]


def find_paragraphs(
    connection: sqlite3.Connection,
    text: str,
    limit: int = 100,
) -> list[RetrievedParagraph]:
    """Return paragraphs containing text."""

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            d.name,
            p.paragraph_number,
            p.paragraph_text
        FROM paragraphs p
        JOIN documents d
            ON d.id = p.document_id
        WHERE
            p.paragraph_text LIKE ?
        ORDER BY
            d.name,
            p.paragraph_number
        LIMIT ?
        """,
        (
            f"%{text}%",
            limit,
        ),
    )

    return [
        RetrievedParagraph(
            document=row[0],
            paragraph_number=row[1],
            text=row[2],
        )
        for row in cursor.fetchall()
    ]