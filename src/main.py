from fastapi import FastAPI
import uvicorn

from src.rag.router import router as rag_router
from src.stammering.router import router as stammer_router

app = FastAPI(
    title="Rag Translation Service API",
)
app.include_router(rag_router)
app.include_router(stammer_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
