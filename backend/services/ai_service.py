"""
AI service — OpenAI GPT integration for temple assistant chat.
"""
import os
import logging
from openai import AsyncOpenAI
from dotenv import load_dotenv
from services.temple_service import build_temple_context

load_dotenv()
logger = logging.getLogger(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
TEMPLE_NAME = os.getenv("TEMPLE_NAME", "Sri Raghavendra Swamy Temple")

client = AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY and not OPENAI_API_KEY.startswith("your_") else None

SYSTEM_PROMPT_TEMPLATE = """You are a respectful AI Temple Assistant for {temple_name}.

CRITICAL RULES:
1. You speak politely and spiritually at all times.
2. You MUST detect whether the user is speaking in Kannada or English.
3. You MUST reply in the SAME language the user used. If they speak Kannada, reply in Kannada. If English, reply in English.
4. Keep answers short, clear, and helpful (2-4 sentences max).
5. NEVER generate fake temple timings or information. Only use the data provided below.
6. If information is not available, politely say: "Please contact the temple office for this information." (or Kannada equivalent)
7. You are knowledgeable about Hindu temple customs, rituals, and traditions.
8. Always be warm and welcoming, like a friendly temple guide.
9. Use respectful greetings appropriate to the context (e.g., "Namaskara", "ನಮಸ್ಕಾರ").
10. When providing timings, be specific and accurate based on the data below.

CURRENT TEMPLE INFORMATION:
{temple_context}

Remember: You represent this sacred temple. Be respectful, accurate, and helpful."""


async def generate_chat_response(
    message: str,
    language: str = "auto",
    conversation_history: list = None,
) -> dict:
    """
    Generate AI response for a temple-related query.
    
    Args:
        message: User's question
        language: Detected language ('en', 'kn', or 'auto')
        conversation_history: Previous conversation messages
    
    Returns:
        dict with 'response' and 'language'
    """
    if not client:
        # Fallback response when API key is not configured
        return _fallback_response(message, language)

    try:
        # Build temple context
        temple_context = await build_temple_context()
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            temple_name=TEMPLE_NAME,
            temple_context=temple_context,
        )

        # Build messages
        messages = [{"role": "system", "content": system_prompt}]

        # Add conversation history (last 10 messages)
        if conversation_history:
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                })

        # Add current message
        if language != "auto":
            lang_hint = "Kannada" if language == "kn" else "English"
            messages.append({
                "role": "user",
                "content": f"[User is speaking in {lang_hint}] {message}",
            })
        else:
            messages.append({"role": "user", "content": message})

        # Call GPT
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500,
        )

        reply = response.choices[0].message.content.strip()

        # Detect response language
        detected_lang = _detect_language(reply)

        return {
            "response": reply,
            "language": detected_lang,
        }

    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return _fallback_response(message, language)


def _detect_language(text: str) -> str:
    """Simple heuristic to detect if text is Kannada or English."""
    kannada_chars = sum(1 for c in text if '\u0C80' <= c <= '\u0CFF')
    total_alpha = sum(1 for c in text if c.isalpha())
    if total_alpha == 0:
        return "en"
    ratio = kannada_chars / total_alpha
    return "kn" if ratio > 0.3 else "en"


def _fallback_response(message: str, language: str) -> dict:
    """Provide a fallback response when OpenAI is not available."""
    detected = _detect_language(message) if language == "auto" else language

    if detected == "kn":
        return {
            "response": "ನಮಸ್ಕಾರ! AI ಸೇವೆ ಪ್ರಸ್ತುತ ಲಭ್ಯವಿಲ್ಲ. ದಯವಿಟ್ಟು ದೇವಸ್ಥಾನದ ಕಚೇರಿಯನ್ನು ಸಂಪರ್ಕಿಸಿ ಅಥವಾ ನಂತರ ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
            "language": "kn",
        }
    else:
        return {
            "response": "Namaskara! The AI service is currently unavailable. Please contact the temple office or try again later.",
            "language": "en",
        }
