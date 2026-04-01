from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
import json
import logging
from app.core.database import get_db
from app.core.websocket_manager import manager
from app.core.redis_client import redis_client
from app.services.message_service import MessageService
from app.services.offline_service import OfflineService
from app.schemas.message import MessageCreate

router = APIRouter(tags=["WebSocket"])
logger = logging.getLogger(__name__)

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    """WebSocket connection endpoint"""
    await manager.connect(websocket, user_id)
    redis_client.add_active_user(user_id)
    
    # Deliver offline messages
    await OfflineService.deliver_offline_messages(db, user_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message["type"] == "message":
                # Send message
                msg_data = message["data"]
                msg = MessageCreate(content=msg_data["content"], receiver_id=msg_data["receiver_id"])
                await MessageService.send_message(db, msg, user_id)
            
            elif message["type"] == "typing":
                # Send typing indicator
                receiver_id = message["data"]["receiver_id"]
                is_typing = message["data"].get("is_typing", True)
                redis_client.set_typing(user_id, receiver_id, is_typing)
                await manager.send_typing(user_id, receiver_id, is_typing)
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        redis_client.remove_active_user(user_id)
        logger.info(f"User {user_id} disconnected")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(user_id)
        redis_client.remove_active_user(user_id)