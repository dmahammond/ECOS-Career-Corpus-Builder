"""Application configuration."""

from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class ProjectSettings:
    """Project metadata."""

    name: str
    version: str


@dataclass(slots=True)
class PathSettings:
    """Application paths currently used by the corpus builder."""

    knowledge_base: str


@dataclass(slots=True)
class Settings:
    """Application settings."""

    project: ProjectSettings
    paths: PathSettings


def load_settings() -> Settings:
    """Load settings from config/settings.yaml."""

    config_path = Path("config") / "settings.yaml"

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return Settings(
        project=ProjectSettings(
            name=config["project"]["name"],
            version=config["project"]["version"],
        ),
        paths=PathSettings(
            knowledge_base=config["paths"]["knowledge_base"],
        ),
    )