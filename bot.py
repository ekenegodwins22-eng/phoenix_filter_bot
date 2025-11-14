"""
Phoenix Filter Bot - Main Entry Point
A next-generation Telegram media distribution bot
"""

import logging
import asyncio
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from config import (
    BOT_TOKEN,
    API_ID,
    API_HASH,
    DATABASE_URI,
    LOG_CHANNEL,
    OWNER_ID,
    validate_config,
)
from handlers import setup_command_handlers, setup_filters, setup_callback_handlers
from handlers.search_handlers import setup_search_handlers
from handlers.admin_handlers import setup_admin_handlers
from handlers.premium_handlers import setup_premium_handlers
from handlers.file_handlers import setup_file_handlers
from handlers.payment_handlers import setup_payment_handlers
from handlers.benefits_handlers import setup_benefits_handlers
from handlers.clone_handlers import setup_clone_handlers
from handlers.advanced_features import setup_advanced_handlers

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhoenixFilterBot:
    """Main bot class"""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.motor_client = None
    
    async def initialize(self):
        """Initialize the bot and database"""
        logger.info("🔥 Initializing Phoenix Filter Bot...")
        
        # Validate configuration
        if not validate_config():
            logger.error("❌ Configuration validation failed!")
            raise ValueError("Invalid configuration")
        
        # Initialize Pyrogram client
        self.client = Client(
            "phoenix_filter_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )
        
        # Initialize MongoDB connection
        try:
            self.motor_client = AsyncIOMotorClient(DATABASE_URI)
            self.db = self.motor_client.phoenix_filter_bot
            
            # Test connection
            await self.motor_client.admin.command('ping')
            logger.info("✅ Database connection successful")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
        
        # Setup handlers
        setup_command_handlers(self.client)
        setup_filters(self.client)
        setup_callback_handlers(self.client)
        setup_search_handlers(self.client, self.db)
        setup_admin_handlers(self.client, self.db)
        setup_premium_handlers(self.client, self.db)
        setup_file_handlers(self.client, self.db)
        setup_payment_handlers(self.client, self.db)
        setup_benefits_handlers(self.client, self.db)
        setup_clone_handlers(self.client, self.db)
        setup_advanced_handlers(self.client, self.db)
        
        logger.info("✅ Bot initialization complete")
    
    async def start(self):
        """Start the bot"""
        try:
            await self.client.start()
            me = await self.client.get_me()
            logger.info(f"✅ Bot started successfully!")
            logger.info(f"   Bot: @{me.username}")
            logger.info(f"   ID: {me.id}")
            
            # Send startup notification to owner
            try:
                await self.client.send_message(
                    OWNER_ID,
                    "🔥 **Phoenix Filter Bot Started**\n\n"
                    "The bot is now online and ready to use!"
                )
            except Exception as e:
                logger.warning(f"Could not send startup message to owner: {e}")
            
            # Keep the bot running
            await asyncio.Event().wait()
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise
    
    async def stop(self):
        """Stop the bot"""
        logger.info("Stopping bot...")
        if self.client:
            await self.client.stop()
        if self.motor_client:
            self.motor_client.close()
        logger.info("✅ Bot stopped")


async def main():
    """Main function"""
    bot = PhoenixFilterBot()
    
    try:
        await bot.initialize()
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
    finally:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
