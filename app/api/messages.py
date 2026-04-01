from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/send", response_model=MessageResponse, status_code=201)
async def send_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Send a new message"""
    try:
        return await MessageService.send_message(db, message, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/conversation/{user_id}", response_model=List[MessageResponse])
async def get_conversation(
    user_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get conversation with another user"""
    return MessageService.get_conversation(db, current_user.id, user_id, limit, offset)

@router.get("/unread/count")
async def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get unread message count"""
    return {"unread_count": MessageService.get_unread_count(db, current_user.id)}

@router.post("/read")
async def mark_read(
    message_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mark messages as read"""
    count = MessageService.mark_as_read(db, message_ids, current_user.id)
    return {"marked_read_count": count}