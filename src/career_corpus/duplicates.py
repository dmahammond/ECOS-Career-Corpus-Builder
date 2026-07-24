"""Duplicate document detection."""

import sqlite3


def find_duplicate_documents(
    connection: sqlite3.Connection,
) -> list[tuple[str, int]]:
    """Return duplicate documents based on SHA-256."""

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            sha256,
            COUNT(*)
        FROM documents
        GROUP BY sha256
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        """
    )

    return cursor.fetchall()