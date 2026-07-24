"""Knowledge curation."""

from dataclasses import dataclass

from career_corpus.classifier import ClassifiedEvidence


CURATED_TYPES = {
    "EXECUTIVE_ACHIEVEMENT",
    "EXECUTIVE_PROFILE",
    "LEADERSHIP",
    "COMPETENCY",
    "CAREER_HISTORY",
}

INSTRUCTION_PHRASES = (
    "always ",
    "never ",
    "workflow",
    "decision dashboard",
    "golden template",
    "submission recommendation",
    "qa review",
    "if apply",
    "if pass",
    "produce:",
    "operating manual",
    "purpose:",
)

PROFILE_PHRASES = (
    "years",
    "experience",
    "executive",
    "vice president",
    "director",
    "industry experience",
)

ACHIEVEMENT_PHRASES = (
    "led",
    "built",
    "created",
    "developed",
    "reduced",
    "improved",
    "saved",
    "delivered",
    "$",
    "%",
)


@dataclass(slots=True)
class CuratedEvidence:
    """Evidence after knowledge curation."""

    knowledge_type: str
    evidence: ClassifiedEvidence


def determine_knowledge_type(
    item: ClassifiedEvidence,
) -> str:
    """Determine the knowledge type for one evidence item."""

    text = item.evidence.text.lower()

    if any(
        phrase in text
        for phrase in INSTRUCTION_PHRASES
    ):
        return "INSTRUCTION"

    if any(
        phrase in text
        for phrase in ACHIEVEMENT_PHRASES
    ):
        return "EXECUTIVE_ACHIEVEMENT"

    if any(
        phrase in text
        for phrase in PROFILE_PHRASES
    ):
        return "EXECUTIVE_PROFILE"

    if item.category == "Leadership":
        return "LEADERSHIP"

    if item.category == "Strategy":
        return "COMPETENCY"

    return "CAREER_HISTORY"


def curate_evidence(
    evidence: list[ClassifiedEvidence],
) -> list[ClassifiedEvidence]:
    """
    Remove non-career knowledge from downstream generators.
    """

    curated: list[ClassifiedEvidence] = []

    for item in evidence:

        knowledge_type = determine_knowledge_type(
            item,
        )

        if knowledge_type in CURATED_TYPES:
            curated.append(item)

    return curated