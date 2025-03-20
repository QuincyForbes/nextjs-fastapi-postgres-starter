from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from api.v1.views.crud import add_message
from db.db import get_db
from models.message import Message
from api.v1.views.schemas import MessageCreate, MessageResponse


router = APIRouter()


@router.post("/messages", status_code=201, response_model=MessageResponse)
async def create_message(message_data: MessageCreate, db: Session = Depends(get_db)):
    """
    Create a new message in a specific thread.

    Args:
        message_data (MessageCreate): The message details, including thread ID, user ID, and message content.
        db (Session, optional): Database session dependency.

    Returns:
        MessageResponse: The created message object.

    Raises:
        HTTPException: If the message cannot be created due to an error.
    """
    try:
        new_message = await add_message(
            db, message_data.thread_id, message_data.user_id, message_data.message
        )
        if not new_message:
            raise HTTPException(status_code=500, detail="Unable to create message")
        return new_message
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Unable to create message: {str(e)}"
        )


@router.get("/messages", response_model=List[MessageResponse])
async def get_messages(thread_id: int, db: AsyncSession = Depends(get_db)):
    """
    Retrieve all messages in a given thread.

    Args:
        thread_id (int): The ID of the thread to retrieve messages from.
        db (AsyncSession, optional): Database session dependency.

    Returns:
        List[MessageResponse]: A list of messages within the specified thread.

    Raises:
        HTTPException: If no messages are found for the given thread ID.
    """
    stmt = select(Message).filter(Message.thread_id == thread_id)
    result = await db.execute(stmt)
    messages = result.scalars().all()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this thread")

    return messages
