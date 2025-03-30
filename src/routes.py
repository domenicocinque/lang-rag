from typing import Any

from fastapi import HTTPException, status
from fastapi.routing import APIRouter
import logging
from sqlmodel import Session, select
from sentence_transformers import SentenceTransformer
import uuid

from src.core.db import engine
from src.models import (
    Sentence,
    TranslationPairCreate,
    RagResponse,
    StammeringCheckResponse,
    HealthCheckResponse,
)
from src.services import detect_stammering
from src.core.config import settings


logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

try:
    model = SentenceTransformer(settings.MODEL_NAME)  # type: ignore
    logger.info("Successfully loaded the sentence transformer model")
except Exception as e:
    logger.error(f"Failed to load the sentence transformer model: {e}")
    raise


router = APIRouter()


@router.post("/pairs", response_model=str, status_code=status.HTTP_201_CREATED)
async def add_translation_pair(pair: TranslationPairCreate) -> Any:
    """
    Add a new translation pair to the database.
    """
    try:
        source_embedding = model.encode(pair.sentence).tolist()
        translation_embedding = model.encode(pair.translation).tolist()

        shared_uuid = uuid.uuid4()
        sentence1 = Sentence(
            id=shared_uuid,
            sentence=pair.sentence,
            language=pair.source_language,
            embedding=source_embedding,
        )
        sentence2 = Sentence(
            id=shared_uuid,
            sentence=pair.translation,
            language=pair.target_language,
            embedding=translation_embedding,
        )

        with Session(engine) as session:
            session.add(sentence1)
            session.add(sentence2)
            session.commit()
            logger.info(f"Successfully added translation pair with ID: {shared_uuid}")
        return "OK"
    except Exception as e:
        logger.error(f"Error adding translation pair: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add translation pair",
        )


@router.get("/prompt", response_model=RagResponse)
async def get_translation_prompt(
    source_language: str, target_language: str, query_sentence: str, top_k: int = 4
) -> Any:
    """
    API endpoint to get a translation prompt with similar examples.
    """
    query_embedding = model.encode(query_sentence).tolist()
    with Session(engine) as session:
        src = Sentence.__table_.alias("src")
        tgt = Sentence.__table__.alias("tgt")
        stmt = (
            select(
                src.c.sentence.label("source_sentence"),
                tgt.c.sentence.label("target_sentence"),
                src.c.embedding.cosine_distance(query_embedding).label("distance"),
            )
            .join(tgt, (src.c.id == tgt.c.id))
            .where(src.c.language == source_language)
            .where(tgt.c.language == target_language)
            .order_by("distance")
            .limit(top_k)
        )
        results = session.exec(stmt).fetchall()

    suggestions = [r[1] for r in results]
    return RagResponse(suggestions=suggestions)


@router.get("/stammering", response_model=StammeringCheckResponse)
def stammering_check(source_sentence: str, translated_sentence: str) -> Any:
    """
    API endpoint to check for stammering in a translated sentence.
    """
    try:
        result_source = detect_stammering(source_sentence)
        result_translated = detect_stammering(translated_sentence)
        result = result_source or result_translated
        return StammeringCheckResponse(has_stammer=result)
    except Exception as e:
        logger.error(f"Error checking for stammering: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check for stammering",
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> Any:
    """
    Health check endpoint to verify the API is running correctly.
    """
    return HealthCheckResponse(
        status="ok",
        model_loaded=model is not None,
        database="connected" if engine else "disconnected",
    )
