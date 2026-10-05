# Inbox AI Architecture

## High-level architecture

```text
┌───────────────────────────────────────────┐
│              Chrome Extension             │
│                                           │
│ Content Scripts → Capture → Storage/UI    │
└──────────────────────┬────────────────────┘
                       │ JSON
                       ▼
┌───────────────────────────────────────────┐
│                 FastAPI                    │
│              backend/app                  │
│                                           │
│  API Routes → Models → RAG Service        │
└──────────────────────┬────────────────────┘
                       │
                       ▼
┌───────────────────────────────────────────┐
│                RAG Engine                 │
│                                           │
│ Chunking → Embeddings → Vector Search    │
└──────────────────────┬────────────────────┘
                       │
                       ▼
             Relevant Context
                       │
                       ▼
              Optional LLM Layer
