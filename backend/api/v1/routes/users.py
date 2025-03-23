from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.schemas.users import UserCreate, UserResponse
from api.v1.services.users import get_or_add_user_service, get_users_service
from db.db import get_db

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def get_or_add_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Create or retrieve a user by name.

    - **user**: User data containing the name.
    - **Returns**: The existing or newly created user.
    """
    return await get_or_add_user_service(db, user.name)


@router.get("/users", status_code=200, response_model=List[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db)):
    """
    Get all users from the database.

    - **Returns**: A list of all users.
    """
    return await get_users_service(db)
