from typing import Optional
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models.message import Message
from models.thread import Thread
from models.user import User
import random


async def get_or_add_user(db: AsyncSession, name: str) -> User | None:
    """
    Gets an existing user with the given name or creates a new one if it doesn't exist.

    Args:
        db (AsyncSession): The asynchronous database session.
        name (str): The name of the user to get or create.

    Returns:
        User | None: The existing or newly created user object if successful, otherwise None.

    Raises:
        IntegrityError: If there is a database constraint violation.
    """
    try:
        # First try to find an existing user with this name
        stmt = select(User).where(User.name == name)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        # If user exists, return it
        if existing_user:
            return existing_user

        # Otherwise create a new user
        new_user = User(name=name)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except IntegrityError:
        await db.rollback()
        return None


async def add_thread(db: AsyncSession, user_id: int) -> Thread | None:
    """
    Creates a new thread asynchronously and commits it to the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user who owns the thread.

    Returns:
        Thread | None: The newly created thread object if successful, otherwise None.

    Raises:
        IntegrityError: If there is a database constraint violation.
    """
    try:
        new_thread = Thread(user_id=user_id)
        db.add(new_thread)
        await db.commit()
        await db.refresh(new_thread)
        return new_thread
    except IntegrityError:
        await db.rollback()
        return None


async def add_thread(db: AsyncSession, user_id: int) -> int:
    """
    Creates a new thread and returns its ID.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user for whom the thread is created.

    Returns:
        int: The ID of the newly created thread.
    """
    try:
        new_thread = Thread(user_id=user_id)
        db.add(new_thread)
        await db.commit()
        await db.refresh(new_thread)
        return new_thread.id
    except IntegrityError:
        await db.rollback()
        return None


async def add_message(
    db: AsyncSession, thread_id: Optional[int], user_id: int, content: str
) -> Message | None:
    """
    Creates a new message asynchronously. If no thread ID is provided,
    a new thread is created before adding the message. The function
    also generates an automated system response.

    Args:
        db (AsyncSession): The asynchronous database session.
        thread_id (Optional[int]): The ID of the thread to which the message belongs. If None, a new thread is created.
        user_id (int): The ID of the user sending the message.
        content (str): The content of the message.

    Returns:
        Message | None: The system-generated response message if successful, otherwise None.

    Raises:
        IntegrityError: If there is a database constraint violation.
    """
    try:
        if thread_id is None:
            thread_id = await add_thread(db, user_id)

        # User's message
        user_message = Message(thread_id=thread_id, content=content, sender_type="User")
        db.add(user_message)

        # System-generated response
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
