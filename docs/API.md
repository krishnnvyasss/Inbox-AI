# API

## POST `/api/ingest`

Uploads a conversation JSON export.

## POST `/api/retrieve`

Example:

```json
{
  "query": "What did I discuss about YOLO?",
  "top_k": 5
}
```

Returns semantically similar conversation chunks.

## POST `/api/rag-context`

Returns retrieved chunks formatted as context for an LLM.
