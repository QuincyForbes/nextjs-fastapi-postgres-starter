from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.messages import MessageCreate, MessageResponse
from api.v1.services.messages import create_message_service, get_messages_service
from db.db import get_db

router = APIRouter()


@router.post("/messages", status_code=201, response_model=MessageResponse)
async def create_message(
    message_data: MessageCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new message in a thread.

    - **message_data**: Includes thread ID, user ID, and message content.
    - **Returns**: The created message.
    """
    return await create_message_service(message_data, db)


@router.get("/messages", status_code=200, response_model=List[MessageResponse])
async def get_messages(thread_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get all messages from a specific thread.

    - **thread_id**: ID of the thread to fetch messages from.
    - **Returns**: A list of messages in the thread.
    """
    return await get_messages_service(thread_id, db)
