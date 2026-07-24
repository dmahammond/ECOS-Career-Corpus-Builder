"""Document classification."""

from enum import Enum


class DocumentType(str, Enum):
    """Supported ECOS document collections."""

    KNOWLEDGE_BASE = "knowledge_base"
    EVIDENCE_VAULT = "evidence_vault"
    STAR_BANK = "star_bank"
    JOB_DESCRIPTION = "job_description"
    UNKNOWN = "unknown"