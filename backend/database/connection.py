"""
MongoDB connection manager using Motor (async driver).
Falls back gracefully if MongoDB is unavailable.
"""
import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

MONGODB_URI = os.getenv("MONGODB_URI", "")

_client: AsyncIOMotorClient | None = None
_db = None


async def connect_to_mongo():
    """Establish connection to MongoDB Atlas."""
    global _client, _db
    if not MONGODB_URI or MONGODB_URI.startswith("mongodb+srv://username"):
        logger.warning("MongoDB URI not configured. Using sample data fallback.")
        return None
    try:
        _client = AsyncIOMotorClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
        # Verify connection
        await _client.admin.command("ping")
        _db = _client.templeai
        logger.info("✅ Connected to MongoDB Atlas successfully.")
        return _db
    except Exception as e:
        logger.warning(f"⚠️ MongoDB connection failed: {e}. Using sample data fallback.")
        _client = None
        _db = None
        return None


async def close_mongo_connection():
    """Close MongoDB connection."""
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed.")


def get_database():
    """Get the database instance. Returns None if not connected."""
    return _db
