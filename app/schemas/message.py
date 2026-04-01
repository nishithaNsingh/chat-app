from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class MessageBase(BaseModel):
    content: str = Field(..., max_length=1000)
    receiver_id: int

class MessageCreate(MessageBase):
    pass

class MessageResponse(BaseModel):
    id: int
    content: str
    sender_id: int
    receiver_id: int
    created_at: datetime
    is_read: bool
    read_at: Optional[datetime]
    is_offline_message: bool
    
    class Config:
        from_attributes = True

class OfflineMessageResponse(BaseModel):
    messages: List[MessageResponse]
    has_more: bool