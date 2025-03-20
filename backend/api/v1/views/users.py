from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from api.v1.views.crud import get_or_add_user
from db.db import get_db
from models.user import User
from api.v1.views.schemas import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (UserCreate): The user data containing the name.
        db (Session, optional): Database session dependency.

    Returns:
        UserResponse: The created user object.

    Raises:
        HTTPException: If an unexpected error occurs during user creation.
    """
    try:
        new_user = await get_or_add_user(db, user.name)
        return new_user
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/users", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    """
    Retrieve all users from the database.

    Args:
        db (Session, optional): Database session dependency.

    Returns:
        List[UserResponse]: A list of user objects.

    Raises:
        HTTPException: If no users are found in the database.
    """
    users = await db.scalars(select(User))
    users = users.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
