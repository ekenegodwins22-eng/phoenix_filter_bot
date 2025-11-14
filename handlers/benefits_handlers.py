"""
Premium benefits display handlers
Shows users their benefits and limitations
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.premium_benefits import PremiumBenefits
from utils.helpers import log_activity
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)


async def handle_benefits_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /benefits command - Show user's benefits"""
    try:
        user_id = message.from_user.id
        benefits = await PremiumBenefits.get_user_benefits(db, user_id)
        
        is_premium = benefits["is_premium"]
        status = "💎 **PREMIUM**" if is_premium else "📋 **FREE**"
        
        benefits_text = f"""
{status}

{PremiumBenefits.get_benefits_text(is_premium)}

**Today's Usage:**
• Searches: {benefits['usage_today']['searches']}/{benefits['limits']['daily_searches']}
• Downloads: {benefits['usage_today']['downloads']}/{benefits['limits']['daily_downloads']}

**Remaining Today:**
• Searches: {benefits['remaining_today']['searches']}
• Downloads: {benefits['remaining_today']['downloads']}
"""
        
        buttons = []
        if not is_premium:
            buttons.append([InlineKeyboardButton("💳 Upgrade to Premium", callback_data="upgrade_premium")])
        
        buttons.append([InlineKeyboardButton("📊 See Comparison", callback_data="show_comparison")])
        
        await message.reply_text(
            benefits_text,
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )
        
        await log_activity(db, user_id, "view_benefits", "Viewed benefits")
        
    except Exception as e:
        logger.error(f"Error in benefits command: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_comparison_callback(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle comparison display"""
    comparison_text = PremiumBenefits.get_comparison_text()
    
    buttons = [
        [InlineKeyboardButton("💳 Get Premium", callback_data="buy_basic")],
        [InlineKeyboardButton("❌ Close", callback_data="close")],
    ]
    
    await callback_query.message.edit_text(
        comparison_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


async def handle_upgrade_callback(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle upgrade button"""
    upgrade_text = """
💎 **Upgrade to Premium**

Choose your plan:

**🥉 Basic - $2.99**
1 Month Premium

**🥈 Standard - $7.99**
3 Months Premium

**🥇 Premium - $19.99**
1 Year Premium
"""
    
    buttons = [
        [
            InlineKeyboardButton("🥉 Basic", callback_data="buy_basic"),
            InlineKeyboardButton("🥈 Standard", callback_data="buy_standard"),
        ],
        [InlineKeyboardButton("🥇 Premium", callback_data="buy_premium")],
        [InlineKeyboardButton("❌ Cancel", callback_data="close")],
    ]
    
    await callback_query.message.edit_text(
        upgrade_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


def setup_benefits_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup benefits handlers"""
    
    @client.on_message(filters.command("benefits"))
    async def benefits_cmd(client: Client, message: Message):
        await handle_benefits_command(client, message, db)
    
    logger.info("✅ Benefits handlers setup complete")
