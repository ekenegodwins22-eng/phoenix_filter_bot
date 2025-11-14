"""
Callback handlers for Phoenix Filter Bot
Handles button callbacks and inline interactions
"""

from pyrogram import Client
from pyrogram.types import CallbackQuery
import logging

logger = logging.getLogger(__name__)


async def handle_join_fsub(client: Client, callback_query: CallbackQuery):
    """Handle Force Subscribe join button callback"""
    await callback_query.answer("Redirecting to channel...", show_alert=False)
    # Will be implemented with actual FSub logic


async def handle_download_file(client: Client, callback_query: CallbackQuery):
    """Handle file download button callback"""
    await callback_query.answer("Preparing download...", show_alert=False)
    # Will be implemented with actual download logic


def setup_callback_handlers(client: Client):
    """Setup all callback handlers"""
    
    @client.on_callback_query()
    async def handle_callbacks(client: Client, callback_query: CallbackQuery):
        data = callback_query.data
        
        if data.startswith("join_fsub_"):
            await handle_join_fsub(client, callback_query)
        elif data.startswith("download_"):
            await handle_download_file(client, callback_query)
        else:
            await callback_query.answer("Unknown action", show_alert=True)
    
    logger.info("✅ Callback handlers setup complete")
