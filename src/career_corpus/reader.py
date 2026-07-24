"""Word document reader."""

from pathlib import Path

from docx import Document


def read_document(path: Path) -> list[str]:
    """
    Read a Word document and return all non-empty paragraphs.
    """

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    return paragraphs