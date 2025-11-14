"""
Search Engine for Phoenix Filter Bot
Handles file searching and indexing
"""

import logging
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from database.models import File

logger = logging.getLogger(__name__)


class SearchEngine:
    """Search engine for finding files in the database"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.files_collection = db.files
    
    async def search(self, query: str, limit: int = 10) -> List[dict]:
        """
        Search for files matching the query
        
        Args:
            query: Search query string
            limit: Maximum number of results
        
        Returns:
            List of matching files
        """
        try:
            # Search in file name and custom name
            results = await self.files_collection.find({
                "$or": [
                    {"file_name": {"$regex": query, "$options": "i"}},
                    {"custom_name": {"$regex": query, "$options": "i"}},
                    {"caption": {"$regex": query, "$options": "i"}},
                ]
            }).limit(limit).to_list(length=limit)
            
            logger.info(f"Search for '{query}' returned {len(results)} results")
            return results
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    async def index_file(self, file_data: dict) -> bool:
        """
        Index a new file in the database
        
        Args:
            file_data: File information dictionary
        
        Returns:
            True if successful, False otherwise
        """
        try:
            result = await self.files_collection.insert_one(file_data)
            logger.info(f"Indexed file: {file_data.get('file_name')} (ID: {result.inserted_id})")
            return True
        except Exception as e:
            logger.error(f"Indexing error: {e}")
            return False
    
    async def get_file_by_id(self, file_id: str) -> Optional[dict]:
        """Get file information by file ID"""
        try:
            file = await self.files_collection.find_one({"file_id": file_id})
            return file
        except Exception as e:
            logger.error(f"Error getting file: {e}")
            return None
    
    async def update_download_count(self, file_id: str) -> bool:
        """Update the download count for a file"""
        try:
            result = await self.files_collection.update_one(
                {"file_id": file_id},
                {"$inc": {"download_count": 1}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating download count: {e}")
            return False
    
    async def get_popular_files(self, limit: int = 10) -> List[dict]:
        """Get most downloaded files"""
        try:
            results = await self.files_collection.find({}).sort("download_count", -1).limit(limit).to_list(length=limit)
            return results
        except Exception as e:
            logger.error(f"Error getting popular files: {e}")
            return []
