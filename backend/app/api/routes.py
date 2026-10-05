import json
from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.services.rag_engine import ConversationRAG

router = APIRouter()
rag = ConversationRAG()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".json"):
        raise HTTPException(400, "Please upload an Inbox AI JSON export.")

    try:
        data = json.loads((await file.read()).decode("utf-8"))
    except Exception as exc:
        raise HTTPException(400, f"Invalid JSON: {exc}")

    if "conversation" not in data:
        raise HTTPException(400, "Invalid Inbox AI export format.")

    return {"ok": True, **rag.add_conversation(data)}


@router.post("/retrieve")
def retrieve(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(400, "Query cannot be empty.")

    top_k = max(1, min(request.top_k, 20))
    results = rag.search(request.query, top_k)

    return {
        "query": request.query,
        "count": len(results),
        "results": results,
    }


@router.post("/rag-context")
def rag_context(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(400, "Query cannot be empty.")

    top_k = max(1, min(request.top_k, 20))
    results = rag.search(request.query, top_k)

    return {
        "query": request.query,
        "context": rag.build_rag_context(request.query, top_k),
        "sources": results,
    }
