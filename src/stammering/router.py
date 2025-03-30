import logging
from typing import Any

from fastapi import HTTPException, status
from fastapi.routing import APIRouter

from src.config import settings
from src.stammering.schemas import StammeringCheckResponse
from src.stammering.services import detect_stammering

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

router = APIRouter()


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
