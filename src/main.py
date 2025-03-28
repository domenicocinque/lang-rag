from fastapi import FastAPI
import uvicorn
import logging

from src.routes import router
from src.core.config import settings

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Rag Translation Service API",
)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
