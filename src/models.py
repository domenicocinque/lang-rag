from typing import Any, Literal

import uuid
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from pgvector.sqlalchemy import VECTOR


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


class TranslationRequest(BaseModel):
    source_language: str = Field(..., max_length=2)
    target_language: str = Field(..., max_length=2)
    sentence: str = Field(description="Sentence to be translated")


class RagResponse(BaseModel):
    suggestions: list[str]


class StammeringCheckResponse(BaseModel):
    has_stammer: bool


class HealthCheckResponse(BaseModel):
    status: Literal["ok"] = "ok"
    model_loaded: bool
    database: Literal["connected", "disconnected"]
