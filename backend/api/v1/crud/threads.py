from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.thread import Thread


async def add_thread(db: AsyncSession, user_id: int) -> Optional[Thread]:
    """
    Creates a new thread for a user.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_id (int): The ID of the user creating the thread.

    Returns:
        Optional[Thread]: The created thread, or None if creation fails.
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


async def get_threads(user_id: int, db: AsyncSession) -> List[Thread]:
    """
    Retrieves all threads associated with a given user ID.

    Args:
        user_id (int): The ID of the user.
        db (AsyncSession): The asynchronous database session.

    Returns:
        List[Thread]: A list of threads belonging to the user.
    """
    stmt = select(Thread).filter(Thread.user_id == user_id)
    result = await db.execute(stmt)
    threads = result.scalars().all()
    return threads
