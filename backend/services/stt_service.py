"""
Speech-to-Text service — OpenAI Whisper API integration.
Supports Kannada and English with auto language detection.
"""
import os
import io
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_") else None


async def transcribe_audio(audio_bytes: bytes, filename: str = "audio.webm") -> dict:
    """
    Transcribe audio using OpenAI Whisper API.
    
    Args:
        audio_bytes: Raw audio bytes from the browser MediaRecorder
        filename: Original filename (used for format detection)
    
    Returns:
        dict with 'text', 'language', and optional 'confidence'
    """
    if not client:
        return {
            "text": "",
            "language": "en",
            "error": "Speech-to-text service is not configured. Please set your OpenAI API key.",
        }

    try:
        # Create a file-like object from bytes
        audio_file = io.BytesIO(audio_bytes)
        audio_file.name = filename  # Whisper needs a filename to detect format

        # Call Whisper API with auto language detection
        response = await client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",  # Get language detection info
        )

        text = response.text.strip()
        detected_language = getattr(response, 'language', 'en')

        # Map Whisper language codes to our codes
        lang_map = {
            'kannada': 'kn',
            'english': 'en',
            'kn': 'kn',
            'en': 'en',
        }
        language = lang_map.get(detected_language.lower() if detected_language else 'en', 'en')

        logger.info(f"Whisper transcription: lang={language}, text={text[:100]}...")

        return {
            "text": text,
            "language": language,
        }

    except Exception as e:
        logger.error(f"Whisper API error: {e}")
        return {
            "text": "",
            "language": "en",
            "error": f"Speech recognition failed: {str(e)}",
        }
