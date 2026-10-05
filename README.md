# Inbox AI

> A Chrome extension for capturing, organizing and semantically searching AI conversations across ChatGPT, Gemini and Claude.

## Project structure

```text
InboxAI/
│
├── extension/                 # Chrome extension
│   ├── manifest.json
│   ├── content scripts
│   ├── popup / dashboard
│   └── assets
│
├── backend/                   # Python/FastAPI backend
│   ├── app/
│   │   ├── api/               # REST endpoints
│   │   ├── core/              # configuration
│   │   ├── models/            # data schemas
│   │   ├── services/          # RAG engine
│   │   └── main.py
│   ├── tests/
│   └── requirements.txt
│
├── docs/                      # Architecture & API documentation
│
└── README.md
```

## AI / RAG pipeline

```text
ChatGPT / Gemini / Claude
          ↓
     Chrome Extension
          ↓
       JSON Export
          ↓
     FastAPI Backend
          ↓
   Text Chunking
          ↓
 Sentence Transformer
     Embeddings
          ↓
   Vector Similarity
          ↓
    Top-K Retrieval
          ↓
    RAG Context
          ↓
       LLM*
```

`*` The retrieval layer works without an LLM API key. An LLM can be connected later for answer generation.

## Main technologies

- JavaScript
- Chrome Extension APIs
- Python
- FastAPI
- Sentence Transformers
- NumPy
- Semantic Search
- RAG
- Vector Embeddings

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [API](docs/API.md)
- [Backend](backend/README.md)

## Security note

Local conversation data and generated vector indexes should not be committed to Git.
