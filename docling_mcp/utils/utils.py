"""General utility functions for document metadata."""

import mimetypes
import platform
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from docling.datamodel.vlm_model_specs import (  # type: ignore[attr-defined]
        InlineVlmOptions,
    )

from docling_mcp.shared import local_document_metadata


def get_document_metadata(document_key: str) -> dict[str, Any]:
    """Get document metadata for a given document key."""
    document_metadata = local_document_metadata.get(document_key)
    if document_metadata is None:
        return {}
    return document_metadata.model_dump()


def get_document_type(source: str) -> str | None:
    """Get document type for a given source."""
    return mimetypes.guess_type(source)[0]


def is_macos() -> bool:
    """Check if the current platform is macOS.

    Returns:
        bool: True if running on macOS (Darwin), False otherwise.
    """
    return platform.system() == "Darwin"


def get_vlm_model_for_platform() -> "InlineVlmOptions":
    """Get the appropriate VLM model based on the current platform.

    Returns:
        VLM model specification: GRANITEDOCLING_MLX for macOS (optimized for Apple Silicon),
                                GRANITEDOCLING_TRANSFORMERS for other platforms.
    """
    if is_macos():
        from docling.datamodel.vlm_model_specs import GRANITEDOCLING_MLX

        return GRANITEDOCLING_MLX
    else:
        from docling.datamodel.vlm_model_specs import (
            GRANITEDOCLING_TRANSFORMERS,
        )

        return GRANITEDOCLING_TRANSFORMERS
