"""
Pydantic models / schemas for the TempleAI backend.
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# ── Chat ──────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = Field(default="auto", description="Language: 'en', 'kn', or 'auto'")
    conversation_history: Optional[List[dict]] = Field(default_factory=list)


class ChatResponse(BaseModel):
    response: str
    language: str
    temple_status: Optional[str] = None


# ── Speech ────────────────────────────────────────────
class STTResponse(BaseModel):
    text: str
    language: str
    confidence: Optional[float] = None


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = Field(default="en")


# ── Temple Data ──────────────────────────────────────
class PoojaSchedule(BaseModel):
    name: str
    name_kn: str
    time: str
    end_time: str
    description: str
    description_kn: str
    type: str  # "daily" | "break" | "special"


class SpecialPooja(BaseModel):
    name: str
    name_kn: str
    day: str
    time: str
    description: str
    description_kn: str


class Festival(BaseModel):
    name: str
    name_kn: str
    date: str
    duration: str
    description: str
    description_kn: str
    is_upcoming: bool = True


class DonationCategory(BaseModel):
    name: str
    name_kn: str
    description: str
    min_amount: int


class Announcement(BaseModel):
    title: str
    title_kn: str
    message: str
    message_kn: str
    date: str
    type: str  # "festival" | "general" | "urgent"
    active: bool = True


class TempleStatus(BaseModel):
    is_open: bool
    status_text: str
    status_text_kn: str
    current_pooja: Optional[str] = None
    current_pooja_kn: Optional[str] = None
    next_pooja: Optional[str] = None
    next_pooja_kn: Optional[str] = None
    next_pooja_time: Optional[str] = None
    opening_time: str
    closing_time: str
