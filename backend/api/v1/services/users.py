from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.crud.users import get_or_add_user, get_users
from api.v1.schemas.users import UserCreate, UserResponse


async def get_or_add_user_service(db: AsyncSession, user: UserCreate) -> UserResponse:
    """
    Retrieve an existing user by name or add a new user if not found.

    Args:
        db (AsyncSession): The async database session.
        user (UserCreate): The user data to retrieve or create.

    Returns:
        UserResponse: The existing or newly created user.

    Raises:
        HTTPException: If the user could not be retrieved or created.
    """
    user_result = await get_or_add_user(db, user)
    if not user_result:
        raise HTTPException(status_code=500, detail="Unable to retrieve or create user")
    return user_result


async def get_users_service(db: AsyncSession) -> List[UserResponse]:
    """
    Retrieve all users from the database.

    Args:
        db (AsyncSession): The async database session.

    Returns:
        List[UserResponse]: A list of user objects.

    Raises:
        HTTPException: If no users are found in the database.
    """
    users = await get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users
