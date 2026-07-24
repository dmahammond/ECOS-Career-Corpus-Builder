"""Evidence query services."""

import sqlite3

from career_corpus.classifier import (
    CATEGORY_ALIASES,
    CATEGORY_KEYWORDS,
    ClassifiedEvidence,
    classify_evidence,
)
from career_corpus.evidence import build_evidence
from career_corpus.retrieval import find_paragraphs


def _expand_terms(term: str) -> list[str]:
    """
    Expand a search term into a concept.

    The search term may match:

    • a category name
    • an alias
    • a keyword

    Once matched, every keyword in that concept becomes
    part of the search.
    """

    lower = term.lower()

    #
    # Direct category match
    #

    for category in CATEGORY_KEYWORDS:

        if lower == category.lower():

            return sorted(
                set(CATEGORY_KEYWORDS[category])
            )

    #
    # Alias match
    #

    for category, aliases in CATEGORY_ALIASES.items():

        if lower in aliases:

            return sorted(
                set(CATEGORY_KEYWORDS[category])
            )

    #
    # Keyword match
    #

    for category, keywords in CATEGORY_KEYWORDS.items():

        if lower in keywords:

            return sorted(
                set(keywords)
            )

    #
    # Default
    #

    return [lower]


def search_evidence(
    connection: sqlite3.Connection,
    text: str,
) -> list[ClassifiedEvidence]:
    """
    Search the corpus.
    """

    paragraphs = []

    seen = set()

    for search_term in _expand_terms(text):

        results = find_paragraphs(
            connection,
            search_term,
        )

        for paragraph in results:

            key = (
                paragraph.document,
                paragraph.paragraph_number,
            )

            if key in seen:
                continue

            seen.add(key)

            paragraphs.append(paragraph)

    evidence = build_evidence(paragraphs)

    classified = classify_evidence(
        evidence
    )

    return sorted(
        classified,
        key=lambda item: (
            item.evidence_score,
            item.achievement_score,
            item.evidence.source_document,
            item.evidence.paragraph_number,
        ),
        reverse=True,
    )