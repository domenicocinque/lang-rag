from typing import Any
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from pgvector.sqlalchemy import VECTOR


class TranslationPairBase(SQLModel):
    source_language: str = Field(..., max_length=2)
    target_language: str = Field(..., max_length=2)
    sentence: str
    translation: str


class TranslationPairCreate(TranslationPairBase):
    pass


class TranslationPair(TranslationPairBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    source_embedding: Any = Field(default=None, sa_type=VECTOR(384))
    translation_embedding: Any = Field(default=None, sa_type=VECTOR(384))


class TranslationRequest(BaseModel):
    source_language: str = Field(..., max_length=2)
    target_language: str = Field(..., max_length=2)
    sentence: str


class TranslationPrompt(BaseModel):
    prompt: str
    suggestions: list[str]


class StammeringCheckResponse(BaseModel):
    has_stammer: bool
