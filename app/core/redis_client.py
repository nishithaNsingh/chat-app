import redis
import json
from typing import Optional, List, Dict
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        try:
            self.client = redis.Redis.from_url(
                settings.get_redis_url(),
                decode_responses=True,
                socket_timeout=5,
                socket_connect_timeout=5
            )
            # Test connection
            self.client.ping()
            logger.info("✅ Redis connected successfully")
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            # Fallback to dummy client for development
            self.client = None
    
    def is_available(self) -> bool:
        """Check if Redis is available"""
        if self.client is None:
            return False
        try:
            self.client.ping()
            return True
        except:
            return False
    
    def add_active_user(self, user_id: int) -> None:
        """Track active user"""
        if not self.is_available():
            return
        try:
            self.client.sadd("active_users", user_id)
        except Exception as e:
            logger.error(f"Redis error: {e}")
    
    def remove_active_user(self, user_id: int) -> None:
        """Remove active user"""
        if not self.is_available():
            return
        try:
            self.client.srem("active_users", user_id)
        except Exception as e:
            logger.error(f"Redis error: {e}")
    
    def is_user_active(self, user_id: int) -> bool:
        """Check if user is online"""
        if not self.is_available():
            return False
        try:
            return self.client.sismember("active_users", user_id)
        except Exception as e:
            logger.error(f"Redis error: {e}")
            return False
    
    def store_offline_message(self, receiver_id: int, message: Dict) -> None:
        """Store message for offline user"""
        if not self.is_available():
            return
        try:
            key = f"offline:{receiver_id}"
            self.client.lpush(key, json.dumps(message))
            self.client.expire(key, 604800)  # 7 days
        except Exception as e:
            logger.error(f"Redis error: {e}")
    
    def get_offline_messages(self, user_id: int, limit: int = 50) -> List[Dict]:
        """Retrieve offline messages"""
        if not self.is_available():
            return []
        try:
            key = f"offline:{user_id}"
            messages = self.client.lrange(key, 0, limit - 1)
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            logger.error(f"Redis error: {e}")
            return []
    
    def clear_offline_messages(self, user_id: int) -> None:
        """Clear offline messages after delivery"""
        if not self.is_available():
            return
        try:
            key = f"offline:{user_id}"
            self.client.delete(key)
        except Exception as e:
            logger.error(f"Redis error: {e}")
    
    def set_typing(self, sender_id: int, receiver_id: int, is_typing: bool = True) -> None:
        """Set typing indicator"""
        if not self.is_available():
            return
        try:
            key = f"typing:{sender_id}:{receiver_id}"
            if is_typing:
                self.client.setex(key, 5, "typing")
            else:
                self.client.delete(key)
        except Exception as e:
            logger.error(f"Redis error: {e}")

redis_client = RedisClient()