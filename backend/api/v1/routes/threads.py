from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.v1.schemas.threads import ThreadResponse
from api.v1.services.threads import get_threads_service
from db.db import get_db

router = APIRouter()


@router.get("/threads", status_code=200, response_model=List[ThreadResponse])
async def get_threads(user_id: int, db: Session = Depends(get_db)):
    """
    Get all threads for a specific user.

    - **user_id**: ID of the user to fetch threads for.
    - **Returns**: A list of threads associated with the user.
    """
    return await get_threads_service(user_id, db)
