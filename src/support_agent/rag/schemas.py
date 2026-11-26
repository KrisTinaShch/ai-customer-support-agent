from datetime import date
from enum import StrEnum
from pathlib import Path

from pydantic import BaseModel, Field


class DocumentLanguage(StrEnum):
    ENGLISH = "en"
    BULGARIAN = "bg"


class DocumentCategory(StrEnum):
    POLICY = "policy"
    PRODUCT = "product"
    MANUAL = "manual"
    TROUBLESHOOTING = "troubleshooting"
    COMPATIBILITY = "compatibility"
    GUIDE = "guide"


class KnowledgeDocument(BaseModel):
    document_id: str
    source_id: str
    language: DocumentLanguage
    category: DocumentCategory
    title: str
    version: str
    updated_at: date
    content: str = Field(min_length=1)
    source_path: Path


class KnowledgeChunk(BaseModel):
    chunk_id: str
    document_id: str
    source_id: str
    language: DocumentLanguage
    category: DocumentCategory
    document_title: str
    section_title: str | None = None
    chunk_index: int = Field(ge=0)
    version: str
    updated_at: date
    content: str = Field(min_length=1)
    source_path: Path
