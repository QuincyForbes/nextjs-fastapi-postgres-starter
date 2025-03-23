from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud.threads import get_threads
from models.thread import Thread


async def get_threads_service(thread_id: int, db: AsyncSession) -> List[Thread]:
    """
    Retrieve threads associated with a given thread ID.

    Args:
        thread_id (int): The ID of the thread to retrieve related threads for.
        db (AsyncSession): The async database session.

    Returns:
        List[Thread]: A list of thread objects.

    Raises:
        HTTPException: If no threads are found with the given ID.
    """
    threads = await get_threads(thread_id, db)
    if not threads:
        raise HTTPException(status_code=404, detail="No messages found for this thread")
    return threads
