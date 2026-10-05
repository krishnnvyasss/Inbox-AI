from app.services.rag_engine import ConversationRAG


def test_chunking():
    chunks = ConversationRAG._chunk_text("hello " * 500)
    assert len(chunks) > 1
