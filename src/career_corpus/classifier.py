"""Evidence classification."""

from dataclasses import dataclass
from pathlib import Path
import re

import yaml

from career_corpus.evidence import Evidence


@dataclass(slots=True)
class ClassifiedEvidence:
    """Evidence enriched with classification information."""

    category: str
    evidence: Evidence
    tags: list[str]
    achievement_score: int
    evidence_score: int
    executive_priority_score: int


DEFAULT_CATEGORY = "General"


EXECUTIVE_BONUS = {
    "Leadership": 25,
    "Strategy": 20,
    "Operational Excellence": 18,
    "Analytics": 15,
    "Digital": 15,
    "Healthcare": 12,
    "General": 0,
}


def _load_rules():
    """
    Load the classification taxonomy.

    Supports both the original schema:

        Leadership:
          - lead
          - manager

    and the newer schema:

        Leadership:
          aliases:
            - leadership
          keywords:
            - lead
            - manager
    """

    config_path = Path("config") / "classification.yaml"

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    category_keywords: dict[str, tuple[str, ...]] = {}
    category_aliases: dict[str, tuple[str, ...]] = {}

    for category, value in config["categories"].items():

        if isinstance(value, dict):

            aliases = tuple(
                alias.lower()
                for alias in value.get("aliases", [])
            )

            keywords = tuple(
                keyword.lower()
                for keyword in value.get("keywords", [])
            )

        else:

            aliases = ()

            keywords = tuple(
                keyword.lower()
                for keyword in value
            )

        category_aliases[category] = aliases
        category_keywords[category] = keywords

    achievement_words = tuple(
        word.lower()
        for word in config["achievement_words"]
    )

    return (
        category_keywords,
        category_aliases,
        achievement_words,
    )


(
    CATEGORY_KEYWORDS,
    CATEGORY_ALIASES,
    ACHIEVEMENT_WORDS,
) = _load_rules()


def _find_tags(text: str) -> list[str]:
    """Return matching category tags."""

    lower = text.lower()

    tags: list[str] = []

    for category, keywords in CATEGORY_KEYWORDS.items():

        if any(keyword in lower for keyword in keywords):

            tags.append(category)

    return sorted(tags)


def _achievement_score(text: str) -> int:
    """Calculate a deterministic achievement score."""

    score = 0

    lower = text.lower()

    if re.search(r"\$\s?\d", text):
        score += 30

    if re.search(r"\d+\s*%", text):
        score += 20

    for word in ACHIEVEMENT_WORDS:

        if word in lower:
            score += 8

    return min(score, 100)


def _evidence_score(
    tags: list[str],
    achievement_score: int,
) -> int:
    """Calculate an overall evidence score."""

    score = achievement_score + len(tags) * 10

    return min(score, 100)


def _executive_priority_score(
    category: str,
    evidence_score: int,
    achievement_score: int,
    text: str,
) -> int:
    """
    Calculate Executive Priority Score (EPS).

    EPS ranks accomplishments for executive resume generation.
    """

    score = evidence_score + achievement_score

    score += EXECUTIVE_BONUS.get(category, 0)

    lower = text.lower()

    executive_terms = (
        "enterprise",
        "executive",
        "vice president",
        "vp",
        "director",
        "strategy",
        "transformation",
        "portfolio",
        "governance",
    )

    for term in executive_terms:
        if term in lower:
            score += 5

    return min(score, 100)


def classify_evidence(
    evidence_list: list[Evidence],
) -> list[ClassifiedEvidence]:
    """
    Classify evidence using the configured taxonomy.
    """

    classified: list[ClassifiedEvidence] = []

    for item in evidence_list:

        tags = _find_tags(item.text)

        category = (
            tags[0]
            if tags
            else DEFAULT_CATEGORY
        )

        achievement = _achievement_score(
            item.text
        )

        evidence_score = _evidence_score(
            tags,
            achievement,
        )

        executive_priority = _executive_priority_score(
            category,
            evidence_score,
            achievement,
            item.text,
        )

        classified.append(
            ClassifiedEvidence(
                category=category,
                evidence=item,
                tags=tags,
                achievement_score=achievement,
                evidence_score=evidence_score,
                executive_priority_score=executive_priority,
            )
        )

    classified.sort(
        key=lambda item: (
            item.executive_priority_score,
            item.evidence_score,
            item.achievement_score,
        ),
        reverse=True,
    )

    return classified