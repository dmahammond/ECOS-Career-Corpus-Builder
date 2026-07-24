"""Executive resume generation."""

from dataclasses import dataclass

from career_corpus.classifier import ClassifiedEvidence


@dataclass(slots=True)
class ResumeSection:
    """A section within a generated resume."""

    title: str
    accomplishments: list[str]


@dataclass(slots=True)
class ExecutiveResume:
    """A generated executive resume."""

    sections: list[ResumeSection]

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def accomplishment_count(self) -> int:
        return sum(
            len(section.accomplishments)
            for section in self.sections
        )


def generate_resume(
    evidence: list[ClassifiedEvidence],
    *,
    maximum_items_per_section: int = 8,
) -> ExecutiveResume:
    """
    Generate a structured executive resume.

    Evidence is grouped by category and ranked by the
    Executive Priority Score calculated by the classifier.
    """

    grouped: dict[str, list[ClassifiedEvidence]] = {}

    for item in evidence:

        grouped.setdefault(
            item.category,
            [],
        ).append(item)

    sections: list[ResumeSection] = []

    for category in sorted(grouped):

        ranked = sorted(
            grouped[category],
            key=lambda item: (
                item.executive_priority_score,
                item.evidence_score,
            ),
            reverse=True,
        )

        accomplishments = [
            item.evidence.text
            for item in ranked[:maximum_items_per_section]
        ]

        sections.append(
            ResumeSection(
                title=category,
                accomplishments=accomplishments,
            )
        )

    return ExecutiveResume(
        sections=sections,
    )