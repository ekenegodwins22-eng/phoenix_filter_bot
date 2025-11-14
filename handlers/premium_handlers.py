"""
Premium and monetization handlers for Phoenix Filter Bot
Handles premium membership and referral system
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS, PREMIUM_ENABLED
from utils.helpers import log_activity
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


async def handle_plan_command(client: Client, message: Message):
    """Handle /plan command - Show premium plans"""
    if not PREMIUM_ENABLED:
        await message.reply_text("❌ Premium feature is currently disabled")
        return
    
    plans_text = """
💎 **Phoenix Filter Bot Premium Plans**

**🥉 Basic Plan**
• Duration: 1 Month
• Price: $2.99
• Features: Unlimited searches, Priority support

**🥈 Standard Plan**
• Duration: 3 Months
• Price: $7.99
• Features: All Basic + Ad-free experience, Custom filters

**🥇 Premium Plan**
• Duration: 1 Year
• Price: $19.99
• Features: All Standard + Exclusive content, Early access

**Special Offer:**
Refer 3 friends and get 1 month free!

Contact: @ph0enix_web for payments
"""
    
    buttons = [
        [InlineKeyboardButton("💳 Get Premium", url="https://t.me/ph0enix_web")],
        [InlineKeyboardButton("📊 My Plan", callback_data="myplan")],
    ]
    
    await message.reply_text(plans_text, reply_markup=InlineKeyboardMarkup(buttons))


async def handle_myplan_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /myplan command - Check user's premium status"""
    if not PREMIUM_ENABLED:
        await message.reply_text("❌ Premium feature is currently disabled")
        return
    
    try:
        user = await db.users.find_one({"user_id": message.from_user.id})
        
        if not user:
            plan_text = "❌ No account found. Use /start to create one."
        elif not user.get("is_premium"):
            plan_text = """
❌ **No Active Premium**

You don't have an active premium subscription.
Use /plan to view available plans.
"""
        else:
            premium_until = user.get("premium_until")
            days_left = (premium_until - datetime.utcnow()).days if premium_until else 0
            
            plan_text = f"""
✅ **Your Premium Status**

💎 Status: Active
📅 Expires: {premium_until.strftime('%Y-%m-%d') if premium_until else 'N/A'}
⏰ Days Left: {days_left}
👥 Referrals: {user.get('referral_count', 0)}
"""
        
        await message.reply_text(plan_text)
        await log_activity(db, message.from_user.id, "check_plan", "Checked premium status")
        
    except Exception as e:
        logger.error(f"Error in myplan command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_add_premium_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /add_premium command - Add premium to user (admin only)"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 3:
        await message.reply_text("Usage: /add_premium <user_id> <days>")
        return
    
    try:
        user_id = int(args[1])
        days = int(args[2])
        
        premium_until = datetime.utcnow() + timedelta(days=days)
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_premium": True,
                    "premium_until": premium_until,
                }
            }
        )
        
        if result.modified_count > 0:
            await message.reply_text(
                f"✅ **Premium Added**\n\n"
                f"User: {user_id}\n"
                f"Duration: {days} days\n"
                f"Expires: {premium_until.strftime('%Y-%m-%d')}"
            )
            
            # Notify user
            try:
                await client.send_message(
                    user_id,
                    f"🎉 **Premium Activated!**\n\n"
                    f"Your premium subscription is now active for {days} days!\n"
                    f"Enjoy unlimited access to all features."
                )
            except:
                pass
            
            await log_activity(db, message.from_user.id, "add_premium", f"Added {days} days to user {user_id}")
        else:
            await message.reply_text(f"❌ User {user_id} not found")
    
    except ValueError:
        await message.reply_text("❌ Invalid user ID or days")
    except Exception as e:
        logger.error(f"Error in add_premium command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_remove_premium_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /remove_premium command - Remove premium from user (admin only)"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /remove_premium <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        result = await db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_premium": False,
                    "premium_until": None,
                }
            }
        )
        
        if result.modified_count > 0:
            await message.reply_text(f"✅ Premium removed from user {user_id}")
            await log_activity(db, message.from_user.id, "remove_premium", f"Removed from user {user_id}")
        else:
            await message.reply_text(f"❌ User {user_id} not found")
    
    except ValueError:
        await message.reply_text("❌ Invalid user ID")
    except Exception as e:
        logger.error(f"Error in remove_premium command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_refer_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /refer command - Get referral link"""
    if not PREMIUM_ENABLED:
        await message.reply_text("❌ Referral system is currently disabled")
        return
    
    try:
        user = await db.users.find_one({"user_id": message.from_user.id})
        
        if not user:
            await message.reply_text("❌ User not found. Use /start first.")
            return
        
        referral_count = user.get("referral_count", 0)
        
        refer_text = f"""
👥 **Referral Program**

Share your referral link and earn rewards!

🔗 Your Referral Link:
`https://t.me/phoenix_filter_bot?start=ref_{message.from_user.id}`

📊 Your Stats:
• Referrals: {referral_count}
• Reward: {referral_count // 3} months free premium

**How it works:**
1. Share your link with friends
2. They join using your link
3. Get 1 month free for every 3 referrals!
"""
        
        await message.reply_text(refer_text)
        await log_activity(db, message.from_user.id, "view_referral", f"Viewed referral link")
        
    except Exception as e:
        logger.error(f"Error in refer command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


def setup_premium_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup premium and monetization handlers"""
    
    @client.on_message(filters.command("plan"))
    async def plan_cmd(client: Client, message: Message):
        await handle_plan_command(client, message)
    
    @client.on_message(filters.command("myplan"))
    async def myplan_cmd(client: Client, message: Message):
        await handle_myplan_command(client, message, db)
    
    @client.on_message(filters.command("add_premium"))
    async def add_premium_cmd(client: Client, message: Message):
        await handle_add_premium_command(client, message, db)
    
    @client.on_message(filters.command("remove_premium"))
    async def remove_premium_cmd(client: Client, message: Message):
        await handle_remove_premium_command(client, message, db)
    
    @client.on_message(filters.command("refer"))
    async def refer_cmd(client: Client, message: Message):
        await handle_refer_command(client, message, db)
    
    logger.info("✅ Premium handlers setup complete")
