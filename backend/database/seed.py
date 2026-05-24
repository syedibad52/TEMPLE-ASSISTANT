"""
Database seed script — populates MongoDB with sample temple data.
Run: python -m database.seed
"""
import asyncio
import json
import logging
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_database():
    """Seed MongoDB with sample temple data."""
    uri = os.getenv("MONGODB_URI", "")
    if not uri or uri.startswith("mongodb+srv://username"):
        logger.error("Please set a valid MONGODB_URI in your .env file")
        return

    # Load sample data
    data_path = Path(__file__).parent.parent / "data" / "sample_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Connect to MongoDB
    client = AsyncIOMotorClient(uri)
    db = client.templeai

    try:
        # Seed temple info
        await db.templeInfo.delete_many({})
        await db.templeInfo.insert_one(data["temple"])
        logger.info("✅ Seeded templeInfo")

        # Seed pooja schedules
        await db.poojaSchedules.delete_many({})
        if data.get("pooja_schedules"):
            await db.poojaSchedules.insert_many(data["pooja_schedules"])
        logger.info(f"✅ Seeded {len(data.get('pooja_schedules', []))} pooja schedules")

        # Seed special poojas
        await db.specialPoojas.delete_many({})
        if data.get("special_poojas"):
            await db.specialPoojas.insert_many(data["special_poojas"])
        logger.info(f"✅ Seeded {len(data.get('special_poojas', []))} special poojas")

        # Seed festivals
        await db.festivals.delete_many({})
        if data.get("festivals"):
            await db.festivals.insert_many(data["festivals"])
        logger.info(f"✅ Seeded {len(data.get('festivals', []))} festivals")

        # Seed announcements
        await db.announcements.delete_many({})
        if data.get("announcements"):
            await db.announcements.insert_many(data["announcements"])
        logger.info(f"✅ Seeded {len(data.get('announcements', []))} announcements")

        logger.info("🛕 Database seeding complete!")

    except Exception as e:
        logger.error(f"Seeding failed: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
