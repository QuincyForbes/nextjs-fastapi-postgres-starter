from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud.messages import add_message, get_message
from api.v1.schemas.messages import MessageCreate
from models.message import Message


async def create_message_service(
    message_data: MessageCreate, db: AsyncSession
) -> Message:
    """
    Create a new message in a specific thread.

    Args:
        message_data (MessageCreate): The data of the message to be created, including thread_id, user_id, and message content.
        db (AsyncSession): The database session.

    Returns:
        Message: The newly created message object.

    Raises:
        HTTPException: If the message could not be created.
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


async def get_messages_service(thread_id: int, db: AsyncSession) -> List[Message]:
    """
    Retrieve all messages from a specific thread.

    Args:
        thread_id (int): The ID of the thread.
        db (AsyncSession): The database session.

    Returns:
        List[Message]: A list of message objects in the specified thread.

    Raises:
        HTTPException: If no messages are found for the thread.
    """
    messages = await get_message(thread_id, db)
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this thread")
    return messages
