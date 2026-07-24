"""Evidence retrieval."""

from dataclasses import dataclass

from career_corpus.retrieval import RetrievedParagraph


@dataclass(slots=True)
class Evidence:
    """Evidence extracted from the corpus."""

    source_document: str
    paragraph_number: int
    text: str

    @property
    def is_quantified(self) -> bool:
        """Return True if the evidence appears to contain a measurable result."""
        return "$" in self.text or "%" in self.text


def build_evidence(
    paragraphs: list[RetrievedParagraph],
) -> list[Evidence]:
    """Convert retrieved paragraphs into evidence objects."""

    evidence: list[Evidence] = []

    for paragraph in paragraphs:
        evidence.append(
            Evidence(
                source_document=paragraph.document,
                paragraph_number=paragraph.paragraph_number,
                text=paragraph.text,
            )
        )

    return evidence