from sqlalchemy.orm import Session
from app.models.message import Message
from app.core.redis_client import redis_client
from app.core.websocket_manager import manager
import logging

logger = logging.getLogger(__name__)

class OfflineService:
    
    @staticmethod
    async def deliver_offline_messages(db: Session, user_id: int) -> list:
        """Deliver all offline messages to user"""
        messages = redis_client.get_offline_messages(user_id)
        
        if not messages:
            return []
        
        delivered = []
        for msg_data in messages:
            # Check if message already exists
            existing = db.query(Message).filter(Message.id == msg_data["id"]).first()
            if not existing:
                msg = Message(**msg_data)
                db.add(msg)
                delivered.append(msg)
        
        db.commit()
        
        if delivered:
            await manager.send_message(user_id, {
                "type": "offline_messages",
                "data": {
                    "count": len(delivered),
                    "messages": [{
                        "id": m.id,
                        "content": m.content,
                        "sender_id": m.sender_id,
                        "created_at": m.created_at.isoformat()
                    } for m in delivered]
                }
            })
        
        redis_client.clear_offline_messages(user_id)
        return delivered