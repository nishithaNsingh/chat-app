from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate
from app.core.redis_client import redis_client
from app.core.websocket_manager import manager
import logging

logger = logging.getLogger(__name__)

class MessageService:
    
    @staticmethod
    async def send_message(db: Session, message: MessageCreate, sender_id: int) -> Message:
        """Send a message"""
        # Verify receiver exists
        receiver = db.query(User).filter(User.id == message.receiver_id).first()
        if not receiver:
            raise ValueError("Receiver not found")
        
        # Check if receiver is online
        is_online = redis_client.is_user_active(message.receiver_id)
        
        # Create message
        db_message = Message(
            content=message.content,
            sender_id=sender_id,
            receiver_id=message.receiver_id,
            is_offline_message=not is_online
        )
        
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        
        # If offline, store in Redis
        if not is_online:
            redis_client.store_offline_message(message.receiver_id, {
                "id": db_message.id,
                "content": db_message.content,
                "sender_id": db_message.sender_id,
                "receiver_id": db_message.receiver_id,
                "created_at": db_message.created_at.isoformat(),
                "is_offline_message": True
            })
            logger.info(f"Stored offline message for user {message.receiver_id}")
        else:
            # Send real-time
            await manager.send_message(message.receiver_id, {
                "type": "message",
                "data": {
                    "id": db_message.id,
                    "content": db_message.content,
                    "sender_id": db_message.sender_id,
                    "created_at": db_message.created_at.isoformat()
                }
            })
        
        return db_message
    
    @staticmethod
    def get_conversation(db: Session, user1: int, user2: int, limit: int = 50, offset: int = 0) -> List[dict]:
        """Get conversation history"""
        messages = db.query(Message).filter(
            or_(
                and_(Message.sender_id == user1, Message.receiver_id == user2),
                and_(Message.sender_id == user2, Message.receiver_id == user1)
            )
        ).order_by(Message.created_at.desc()).offset(offset).limit(limit).all()
        
        return [{
            "id": m.id,
            "content": m.content,
            "sender_id": m.sender_id,
            "receiver_id": m.receiver_id,
            "created_at": m.created_at.isoformat(),
            "is_read": m.is_read,
            "is_offline_message": m.is_offline_message
        } for m in messages]
    
    @staticmethod
    def mark_as_read(db: Session, message_ids: List[int], user_id: int) -> int:
        """Mark messages as read"""
        updated = db.query(Message).filter(
            Message.id.in_(message_ids),
            Message.receiver_id == user_id,
            Message.is_read == False
        ).update({"is_read": True, "read_at": datetime.utcnow()}, synchronize_session=False)
        
        db.commit()
        return updated
    
    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """Get unread message count"""
        return db.query(Message).filter(
            Message.receiver_id == user_id,
            Message.is_read == False
        ).count()