from fastapi import FastAPI, HTTPException, status
import uvicorn
import logging
from sqlmodel import (
    Session,
    select,
)
from sentence_transformers import SentenceTransformer

from src.core.db import engine
from src.models import (
    TranslationPairCreate,
    TranslationPair,
    TranslationPrompt,
    StammeringCheckResponse,
)
from src.services import detect_stammering

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rag Translation Service API",
)

try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("Successfully loaded the sentence transformer model")
except Exception as e:
    logger.error(f"Failed to load the sentence transformer model: {e}")
    raise


@app.post("/pairs", response_model=str, status_code=status.HTTP_201_CREATED)
async def add_translation_pair(pair: TranslationPairCreate):
    """
    Add a new translation pair to the database.

    Args:
        pair (TranslationPairCreate): The translation pair to add.

    Returns:
        str: "OK" if the pair was added successfully.
    """
    try:
        source_embedding = model.encode(pair.sentence).tolist()
        translation_embedding = model.encode(pair.translation).tolist()

        translation_pair = TranslationPair(
            source_language=pair.source_language,
            target_language=pair.target_language,
            sentence=pair.sentence,
            translation=pair.translation,
            source_embedding=source_embedding,
            translation_embedding=translation_embedding,
        )

        with Session(engine) as session:
            session.add(translation_pair)
            session.commit()
            logger.info(
                f"Successfully added translation pair with ID: {translation_pair.id}"
            )
        return "OK"
    except Exception as e:
        logger.error(f"Error adding translation pair: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add translation pair",
        )


@app.get("/prompt", response_model=TranslationPrompt)
async def get_translation_prompt(
    source_language: str, target_language: str, query_sentence: str
):
    """
    API endpoint to get a translation prompt with similar examples.

    Args:
        source_language (str): The source language code.
        target_language (str): The target language code.
        query_sentence (str): The sentence to translate.

    Returns:
        TranslationPrompt: The translation prompt with suggestions.
    """
    try:
        embedding = model.encode(query_sentence).tolist()

        if source_language == "it":
            query = (
                select(TranslationPair)
                .order_by(
                    TranslationPair.translation_embedding.cosine_distance(embedding)
                )
                .limit(4)
            )
        else:
            query = (
                select(TranslationPair)
                .order_by(TranslationPair.source_embedding.cosine_distance(embedding))
                .limit(4)
            )

        with Session(engine) as session:
            results = session.exec(query).fetchall()

        suggestions = [result.translation for result in results]
        prompt = (
            f"Translate the following {source_language} text to {target_language}:\n"
        )
        prompt += f"Text: {query_sentence}\n"

        if suggestions:
            prompt += "\nSimilar previous translations:\n"
            for i, suggestion in enumerate(suggestions, 1):
                prompt += f"{i}. {suggestion}\n"

        return TranslationPrompt(prompt=prompt, suggestions=suggestions)
    except Exception as e:
        logger.error(f"Error generating translation prompt: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate translation prompt",
        )


@app.get("/stammering", response_model=StammeringCheckResponse)
def stammering_check(
    source_sentence: str, translated_sentence: str
) -> StammeringCheckResponse:
    """
    API endpoint to check for stammering in a translated sentence.

    Args:
        source_sentence (str): The original sentence.
        translated_sentence (str): The translated sentence.

    Returns:
        StammeringCheckResponse: A boolean indicating if the sentence has stammering.
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


@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is running correctly.

    Returns:
        dict: Status information about the API.
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "database": "connected" if engine else "disconnected",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
