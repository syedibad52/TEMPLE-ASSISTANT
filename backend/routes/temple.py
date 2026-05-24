"""
Temple information API routes — temple status, pooja timings, festivals, etc.
"""
import logging
from fastapi import APIRouter, HTTPException
from services.temple_service import (
    get_temple_status,
    get_pooja_schedules,
    get_special_poojas,
    get_festivals,
    get_announcements,
    get_temple_info,
    get_prasada_timings,
    get_parking_info,
    get_donations_info,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/api/temple-status")
async def temple_status():
    """Get current temple status (open/closed) and current/next pooja info."""
    try:
        status = await get_temple_status()
        return status
    except Exception as e:
        logger.error(f"Temple status error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get temple status")


@router.get("/api/temple-info")
async def temple_info():
    """Get temple basic information."""
    try:
        info = await get_temple_info()
        return info
    except Exception as e:
        logger.error(f"Temple info error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get temple info")


@router.get("/api/pooja-timings")
async def pooja_timings():
    """Get daily pooja schedule."""
    try:
        schedules = await get_pooja_schedules()
        special = await get_special_poojas()
        return {
            "daily": schedules,
            "special": special,
        }
    except Exception as e:
        logger.error(f"Pooja timings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get pooja timings")


@router.get("/api/festivals")
async def festivals():
    """Get upcoming festivals."""
    try:
        festival_list = await get_festivals()
        return {"festivals": festival_list}
    except Exception as e:
        logger.error(f"Festivals error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get festivals")


@router.get("/api/announcements")
async def announcements():
    """Get active announcements."""
    try:
        announcement_list = await get_announcements()
        return {"announcements": announcement_list}
    except Exception as e:
        logger.error(f"Announcements error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get announcements")


@router.get("/api/prasada-timings")
async def prasada_timings():
    """Get prasada distribution timings."""
    try:
        timings = await get_prasada_timings()
        return timings
    except Exception as e:
        logger.error(f"Prasada timings error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get prasada timings")


@router.get("/api/parking")
async def parking():
    """Get parking information."""
    try:
        info = await get_parking_info()
        return info
    except Exception as e:
        logger.error(f"Parking info error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get parking info")


@router.get("/api/donations")
async def donations():
    """Get donation categories and bank details."""
    try:
        info = await get_donations_info()
        return info
    except Exception as e:
        logger.error(f"Donations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get donation info")
