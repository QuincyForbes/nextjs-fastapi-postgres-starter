from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from db.db import get_db
from models.thread import Thread
from api.v1.views.schemas import ThreadResponse

router = APIRouter()


@router.get("/threads", response_model=List[ThreadResponse])
async def get_threads(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all threads associated with a specific user.

    Args:
        user_id (int): The ID of the user whose threads are being retrieved.
        db (Session, optional): Database session dependency.

    Returns:
        List[ThreadResponse]: A list of thread objects for the specified user.

    Raises:
        HTTPException: If no threads are found for the given user.
    """
    stmt = select(Thread).filter(Thread.user_id == user_id)
    result = await db.execute(stmt)
    threads = result.scalars().all()

    if not threads:
        raise HTTPException(status_code=404, detail="No threads found for this user")

    return threads
