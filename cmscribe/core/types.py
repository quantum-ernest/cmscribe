"""Shared types and enums for the cmscribe package."""

from enum import Enum


class CommitFormat(Enum):
    """Supported commit message formats."""

    CONVENTIONAL = "conventional"
    SEMANTIC = "semantic"
    SIMPLE = "simple"
    ANGULAR = "angular"
