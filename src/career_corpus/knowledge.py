"""Knowledge artifact generation."""

from dataclasses import dataclass

from career_corpus.classifier import ClassifiedEvidence


@dataclass(slots=True)
class KnowledgeArtifact:
    """A collection of classified evidence."""

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


def build_knowledge_artifact(
    title: str,
    evidence: list[ClassifiedEvidence],
) -> KnowledgeArtifact:
    """
    Build a knowledge artifact.

    This establishes the canonical object that future
    modules (resume generation, STAR stories, interview
    responses, cover letters) will consume.
    """

    return KnowledgeArtifact(
        title=title,
        evidence=evidence,
    )