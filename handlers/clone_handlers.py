"""
Bot cloning feature - Allow users to create their own bot instances
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from motor.motor_asyncio import AsyncIOMotorDatabase
from utils.emoji_messages import EmojiMessages, EMOJIS
from utils.helpers import log_activity
import secrets
import logging

logger = logging.getLogger(__name__)


async def handle_clone_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /clone command - Create bot clone"""
    try:
        user_id = message.from_user.id
        
        # Check if user already has a cloned bot
        existing_clone = await db.cloned_bots.find_one({"owner_id": user_id})
        if existing_clone:
            await message.reply_text(
                f"{EMOJIS['info']} You already have a cloned bot!\n\n"
                f"Bot Token: `{existing_clone['bot_token']}`\n"
                f"Created: {existing_clone['created_at']}\n\n"
                f"Use /clone_info to see more details"
            )
            return
        
        # Show clone information
        clone_info = f"""
{EMOJIS['bot']} **Create Your Own Phoenix Filter Bot Clone**

{EMOJIS['info']} Steps to create your clone:

1️⃣ Go to @BotFather on Telegram
2️⃣ Create a new bot with /newbot
3️⃣ Copy your bot token
4️⃣ Send me the token using:
   /clone_setup <your_bot_token>

{EMOJIS['warning']} Keep your bot token secret!
{EMOJIS['info']} Your clone will have all Phoenix features!

{EMOJIS['link']} Need help? Contact @ph0enix_web
"""
        
        buttons = [
            [InlineKeyboardButton("📖 BotFather Guide", url="https://t.me/BotFather")],
            [InlineKeyboardButton("❌ Cancel", callback_data="close")],
        ]
        
        await message.reply_text(
            clone_info,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        await log_activity(db, user_id, "clone_info_viewed", "Viewed clone information")
        
    except Exception as e:
        logger.error(f"Error in clone command: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


async def handle_clone_setup(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /clone_setup <token> - Setup cloned bot"""
    try:
        user_id = message.from_user.id
        args = message.text.split(maxsplit=1)
        
        if len(args) < 2:
            await message.reply_text(
                f"{EMOJIS['error']} Usage: /clone_setup <bot_token>\n\n"
                f"Example: /clone_setup 123456:ABC-DEF123456"
            )
            return
        
        bot_token = args[1].strip()
        
        # Validate token format
        if ":" not in bot_token:
            await message.reply_text(
                f"{EMOJIS['error']} Invalid bot token format!\n\n"
                f"Token should look like: 123456:ABC-DEF123456"
            )
            return
        
        # Check if token already exists
        existing = await db.cloned_bots.find_one({"bot_token": bot_token})
        if existing:
            await message.reply_text(
                f"{EMOJIS['error']} This bot token is already registered!"
            )
            return
        
        # Generate unique clone ID
        clone_id = secrets.token_hex(8)
        
        # Store clone configuration
        clone_config = {
            "clone_id": clone_id,
            "owner_id": user_id,
            "bot_token": bot_token,
            "created_at": message.date,
            "status": "active",
            "features": {
                "search": True,
                "download": True,
                "premium": True,
                "fsub": True,
                "admin": True,
            },
            "settings": {
                "prefix": "/",
                "language": "en",
                "timezone": "UTC",
            }
        }
        
        await db.cloned_bots.insert_one(clone_config)
        
        # Create success message
        success_msg = f"""
{EMOJIS['success']} **Clone Created Successfully!** {EMOJIS['success']}

{EMOJIS['bot']} Clone ID: `{clone_id}`
🔑 Bot Token: `{bot_token}`
{EMOJIS['rocket']} Status: Active

{EMOJIS['info']} Your clone is ready to use!

**Next Steps:**
1. Add your bot to a group/channel
2. Configure Force Subscribe with /fsub
3. Upload files to your file channel
4. Users can search and download!

{EMOJIS['link']} Support: @ph0enix_web
"""
        
        await message.reply_text(success_msg)
        
        # Log activity
        await log_activity(db, user_id, "bot_cloned", f"Created bot clone: {clone_id}")
        
    except Exception as e:
        logger.error(f"Error in clone setup: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


async def handle_clone_info(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /clone_info - Show clone information"""
    try:
        user_id = message.from_user.id
        
        clone = await db.cloned_bots.find_one({"owner_id": user_id})
        
        if not clone:
            await message.reply_text(
                f"{EMOJIS['info']} You don't have a cloned bot yet.\n"
                f"Use /clone to create one!"
            )
            return
        
        info_msg = f"""
{EMOJIS['bot']} **Your Clone Information**

{EMOJIS['info']} Clone ID: `{clone['clone_id']}`
🔑 Bot Token: `{clone['bot_token']}`
{EMOJIS['clock']} Created: {clone['created_at']}
{EMOJIS['success']} Status: {clone['status'].upper()}

**Features Enabled:**
✅ Search: {clone['features']['search']}
✅ Download: {clone['features']['download']}
✅ Premium: {clone['features']['premium']}
✅ Force Subscribe: {clone['features']['fsub']}
✅ Admin: {clone['features']['admin']}

**Settings:**
⚙️ Prefix: {clone['settings']['prefix']}
🌐 Language: {clone['settings']['language']}
🕐 Timezone: {clone['settings']['timezone']}

{EMOJIS['info']} Use /clone_update to modify settings
"""
        
        buttons = [
            [InlineKeyboardButton("⚙️ Update Settings", callback_data="clone_settings")],
            [InlineKeyboardButton("🗑️ Delete Clone", callback_data="clone_delete")],
        ]
        
        await message.reply_text(
            info_msg,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        
        await log_activity(db, user_id, "clone_info_viewed", "Viewed clone info")
        
    except Exception as e:
        logger.error(f"Error in clone info: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


async def handle_clone_delete(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /clone_delete - Delete cloned bot"""
    try:
        user_id = message.from_user.id
        
        clone = await db.cloned_bots.find_one({"owner_id": user_id})
        
        if not clone:
            await message.reply_text(
                f"{EMOJIS['error']} You don't have a cloned bot to delete!"
            )
            return
        
        # Delete the clone
        await db.cloned_bots.delete_one({"owner_id": user_id})
        
        await message.reply_text(
            f"{EMOJIS['success']} Your bot clone has been deleted!\n\n"
            f"Use /clone to create a new one."
        )
        
        await log_activity(db, user_id, "bot_clone_deleted", "Deleted bot clone")
        
    except Exception as e:
        logger.error(f"Error in clone delete: {e}")
        await message.reply_text(EmojiMessages.error_message(str(e)))


def setup_clone_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup clone handlers"""
    
    @client.on_message(filters.command("clone"))
    async def clone_cmd(client: Client, message: Message):
        await handle_clone_command(client, message, db)
    
    @client.on_message(filters.command("clone_setup"))
    async def clone_setup_cmd(client: Client, message: Message):
        await handle_clone_setup(client, message, db)
    
    @client.on_message(filters.command("clone_info"))
    async def clone_info_cmd(client: Client, message: Message):
        await handle_clone_info(client, message, db)
    
    @client.on_message(filters.command("clone_delete"))
    async def clone_delete_cmd(client: Client, message: Message):
        await handle_clone_delete(client, message, db)
    
    logger.info("✅ Clone handlers setup complete")
