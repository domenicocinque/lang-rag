import uuid
from typing import Any

from pgvector.sqlalchemy import VECTOR
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class TranslationPairBase(BaseModel):
    source_language: str = Field(..., max_length=2)
    target_language: str = Field(..., max_length=2)
    sentence: str = Field(description="Original sentence in source language")
    translation: str = Field(description="Translated sentence in target language")


class TranslationPairCreate(TranslationPairBase):
    pass


class Sentence(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    language: str = Field(..., max_length=2, primary_key=True)
    sentence: str
    embedding: Any = Field(default=None, sa_type=VECTOR(384))


class RagResponse(BaseModel):
    suggestions: list[str]
