from typing import Optional

from pydantic import BaseModel


class MessageCreate(BaseModel):
    thread_id: Optional[int]
    user_id: int
    message: str


class MessageResponse(BaseModel):
    id: int
    thread_id: int
    sender_type: Optional[str]
    content: str

    class Config:
        from_attributes = True
