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

    def render(self) -> str:
        """
        Render the resume as formatted text.
        """

        lines: list[str] = []

        lines.append("=" * 60)
        lines.append("EXECUTIVE RESUME")
        lines.append("=" * 60)
        lines.append("")

        for section in self.sections:

            lines.append(section.title.upper())
            lines.append("-" * len(section.title))
            lines.append("")

            for accomplishment in section.accomplishments:
                lines.append(f"• {accomplishment}")

            lines.append("")

        return "\n".join(lines)


def generate_resume(
    evidence: list[ClassifiedEvidence],
    *,
    maximum_items_per_section: int = 8,
) -> ExecutiveResume:
    """
    Generate a structured executive resume.

    Evidence is grouped by category and ranked by the
    Executive Priority Score.
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
                item.achievement_score,
            ),
            reverse=True,
        )

        accomplishments = [
            item.evidence.text.strip()
            for item in ranked[:maximum_items_per_section]
            if item.evidence.text.strip()
        ]

        if accomplishments:
            sections.append(
                ResumeSection(
                    title=category,
                    accomplishments=accomplishments,
                )
            )

    return ExecutiveResume(
        sections=sections,
    )