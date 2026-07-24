"""Corpus inspection utilities."""

from career_corpus.classifier import ClassifiedEvidence


def print_inspection(
    evidence: list[ClassifiedEvidence],
    *,
    limit: int = 25,
) -> None:
    """
    Print a developer inspection view of the classified evidence.
    """

    print("=" * 60)
    print("CORPUS INSPECTION")
    print("=" * 60)
    print()

    for index, item in enumerate(evidence[:limit], start=1):

        print(f"[{index}]")
        print(f"Category : {item.category}")
        print(f"Score    : {item.evidence_score}")

        if item.tags:
            print(f"Tags     : {', '.join(item.tags)}")
        else:
            print("Tags     : (none)")

        print(f"Document : {item.evidence.document}")
        print(f"Paragraph: {item.evidence.paragraph_number}")
        print()

        text = item.evidence.text.strip()

        if len(text) > 250:
            text = text[:250] + "..."

        print(text)
        print("-" * 60)

    print()
    print(
        f"Displayed {min(limit, len(evidence))} "
        f"of {len(evidence)} evidence items."
    )