from pydantic import BaseModel, Field, constr
from typing import Optional, Dict, Any, List


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: constr(strip_whitespace=True, min_length=1)  # type: ignore
    persona: Optional[str] = Field(
        default=None, description="Persona style (e.g., Tutor, Therapist)"
    )
    history: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Chat history for context"
    )


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    response: str
    model: str
    usage: Dict[str, Any] = {}
    persona_applied: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    model: str
