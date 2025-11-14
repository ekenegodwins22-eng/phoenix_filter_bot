"""
Search handlers for Phoenix Filter Bot
Handles search queries and file delivery
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import SearchEngine, FSubManager
from utils.helpers import log_activity, format_file_info
from config import ADMINS, PM_SEARCH_ENABLED, FORCE_SUB_ENABLED
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


async def handle_search_query(
    client: Client,
    message: Message,
    db: AsyncIOMotorDatabase,
    search_engine: SearchEngine,
    fsub_manager: FSubManager
):
    """
    Handle search queries from users
    Supports both DM and group searches
    """
    query = message.text.strip()
    
    # Check if search is enabled for PM
    if message.chat.type == "private" and not PM_SEARCH_ENABLED:
        await message.reply_text("❌ Private message search is currently disabled.")
        return
    
    # Show searching indicator
    searching_msg = await message.reply_text(f"🔍 Searching for **{query}**...")
    
    try:
        # Perform search
        results = await search_engine.search(query, limit=10)
        
        if not results:
            await searching_msg.edit_text(f"❌ No results found for **{query}**")
            await log_activity(db, message.from_user.id, "search", f"Query: {query} (No results)")
            return
        
        # Check Force Subscribe if enabled
        if FORCE_SUB_ENABLED:
            missing_channels = await fsub_manager.get_missing_fsub_channels(
                client,
                message.from_user.id,
                message.chat.id
            )
            
            if missing_channels:
                # Create join buttons
                buttons = []
                for channel_id in missing_channels:
                    try:
                        channel = await client.get_chat(channel_id)
                        buttons.append([
                            InlineKeyboardButton(
                                f"Join {channel.title}",
                                url=f"https://t.me/{channel.username}" if channel.username else None
                            )
                        ])
                    except:
                        pass
                
                fsub_text = f"""
❌ **Access Denied**

You need to join the following channel(s) to access files:
"""
                
                await searching_msg.edit_text(
                    fsub_text,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                await log_activity(db, message.from_user.id, "fsub_required", f"Query: {query}")
                return
        
        # Format and send results
        results_text = f"🎬 **Search Results for: {query}**\n\n"
        
        for idx, file in enumerate(results[:5], 1):  # Show top 5 results
            results_text += f"{idx}. {format_file_info(file)}\n\n"
        
        # Create download buttons
        buttons = []
        for idx, file in enumerate(results[:5], 1):
            buttons.append([
                InlineKeyboardButton(
                    f"📥 Download #{idx}",
                    callback_data=f"download_{file['_id']}"
                )
            ])
        
        await searching_msg.edit_text(
            results_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        # Log search
        await log_activity(db, message.from_user.id, "search", f"Query: {query} ({len(results)} results)")
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        await searching_msg.edit_text("❌ An error occurred during search. Please try again.")


async def handle_index_command(
    client: Client,
    message: Message,
    db: AsyncIOMotorDatabase,
    search_engine: SearchEngine
):
    """Handle /index command - Index files from channel"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    # Get the channel to index
    channel_id = message.reply_to_message.chat.id if message.reply_to_message else None
    
    if not channel_id:
        await message.reply_text(
            "❌ Please reply to a message in the channel you want to index."
        )
        return
    
    indexing_msg = await message.reply_text("📑 Starting indexing process...")
    
    try:
        indexed_count = 0
        
        # Get all messages from channel
        async for msg in client.get_chat_history(channel_id):
            if msg.media:
                file_data = {
                    "file_id": msg.media.file_id if hasattr(msg.media, 'file_id') else None,
                    "file_name": msg.media.file_name if hasattr(msg.media, 'file_name') else "Unknown",
                    "file_type": msg.media.__class__.__name__.lower(),
                    "file_size": msg.media.file_size if hasattr(msg.media, 'file_size') else 0,
                    "mime_type": msg.media.mime_type if hasattr(msg.media, 'mime_type') else None,
                    "channel_id": channel_id,
                    "message_id": msg.id,
                    "caption": msg.caption or None,
                }
                
                if await search_engine.index_file(file_data):
                    indexed_count += 1
        
        await indexing_msg.edit_text(
            f"✅ **Indexing Complete**\n\n"
            f"📊 Files indexed: {indexed_count}"
        )
        
        await log_activity(db, message.from_user.id, "index", f"Indexed {indexed_count} files")
        
    except Exception as e:
        logger.error(f"Indexing error: {e}")
        await indexing_msg.edit_text(f"❌ Indexing failed: {str(e)}")


async def handle_delete_command(
    client: Client,
    message: Message,
    db: AsyncIOMotorDatabase,
    search_engine: SearchEngine
):
    """Handle /delete command - Delete a specific file from index"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    # Parse file ID from command
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /delete <file_id>")
        return
    
    file_id = args[1]
    
    try:
        result = await db.files.delete_one({"file_id": file_id})
        
        if result.deleted_count > 0:
            await message.reply_text(f"✅ File deleted successfully")
            await log_activity(db, message.from_user.id, "delete_file", f"File ID: {file_id}")
        else:
            await message.reply_text(f"❌ File not found")
    
    except Exception as e:
        logger.error(f"Delete error: {e}")
        await message.reply_text(f"❌ Error deleting file: {str(e)}")


def setup_search_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup search-related handlers"""
    
    search_engine = SearchEngine(db)
    fsub_manager = FSubManager(db)
    
    @client.on_message(filters.text & ~filters.command & filters.private)
    async def handle_pm_search(client: Client, message: Message):
        """Handle search queries in private messages"""
        await handle_search_query(client, message, db, search_engine, fsub_manager)
    
    @client.on_message(filters.command("index"))
    async def index_cmd(client: Client, message: Message):
        await handle_index_command(client, message, db, search_engine)
    
    @client.on_message(filters.command("delete"))
    async def delete_cmd(client: Client, message: Message):
        await handle_delete_command(client, message, db, search_engine)
    
    logger.info("✅ Search handlers setup complete")
    
    return search_engine, fsub_manager
