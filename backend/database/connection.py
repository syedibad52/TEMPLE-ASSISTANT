"""SQLite async connection using `databases` and SQLAlchemy.

Defines the tables used by the application and exposes `database` for
async access. Uses `DATABASE_URL` environment variable or falls back to
`sqlite:///./temple.db` for local development.
"""
import os
import logging
import databases
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./temple.db")

# Async database object used throughout the app
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Tables
temple_info = sqlalchemy.Table(
    "temple_info",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("data", sqlalchemy.JSON),
)

pooja_schedules = sqlalchemy.Table(
    "pooja_schedules",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("name_kn", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column("end_time", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("description_kn", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
)

special_poojas = sqlalchemy.Table(
    "special_poojas",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("name_kn", sqlalchemy.String),
    sqlalchemy.Column("day", sqlalchemy.String),
    sqlalchemy.Column("time", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("description_kn", sqlalchemy.String),
)

festivals = sqlalchemy.Table(
    "festivals",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("name_kn", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("duration", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("description_kn", sqlalchemy.String),
    sqlalchemy.Column("is_upcoming", sqlalchemy.Boolean, default=True),
)

announcements = sqlalchemy.Table(
    "announcements",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("title_kn", sqlalchemy.String),
    sqlalchemy.Column("message", sqlalchemy.String),
    sqlalchemy.Column("message_kn", sqlalchemy.String),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("type", sqlalchemy.String),
    sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
)

# A lightweight key/value table for misc JSON blobs (donations, parking, timings)
meta = sqlalchemy.Table(
    "meta",
    metadata,
    sqlalchemy.Column("key", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("value", sqlalchemy.JSON),
)


async def connect_to_db():
    """Create tables (if needed) and connect the async database."""
    try:
        # check_same_thread is SQLite-specific; omit it for other databases
        connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
        engine = sqlalchemy.create_engine(DATABASE_URL, connect_args=connect_args)
        metadata.create_all(engine)
        await database.connect()
        logger.info("✅ Connected to local SQL database.")
    except Exception as e:
        logger.error(f"Failed to initialize SQL database: {e}")


async def close_db():
    """Disconnect the async database."""
    try:
        await database.disconnect()
        logger.info("SQL database disconnected.")
    except Exception:
        pass


def get_database():
    """Return the async `database` object for queries."""
    return database
