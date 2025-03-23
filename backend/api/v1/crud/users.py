from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User


async def get_or_add_user(db: AsyncSession, name: str) -> Optional[User]:
    """
    Retrieves an existing user by name, or creates a new user if not found.

    Args:
        db (AsyncSession): The asynchronous database session.
        name (str): The name of the user to retrieve or create.

    Returns:
        Optional[User]: The existing or newly created user, or None if operation fails.
    """
    try:
        stmt = select(User).where(User.name == name)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            return existing_user

        new_user = User(name=name)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    except IntegrityError:
        await db.rollback()
        stmt = select(User).where(User.name == name)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()


async def get_users(db: AsyncSession) -> List[User]:
    """
    Retrieves all users from the database.

    Args:
        db (AsyncSession): The asynchronous database session.

    Returns:
        List[User]: A list of all users.
    """
    users = await db.scalars(select(User))
    return users.all()
