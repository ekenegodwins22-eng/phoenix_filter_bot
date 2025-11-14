"""
Admin command handlers for Phoenix Filter Bot
Handles admin-only operations
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, OWNER_ID
from utils.helpers import log_activity, format_user_info
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


async def handle_users_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /users command - List all users"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    try:
        users = await db.users.find({}).to_list(length=None)
        total_users = len(users)
        premium_users = len([u for u in users if u.get("is_premium")])
        banned_users = len([u for u in users if u.get("is_banned")])
        
        stats_text = f"""
👥 **User Statistics**

📊 Total Users: {total_users}
💎 Premium Users: {premium_users}
🚫 Banned Users: {banned_users}

**Recent Users:**
"""
        
        # Show last 5 users
        recent_users = sorted(users, key=lambda x: x.get("last_seen", ""), reverse=True)[:5]
        for user in recent_users:
            stats_text += f"\n• {user.get('first_name', 'Unknown')} (@{user.get('username', 'N/A')}) - ID: {user['user_id']}"
        
        await message.reply_text(stats_text)
        await log_activity(db, message.from_user.id, "view_users", f"Viewed {total_users} users")
        
    except Exception as e:
        logger.error(f"Error in users command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_ban_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /ban command - Ban a user"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /ban <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_banned": True}}
        )
        
        if result.modified_count > 0:
            await message.reply_text(f"✅ User {user_id} has been banned")
            await log_activity(db, message.from_user.id, "ban_user", f"Banned user {user_id}")
        else:
            await message.reply_text(f"❌ User {user_id} not found")
    
    except ValueError:
        await message.reply_text("❌ Invalid user ID")
    except Exception as e:
        logger.error(f"Error in ban command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_unban_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /unban command - Unban a user"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /unban <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {"$set": {"is_banned": False}}
        )
        
        if result.modified_count > 0:
            await message.reply_text(f"✅ User {user_id} has been unbanned")
            await log_activity(db, message.from_user.id, "unban_user", f"Unbanned user {user_id}")
        else:
            await message.reply_text(f"❌ User {user_id} not found")
    
    except ValueError:
        await message.reply_text("❌ Invalid user ID")
    except Exception as e:
        logger.error(f"Error in unban command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_broadcast_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /broadcast command - Send message to all users"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    # Get message to broadcast
    if not message.reply_to_message:
        await message.reply_text("❌ Please reply to the message you want to broadcast")
        return
    
    broadcast_msg = message.reply_to_message
    status_msg = await message.reply_text("📢 Starting broadcast...")
    
    try:
        users = await db.users.find({"is_banned": False}).to_list(length=None)
        
        success_count = 0
        failed_count = 0
        
        for user in users:
            try:
                await broadcast_msg.copy(user["user_id"])
                success_count += 1
            except:
                failed_count += 1
        
        await status_msg.edit_text(
            f"✅ **Broadcast Complete**\n\n"
            f"✅ Sent: {success_count}\n"
            f"❌ Failed: {failed_count}"
        )
        
        await log_activity(db, message.from_user.id, "broadcast", f"Sent to {success_count} users")
        
    except Exception as e:
        logger.error(f"Error in broadcast command: {e}")
        await status_msg.edit_text(f"❌ Error: {str(e)}")


async def handle_fsub_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /fsub command - Add Force Subscribe channel"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /fsub <channel_username_or_id>")
        return
    
    channel_input = args[1]
    
    try:
        # Try to get the channel
        if channel_input.startswith("@"):
            channel = await client.get_chat(channel_input)
        else:
            channel = await client.get_chat(int(channel_input))
        
        # Add to database
        await db.fsub_channels.insert_one({
            "chat_id": message.chat.id,
            "channel_id": channel.id,
            "added_by": message.from_user.id,
            "added_at": __import__('datetime').datetime.utcnow(),
        })
        
        await message.reply_text(
            f"✅ **Force Subscribe Added**\n\n"
            f"Channel: {channel.title}\n"
            f"Users must join this channel to access files"
        )
        
        await log_activity(db, message.from_user.id, "add_fsub", f"Added {channel.title}")
        
    except Exception as e:
        logger.error(f"Error in fsub command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_nofsub_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /nofsub command - Remove Force Subscribe channel"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /nofsub <channel_username_or_id>")
        return
    
    channel_input = args[1]
    
    try:
        # Try to get the channel
        if channel_input.startswith("@"):
            channel = await client.get_chat(channel_input)
        else:
            channel = await client.get_chat(int(channel_input))
        
        # Remove from database
        result = await db.fsub_channels.delete_one({
            "chat_id": message.chat.id,
            "channel_id": channel.id,
        })
        
        if result.deleted_count > 0:
            await message.reply_text(f"✅ Force Subscribe removed for {channel.title}")
            await log_activity(db, message.from_user.id, "remove_fsub", f"Removed {channel.title}")
        else:
            await message.reply_text(f"❌ Force Subscribe not found for this channel")
    
    except Exception as e:
        logger.error(f"Error in nofsub command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


def setup_admin_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup admin command handlers"""
    
    @client.on_message(filters.command("users"))
    async def users_cmd(client: Client, message: Message):
        await handle_users_command(client, message, db)
    
    @client.on_message(filters.command("ban"))
    async def ban_cmd(client: Client, message: Message):
        await handle_ban_command(client, message, db)
    
    @client.on_message(filters.command("unban"))
    async def unban_cmd(client: Client, message: Message):
        await handle_unban_command(client, message, db)
    
    @client.on_message(filters.command("broadcast"))
    async def broadcast_cmd(client: Client, message: Message):
        await handle_broadcast_command(client, message, db)
    
    @client.on_message(filters.command("fsub"))
    async def fsub_cmd(client: Client, message: Message):
        await handle_fsub_command(client, message, db)
    
    @client.on_message(filters.command("nofsub"))
    async def nofsub_cmd(client: Client, message: Message):
        await handle_nofsub_command(client, message, db)
    
    logger.info("✅ Admin handlers setup complete")
