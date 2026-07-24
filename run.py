"""ECOS Career Corpus Builder
Application Entry Point
"""

import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from career_corpus.models import DocumentRecord
from career_corpus.corpus import build_corpus
from career_corpus.app import main

print("DocumentRecord signature:")
print(inspect.signature(DocumentRecord))
print()

print("DocumentRecord loaded from:")
print(inspect.getfile(DocumentRecord))
print()

print("Corpus loaded from:")
print(inspect.getfile(build_corpus))
print()

raise SystemExit(main())