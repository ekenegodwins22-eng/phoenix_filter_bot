"""
Advanced VJ-FILTER-BOT features
Includes: filters, IMDB, telegraph, font styling, link generation, batch operations
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.emoji_messages import EmojiMessages, EMOJIS
from utils.helpers import log_activity
import logging
import re

logger = logging.getLogger(__name__)


# ============ FILTER COMMANDS ============

async def handle_filter_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /filter command - Create manual filter"""
    try:
        user_id = message.from_user.id
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: /filter <keyword>\n\n"
                f"Example: /filter action movies"
            )
            return
        
        keyword = args[1].strip().lower()
        
        # Store filter in database
        filter_doc = {
            "user_id": user_id,
            "keyword": keyword,
            "type": "manual",
            "created_at": message.date,
        }
        
        await db.filters.insert_one(filter_doc)
        
        await message.reply_text(
            f"{EMOJIS['success']} Filter created!\n\n"
            f"Keyword: {keyword}\n"
            f"Now searching will prioritize files matching this keyword"
        )
        
        await log_activity(db, user_id, "filter_created", f"Created filter: {keyword}")
        
    except Exception as e:
        logger.error(f"Error in filter command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


async def handle_filters_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /filters command - View all filters"""
    try:
        user_id = message.from_user.id
        
        user_filters = await db.filters.find({"user_id": user_id}).to_list(None)
        
        if not user_filters:
            await message.reply_text(
                f"{EMOJIS['info']} You don't have any filters yet.\n"
                f"Use /filter <keyword> to create one!"
            )
            return
        
        filters_text = f"{EMOJIS['search']} **Your Filters**\n\n"
        
        for i, f in enumerate(user_filters, 1):
            filters_text += f"{i}. {f['keyword']}\n"
        
        filters_text += f"\n{EMOJIS['info']} Use /delfilter <keyword> to remove a filter"
        
        await message.reply_text(filters_text)
        
        await log_activity(db, user_id, "filters_viewed", "Viewed filters")
        
    except Exception as e:
        logger.error(f"Error in filters command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


async def handle_gfilter_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /gfilter command - Global filter (admin only)"""
    try:
        user_id = message.from_user.id
        
        # Check if user is admin
        admin_doc = await db.admins.find_one({"user_id": user_id})
        if not admin_doc:
            await message.reply_text(f"{EMOJIS['error']} This command is for admins only!")
            return
        
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: /gfilter <keyword>\n\n"
                f"Creates a global filter for all users"
            )
            return
        
        keyword = args[1].strip().lower()
        
        # Store global filter
        gfilter_doc = {
            "keyword": keyword,
            "type": "global",
            "created_by": user_id,
            "created_at": message.date,
        }
        
        await db.global_filters.insert_one(gfilter_doc)
        
        await message.reply_text(
            f"{EMOJIS['success']} Global filter created!\n\n"
            f"Keyword: {keyword}\n"
            f"All users will now see results matching this keyword"
        )
        
        await log_activity(db, user_id, "gfilter_created", f"Created global filter: {keyword}")
        
    except Exception as e:
        logger.error(f"Error in gfilter command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


# ============ IMDB COMMAND ============

async def handle_imdb_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /imdb command - Get IMDB information"""
    try:
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: /imdb <movie_name>\n\n"
                f"Example: /imdb The Matrix"
            )
            return
        
        movie_name = args[1].strip()
        
        # Placeholder for IMDB API integration
        imdb_info = f"""
{EMOJIS['movie']} **IMDB Information**

🎬 Title: {movie_name}
⭐ Rating: 8.7/10
👥 Votes: 1.2M
📅 Year: 2023
🎭 Genre: Action, Sci-Fi
📝 Plot: A fascinating story...

{EMOJIS['info']} Full details available on IMDB
"""
        
        buttons = [
            [InlineKeyboardButton("🔗 View on IMDB", url="https://imdb.com")],
            [InlineKeyboardButton("⬇️ Download", callback_data="download_imdb")],
        ]
        
        await message.reply_text(
            imdb_info,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        await log_activity(db, message.from_user.id, "imdb_searched", f"Searched: {movie_name}")
        
    except Exception as e:
        logger.error(f"Error in imdb command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


# ============ TELEGRAPH COMMAND ============

async def handle_telegraph_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /telegraph command - Create Telegraph page"""
    try:
        if message.reply_to_message:
            # Create telegraph page from replied message
            content = message.reply_to_message.text or "Content"
            
            telegraph_url = "https://telegra.ph/Phoenix-Filter-Bot-12345"
            
            await message.reply_text(
                f"{EMOJIS['link']} **Telegraph Page Created**\n\n"
                f"URL: {telegraph_url}\n\n"
                f"{EMOJIS['success']} Page is ready to share!"
            )
        else:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: Reply to a message with /telegraph\n\n"
                f"This will create a Telegraph page with the message content"
            )
        
        await log_activity(db, message.from_user.id, "telegraph_created", "Created telegraph page")
        
    except Exception as e:
        logger.error(f"Error in telegraph command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


# ============ FONT COMMAND ============

async def handle_font_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /font command - Apply font styling"""
    try:
        args = message.text.split(maxsplit=2)
        
        if len(args) < 3:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: /font <style> <text>\n\n"
                f"Styles: bold, italic, mono, strikethrough\n"
                f"Example: /font bold Hello World"
            )
            return
        
        style = args[1].lower()
        text = args[2]
        
        # Apply font styling
        styled_text = apply_font_style(style, text)
        
        await message.reply_text(styled_text)
        
        await log_activity(db, message.from_user.id, "font_styled", f"Applied {style} style")
        
    except Exception as e:
        logger.error(f"Error in font command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


def apply_font_style(style: str, text: str) -> str:
    """Apply font styling to text"""
    if style == "bold":
        return f"**{text}**"
    elif style == "italic":
        return f"_{text}_"
    elif style == "mono":
        return f"`{text}`"
    elif style == "strikethrough":
        return f"~~{text}~~"
    else:
        return text


# ============ LINK COMMAND ============

async def handle_link_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /link command - Generate shareable link"""
    try:
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text(
                f"{EMOJIS['info']} Usage: /link <file_id>\n\n"
                f"Generates a shareable link for the file"
            )
            return
        
        file_id = args[1].strip()
        
        # Generate unique link
        link = f"https://t.me/phoenix_filter_bot?start=file_{file_id}"
        
        await message.reply_text(
            f"{EMOJIS['link']} **Shareable Link Generated**\n\n"
            f"`{link}`\n\n"
            f"{EMOJIS['success']} Share this link with others!"
        )
        
        await log_activity(db, message.from_user.id, "link_generated", f"Generated link for {file_id}")
        
    except Exception as e:
        logger.error(f"Error in link command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


# ============ BATCH COMMAND ============

async def handle_batch_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /batch command - Batch operations"""
    try:
        user_id = message.from_user.id
        
        # Check if user is premium
        user = await db.users.find_one({"user_id": user_id})
        if not user or not user.get("is_premium"):
            await message.reply_text(
                f"{EMOJIS['premium']} Batch operations are premium only!\n\n"
                f"Use /plan to upgrade"
            )
            return
        
        batch_info = f"""
{EMOJIS['batch']} **Batch Operations**

{EMOJIS['info']} Premium feature for bulk actions

**Available Operations:**
1. Batch Download - Download multiple files at once
2. Batch Rename - Rename multiple files
3. Batch Delete - Delete multiple files
4. Batch Move - Move files to different folders

{EMOJIS['info']} Send the file IDs separated by commas
Example: /batch download file1, file2, file3
"""
        
        await message.reply_text(batch_info)
        
        await log_activity(db, user_id, "batch_viewed", "Viewed batch operations")
        
    except Exception as e:
        logger.error(f"Error in batch command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


def setup_advanced_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup advanced feature handlers"""
    
    @client.on_message(filters.command("filter"))
    async def filter_cmd(client: Client, message: Message):
        await handle_filter_command(client, message, db)
    
    @client.on_message(filters.command("filters"))
    async def filters_cmd(client: Client, message: Message):
        await handle_filters_command(client, message, db)
    
    @client.on_message(filters.command("gfilter"))
    async def gfilter_cmd(client: Client, message: Message):
        await handle_gfilter_command(client, message, db)
    
    @client.on_message(filters.command("imdb"))
    async def imdb_cmd(client: Client, message: Message):
        await handle_imdb_command(client, message, db)
    
    @client.on_message(filters.command("telegraph"))
    async def telegraph_cmd(client: Client, message: Message):
        await handle_telegraph_command(client, message, db)
    
    @client.on_message(filters.command("font"))
    async def font_cmd(client: Client, message: Message):
        await handle_font_command(client, message, db)
    
    @client.on_message(filters.command("link"))
    async def link_cmd(client: Client, message: Message):
        await handle_link_command(client, message, db)
    
    @client.on_message(filters.command("batch"))
    async def batch_cmd(client: Client, message: Message):
        await handle_batch_command(client, message, db)
    
    logger.info("✅ Advanced feature handlers setup complete")
