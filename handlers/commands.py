"""
Command handlers for Phoenix Filter Bot
Handles all /command interactions
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from config import OWNER_ID, OWNER_USERNAME, ADMINS
import logging

logger = logging.getLogger(__name__)


async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    
    welcome_text = f"""
🔥 **Welcome to Phoenix Filter Bot** 🔥

Hello {user.mention}! 

I'm a powerful media distribution bot with advanced features:
✨ **Auto-Filter Search** - Just type what you're looking for
🔐 **Force Subscribe** - Access premium content
💎 **Premium Membership** - Unlock exclusive features
📊 **Advanced Admin Tools** - Complete control

**Quick Start:**
• Just send me a search query (no /search needed)
• Join required channels to access files
• Use /help for all available commands

**Need Help?**
Contact: @{OWNER_USERNAME}

**Credits:**
Built with ❤️ by Manus AI
"""
    
    await message.reply_text(welcome_text, disable_web_page_preview=True)
    logger.info(f"User {user.id} started the bot")


async def help_command(client: Client, message: Message):
    """Handle /help command"""
    help_text = """
🆘 **Phoenix Filter Bot - Help**

**User Commands:**
• /start - Start the bot
• /help - Show this help message
• /myplan - Check your premium status
• /id - Get your Telegram ID
• /info - Get your user info

**Search:**
Just send any text in DM or group to search!
Example: "Superman" or "Avengers"

**Premium Commands:**
• /plan - View premium plans
• /myplan - Check your current plan
• /refer - Get your referral link

**File Management:**
• /rename - Rename a file
• /set_caption - Add caption to file
• /set_thumb - Set thumbnail

**Admin Commands** (Admin only):
• /index - Index files from channel
• /stats - View bot statistics
• /users - List all users
• /ban @user - Ban a user
• /unban @user - Unban a user
• /broadcast - Send message to all users
• /fsub @channel - Add Force Subscribe channel
• /nofsub - Remove Force Subscribe

**More Help:**
Contact: @{OWNER_USERNAME}
"""
    
    await message.reply_text(help_text, disable_web_page_preview=True)


async def id_command(client: Client, message: Message):
    """Handle /id command - Get user/chat IDs"""
    user = message.from_user
    chat = message.chat
    
    info_text = f"""
**Your Information:**

👤 **User ID:** `{user.id}`
📝 **Username:** @{user.username or 'Not set'}
📌 **Name:** {user.first_name} {user.last_name or ''}

💬 **Chat ID:** `{chat.id}`
🏷️ **Chat Type:** {chat.type}
"""
    
    await message.reply_text(info_text)


async def info_command(client: Client, message: Message):
    """Handle /info command - Get user information"""
    user = message.from_user
    
    info_text = f"""
**User Information:**

👤 **ID:** {user.id}
📝 **Username:** @{user.username or 'Not set'}
✍️ **First Name:** {user.first_name}
✍️ **Last Name:** {user.last_name or 'Not set'}
🤖 **Is Bot:** {user.is_bot}
🔒 **Is Premium:** {user.is_premium}
"""
    
    await message.reply_text(info_text)


async def stats_command(client: Client, message: Message):
    """Handle /stats command - Show bot statistics"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    stats_text = """
📊 **Phoenix Filter Bot Statistics**

(Statistics module coming soon)

• Total Users: Loading...
• Total Files: Loading...
• Total Searches: Loading...
• Premium Users: Loading...
"""
    
    await message.reply_text(stats_text)


def setup_command_handlers(client: Client):
    """Setup all command handlers"""
    
    @client.on_message(filters.command("start"))
    async def start(client: Client, message: Message):
        await start_command(client, message)
    
    @client.on_message(filters.command("help"))
    async def help_cmd(client: Client, message: Message):
        await help_command(client, message)
    
    @client.on_message(filters.command("id"))
    async def id_cmd(client: Client, message: Message):
        await id_command(client, message)
    
    @client.on_message(filters.command("info"))
    async def info_cmd(client: Client, message: Message):
        await info_command(client, message)
    
    @client.on_message(filters.command("stats"))
    async def stats_cmd(client: Client, message: Message):
        await stats_command(client, message)
    
    logger.info("✅ Command handlers setup complete")
