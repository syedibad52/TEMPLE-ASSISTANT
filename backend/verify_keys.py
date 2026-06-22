"""Verify all API keys are valid by making minimal test calls."""
import os
import sys
import asyncio
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
load_dotenv()


async def verify_groq():
    """Test the Groq/OpenAI API key."""
    from openai import AsyncOpenAI

    api_key = os.getenv("OPENAI_API_KEY", "")
    base_url = os.getenv("OPENAI_BASE_URL", None)
    model = os.getenv("AI_MODEL", "gpt-4o-mini")

    if not api_key or api_key.startswith("your_"):
        print("[FAIL] GROQ/OPENAI: No API key set")
        return

    kwargs = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    provider = "Groq" if base_url and "groq" in base_url else "OpenAI"
    print(f"[....] Testing {provider} Chat (model={model})...")
    client = AsyncOpenAI(**kwargs)

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say hello in one word"}],
            max_tokens=10,
        )
        reply = response.choices[0].message.content.strip()
        print(f"[PASS] {provider} CHAT: Working! Response: \"{reply}\"")
    except Exception as e:
        print(f"[FAIL] {provider} CHAT: Failed -- {e}")


async def verify_stt():
    """Check STT config."""
    stt_model = os.getenv("STT_MODEL", "whisper-1")
    base_url = os.getenv("OPENAI_BASE_URL", None)
    if base_url and "groq" in base_url:
        print(f"[PASS] GROQ STT: Model '{stt_model}' configured (will work when audio is sent)")
    else:
        print(f"[INFO] STT: Model '{stt_model}' configured (OpenAI Whisper)")


async def verify_elevenlabs():
    """Test ElevenLabs API key using direct HTTP call."""
    import httpx

    api_key = os.getenv("ELEVENLABS_API_KEY", "")
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "") or "21m00Tcm4TlvDq8ikWAM"

    if not api_key or api_key.startswith("your_"):
        print("[FAIL] ELEVENLABS: No API key set")
        return

    print(f"[....] Testing ElevenLabs (voice_id={voice_id})...")
    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key,
        }
        payload = {
            "text": "Hello",
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            print(f"[PASS] ELEVENLABS: Working! Generated {len(response.content)} bytes of audio")
        elif response.status_code == 401:
            print(f"[FAIL] ELEVENLABS: Invalid API key (401 Unauthorized)")
        else:
            print(f"[FAIL] ELEVENLABS: HTTP {response.status_code} -- {response.text[:200]}")
    except Exception as e:
        print(f"[FAIL] ELEVENLABS: Failed -- {e}")


async def main():
    print("=" * 50)
    print("TempleAI -- API Key Verification")
    print("=" * 50)
    print()
    await verify_groq()
    print()
    await verify_stt()
    print()
    await verify_elevenlabs()
    print()
    print("=" * 50)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
