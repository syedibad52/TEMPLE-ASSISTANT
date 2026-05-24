"""
Chat API route — handles AI-powered temple assistant conversations.
"""
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from services.ai_service import generate_chat_response

logger = logging.getLogger(__name__)
router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = Field(default="auto")
    conversation_history: Optional[List[dict]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    response: str
    language: str


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return an AI-generated response.
    The AI uses temple context data to answer questions accurately.
    """
    try:
        # Sanitize input
        message = request.message.strip()
        if not message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        # Validate language
        valid_langs = {"auto", "en", "kn"}
        language = request.language if request.language in valid_langs else "auto"

        # Generate AI response
        result = await generate_chat_response(
            message=message,
            language=language,
            conversation_history=request.conversation_history or [],
        )

        return ChatResponse(
            response=result["response"],
            language=result["language"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process your request. Please try again.")
