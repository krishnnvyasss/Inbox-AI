# Inbox AI Backend

FastAPI backend responsible for conversation ingestion and semantic retrieval.

## Structure

```text
backend/
├── app/
│   ├── api/          # HTTP routes
│   ├── core/         # configuration
│   ├── models/       # request/response schemas
│   ├── services/     # RAG business logic
│   └── main.py       # FastAPI entry point
├── tests/
└── requirements.txt
```

## Run

```bash
cd backend
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## RAG pipeline

```text
JSON conversation
      ↓
Normalization
      ↓
Overlapping chunks
      ↓
Sentence Transformer embeddings
      ↓
Local vector index
      ↓
Cosine similarity
      ↓
Top-K context
```
