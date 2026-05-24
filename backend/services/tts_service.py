"""
Text-to-Speech service — ElevenLabs API integration.
Supports multilingual voice generation for Kannada and English.
"""
import os
import io
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")

_client = None


def _get_client():
    """Lazy-initialize ElevenLabs client."""
    global _client
    if _client is None and ELEVENLABS_API_KEY and not ELEVENLABS_API_KEY.startswith("your_"):
        try:
            from elevenlabs.client import ElevenLabs
            _client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize ElevenLabs client: {e}")
    return _client


async def generate_speech(text: str, language: str = "en") -> bytes | None:
    """
    Generate speech audio from text using ElevenLabs API.
    
    Args:
        text: Text to convert to speech
        language: Language code ('en' or 'kn')
    
    Returns:
        Audio bytes (MP3) or None if service unavailable
    """
    client = _get_client()
    if not client:
        logger.warning("ElevenLabs not configured. TTS unavailable.")
        return None

    try:
        # Use multilingual model for Kannada support
        model_id = "eleven_multilingual_v2"
        
        # Use configured voice or default
        voice_id = ELEVENLABS_VOICE_ID if ELEVENLABS_VOICE_ID and not ELEVENLABS_VOICE_ID.startswith("your_") else "21m00Tcm4TlvDq8ikWAM"  # Rachel (default)

        # Generate audio
        audio_generator = client.generate(
            text=text,
            voice=voice_id,
            model=model_id,
        )

        # Collect audio bytes from generator
        audio_chunks = []
        for chunk in audio_generator:
            audio_chunks.append(chunk)
        
        audio_bytes = b"".join(audio_chunks)
        
        logger.info(f"Generated TTS audio: {len(audio_bytes)} bytes, lang={language}")
        return audio_bytes

    except Exception as e:
        logger.error(f"ElevenLabs TTS error: {e}")
        return None
