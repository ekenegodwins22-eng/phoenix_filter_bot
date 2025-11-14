"""
Premium benefits and restrictions system
Defines what free users can do vs premium users
"""

from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PremiumBenefits:
    """Manage premium features and restrictions"""
    
    # Free user limits
    FREE_LIMITS = {
        "daily_searches": 20,  # Free users can search 20 times per day
        "daily_downloads": 5,  # Free users can download 5 files per day
        "max_file_size_mb": 100,  # Free users limited to 100MB files
        "storage_mb": 500,  # Free users get 500MB storage
        "concurrent_downloads": 1,  # Free users can download 1 file at a time
        "batch_operations": False,  # Free users cannot do batch operations
        "custom_filters": False,  # Free users cannot create custom filters
        "priority_support": False,  # Free users don't get priority support
        "ad_free": False,  # Free users see ads
    }
    
    # Premium user limits (unlimited or much higher)
    PREMIUM_LIMITS = {
        "daily_searches": 999999,  # Unlimited
        "daily_downloads": 999999,  # Unlimited
        "max_file_size_mb": 5000,  # 5GB files
        "storage_mb": 100000,  # 100GB storage
        "concurrent_downloads": 10,  # 10 concurrent downloads
        "batch_operations": True,  # Can do batch operations
        "custom_filters": True,  # Can create custom filters
        "priority_support": True,  # Priority support
        "ad_free": True,  # No ads
    }
    
    @staticmethod
    async def is_premium(db: AsyncIOMotorDatabase, user_id: int) -> bool:
        """Check if user has active premium"""
        try:
            user = await db.users.find_one({"user_id": user_id})
            
            if not user:
                return False
            
            if not user.get("is_premium"):
                return False
            
            premium_until = user.get("premium_until")
            if not premium_until:
                return False
            
            # Check if premium has expired
            if premium_until < datetime.utcnow():
                # Expire the premium
                await db.users.update_one(
                    {"user_id": user_id},
                    {"$set": {"is_premium": False, "premium_until": None}}
                )
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error checking premium status: {e}")
            return False
    
    @staticmethod
    def get_limits(is_premium: bool) -> dict:
        """Get feature limits for user"""
        return PremiumBenefits.PREMIUM_LIMITS if is_premium else PremiumBenefits.FREE_LIMITS
    
    @staticmethod
    async def check_daily_searches(db: AsyncIOMotorDatabase, user_id: int) -> tuple[bool, int]:
        """
        Check if user can perform a search today
        Returns: (can_search, searches_remaining)
        """
        is_premium = await PremiumBenefits.is_premium(db, user_id)
        limits = PremiumBenefits.get_limits(is_premium)
        daily_limit = limits["daily_searches"]
        
        if daily_limit == 999999:  # Premium
            return True, daily_limit
        
        # Get today's search count
        today = datetime.utcnow().date()
        search_log = await db.search_logs.find_one({
            "user_id": user_id,
            "date": today,
        })
        
        searches_today = search_log["count"] if search_log else 0
        remaining = daily_limit - searches_today
        
        return searches_today < daily_limit, remaining
    
    @staticmethod
    async def log_search(db: AsyncIOMotorDatabase, user_id: int):
        """Log a search for daily limit tracking"""
        try:
            today = datetime.utcnow().date()
            
            await db.search_logs.update_one(
                {"user_id": user_id, "date": today},
                {"$inc": {"count": 1}},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error logging search: {e}")
    
    @staticmethod
    async def check_daily_downloads(db: AsyncIOMotorDatabase, user_id: int) -> tuple[bool, int]:
        """
        Check if user can download today
        Returns: (can_download, downloads_remaining)
        """
        is_premium = await PremiumBenefits.is_premium(db, user_id)
        limits = PremiumBenefits.get_limits(is_premium)
        daily_limit = limits["daily_downloads"]
        
        if daily_limit == 999999:  # Premium
            return True, daily_limit
        
        # Get today's download count
        today = datetime.utcnow().date()
        download_log = await db.download_logs.find_one({
            "user_id": user_id,
            "date": today,
        })
        
        downloads_today = download_log["count"] if download_log else 0
        remaining = daily_limit - downloads_today
        
        return downloads_today < daily_limit, remaining
    
    @staticmethod
    async def log_download(db: AsyncIOMotorDatabase, user_id: int):
        """Log a download for daily limit tracking"""
        try:
            today = datetime.utcnow().date()
            
            await db.download_logs.update_one(
                {"user_id": user_id, "date": today},
                {"$inc": {"count": 1}},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error logging download: {e}")
    
    @staticmethod
    async def get_user_benefits(db: AsyncIOMotorDatabase, user_id: int) -> dict:
        """Get all benefits for a user"""
        is_premium = await PremiumBenefits.is_premium(db, user_id)
        limits = PremiumBenefits.get_limits(is_premium)
        
        # Get daily usage
        today = datetime.utcnow().date()
        search_log = await db.search_logs.find_one({"user_id": user_id, "date": today})
        download_log = await db.download_logs.find_one({"user_id": user_id, "date": today})
        
        searches_today = search_log["count"] if search_log else 0
        downloads_today = download_log["count"] if download_log else 0
        
        return {
            "is_premium": is_premium,
            "limits": limits,
            "usage_today": {
                "searches": searches_today,
                "downloads": downloads_today,
            },
            "remaining_today": {
                "searches": limits["daily_searches"] - searches_today,
                "downloads": limits["daily_downloads"] - downloads_today,
            }
        }
    
    @staticmethod
    def get_benefits_text(is_premium: bool) -> str:
        """Get formatted benefits text"""
        if is_premium:
            return """
💎 **Premium Benefits** ✨

✅ Unlimited daily searches
✅ Unlimited daily downloads
✅ Access to 5GB files
✅ 100GB storage space
✅ 10 concurrent downloads
✅ Batch operations
✅ Custom filters
✅ Priority support
✅ Ad-free experience
✅ Early access to new features
"""
        else:
            return """
📋 **Free Plan Limitations**

❌ Limited to 20 searches/day
❌ Limited to 5 downloads/day
❌ Max file size: 100MB
❌ Storage: 500MB
❌ 1 concurrent download
❌ No batch operations
❌ No custom filters
❌ Standard support
❌ Ads enabled
❌ No early access

💡 Upgrade to Premium to unlock all features!
"""
    
    @staticmethod
    def get_comparison_text() -> str:
        """Get feature comparison table"""
        return """
📊 **Feature Comparison**

| Feature | Free | Premium |
|---------|------|---------|
| Daily Searches | 20 | Unlimited |
| Daily Downloads | 5 | Unlimited |
| Max File Size | 100MB | 5GB |
| Storage | 500MB | 100GB |
| Concurrent Downloads | 1 | 10 |
| Batch Operations | ❌ | ✅ |
| Custom Filters | ❌ | ✅ |
| Priority Support | ❌ | ✅ |
| Ad-Free | ❌ | ✅ |
| Early Access | ❌ | ✅ |

💳 **Upgrade Now** - Use /buy to get premium!
"""
