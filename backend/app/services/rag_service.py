from __future__ import annotations

from backend.app.core.config import settings
from backend.app.schemas.assistant import AssistantQueryResponse
from rag_assistant.chatbot.assistant import ask_assistant


class RagService:
    def query(self, text: str) -> AssistantQueryResponse:
        answer, sources = ask_assistant(
            query=text,
            provider=settings.LLM_PROVIDER,
            model_name=settings.LLM_MODEL,
            api_key=settings.OPENAI_API_KEY,
            index_dir=settings.VECTOR_DB_PATH,
        )
        return AssistantQueryResponse(answer=answer, sources=sources)
