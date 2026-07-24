"""
Document loading utilities.
"""

from pathlib import Path


def list_documents(folder: str) -> list[Path]:
    """
    Return every .docx file in a folder.
    """

    path = Path(folder)

    if not path.exists():
        return []

    return sorted(path.glob("*.docx"))