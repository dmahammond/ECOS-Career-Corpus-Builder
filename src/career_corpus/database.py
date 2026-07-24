"""SQLite database support."""

import sqlite3
from pathlib import Path

from career_corpus.models import DocumentRecord


def initialize_database(database_path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            sha256 TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paragraphs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_id INTEGER NOT NULL,
            paragraph_number INTEGER NOT NULL,
            paragraph_text TEXT NOT NULL,
            FOREIGN KEY(document_id) REFERENCES documents(id)
        )
    """)

    connection.commit()

    return connection


def save_corpus(
    connection: sqlite3.Connection,
    corpus: list[DocumentRecord],
) -> tuple[int, int]:

    cursor = connection.cursor()

    cursor.execute("DELETE FROM paragraphs")
    cursor.execute("DELETE FROM documents")

    document_count = 0
    paragraph_count = 0

    for document in corpus:

        cursor.execute(
            """
            INSERT INTO documents(
                name,
                path,
                sha256
            )
            VALUES (?, ?, ?)
            """,
            (
                document.name,
                str(document.path),
                document.sha256,
            ),
        )

        document_id = cursor.lastrowid

        document_count += 1

        for paragraph in document.paragraphs:

            cursor.execute(
                """
                INSERT INTO paragraphs(
                    document_id,
                    paragraph_number,
                    paragraph_text
                )
                VALUES (?, ?, ?)
                """,
                (
                    document_id,
                    paragraph.number,
                    paragraph.text,
                ),
            )

            paragraph_count += 1

    connection.commit()

    return document_count, paragraph_count