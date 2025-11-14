"""
Emoji-enhanced messages for Phoenix Filter Bot
Makes messages more lively and engaging
"""

EMOJIS = {
    # Status emojis
    "success": "✅",
    "error": "❌",
    "warning": "⚠️",
    "info": "ℹ️",
    "loading": "⏳",
    "rocket": "🚀",
    
    # Feature emojis
    "search": "🔍",
    "download": "⬇️",
    "upload": "⬆️",
    "file": "📁",
    "movie": "🎬",
    "tv": "📺",
    "music": "🎵",
    "document": "📄",
    "image": "🖼️",
    "video": "🎥",
    
    # Premium emojis
    "premium": "💎",
    "star": "⭐",
    "crown": "👑",
    "gold": "🥇",
    "silver": "🥈",
    "bronze": "🥉",
    
    # Action emojis
    "ban": "🚫",
    "unban": "✔️",
    "delete": "🗑️",
    "edit": "✏️",
    "copy": "📋",
    "link": "🔗",
    "share": "📤",
    
    # Money/Payment emojis
    "money": "💰",
    "wallet": "💳",
    "coin": "🪙",
    "dollar": "💵",
    "euro": "💶",
    "crypto": "🔐",
    
    # User emojis
    "user": "👤",
    "users": "👥",
    "admin": "👨‍💼",
    "bot": "🤖",
    "person": "👨",
    
    # Chat emojis
    "message": "💬",
    "chat": "💭",
    "notification": "🔔",
    "bell": "🔔",
    "muted": "🔇",
    
    # Time emojis
    "clock": "⏰",
    "calendar": "📅",
    "timer": "⏱️",
    "hourglass": "⌛",
    
    # Phoenix specific
    "phoenix": "🔥",
    "fire": "🔥",
    "flame": "🔥",
}


class EmojiMessages:
    """Generate emoji-enhanced messages"""
    
    @staticmethod
    def welcome() -> str:
        """Welcome message with emojis"""
        return f"""
{EMOJIS['phoenix']} **Welcome to Phoenix Filter Bot** {EMOJIS['phoenix']}

🚀 The ultimate media distribution bot with advanced features!

{EMOJIS['search']} **Features:**
• Unlimited search capabilities
• Fast file delivery
• Premium membership
• Force Subscribe management
• Admin controls
• And much more!

{EMOJIS['info']} Use /help to see all commands
{EMOJIS['premium']} Use /plan to upgrade to premium
{EMOJIS['link']} Contact: @ph0enix_web
"""
    
    @staticmethod
    def help_message() -> str:
        """Help message with emojis"""
        return f"""
{EMOJIS['info']} **Phoenix Filter Bot - Help**

{EMOJIS['search']} **Search Commands:**
• Just type the movie/file name to search
• /search <query> - Manual search
• /filter <query> - Filter results

{EMOJIS['download']} **Download Commands:**
• /download <file_id> - Download file
• /stream <file_id> - Stream file
• /rename <file_id> <new_name> - Rename file

{EMOJIS['premium']} **Premium Commands:**
• /plan - View premium plans
• /myplan - Check your premium status
• /benefits - View your benefits
• /buy - Purchase premium

{EMOJIS['admin']} **Admin Commands:**
• /users - List all users
• /ban <user_id> - Ban user
• /unban <user_id> - Unban user
• /broadcast <message> - Send message to all users
• /fsub add @channel - Add Force Subscribe
• /fsub remove @channel - Remove Force Subscribe

{EMOJIS['info']} For more help, contact @ph0enix_web
"""
    
    @staticmethod
    def search_result(query: str, results_count: int) -> str:
        """Search result message"""
        return f"""
{EMOJIS['search']} **Search Results for: {query}**

Found {results_count} result(s) {EMOJIS['rocket']}

{EMOJIS['file']} Files are loading...
"""
    
    @staticmethod
    def file_found(filename: str, size: str) -> str:
        """File found message"""
        return f"""
{EMOJIS['file']} **File Found!**

📝 Name: {filename}
📊 Size: {size}
{EMOJIS['download']} Ready to download!
"""
    
    @staticmethod
    def premium_activated(days: int) -> str:
        """Premium activated message"""
        return f"""
{EMOJIS['premium']} **Premium Activated!** {EMOJIS['premium']}

{EMOJIS['star']} Congratulations! You now have premium access!

{EMOJIS['clock']} Duration: {days} days
{EMOJIS['rocket']} Enjoy unlimited features!

{EMOJIS['success']} Premium benefits unlocked:
✅ Unlimited searches
✅ Unlimited downloads
✅ No ads
✅ Priority support
✅ And more!
"""
    
    @staticmethod
    def payment_received(amount: str, plan: str) -> str:
        """Payment received message"""
        return f"""
{EMOJIS['money']} **Payment Received!** {EMOJIS['money']}

{EMOJIS['wallet']} Amount: {amount}
📦 Plan: {plan}
{EMOJIS['loading']} Status: Awaiting admin verification

⏳ This usually takes 5-30 minutes
{EMOJIS['info']} You'll be notified when approved!
"""
    
    @staticmethod
    def user_banned(user_id: int) -> str:
        """User banned message"""
        return f"""
{EMOJIS['ban']} **User Banned**

👤 User ID: {user_id}
{EMOJIS['clock']} Time: Now
{EMOJIS['success']} User has been banned from the bot
"""
    
    @staticmethod
    def force_sub_required(channels: list) -> str:
        """Force subscribe required message"""
        message = f"{EMOJIS['warning']} **Join Required Channels** {EMOJIS['warning']}\n\n"
        message += "You must join these channels to access files:\n\n"
        
        for i, channel in enumerate(channels, 1):
            message += f"{i}. {channel}\n"
        
        message += f"\n{EMOJIS['info']} After joining, try again!"
        return message
    
    @staticmethod
    def admin_broadcast(message: str) -> str:
        """Admin broadcast message"""
        return f"""
{EMOJIS['notification']} **Broadcast Message**

{message}

{EMOJIS['success']} Message sent to all users!
"""
    
    @staticmethod
    def stats_message(users: int, files: int, downloads: int) -> str:
        """Bot statistics message"""
        return f"""
{EMOJIS['info']} **Phoenix Filter Bot - Statistics**

{EMOJIS['user']} Total Users: {users}
{EMOJIS['file']} Total Files: {files}
{EMOJIS['download']} Total Downloads: {downloads}

{EMOJIS['rocket']} Bot is running smoothly!
"""
    
    @staticmethod
    def error_message(error: str) -> str:
        """Error message"""
        return f"""
{EMOJIS['error']} **Error Occurred**

{error}

{EMOJIS['info']} Please try again or contact @ph0enix_web
"""
    
    @staticmethod
    def loading_message() -> str:
        """Loading message"""
        return f"{EMOJIS['loading']} Processing... Please wait..."
    
    @staticmethod
    def success_message(message: str) -> str:
        """Success message"""
        return f"{EMOJIS['success']} {message}"
    
    @staticmethod
    def info_message(message: str) -> str:
        """Info message"""
        return f"{EMOJIS['info']} {message}"
    
    @staticmethod
    def warning_message(message: str) -> str:
        """Warning message"""
        return f"{EMOJIS['warning']} {message}"


def format_with_emoji(text: str, emoji_key: str = None) -> str:
    """Format text with emoji"""
    if emoji_key and emoji_key in EMOJIS:
        return f"{EMOJIS[emoji_key]} {text}"
    return text


def get_emoji(key: str) -> str:
    """Get emoji by key"""
    return EMOJIS.get(key, "")
