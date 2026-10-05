from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Inbox AI API",
    description="Backend API for conversation ingestion and semantic retrieval.",
    version="1.0.0",
)

app.include_router(router, prefix="/api")


@app.get("/health")
def health():
    return {"status": "ok"}
