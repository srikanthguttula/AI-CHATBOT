from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict

from APP.config import settings
from APP.schemas import ChatRequest, ChatResponse, HealthResponse
from APP.services.llm_service import chat_completion

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS (optional: adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok", "model": settings.openai_model}


@app.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat(body: ChatRequest) -> ChatResponse:
    """Chat endpoint that sends user input to the LLM."""
    try:
        result = await chat_completion(body.message, body.persona, body.history)
        return ChatResponse(**result)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to generate response")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
