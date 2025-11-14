"""
Database Models for Phoenix Filter Bot
Using MongoDB with Motor (async driver)
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class User(BaseModel):
    """User model for tracking bot users"""
    
    user_id: int = Field(..., description="Telegram user ID")
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_premium: bool = False
    premium_until: Optional[datetime] = None
    referrer_id: Optional[int] = None
    referral_count: int = 0
    is_banned: bool = False
    joined_at: datetime = Field(default_factory=datetime.utcnow)
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123456789,
                "username": "example_user",
                "first_name": "John",
                "last_name": "Doe",
                "is_premium": False,
                "premium_until": None,
                "referrer_id": None,
                "referral_count": 0,
                "is_banned": False,
                "joined_at": "2024-01-01T00:00:00",
                "last_seen": "2024-01-01T12:00:00",
            }
        }


class File(BaseModel):
    """File model for indexed media files"""
    
    file_id: str = Field(..., description="Telegram file ID")
    file_name: str
    file_type: str  # video, document, audio, photo, etc.
    file_size: int
    mime_type: Optional[str] = None
    channel_id: int
    message_id: int
    custom_name: Optional[str] = None
    caption: Optional[str] = None
    thumbnail: Optional[str] = None
    duration: Optional[int] = None  # For videos/audio
    indexed_at: datetime = Field(default_factory=datetime.utcnow)
    download_count: int = 0
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "AgADBAADr6cxG...",
                "file_name": "movie.mp4",
                "file_type": "video",
                "file_size": 1024000,
                "mime_type": "video/mp4",
                "channel_id": -1002458488257,
                "message_id": 12345,
                "custom_name": "Superman (2013)",
                "caption": "High quality movie",
                "thumbnail": None,
                "duration": 7200,
                "indexed_at": "2024-01-01T00:00:00",
                "download_count": 0,
            }
        }


class Filter(BaseModel):
    """Filter model for manual filters"""
    
    filter_id: str = Field(..., description="Unique filter ID")
    chat_id: int
    keyword: str
    file_ids: List[str] = []
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_global: bool = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "filter_id": "filter_123",
                "chat_id": -1001234567890,
                "keyword": "Superman",
                "file_ids": ["AgADBAADr6cxG...", "AgADBAADr6cxH..."],
                "created_by": 123456789,
                "created_at": "2024-01-01T00:00:00",
                "is_global": False,
            }
        }


class Premium(BaseModel):
    """Premium membership model"""
    
    user_id: int = Field(..., description="Telegram user ID")
    plan_type: str  # basic, standard, premium
    purchase_date: datetime = Field(default_factory=datetime.utcnow)
    expiry_date: datetime
    is_active: bool = True
    purchase_price: Optional[float] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 123456789,
                "plan_type": "premium",
                "purchase_date": "2024-01-01T00:00:00",
                "expiry_date": "2024-02-01T00:00:00",
                "is_active": True,
                "purchase_price": 9.99,
            }
        }


class FSub(BaseModel):
    """Force Subscribe model for tracking dynamic FSub channels"""
    
    chat_id: int = Field(..., description="Group/channel ID")
    channel_id: int = Field(..., description="Force Subscribe channel ID")
    added_by: int
    added_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "chat_id": -1001234567890,
                "channel_id": -1002533961050,
                "added_by": 123456789,
                "added_at": "2024-01-01T00:00:00",
            }
        }


class Log(BaseModel):
    """Activity log model"""
    
    log_id: str = Field(..., description="Unique log ID")
    user_id: Optional[int] = None
    action: str  # search, download, join, etc.
    details: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "log_id": "log_123",
                "user_id": 123456789,
                "action": "search",
                "details": "Searched for 'Superman'",
                "timestamp": "2024-01-01T12:00:00",
            }
        }
