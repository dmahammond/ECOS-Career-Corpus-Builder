"""Knowledge artifact generation."""

from dataclasses import dataclass, field
from collections import defaultdict

from career_corpus.classifier import ClassifiedEvidence


@dataclass(slots=True)
class KnowledgeArtifact:
    """Canonical executive knowledge artifact."""

    title: str
    evidence: list[ClassifiedEvidence]

    @property
    def evidence_count(self) -> int:
        """Return the number of evidence items."""
        return len(self.evidence)

    @property
    def average_evidence_score(self) -> float:
        """Return the average evidence score."""
        if not self.evidence:
            return 0.0

        return (
            sum(item.evidence_score for item in self.evidence)
            / len(self.evidence)
        )

    @property
    def highest_evidence_score(self) -> int:
        """Return the highest evidence score."""
        if not self.evidence:
            return 0

        return max(
            item.evidence_score
            for item in self.evidence
        )


@dataclass(slots=True)
class ExecutiveCapability:
    """Evidence grouped into a single executive capability."""

    name: str
    evidence: list[ClassifiedEvidence] = field(default_factory=list)

    @property
    def evidence_count(self) -> int:
        return len(self.evidence)

    @property
    def average_score(self) -> float:
        if not self.evidence:
            return 0.0

        return (
            sum(item.evidence_score for item in self.evidence)
            / len(self.evidence)
        )

    @property
    def highest_score(self) -> int:
        if not self.evidence:
            return 0

        return max(
            item.evidence_score
            for item in self.evidence
        )

    def ranked_evidence(self) -> list[ClassifiedEvidence]:
        """Return evidence sorted by strength."""
        return sorted(
            self.evidence,
            key=lambda item: (
                item.evidence_score,
                item.achievement_score,
            ),
            reverse=True,
        )


@dataclass(slots=True)
class ExecutiveKnowledge:
    """Structured executive knowledge."""

    artifact: KnowledgeArtifact
    capabilities: list[ExecutiveCapability]

    @property
    def capability_count(self) -> int:
        return len(self.capabilities)

    def top_capabilities(
        self,
        limit: int = 10,
    ) -> list[ExecutiveCapability]:
        """Return highest-value capability groups."""
        return sorted(
            self.capabilities,
            key=lambda capability: (
                capability.highest_score,
                capability.average_score,
                capability.evidence_count,
            ),
            reverse=True,
        )[:limit]

    def top_evidence(
        self,
        limit: int = 25,
    ) -> list[ClassifiedEvidence]:
        """Return the strongest evidence across all categories."""
        return sorted(
            self.artifact.evidence,
            key=lambda item: (
                item.evidence_score,
                item.achievement_score,
            ),
            reverse=True,
        )[:limit]


def build_knowledge_artifact(
    title: str,
    evidence: list[ClassifiedEvidence],
) -> KnowledgeArtifact:
    """
    Build the canonical knowledge artifact.
    """

    return KnowledgeArtifact(
        title=title,
        evidence=evidence,
    )


def build_executive_knowledge(
    artifact: KnowledgeArtifact,
) -> ExecutiveKnowledge:
    """
    Build structured executive knowledge grouped by capability.
    """

    grouped: dict[str, list[ClassifiedEvidence]] = defaultdict(list)

    for item in artifact.evidence:
        grouped[item.category].append(item)

    capabilities = [
        ExecutiveCapability(
            name=name,
            evidence=sorted(
                items,
                key=lambda evidence: (
                    evidence.evidence_score,
                    evidence.achievement_score,
                ),
                reverse=True,
            ),
        )
        for name, items in sorted(grouped.items())
    ]

    return ExecutiveKnowledge(
        artifact=artifact,
        capabilities=capabilities,
    )