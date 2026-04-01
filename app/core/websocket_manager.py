from typing import Dict
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int) -> None:
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        logger.info(f"User {user_id} connected. Active: {len(self.active_connections)}")
    
    def disconnect(self, user_id: int) -> None:
        """Remove disconnected user"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"User {user_id} disconnected")
    
    async def send_message(self, user_id: int, message: dict) -> bool:
        """Send message to specific user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
                return True
            except Exception as e:
                logger.error(f"Failed to send to {user_id}: {e}")
        return False
    
    async def send_typing(self, sender_id: int, receiver_id: int, is_typing: bool) -> None:
        """Send typing indicator"""
        await self.send_message(receiver_id, {
            "type": "typing",
            "data": {"user_id": sender_id, "is_typing": is_typing}
        })

manager = ConnectionManager()