"""
Message filters for Phoenix Filter Bot
Handles filtering logic for different message types
"""

from pyrogram import filters
from pyrogram.types import Message
from config import ADMINS, PM_SEARCH_ENABLED
import logging

logger = logging.getLogger(__name__)


def is_admin(client, message: Message) -> bool:
    """Check if user is an admin"""
    return message.from_user.id in ADMINS


def is_private_chat(client, message: Message) -> bool:
    """Check if message is from private chat"""
    return message.chat.type == "private"


def is_group_chat(client, message: Message) -> bool:
    """Check if message is from group"""
    return message.chat.type in ["group", "supergroup"]


def is_search_query(client, message: Message) -> bool:
    """Check if message is a search query (not a command)"""
    if not message.text:
        return False
    
    # If it starts with /, it's a command, not a search
    if message.text.startswith("/"):
        return False
    
    return True


def setup_filters(client):
    """Setup all message filters"""
    
    # Create custom filters
    admin_filter = filters.create(is_admin)
    private_filter = filters.create(is_private_chat)
    group_filter = filters.create(is_group_chat)
    search_filter = filters.create(is_search_query)
    
    logger.info("✅ Message filters setup complete")
    
    return {
        "admin": admin_filter,
        "private": private_filter,
        "group": group_filter,
        "search": search_filter,
    }
