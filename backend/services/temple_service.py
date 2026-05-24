"""
Temple data service — fetches temple information from MongoDB or falls back to sample JSON.
Computes live temple status based on current time.
"""
import json
import os
import logging
from datetime import datetime, time
from pathlib import Path
from database.connection import get_database

logger = logging.getLogger(__name__)

# Load sample data as fallback
SAMPLE_DATA_PATH = Path(__file__).parent.parent / "data" / "sample_data.json"
_sample_data: dict = {}


def _load_sample_data() -> dict:
    """Load sample temple data from JSON file."""
    global _sample_data
    if not _sample_data:
        try:
            with open(SAMPLE_DATA_PATH, "r", encoding="utf-8") as f:
                _sample_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load sample data: {e}")
            _sample_data = {}
    return _sample_data


async def get_temple_info() -> dict:
    """Get temple basic info."""
    db = get_database()
    if db:
        try:
            info = await db.templeInfo.find_one({}, {"_id": 0})
            if info:
                return info
        except Exception as e:
            logger.warning(f"DB fetch failed for temple info: {e}")
    data = _load_sample_data()
    return data.get("temple", {})


async def get_pooja_schedules() -> list:
    """Get daily pooja schedules."""
    db = get_database()
    if db:
        try:
            cursor = db.poojaSchedules.find({}, {"_id": 0}).sort("time", 1)
            schedules = await cursor.to_list(length=50)
            if schedules:
                return schedules
        except Exception as e:
            logger.warning(f"DB fetch failed for pooja schedules: {e}")
    data = _load_sample_data()
    return data.get("pooja_schedules", [])


async def get_special_poojas() -> list:
    """Get special pooja schedules."""
    db = get_database()
    if db:
        try:
            cursor = db.specialPoojas.find({}, {"_id": 0})
            poojas = await cursor.to_list(length=50)
            if poojas:
                return poojas
        except Exception as e:
            logger.warning(f"DB fetch failed for special poojas: {e}")
    data = _load_sample_data()
    return data.get("special_poojas", [])


async def get_festivals() -> list:
    """Get upcoming festivals."""
    db = get_database()
    if db:
        try:
            cursor = db.festivals.find({"is_upcoming": True}, {"_id": 0})
            festivals = await cursor.to_list(length=50)
            if festivals:
                return festivals
        except Exception as e:
            logger.warning(f"DB fetch failed for festivals: {e}")
    data = _load_sample_data()
    return data.get("festivals", [])


async def get_announcements() -> list:
    """Get active announcements."""
    db = get_database()
    if db:
        try:
            cursor = db.announcements.find({"active": True}, {"_id": 0})
            announcements = await cursor.to_list(length=50)
            if announcements:
                return announcements
        except Exception as e:
            logger.warning(f"DB fetch failed for announcements: {e}")
    data = _load_sample_data()
    return [a for a in data.get("announcements", []) if a.get("active")]


async def get_donations_info() -> dict:
    """Get donation categories and bank details."""
    data = _load_sample_data()
    return data.get("donations", {})


async def get_parking_info() -> dict:
    """Get parking availability info."""
    data = _load_sample_data()
    return data.get("parking", {})


async def get_prasada_timings() -> dict:
    """Get prasada distribution timings."""
    data = _load_sample_data()
    return data.get("prasada_timings", {})


def _parse_time(time_str: str) -> time:
    """Parse HH:MM time string."""
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))


async def get_temple_status() -> dict:
    """Compute live temple status based on current time (IST)."""
    data = _load_sample_data()
    timings = data.get("timings", {})
    schedules = data.get("pooja_schedules", [])

    now = datetime.now()
    current_time = now.time()

    opening = _parse_time(timings.get("opening_time", "05:00"))
    closing = _parse_time(timings.get("closing_time", "21:00"))
    break_start = _parse_time(timings.get("morning_break_start", "12:30"))
    break_end = _parse_time(timings.get("morning_break_end", "16:00"))

    # Determine if temple is open
    is_open = False
    if opening <= current_time <= closing:
        if break_start <= current_time <= break_end:
            is_open = False
        else:
            is_open = True

    # Status text
    if is_open:
        status_text = "OPEN"
        status_text_kn = "ತೆರೆದಿದೆ"
    elif break_start <= current_time <= break_end:
        status_text = "CLOSED (Afternoon Break)"
        status_text_kn = "ಮುಚ್ಚಿದೆ (ಮಧ್ಯಾಹ್ನದ ವಿರಾಮ)"
    else:
        status_text = "CLOSED"
        status_text_kn = "ಮುಚ್ಚಿದೆ"

    # Find current and next pooja
    current_pooja = None
    current_pooja_kn = None
    next_pooja = None
    next_pooja_kn = None
    next_pooja_time = None

    for schedule in schedules:
        if schedule.get("type") == "break":
            continue
        pooja_start = _parse_time(schedule["time"])
        pooja_end = _parse_time(schedule["end_time"])
        if pooja_start <= current_time <= pooja_end:
            current_pooja = schedule["name"]
            current_pooja_kn = schedule.get("name_kn", schedule["name"])
        elif current_time < pooja_start and next_pooja is None:
            next_pooja = schedule["name"]
            next_pooja_kn = schedule.get("name_kn", schedule["name"])
            next_pooja_time = schedule["time"]

    return {
        "is_open": is_open,
        "status_text": status_text,
        "status_text_kn": status_text_kn,
        "current_pooja": current_pooja,
        "current_pooja_kn": current_pooja_kn,
        "next_pooja": next_pooja,
        "next_pooja_kn": next_pooja_kn,
        "next_pooja_time": next_pooja_time,
        "opening_time": timings.get("opening_time", "05:00"),
        "closing_time": timings.get("closing_time", "21:00"),
    }


async def build_temple_context() -> str:
    """
    Build a text context string with all temple information for the AI prompt.
    This is injected into the GPT system message so the AI has full temple knowledge.
    """
    info = await get_temple_info()
    status = await get_temple_status()
    schedules = await get_pooja_schedules()
    special = await get_special_poojas()
    festivals = await get_festivals()
    prasada = await get_prasada_timings()
    parking = await get_parking_info()
    donations = await get_donations_info()
    announcements = await get_announcements()
    data = _load_sample_data()
    timings = data.get("timings", {})

    context_parts = []

    # Temple Info
    context_parts.append(f"TEMPLE NAME: {info.get('name', 'N/A')}")
    context_parts.append(f"TEMPLE NAME (Kannada): {info.get('name_kn', 'N/A')}")
    context_parts.append(f"ADDRESS: {info.get('address', 'N/A')}")
    context_parts.append(f"PHONE: {info.get('phone', 'N/A')}")
    context_parts.append(f"EMAIL: {info.get('email', 'N/A')}")

    # Current Status
    context_parts.append(f"\nCURRENT TEMPLE STATUS: {status['status_text']} ({status['status_text_kn']})")
    if status.get("current_pooja"):
        context_parts.append(f"CURRENT POOJA: {status['current_pooja']} ({status.get('current_pooja_kn', '')})")
    if status.get("next_pooja"):
        context_parts.append(f"NEXT POOJA: {status['next_pooja']} ({status.get('next_pooja_kn', '')}) at {status['next_pooja_time']}")

    # Timings
    context_parts.append(f"\nTEMPLE TIMINGS:")
    context_parts.append(f"  Opening: {timings.get('opening_time', '05:00')}")
    context_parts.append(f"  Closing: {timings.get('closing_time', '21:00')}")
    context_parts.append(f"  Afternoon Break: {timings.get('morning_break_start', '12:30')} - {timings.get('morning_break_end', '16:00')}")
    darshan = timings.get("darshan_timings", {})
    if darshan:
        general = darshan.get("general", {})
        context_parts.append(f"  General Darshan: Morning {general.get('morning', 'N/A')}, Evening {general.get('evening', 'N/A')}")

    # Daily Poojas
    context_parts.append(f"\nDAILY POOJA SCHEDULE:")
    for s in schedules:
        if s.get("type") != "break":
            context_parts.append(f"  {s['time']} - {s['end_time']}: {s['name']} ({s.get('name_kn', '')})")

    # Special Poojas
    if special:
        context_parts.append(f"\nSPECIAL POOJAS:")
        for sp in special:
            context_parts.append(f"  {sp['day']}: {sp['name']} ({sp.get('name_kn', '')}) at {sp['time']}")

    # Festivals
    if festivals:
        context_parts.append(f"\nUPCOMING FESTIVALS:")
        for f in festivals:
            context_parts.append(f"  {f['name']} ({f.get('name_kn', '')}) — {f['date']} ({f['duration']})")

    # Prasada
    if prasada:
        context_parts.append(f"\nPRASADA TIMINGS:")
        morning = prasada.get("morning", {})
        evening = prasada.get("evening", {})
        if morning:
            context_parts.append(f"  Morning: {morning.get('time', 'N/A')} — {', '.join(morning.get('items', []))}")
        if evening:
            context_parts.append(f"  Evening: {evening.get('time', 'N/A')} — {', '.join(evening.get('items', []))}")

    # Parking
    if parking:
        context_parts.append(f"\nPARKING:")
        context_parts.append(f"  Available: {'Yes' if parking.get('available') else 'No'}")
        context_parts.append(f"  Two-wheeler: {parking.get('two_wheeler', 'N/A')}, Four-wheeler: {parking.get('four_wheeler', 'N/A')}")

    # Donations
    if donations:
        context_parts.append(f"\nDONATION CATEGORIES:")
        for cat in donations.get("categories", []):
            context_parts.append(f"  {cat['name']} — Min ₹{cat['min_amount']}")

    # Announcements
    if announcements:
        context_parts.append(f"\nANNOUNCEMENTS:")
        for a in announcements:
            context_parts.append(f"  {a['title']}: {a['message']}")

    return "\n".join(context_parts)
