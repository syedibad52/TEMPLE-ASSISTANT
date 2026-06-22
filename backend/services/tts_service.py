"""
Text-to-Speech service — ElevenLabs API integration (using direct HTTP).
Supports multilingual voice generation for Kannada and English.
Uses httpx instead of the elevenlabs SDK to avoid Windows long-path issues.
"""
import os
import logging
import httpx
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

# Default voice (Rachel) if no voice ID configured
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"


def _is_configured() -> bool:
    """Check if ElevenLabs is properly configured."""
    return bool(ELEVENLABS_API_KEY and not ELEVENLABS_API_KEY.startswith("your_"))


async def generate_speech(text: str, language: str = "en") -> bytes | None:
    """
    Generate speech audio from text using ElevenLabs API (direct HTTP).
    
    Args:
        text: Text to convert to speech
        language: Language code ('en' or 'kn')
    
    Returns:
        Audio bytes (MP3) or None if service unavailable
    """
    if not _is_configured():
        logger.warning("ElevenLabs not configured. TTS unavailable.")
        return None

    try:
        voice_id = ELEVENLABS_VOICE_ID if ELEVENLABS_VOICE_ID and not ELEVENLABS_VOICE_ID.startswith("your_") else DEFAULT_VOICE_ID
        url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY,
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
            },
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            logger.error(f"ElevenLabs API error {response.status_code}: {response.text[:200]}")
            return None

        audio_bytes = response.content
        logger.info(f"Generated TTS audio: {len(audio_bytes)} bytes, lang={language}")
        return audio_bytes

    except Exception as e:
        logger.error(f"ElevenLabs TTS error: {e}")
        return None
