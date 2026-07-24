"""Executive Knowledge Engine."""

from collections import defaultdict
from dataclasses import dataclass

from career_corpus.classifier import ClassifiedEvidence


@dataclass(slots=True)
class KnowledgeSection:
    """A competency section within the executive knowledge base."""

    name: str
    evidence: list[ClassifiedEvidence]


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


def build_executive_knowledge(
    evidence: list[ClassifiedEvidence],
) -> ExecutiveKnowledgeBase:
    """
    Build a structured executive knowledge base.

    Evidence is grouped by its primary category and sorted
    by evidence score within each category.
    """

    grouped: dict[str, list[ClassifiedEvidence]] = defaultdict(list)

    for item in evidence:
        grouped[item.category].append(item)

    sections: list[KnowledgeSection] = []

    for category in sorted(grouped):

        ranked = sorted(
            grouped[category],
            key=lambda x: x.evidence_score,
            reverse=True,
        )

        sections.append(
            KnowledgeSection(
                name=category,
                evidence=ranked,
            )
        )

    return ExecutiveKnowledgeBase(
        sections=sections,
    )