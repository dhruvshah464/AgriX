from __future__ import annotations

from pydantic import BaseModel


class AssistantQueryRequest(BaseModel):
    query: str


class AssistantQueryResponse(BaseModel):
    answer: str
    sources: list[str]
