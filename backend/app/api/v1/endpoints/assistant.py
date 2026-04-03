from fastapi import APIRouter

from backend.app.schemas.assistant import AssistantQueryRequest, AssistantQueryResponse
from backend.app.services.rag_service import RagService

router = APIRouter()
service = RagService()


@router.post("/query", response_model=AssistantQueryResponse)
def query(payload: AssistantQueryRequest) -> AssistantQueryResponse:
    return service.query(payload.query)
