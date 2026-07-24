"""Executive Knowledge Engine."""

from collections import defaultdict
from dataclasses import dataclass

from career_corpus.classifier import ClassifiedEvidence


@dataclass(slots=True)
class KnowledgeSection:
    """A competency section within the executive knowledge base."""

    name: str
    evidence: list[ClassifiedEvidence]

    @property
    def evidence_count(self) -> int:
        """Return the number of evidence items."""
        return len(self.evidence)

    @property
    def highest_score(self) -> int:
        """Highest evidence score within the section."""
        if not self.evidence:
            return 0

        return max(
            item.evidence_score
            for item in self.evidence
        )

    @property
    def average_score(self) -> float:
        """Average evidence score within the section."""
        if not self.evidence:
            return 0.0

        return (
            sum(item.evidence_score for item in self.evidence)
            / len(self.evidence)
        )

    def top_evidence(
        self,
        limit: int = 10,
    ) -> list[ClassifiedEvidence]:
        """Return the strongest evidence within this section."""
        return self.evidence[:limit]


@dataclass(slots=True)
class ExecutiveKnowledgeBase:
    """Structured executive knowledge."""

    sections: list[KnowledgeSection]

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def evidence_count(self) -> int:
        return sum(
            len(section.evidence)
            for section in self.sections
        )

    def top_sections(
        self,
        limit: int = 10,
    ) -> list[KnowledgeSection]:
        """Return the strongest executive capability areas."""

        return sorted(
            self.sections,
            key=lambda section: (
                section.highest_score,
                section.average_score,
                section.evidence_count,
            ),
            reverse=True,
        )[:limit]

    def top_evidence(
        self,
        limit: int = 25,
    ) -> list[ClassifiedEvidence]:
        """Return the strongest evidence across all sections."""

        ranked: list[ClassifiedEvidence] = []

        for section in self.sections:
            ranked.extend(section.evidence)

        ranked.sort(
            key=lambda item: (
                item.evidence_score,
                item.achievement_score,
            ),
            reverse=True,
        )

        return ranked[:limit]


def build_executive_knowledge(
    evidence: list[ClassifiedEvidence],
) -> ExecutiveKnowledgeBase:
    """
    Build a structured executive knowledge base.

    Evidence is grouped by category and ranked according to
    evidence strength. This knowledge base becomes the
    canonical source for resume generation, cover letters,
    STAR stories, interview preparation, and executive
    reporting.
    """

    grouped: dict[str, list[ClassifiedEvidence]] = defaultdict(list)

    for item in evidence:
        grouped[item.category].append(item)

    sections: list[KnowledgeSection] = []

    for category in sorted(grouped):

        ranked = sorted(
            grouped[category],
            key=lambda item: (
                item.evidence_score,
                item.achievement_score,
            ),
            reverse=True,
        )

        sections.append(
            KnowledgeSection(
                name=category,
                evidence=ranked,
            )
        )

    sections.sort(
        key=lambda section: (
            section.highest_score,
            section.average_score,
            section.evidence_count,
        ),
        reverse=True,
    )

    return ExecutiveKnowledgeBase(
        sections=sections,
    )