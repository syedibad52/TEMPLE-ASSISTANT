"""Database seed script — populates local SQLite with sample temple data.
Run: python -m database.seed
"""
import asyncio
import json
import logging
from pathlib import Path
from dotenv import load_dotenv
import os

from database.connection import (
    database,
    temple_info,
    pooja_schedules,
    special_poojas,
    festivals,
    announcements,
    meta,
)

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_database():
    data_path = Path(__file__).parent.parent / "data" / "sample_data.json"
    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    await database.connect()
    try:
        # Clear tables
        await database.execute(temple_info.delete())
        await database.execute(pooja_schedules.delete())
        await database.execute(special_poojas.delete())
        await database.execute(festivals.delete())
        await database.execute(announcements.delete())
        await database.execute(meta.delete())

        # Insert temple info (single row)
        await database.execute(
            temple_info.insert().values(id=1, data=data.get("temple", {}))
        )

        # Insert pooja schedules
        for p in data.get("pooja_schedules", []):
            await database.execute(
                pooja_schedules.insert().values(
                    name=p.get("name"),
                    name_kn=p.get("name_kn"),
                    time=p.get("time"),
                    end_time=p.get("end_time"),
                    description=p.get("description"),
                    description_kn=p.get("description_kn"),
                    type=p.get("type"),
                )
            )

        # Insert special poojas
        for s in data.get("special_poojas", []):
            await database.execute(
                special_poojas.insert().values(
                    name=s.get("name"),
                    name_kn=s.get("name_kn"),
                    day=s.get("day"),
                    time=s.get("time"),
                    description=s.get("description"),
                    description_kn=s.get("description_kn"),
                )
            )

        # Insert festivals
        for f in data.get("festivals", []):
            await database.execute(
                festivals.insert().values(
                    name=f.get("name"),
                    name_kn=f.get("name_kn"),
                    date=f.get("date"),
                    duration=f.get("duration"),
                    description=f.get("description"),
                    description_kn=f.get("description_kn"),
                    is_upcoming=f.get("is_upcoming", True),
                )
            )

        # Insert announcements
        for a in data.get("announcements", []):
            await database.execute(
                announcements.insert().values(
                    title=a.get("title"),
                    title_kn=a.get("title_kn"),
                    message=a.get("message"),
                    message_kn=a.get("message_kn"),
                    date=a.get("date"),
                    type=a.get("type"),
                    active=a.get("active", True),
                )
            )

        # Insert meta JSON blobs (donations, parking, prasada_timings, timings)
        for key in ("donations", "parking", "prasada_timings", "timings"):
            if key in data:
                await database.execute(
                    meta.insert().values(key=key, value=data.get(key))
                )

        logger.info("🛕 Database seeding complete!")

    except Exception as e:
        logger.error(f"Seeding failed: {e}")
    finally:
        await database.disconnect()


if __name__ == "__main__":
    asyncio.run(seed_database())
