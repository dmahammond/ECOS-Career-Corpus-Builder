"""Document metadata."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class DocumentMetadata:
    """Metadata describing a source document."""

    document_type: str
    document_role: str
    title: str


def _load_role_config() -> tuple[dict[str, str], str]:
    config_path = Path("config") / "document_roles.yaml"

    if not config_path.exists():
        return {}, "evidence"

    with config_path.open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    roles = {
        filename: values.get("role", "evidence").lower()
        for filename, values in config.get("roles", {}).items()
    }

    default_role = config.get(
        "default_role",
        "evidence",
    ).lower()

    return roles, default_role


_DOCUMENT_ROLES, _DEFAULT_ROLE = _load_role_config()


def determine_document_role(path: Path) -> str:
    return _DOCUMENT_ROLES.get(
        path.name,
        _DEFAULT_ROLE,
    )


def determine_document_type(path: Path) -> str:
    name = path.name.lower()

    if "experience" in name:
        return "experience"

    if "achievement" in name:
        return "achievement"

    if "star" in name:
        return "star"

    if "foundation" in name:
        return "foundation"

    if "resume" in name:
        return "resume"

    return "general"


def build_document_metadata(path: Path) -> DocumentMetadata:
    return DocumentMetadata(
        document_type=determine_document_type(path),
        document_role=determine_document_role(path),
        title=path.stem,
    )


# ------------------------------------------------------------------
# Backward compatibility
# ------------------------------------------------------------------

def get_document_metadata(path: Path) -> DocumentMetadata:
    """
    Backward-compatible API expected by the existing corpus builder.
    """
    return build_document_metadata(path)