"""SHA-256 hashing utilities."""

import hashlib
from pathlib import Path


def sha256_file(path: Path) -> str:
    """Return the SHA-256 hash of a file."""

    digest = hashlib.sha256()

    with path.open("rb") as file:
        while True:
            block = file.read(65536)

            if not block:
                break

            digest.update(block)

    return digest.hexdigest()