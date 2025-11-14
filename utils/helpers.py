"""
Helper utilities for Phoenix Filter Bot
"""

import logging
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Optional

logger = logging.getLogger(__name__)


async def log_activity(
    db: AsyncIOMotorDatabase,
    user_id: Optional[int],
    action: str,
    details: Optional[str] = None
) -> bool:
    """
    Log an activity to the database
    
    Args:
        db: MongoDB database instance
        user_id: User's Telegram ID (optional)
        action: Action type (search, download, join, etc.)
        details: Additional details about the action
    
    Returns:
        True if successful, False otherwise
    """
    try:
        log_entry = {
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow(),
        }
        
        result = await db.logs.insert_one(log_entry)
        logger.debug(f"Logged activity: {action} by user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error logging activity: {e}")
        return False


def format_file_info(file_data: dict) -> str:
    """
    Format file information for display
    
    Args:
        file_data: File document from database
    
    Returns:
        Formatted string with file information
    """
    try:
        name = file_data.get("custom_name") or file_data.get("file_name", "Unknown")
        file_type = file_data.get("file_type", "unknown").upper()
        size_mb = file_data.get("file_size", 0) / (1024 * 1024)
        downloads = file_data.get("download_count", 0)
        
        info = f"""
📄 **{name}**
🏷️ Type: {file_type}
📊 Size: {size_mb:.2f} MB
⬇️ Downloads: {downloads}
"""
        
        if file_data.get("caption"):
            info += f"📝 {file_data.get('caption')}\n"
        
        return info.strip()
    except Exception as e:
        logger.error(f"Error formatting file info: {e}")
        return "File information unavailable"


def format_user_info(user_data: dict) -> str:
    """Format user information for display"""
    try:
        user_id = user_data.get("user_id", "Unknown")
        username = user_data.get("username", "Not set")
        is_premium = "✅ Yes" if user_data.get("is_premium") else "❌ No"
        joined_at = user_data.get("joined_at", "Unknown")
        
        info = f"""
👤 **User Information**
🆔 ID: {user_id}
📝 Username: @{username}
💎 Premium: {is_premium}
📅 Joined: {joined_at}
"""
        
        return info.strip()
    except Exception as e:
        logger.error(f"Error formatting user info: {e}")
        return "User information unavailable"


def get_file_size_readable(size_bytes: int) -> str:
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


def escape_markdown(text: str) -> str:
    """Escape special Markdown characters"""
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')
    return text
