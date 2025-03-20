from typing import Optional
from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ThreadCreate(BaseModel):
    name: str


class ThreadResponse(BaseModel):
    id: int
    user_id: int

    class Config:
        from_attributes = True


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
