"""
Database Schemas for Avang Platform

Each Pydantic model maps to a MongoDB collection using the lowercase class name.
Examples:
- Video -> "video"
- Show -> "show"
- Genre -> "genre"
- LiveChannel -> "livechannel"
- EventTicket -> "eventticket"
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class LiveChannel(BaseModel):
    name: str = Field(..., description="Channel name")
    stream_url: HttpUrl = Field(..., description="HLS/DASH or embed URL for live stream")
    thumbnail: Optional[HttpUrl] = Field(None, description="Preview image URL")
    description: Optional[str] = None

class Video(BaseModel):
    title: str
    artist: str
    thumbnail: Optional[HttpUrl] = None
    video_url: HttpUrl
    genre: Optional[str] = None
    release_date: Optional[str] = Field(None, description="ISO date string")

class Show(BaseModel):
    title: str
    synopsis: Optional[str] = None
    schedule: Optional[str] = Field(None, description="e.g., Fridays 8pm GMT")
    poster: Optional[HttpUrl] = None
    stream_url: Optional[HttpUrl] = None

class Genre(BaseModel):
    name: str
    description: Optional[str] = None
    cover: Optional[HttpUrl] = None

class EventTicket(BaseModel):
    event_id: str
    event_name: str
    date: str
    price_matic: float = Field(..., ge=0)
    poster: Optional[HttpUrl] = None
    venue: Optional[str] = None

class PurchaseRequest(BaseModel):
    wallet_address: str = Field(..., description="Polygon wallet address (0x...)")
    event_id: str

class PurchaseResponse(BaseModel):
    status: str
    tx_hash: str
    network: str
    token_symbol: str
