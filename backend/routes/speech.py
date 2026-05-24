"""
Speech API routes — handles speech-to-text and text-to-speech operations.
"""
import logging
from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import Response
from pydantic import BaseModel, Field
from typing import Optional
from services.stt_service import transcribe_audio
from services.tts_service import generate_speech

logger = logging.getLogger(__name__)
router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = Field(default="en")


class STTResponse(BaseModel):
    text: str
    language: str
    error: Optional[str] = None


@router.post("/api/speech-to-text", response_model=STTResponse)
async def speech_to_text(audio: UploadFile = File(...)):
    """
    Convert speech audio to text using OpenAI Whisper.
    Supports Kannada and English with auto language detection.
    Accepts audio files (webm, wav, mp3, m4a, ogg).
    """
    try:
        # Validate file type
        allowed_types = {
            "audio/webm", "audio/wav", "audio/mpeg", "audio/mp3",
            "audio/mp4", "audio/m4a", "audio/ogg", "audio/x-wav",
            "video/webm",  # Chrome sometimes sends webm as video
        }
        content_type = audio.content_type or ""
        # Be lenient with content type checking
        if content_type and content_type not in allowed_types and not content_type.startswith("audio/"):
            logger.warning(f"Unexpected content type: {content_type}, proceeding anyway")

        # Read audio data
        audio_bytes = await audio.read()
        if len(audio_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")

        # Max 25MB (Whisper API limit)
        if len(audio_bytes) > 25 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Audio file too large. Maximum 25MB.")

        # Determine filename for format detection
        filename = audio.filename or "audio.webm"

        # Transcribe
        result = await transcribe_audio(audio_bytes, filename)

        if result.get("error"):
            return STTResponse(text="", language="en", error=result["error"])

        return STTResponse(
            text=result["text"],
            language=result["language"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"STT endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Speech recognition failed. Please try again.")


@router.post("/api/text-to-speech")
async def text_to_speech(request: TTSRequest):
    """
    Convert text to speech audio using ElevenLabs.
    Returns MP3 audio bytes.
    """
    try:
        text = request.text.strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        language = request.language if request.language in {"en", "kn"} else "en"

        # Generate speech
        audio_bytes = await generate_speech(text, language)

        if audio_bytes is None:
            raise HTTPException(
                status_code=503,
                detail="Text-to-speech service is not available. Please configure your ElevenLabs API key.",
            )

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=response.mp3",
                "Cache-Control": "no-cache",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"TTS endpoint error: {e}")
        raise HTTPException(status_code=500, detail="Speech generation failed. Please try again.")
