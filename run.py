"""ECOS Career Corpus Builder.

Application entry point.
"""

import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent / "src"),
)

from career_corpus.app import main


if __name__ == "__main__":
    raise SystemExit(main())