# RAG Assistant Pipeline

## Steps
1. Load agronomy knowledge docs from `datasets/external/agri_knowledge.txt`
2. Create embeddings via SentenceTransformers (with deterministic fallback)
3. Build FAISS index (fallback to numpy vectors)
4. Retrieve top-k relevant context
5. Generate answer via OpenAI (or fallback response)

## Modules
- Embeddings: `rag_assistant/embeddings/build_embeddings.py`
- Indexing: `rag_assistant/vector_db/index_manager.py`
- Retrieval: `rag_assistant/vector_db/retriever.py`
- Assistant: `rag_assistant/chatbot/assistant.py`
