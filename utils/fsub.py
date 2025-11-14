"""
Force Subscribe Manager for Phoenix Filter Bot
Handles Force Subscribe logic and verification
"""

import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from pyrogram import Client
from pyrogram.errors import UserNotParticipant
from config import FORCE_SUB_CHANNEL

logger = logging.getLogger(__name__)


class FSubManager:
    """Manager for Force Subscribe functionality"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.fsub_collection = db.fsub_channels
    
    async def add_fsub_channel(self, chat_id: int, channel_id: int, added_by: int) -> bool:
        """
        Add a Force Subscribe channel to a group
        
        Args:
            chat_id: Group/channel ID
            channel_id: Force Subscribe channel ID
            added_by: Admin user ID who added it
        
        Returns:
            True if successful, False otherwise
        """
        try:
            await self.fsub_collection.insert_one({
                "chat_id": chat_id,
                "channel_id": channel_id,
                "added_by": added_by,
                "added_at": datetime.utcnow(),
            })
            logger.info(f"Added FSub channel {channel_id} to group {chat_id}")
            return True
        except Exception as e:
            logger.error(f"Error adding FSub channel: {e}")
            return False
    
    async def remove_fsub_channel(self, chat_id: int, channel_id: int) -> bool:
        """Remove a Force Subscribe channel from a group"""
        try:
            result = await self.fsub_collection.delete_one({
                "chat_id": chat_id,
                "channel_id": channel_id,
            })
            if result.deleted_count > 0:
                logger.info(f"Removed FSub channel {channel_id} from group {chat_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing FSub channel: {e}")
            return False
    
    async def get_fsub_channels(self, chat_id: int) -> List[int]:
        """Get all Force Subscribe channels for a group"""
        try:
            channels = await self.fsub_collection.find({"chat_id": chat_id}).to_list(length=None)
            return [ch["channel_id"] for ch in channels]
        except Exception as e:
            logger.error(f"Error getting FSub channels: {e}")
            return []
    
    async def verify_fsub(self, client: Client, user_id: int, chat_id: int) -> bool:
        """
        Verify if user has joined all required Force Subscribe channels
        
        Args:
            client: Pyrogram client
            user_id: User's Telegram ID
            chat_id: Group/channel ID
        
        Returns:
            True if user has joined all required channels, False otherwise
        """
        try:
            # Check primary mandatory channel
            if not await self._check_membership(client, user_id, FORCE_SUB_CHANNEL):
                return False
            
            # Check dynamic FSub channels for this group
            fsub_channels = await self.get_fsub_channels(chat_id)
            for channel_id in fsub_channels:
                if not await self._check_membership(client, user_id, channel_id):
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Error verifying FSub: {e}")
            return False
    
    async def _check_membership(self, client: Client, user_id: int, channel_id: int) -> bool:
        """Check if user is a member of a channel"""
        try:
            await client.get_chat_member(channel_id, user_id)
            return True
        except UserNotParticipant:
            return False
        except Exception as e:
            logger.error(f"Error checking membership: {e}")
            return False
    
    async def get_missing_fsub_channels(self, client: Client, user_id: int, chat_id: int) -> List[int]:
        """Get list of channels the user hasn't joined"""
        try:
            missing = []
            
            # Check primary mandatory channel
            if not await self._check_membership(client, user_id, FORCE_SUB_CHANNEL):
                missing.append(FORCE_SUB_CHANNEL)
            
            # Check dynamic FSub channels
            fsub_channels = await self.get_fsub_channels(chat_id)
            for channel_id in fsub_channels:
                if not await self._check_membership(client, user_id, channel_id):
                    missing.append(channel_id)
            
            return missing
        except Exception as e:
            logger.error(f"Error getting missing FSub channels: {e}")
            return []


from datetime import datetime
