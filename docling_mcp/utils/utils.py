"""General utility functions for document metadata."""

from docling_mcp.shared import local_document_metadata


def get_document_metadata(document_key: str) -> dict:
    """Get document metadata for a given document key."""
    document_metadata = local_document_metadata.get(document_key)
    if document_metadata is None:
        return {}
    return document_metadata.model_dump()
