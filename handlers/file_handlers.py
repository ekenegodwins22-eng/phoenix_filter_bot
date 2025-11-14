"""
File management handlers for Phoenix Filter Bot
Handles file renaming, captions, thumbnails, and streaming
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import RENAME_ENABLED, STREAM_ENABLED
from utils.helpers import log_activity
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


# Store temporary rename context
rename_context = {}


async def handle_rename_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /rename command - Rename a file"""
    if not RENAME_ENABLED:
        await message.reply_text("❌ Rename feature is currently disabled")
        return
    
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file to rename it")
        return
    
    # Store context for next message
    rename_context[message.from_user.id] = {
        "message_id": message.reply_to_message.id,
        "chat_id": message.chat.id,
    }
    
    await message.reply_text(
        "📝 **Rename File**\n\n"
        "Send the new name for this file:"
    )


async def handle_set_caption_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /set_caption command - Add caption to file"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("Usage: /set_caption <caption_text>")
        return
    
    caption = args[1]
    
    try:
        result = await db.files.update_one(
            {"file_id": file_id},
            {"$set": {"caption": caption}}
        )
        
        if result.modified_count > 0:
            await message.reply_text(f"✅ Caption updated:\n\n{caption}")
            await log_activity(db, message.from_user.id, "set_caption", f"Set caption for file {file_id}")
        else:
            await message.reply_text("❌ File not found in database")
    
    except Exception as e:
        logger.error(f"Error setting caption: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_see_caption_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /see_caption command - View file caption"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    try:
        file = await db.files.find_one({"file_id": file_id})
        
        if file and file.get("caption"):
            await message.reply_text(f"📝 **Caption:**\n\n{file['caption']}")
        else:
            await message.reply_text("❌ No caption set for this file")
    
    except Exception as e:
        logger.error(f"Error viewing caption: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_del_caption_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /del_caption command - Delete file caption"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    try:
        result = await db.files.update_one(
            {"file_id": file_id},
            {"$set": {"caption": None}}
        )
        
        if result.modified_count > 0:
            await message.reply_text("✅ Caption deleted")
            await log_activity(db, message.from_user.id, "del_caption", f"Deleted caption for file {file_id}")
        else:
            await message.reply_text("❌ File not found")
    
    except Exception as e:
        logger.error(f"Error deleting caption: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_stream_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /stream command - Generate stream and download links"""
    if not STREAM_ENABLED:
        await message.reply_text("❌ Streaming feature is currently disabled")
        return
    
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    try:
        file_msg = message.reply_to_message
        file_id = file_msg.media.file_id if hasattr(file_msg.media, 'file_id') else None
        file_name = file_msg.media.file_name if hasattr(file_msg.media, 'file_name') else "file"
        
        if not file_id:
            await message.reply_text("❌ Could not get file ID")
            return
        
        # Generate stream link (placeholder - would integrate with actual streaming service)
        stream_link = f"https://stream.example.com/file/{file_id}"
        download_link = f"https://download.example.com/file/{file_id}"
        
        stream_text = f"""
🎬 **Stream Links**

📄 File: {file_name}

🎥 Stream Link:
`{stream_link}`

📥 Download Link:
`{download_link}`

**Players Supported:**
• VLC Media Player
• MX Player
• Telegram
• Browser
"""
        
        await message.reply_text(stream_text)
        await log_activity(db, message.from_user.id, "stream", f"Generated stream for {file_name}")
        
    except Exception as e:
        logger.error(f"Error generating stream: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_set_thumb_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /set_thumb command - Set thumbnail for file"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    if not message.media or not message.media.photo:
        await message.reply_text("❌ Please send a photo as thumbnail")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    thumb_file_id = message.media.photo.file_id
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    try:
        result = await db.files.update_one(
            {"file_id": file_id},
            {"$set": {"thumbnail": thumb_file_id}}
        )
        
        if result.modified_count > 0:
            await message.reply_text("✅ Thumbnail set successfully")
            await log_activity(db, message.from_user.id, "set_thumb", f"Set thumbnail for file {file_id}")
        else:
            await message.reply_text("❌ File not found")
    
    except Exception as e:
        logger.error(f"Error setting thumbnail: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_view_thumb_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /view_thumb command - View file thumbnail"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    try:
        file = await db.files.find_one({"file_id": file_id})
        
        if file and file.get("thumbnail"):
            await client.send_photo(message.chat.id, file["thumbnail"])
        else:
            await message.reply_text("❌ No thumbnail set for this file")
    
    except Exception as e:
        logger.error(f"Error viewing thumbnail: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_del_thumb_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /del_thumb command - Delete file thumbnail"""
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply_text("❌ Please reply to a media file")
        return
    
    file_id = message.reply_to_message.media.file_id if hasattr(message.reply_to_message.media, 'file_id') else None
    
    if not file_id:
        await message.reply_text("❌ Could not get file ID")
        return
    
    try:
        result = await db.files.update_one(
            {"file_id": file_id},
            {"$set": {"thumbnail": None}}
        )
        
        if result.modified_count > 0:
            await message.reply_text("✅ Thumbnail deleted")
            await log_activity(db, message.from_user.id, "del_thumb", f"Deleted thumbnail for file {file_id}")
        else:
            await message.reply_text("❌ File not found")
    
    except Exception as e:
        logger.error(f"Error deleting thumbnail: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


def setup_file_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup file management handlers"""
    
    @client.on_message(filters.command("rename"))
    async def rename_cmd(client: Client, message: Message):
        await handle_rename_command(client, message, db)
    
    @client.on_message(filters.command("set_caption"))
    async def set_caption_cmd(client: Client, message: Message):
        await handle_set_caption_command(client, message, db)
    
    @client.on_message(filters.command("see_caption"))
    async def see_caption_cmd(client: Client, message: Message):
        await handle_see_caption_command(client, message, db)
    
    @client.on_message(filters.command("del_caption"))
    async def del_caption_cmd(client: Client, message: Message):
        await handle_del_caption_command(client, message, db)
    
    @client.on_message(filters.command("stream"))
    async def stream_cmd(client: Client, message: Message):
        await handle_stream_command(client, message, db)
    
    @client.on_message(filters.command("set_thumb"))
    async def set_thumb_cmd(client: Client, message: Message):
        await handle_set_thumb_command(client, message, db)
    
    @client.on_message(filters.command("view_thumb"))
    async def view_thumb_cmd(client: Client, message: Message):
        await handle_view_thumb_command(client, message, db)
    
    @client.on_message(filters.command("del_thumb"))
    async def del_thumb_cmd(client: Client, message: Message):
        await handle_del_thumb_command(client, message, db)
    
    logger.info("✅ File handlers setup complete")
