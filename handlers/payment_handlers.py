"""
Payment handlers for Phoenix Filter Bot
Handles USDT payments and premium activation
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    ADMINS,
    PAYMENT_ENABLED,
    USDT_BEP20_ADDRESS,
    USDT_SOL_ADDRESS,
    PAYMENT_TIMEOUT_MINUTES,
    OWNER_ID,
)
from utils.helpers import log_activity
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)


# Store pending payments temporarily
pending_payments = {}


async def handle_buy_command(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /buy command - Show payment options"""
    if not PAYMENT_ENABLED:
        await message.reply_text("❌ Payment system is currently disabled")
        return
    
    buy_text = f"""
💳 **Phoenix Filter Bot - Premium Plans**

Choose your plan and payment method:

**🥉 Basic Plan - $2.99**
Duration: 1 Month
Features: Unlimited searches, Priority support

**🥈 Standard Plan - $7.99**
Duration: 3 Months
Features: All Basic + Ad-free + Custom filters

**🥇 Premium Plan - $19.99**
Duration: 1 Year
Features: All Standard + Exclusive content + Early access

---

**Payment Methods:**
We accept USDT on:
• 🔗 BSC (Binance Smart Chain)
• ◎ Solana

Click below to select your plan and payment method:
"""
    
    buttons = [
        [
            InlineKeyboardButton("🥉 Basic ($2.99)", callback_data="buy_basic"),
            InlineKeyboardButton("🥈 Standard ($7.99)", callback_data="buy_standard"),
        ],
        [InlineKeyboardButton("🥇 Premium ($19.99)", callback_data="buy_premium")],
        [InlineKeyboardButton("❓ Need Help?", url=f"https://t.me/{OWNER_ID}")],
    ]
    
    await message.reply_text(buy_text, reply_markup=InlineKeyboardMarkup(buttons))


async def handle_payment_callback(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle payment plan selection"""
    data = callback_query.data
    user_id = callback_query.from_user.id
    
    # Parse plan from callback data
    if data.startswith("buy_"):
        plan = data.replace("buy_", "")
        
        # Plan details
        plans = {
            "basic": {"name": "Basic", "price": 2.99, "days": 30},
            "standard": {"name": "Standard", "price": 7.99, "days": 90},
            "premium": {"name": "Premium", "price": 19.99, "days": 365},
        }
        
        if plan not in plans:
            await callback_query.answer("Invalid plan", show_alert=True)
            return
        
        plan_info = plans[plan]
        payment_id = str(uuid.uuid4())[:8]
        
        # Store pending payment
        pending_payments[payment_id] = {
            "user_id": user_id,
            "plan": plan,
            "price": plan_info["price"],
            "days": plan_info["days"],
            "created_at": datetime.utcnow(),
            "status": "pending",
        }
        
        # Create payment instructions
        payment_text = f"""
💰 **Payment Instructions**

Plan: {plan_info['name']} (${plan_info['price']})
Duration: {plan_info['days']} days

Payment ID: `{payment_id}`

Choose your payment method:
"""
        
        buttons = [
            [InlineKeyboardButton("🔗 BSC (USDT)", callback_data=f"pay_bsc_{payment_id}")],
            [InlineKeyboardButton("◎ Solana (USDT)", callback_data=f"pay_sol_{payment_id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")],
        ]
        
        await callback_query.message.edit_text(
            payment_text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        await callback_query.answer()


async def handle_bsc_payment(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle BSC payment option"""
    payment_id = callback_query.data.replace("pay_bsc_", "")
    user_id = callback_query.from_user.id
    
    if payment_id not in pending_payments:
        await callback_query.answer("Payment expired", show_alert=True)
        return
    
    payment = pending_payments[payment_id]
    plan_info = {
        "basic": {"name": "Basic", "price": 2.99, "days": 30},
        "standard": {"name": "Standard", "price": 7.99, "days": 90},
        "premium": {"name": "Premium", "price": 19.99, "days": 365},
    }[payment["plan"]]
    
    payment_text = f"""
🔗 **Send USDT on BSC (Binance Smart Chain)**

**Wallet Address:**
`{USDT_BEP20_ADDRESS}`

**Amount to Send:** {payment['price']} USDT
**Payment ID:** `{payment_id}`

**Steps:**
1. Open your wallet (MetaMask, Trust Wallet, etc.)
2. Send exactly {payment['price']} USDT to the address above
3. Include the Payment ID in the memo/note if possible
4. Wait for confirmation (usually 1-2 minutes)
5. Send the transaction hash to @{OWNER_ID} with Payment ID: {payment_id}

⏰ **Expires in:** {PAYMENT_TIMEOUT_MINUTES} minutes

After payment is confirmed, you'll get {plan_info['days']} days of {plan_info['name']} premium!
"""
    
    buttons = [
        [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"confirm_payment_{payment_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")],
    ]
    
    await callback_query.message.edit_text(
        payment_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


async def handle_sol_payment(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle Solana payment option"""
    payment_id = callback_query.data.replace("pay_sol_", "")
    user_id = callback_query.from_user.id
    
    if payment_id not in pending_payments:
        await callback_query.answer("Payment expired", show_alert=True)
        return
    
    payment = pending_payments[payment_id]
    plan_info = {
        "basic": {"name": "Basic", "price": 2.99, "days": 30},
        "standard": {"name": "Standard", "price": 7.99, "days": 90},
        "premium": {"name": "Premium", "price": 19.99, "days": 365},
    }[payment["plan"]]
    
    payment_text = f"""
◎ **Send USDT on Solana**

**Wallet Address:**
`{USDT_SOL_ADDRESS}`

**Amount to Send:** {payment['price']} USDT
**Payment ID:** `{payment_id}`

**Steps:**
1. Open your Solana wallet (Phantom, Solflare, etc.)
2. Send exactly {payment['price']} USDT to the address above
3. Include the Payment ID in the memo if possible
4. Wait for confirmation (usually 10-30 seconds on Solana)
5. Send the transaction hash to @{OWNER_ID} with Payment ID: {payment_id}

⏰ **Expires in:** {PAYMENT_TIMEOUT_MINUTES} minutes

After payment is confirmed, you'll get {plan_info['days']} days of {plan_info['name']} premium!
"""
    
    buttons = [
        [InlineKeyboardButton("✅ I've Sent Payment", callback_data=f"confirm_payment_{payment_id}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_payment")],
    ]
    
    await callback_query.message.edit_text(
        payment_text,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    await callback_query.answer()


async def handle_confirm_payment(client: Client, callback_query, db: AsyncIOMotorDatabase):
    """Handle payment confirmation"""
    payment_id = callback_query.data.replace("confirm_payment_", "")
    user_id = callback_query.from_user.id
    
    if payment_id not in pending_payments:
        await callback_query.answer("Payment expired", show_alert=True)
        return
    
    payment = pending_payments[payment_id]
    
    # Store payment in database for admin verification
    await db.payments.insert_one({
        "payment_id": payment_id,
        "user_id": user_id,
        "plan": payment["plan"],
        "price": payment["price"],
        "days": payment["days"],
        "status": "awaiting_verification",
        "created_at": payment["created_at"],
        "verified_at": None,
    })
    
    confirmation_text = f"""
✅ **Payment Submitted**

Payment ID: `{payment_id}`
Plan: {payment['plan'].capitalize()}
Amount: ${payment['price']}

Your payment is awaiting admin verification.
You will be notified once it's confirmed.

This usually takes 5-30 minutes.
"""
    
    await callback_query.message.edit_text(confirmation_text)
    
    # Notify admin
    try:
        await client.send_message(
            OWNER_ID,
            f"""
🔔 **New Payment Received**

Payment ID: `{payment_id}`
User: {callback_query.from_user.mention}
User ID: {user_id}
Plan: {payment['plan'].capitalize()}
Amount: ${payment['price']}
Duration: {payment['days']} days

Please verify the payment on the blockchain and approve using:
/approve_payment {payment_id}

Or reject with:
/reject_payment {payment_id}
"""
        )
    except Exception as e:
        logger.error(f"Could not notify admin: {e}")
    
    await callback_query.answer()
    await log_activity(db, user_id, "payment_submitted", f"Payment {payment_id} submitted")


async def handle_approve_payment(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /approve_payment command - Admin only"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /approve_payment <payment_id>")
        return
    
    payment_id = args[1]
    
    try:
        # Get payment from database
        payment = await db.payments.find_one({"payment_id": payment_id})
        
        if not payment:
            await message.reply_text(f"❌ Payment {payment_id} not found")
            return
        
        if payment["status"] != "awaiting_verification":
            await message.reply_text(f"❌ Payment {payment_id} is not pending verification")
            return
        
        user_id = payment["user_id"]
        days = payment["days"]
        plan = payment["plan"]
        
        # Update payment status
        await db.payments.update_one(
            {"payment_id": payment_id},
            {
                "$set": {
                    "status": "approved",
                    "verified_at": datetime.utcnow(),
                }
            }
        )
        
        # Add premium to user
        premium_until = datetime.utcnow() + timedelta(days=days)
        
        await db.users.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "is_premium": True,
                    "premium_until": premium_until,
                }
            },
            upsert=True
        )
        
        await message.reply_text(
            f"✅ **Payment Approved**\n\n"
            f"Payment ID: {payment_id}\n"
            f"User: {user_id}\n"
            f"Plan: {plan.capitalize()}\n"
            f"Duration: {days} days\n"
            f"Expires: {premium_until.strftime('%Y-%m-%d')}"
        )
        
        # Notify user
        try:
            await client.send_message(
                user_id,
                f"""
🎉 **Payment Approved!**

Your {plan.capitalize()} premium subscription is now active!

Duration: {days} days
Expires: {premium_until.strftime('%Y-%m-%d')}

Enjoy unlimited access to all premium features! 🚀
"""
            )
        except Exception as e:
            logger.warning(f"Could not notify user: {e}")
        
        await log_activity(db, message.from_user.id, "approve_payment", f"Approved payment {payment_id}")
        
    except Exception as e:
        logger.error(f"Error approving payment: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


async def handle_reject_payment(client: Client, message: Message, db: AsyncIOMotorDatabase):
    """Handle /reject_payment command - Admin only"""
    if message.from_user.id not in ADMINS:
        await message.reply_text("❌ This command is only for admins!")
        return
    
    args = message.text.split()
    if len(args) < 2:
        await message.reply_text("Usage: /reject_payment <payment_id>")
        return
    
    payment_id = args[1]
    
    try:
        payment = await db.payments.find_one({"payment_id": payment_id})
        
        if not payment:
            await message.reply_text(f"❌ Payment {payment_id} not found")
            return
        
        # Update payment status
        await db.payments.update_one(
            {"payment_id": payment_id},
            {"$set": {"status": "rejected"}}
        )
        
        await message.reply_text(f"✅ Payment {payment_id} rejected")
        
        # Notify user
        try:
            await client.send_message(
                payment["user_id"],
                f"""
❌ **Payment Rejected**

Payment ID: {payment_id}

Your payment could not be verified. Please contact @{OWNER_ID} for more information.
"""
            )
        except Exception as e:
            logger.warning(f"Could not notify user: {e}")
        
        await log_activity(db, message.from_user.id, "reject_payment", f"Rejected payment {payment_id}")
        
    except Exception as e:
        logger.error(f"Error rejecting payment: {e}")
        await message.reply_text(f"❌ Error: {str(e)}")


def setup_payment_handlers(client: Client, db: AsyncIOMotorDatabase):
    """Setup payment handlers"""
    
    @client.on_message(filters.command("buy"))
    async def buy_cmd(client: Client, message: Message):
        await handle_buy_command(client, message, db)
    
    @client.on_message(filters.command("approve_payment"))
    async def approve_payment_cmd(client: Client, message: Message):
        await handle_approve_payment(client, message, db)
    
    @client.on_message(filters.command("reject_payment"))
    async def reject_payment_cmd(client: Client, message: Message):
        await handle_reject_payment(client, message, db)
    
    @client.on_callback_query()
    async def handle_callbacks(client: Client, callback_query):
        data = callback_query.data
        
        if data.startswith("buy_"):
            await handle_payment_callback(client, callback_query, db)
        elif data.startswith("pay_bsc_"):
            await handle_bsc_payment(client, callback_query, db)
        elif data.startswith("pay_sol_"):
            await handle_sol_payment(client, callback_query, db)
        elif data.startswith("confirm_payment_"):
            await handle_confirm_payment(client, callback_query, db)
        elif data == "cancel_payment":
            await callback_query.message.delete()
            await callback_query.answer()
    
    logger.info("✅ Payment handlers setup complete")
