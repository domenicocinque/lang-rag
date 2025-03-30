import logging
import uuid
from typing import Any

from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from sentence_transformers import SentenceTransformer

from src.config import settings
from src.db import engine
from src.rag.repositories import SentenceRepository
from src.rag.schemas import (
    Sentence,
    TranslationPairCreate,
    RagResponse,
)

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

try:
    model = SentenceTransformer(settings.MODEL_NAME)  # type: ignore
    logger.info("Successfully loaded the sentence transformer model")
except Exception as e:
    logger.error(f"Failed to load the sentence transformer model: {e}")
    raise


router = APIRouter()
sentence_repository = SentenceRepository(engine=engine)


@router.post("/pairs", response_model=str, status_code=status.HTTP_201_CREATED)
def add_translation_pair(pair: TranslationPairCreate) -> Any:
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
        sentence_repository.add_sentence_couple(sentence1, sentence2)
        return "OK"
    except Exception as e:
        logger.error(f"Error adding translation pair: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add translation pair",
        )


@router.get("/prompt", response_model=RagResponse)
def get_translation_prompt(
    source_language: str, target_language: str, query_sentence: str, top_k: int = 4
) -> Any:
    """
    API endpoint to get a translation prompt with similar examples.
    """
    query_embedding = model.encode(query_sentence).tolist()
    suggestions = sentence_repository.get_potential_translations(
        source_language=source_language,
        target_language=target_language,
        query_embedding=query_embedding,
        top_k=top_k,
    )
    return RagResponse(suggestions=suggestions)
