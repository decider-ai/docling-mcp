"""Global schemas file."""

from typing import Optional

from pydantic import BaseModel


class DocumentMetadata(BaseModel):
    """Class for storing metadata of the docling document."""

    created_at: str
    updated_at: Optional[str] = None
    source: Optional[str] = None
    type: Optional[str] = None

    # title: str
    # author: str
    # language: str
