"""
Phoenix Filter Bot Configuration
All configuration is loaded from environment variables
"""

import os
from typing import List, Optional

# ============================================================================
# ESSENTIAL CREDENTIALS (Required - No Defaults)
# ============================================================================

BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
"""Telegram bot token from BotFather"""

API_ID: int = int(os.getenv("API_ID", "0"))
"""Telegram API ID from telegram.org"""

API_HASH: str = os.getenv("API_HASH", "")
"""Telegram API Hash from telegram.org"""

DATABASE_URI: str = os.getenv("DATABASE_URI", "mongodb://localhost:27017/phoenix_filter_bot")
"""MongoDB connection string"""

# ============================================================================
# CORE CONFIGURATION
# ============================================================================

OWNER_ID: int = int(os.getenv("OWNER_ID", "0"))
"""Bot owner's Telegram user ID"""

OWNER_USERNAME: str = os.getenv("BOT_USERNAME", "ph0enix_web")
"""Bot owner's Telegram username (for 'Powered by' link)"""

LOG_CHANNEL: int = int(os.getenv("LOG_CHANNEL", "-1002450940556"))
"""Channel ID for logging bot activities"""

CHANNELS: List[int] = [
    int(ch.strip()) for ch in os.getenv("CHANNELS", "-1002458488257").split()
]
"""File channel IDs for indexing (space-separated)"""

ADMINS: List[int] = [
    int(admin.strip()) for admin in os.getenv("ADMINS", "6304040346").split()
]
"""Admin user IDs (space-separated)"""

# ============================================================================
# FORCE SUBSCRIBE CONFIGURATION
# ============================================================================

FORCE_SUB_ENABLED: bool = os.getenv("FORCE_SUB_ENABLED", "True").lower() == "true"
"""Enable/Disable Force Subscribe feature"""

FORCE_SUB_CHANNEL: int = int(os.getenv("FORCE_SUB_CHANNEL", "-1002533961050"))
"""Primary mandatory Force Subscribe channel"""

# ============================================================================
# FEATURE TOGGLES
# ============================================================================

PM_SEARCH_ENABLED: bool = os.getenv("PM_SEARCH_ENABLED", "True").lower() == "true"
"""Enable search in private messages"""

RENAME_ENABLED: bool = os.getenv("RENAME_ENABLED", "True").lower() == "true"
"""Enable file rename feature"""

STREAM_ENABLED: bool = os.getenv("STREAM_ENABLED", "True").lower() == "true"
"""Enable streaming feature"""

SHORTLINK_ENABLED: bool = os.getenv("SHORTLINK_ENABLED", "True").lower() == "true"
"""Enable URL shortener integration"""

PREMIUM_ENABLED: bool = os.getenv("PREMIUM_ENABLED", "True").lower() == "true"
"""Enable premium membership system"""

CLONE_ENABLED: bool = os.getenv("CLONE_ENABLED", "True").lower() == "true"
"""Enable bot cloning feature"""

AUTO_APPROVE_ENABLED: bool = os.getenv("AUTO_APPROVE_ENABLED", "False").lower() == "true"
"""Enable auto-approval of requests"""

# ============================================================================
# PAYMENT CONFIGURATION
# ============================================================================

PAYMENT_ENABLED: bool = os.getenv("PAYMENT_ENABLED", "True").lower() == "true"
"""Enable/Disable payment system"""

USDT_BEP20_ADDRESS: str = os.getenv("USDT_BEP20_ADDRESS", "0x58A07f2Ef69a4d7a0C20c0C6B079f059fdE2F669")
"""USDT BEP20 (BSC) wallet address"""

USDT_SOL_ADDRESS: str = os.getenv("USDT_SOL_ADDRESS", "AWDJkMbS4rBCTrzP2AkwfsEBKJobB4rTw2PE2oxb8h1r")
"""USDT SOL (Solana) wallet address"""

PAYMENT_TIMEOUT_MINUTES: int = int(os.getenv("PAYMENT_TIMEOUT_MINUTES", "30"))
"""Time to wait for payment confirmation (minutes)"""

# ============================================================================
# OPTIONAL CUSTOMIZATION
# ============================================================================

SHORTLINK_API_KEY: Optional[str] = os.getenv("SHORTLINK_API_KEY")
"""API key for URL shortener service"""

SHORTLINK_API_URL: Optional[str] = os.getenv("SHORTLINK_API_URL")
"""URL shortener service endpoint"""

STREAM_SERVER_URL: Optional[str] = os.getenv("STREAM_SERVER_URL")
"""Custom streaming server URL"""

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> bool:
    """Validate that all required configuration is present"""
    errors = []
    
    if not BOT_TOKEN:
        errors.append("BOT_TOKEN is required")
    if not API_ID or API_ID == 0:
        errors.append("API_ID is required and must be a valid integer")
    if not API_HASH:
        errors.append("API_HASH is required")
    if not DATABASE_URI:
        errors.append("DATABASE_URI is required")
    if not OWNER_ID or OWNER_ID == 0:
        errors.append("OWNER_ID is required and must be a valid integer")
    if not LOG_CHANNEL or LOG_CHANNEL == 0:
        errors.append("LOG_CHANNEL is required and must be a valid integer")
    if not CHANNELS:
        errors.append("CHANNELS is required and must contain at least one channel ID")
    if not ADMINS:
        errors.append("ADMINS is required and must contain at least one admin ID")
    
    if errors:
        print("Configuration Validation Errors:")
        for error in errors:
            print(f"  ❌ {error}")
        return False
    
    print("✅ Configuration validation passed")
    return True


if __name__ == "__main__":
    validate_config()
