"""Application entry point."""

from pathlib import Path
import sys

from career_corpus.classifier import classify_evidence
from career_corpus.config import load_settings
from career_corpus.corpus import build_corpus
from career_corpus.curation import curate_evidence
from career_corpus.database import (
    initialize_database,
    save_corpus,
)
from career_corpus.duplicates import find_duplicate_documents
from career_corpus.evidence import build_evidence
from career_corpus.knowledge import build_knowledge_artifact
from career_corpus.reporting import build_executive_report
from career_corpus.resume_generator import generate_resume
from career_corpus.search import search_evidence
from career_corpus.statistics import print_statistics
from career_corpus.retrieval import get_all_paragraphs


def main() -> int:
    """Run the Career Corpus Builder."""

    settings = load_settings()

    print("=" * 60)
    print(settings.project.name)
    print(f"Version {settings.project.version}")
    print("=" * 60)
    print()

    print("Configuration loaded successfully.")
    print(f"Knowledge Base: {settings.paths.knowledge_base}")
    print()

    corpus = build_corpus(settings.paths.knowledge_base)

    database = initialize_database(Path("CareerCorpus.db"))

    document_count, paragraph_count = save_corpus(
        database,
        corpus,
    )

    duplicates = find_duplicate_documents(database)

    retrieved = get_all_paragraphs(database)

    evidence = build_evidence(retrieved)

    classified = classify_evidence(evidence)

    #
    # Sprint 11
    # Remove operational instructions before any
    # downstream artifact consumes the evidence.
    #
    classified = curate_evidence(classified)

    artifact = build_knowledge_artifact(
        title="Complete Knowledge Base",
        evidence=classified,
    )

    print(f"Documents Loaded : {document_count}")
    print(f"Paragraphs Loaded: {paragraph_count}")
    print()

    print(f"Duplicate Documents: {len(duplicates)}")
    print()

    print_statistics(artifact)

    #
    # Resume mode
    #

    if len(sys.argv) >= 2 and sys.argv[1].lower() == "resume":

        resume = generate_resume(
            artifact.evidence,
        )

        print()
        print(resume.render())

    #
    # Search mode
    #

    elif len(sys.argv) >= 3 and sys.argv[1].lower() == "search":

        query = " ".join(sys.argv[2:])

        print()

        search_evidence(
            artifact,
            query,
        )

    #
    # Executive report mode
    #

    elif len(sys.argv) >= 2 and sys.argv[1].lower() == "report":

        print()
        print(
            build_executive_report(
                artifact.evidence,
            )
        )

    print()

    print("SQLite database created successfully.")
    print("Database: CareerCorpus.db")

    database.close()

    return 0