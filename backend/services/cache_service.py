"""
Simple in-memory cache service for API-Football responses
Reduces API calls and improves response times
"""

import time
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self, default_ttl: int = 900):  # 15 minutes default
        """
        Initialize cache service
        
        Args:
            default_ttl: Default time-to-live in seconds
        """
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl
        
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if not expired"""
        if key not in self.cache:
            return None
            
        cache_entry = self.cache[key]
        current_time = time.time()
        
        if current_time > cache_entry['expires_at']:
            # Cache expired, remove entry
            del self.cache[key]
            return None
            
        logger.debug(f"Cache hit for key: {key}")
        return cache_entry['data']
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        if ttl is None:
            ttl = self.default_ttl
            
        expires_at = time.time() + ttl
        
        self.cache[key] = {
            'data': value,
            'expires_at': expires_at,
            'created_at': time.time()
        }
        
        logger.debug(f"Cache set for key: {key}, expires in {ttl} seconds")
    
    def delete(self, key: str) -> bool:
        """Delete specific cache entry"""
        if key in self.cache:
            del self.cache[key]
            logger.debug(f"Cache deleted for key: {key}")
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self.cache.clear()
        logger.debug("Cache cleared")
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count of removed items"""
        current_time = time.time()
        expired_keys = []
        
        for key, entry in self.cache.items():
            if current_time > entry['expires_at']:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self.cache[key]
            
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")
            
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        current_time = time.time()
        active_entries = 0
        expired_entries = 0
        
        for entry in self.cache.values():
            if current_time > entry['expires_at']:
                expired_entries += 1
            else:
                active_entries += 1
        
        return {
            'total_entries': len(self.cache),
            'active_entries': active_entries,
            'expired_entries': expired_entries,
            'cache_size_bytes': len(str(self.cache))
        }

# Global cache instance for API-Football data
api_football_cache = CacheService(default_ttl=900)  # 15 minutes for football data