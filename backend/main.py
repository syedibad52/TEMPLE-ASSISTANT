"""
TempleAI Voice Assistant — FastAPI Backend
==========================================
Main application entry point.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv

from database.connection import connect_to_mongo, close_mongo_connection
from routes.chat import router as chat_router
from routes.speech import router as speech_router
from routes.temple import router as temple_router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Rate Limiter ──────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ── App Lifespan ──────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    logger.info("🛕 Starting TempleAI Backend...")
    await connect_to_mongo()
    logger.info("🛕 TempleAI Backend is ready!")
    yield
    logger.info("🛕 Shutting down TempleAI Backend...")
    await close_mongo_connection()


# ── Create FastAPI App ────────────────────────────────
app = FastAPI(
    title="TempleAI Voice Assistant API",
    description="AI-powered temple guide with bilingual (Kannada + English) voice support",
    version="1.0.0",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS — allow frontend access
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Global Error Handler ─────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


# ── Mount Routes ─────────────────────────────────────
app.include_router(chat_router, tags=["Chat"])
app.include_router(speech_router, tags=["Speech"])
app.include_router(temple_router, tags=["Temple"])


# ── Health Check ─────────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "TempleAI Voice Assistant API",
        "version": "1.0.0",
    }


@app.get("/api/health", tags=["Health"])
async def api_health():
    return {
        "status": "healthy",
        "openai_configured": bool(os.getenv("OPENAI_API_KEY", "").strip() and not os.getenv("OPENAI_API_KEY", "").startswith("your_")),
        "elevenlabs_configured": bool(os.getenv("ELEVENLABS_API_KEY", "").strip() and not os.getenv("ELEVENLABS_API_KEY", "").startswith("your_")),
        "mongodb_configured": bool(os.getenv("MONGODB_URI", "").strip() and not os.getenv("MONGODB_URI", "").startswith("mongodb+srv://username")),
    }


# ── Run ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
