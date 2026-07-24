"""Executive reporting."""

from collections import defaultdict

from career_corpus.classifier import ClassifiedEvidence


def build_executive_report(
    evidence: list[ClassifiedEvidence],
) -> str:
    """Build a text Executive Evidence Report."""

    lines: list[str] = []

    lines.append("=" * 60)
    lines.append("EXECUTIVE EVIDENCE REPORT")
    lines.append("=" * 60)
    lines.append("")

    lines.append(f"Total Evidence: {len(evidence)}")
    lines.append("")

    #
    # Category summary
    #

    category_counts: dict[str, int] = defaultdict(int)

    for item in evidence:
        category_counts[item.category] += 1

    lines.append("Evidence by Category")
    lines.append("-" * 30)

    for category in sorted(category_counts):
        lines.append(
            f"{category:<28} {category_counts[category]}"
        )

    lines.append("")
    lines.append("Top Evidence")
    lines.append("-" * 30)

    top = sorted(
        evidence,
        key=lambda x: x.evidence_score,
        reverse=True,
    )[:15]

    for item in top:

        lines.append(
            f"[{item.evidence_score:3}] "
            f"{item.category}"
        )

        lines.append(
            f"Document : {item.evidence.source_document}"
        )

        lines.append(
            f"Paragraph: {item.evidence.paragraph_number}"
        )

        lines.append(item.evidence.text)

        lines.append("")

    return "\n".join(lines)