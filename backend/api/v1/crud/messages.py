import random
from typing import List, Optional

from psycopg2 import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud.threads import add_thread
from models.message import Message


async def add_message(
    db: AsyncSession, thread_id: Optional[int], user_id: int, content: str
) -> Optional[Message]:
    """
    Adds a new message to a thread. If no thread ID is provided, a new thread is created.
    Also generates a system-generated reply message.

    Args:
        db (AsyncSession): The asynchronous database session.
        thread_id (Optional[int]): The ID of the thread, or None to create a new one.
        user_id (int): The ID of the user sending the message.
        content (str): The message content.

    Returns:
        Optional[Message]: The system-generated response message, or None if operation fails.
    """
    try:
        if thread_id is None:
            thread = await add_thread(db, user_id)
            if not thread:
                return None
            thread_id = thread.id

        user_message = Message(thread_id=thread_id, content=content, sender_type="User")
        db.add(user_message)

        bot_message = Message(
            thread_id=thread_id,
            content=str(random.randint(1, 100)),
            sender_type="System",
        )
        db.add(bot_message)

        await db.commit()
        await db.refresh(user_message)
        await db.refresh(bot_message)

        return bot_message
    except IntegrityError:
        await db.rollback()
        return None


async def get_message(
    thread_id: Optional[int],
    db: AsyncSession,
) -> List[Message]:
    """
    Retrieves all messages associated with a given thread ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        thread_id (Optional[int]): The ID of the thread.

    Returns:
        List[Message]: A list of messages in the thread.
    """
    stmt = select(Message).filter(Message.thread_id == thread_id)
    result = await db.execute(stmt)
    messages = result.scalars().all()
    return messages
