from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class User(Base):
    """
    Represents a user of the system.

    Attributes:
        id (int): The unique identifier for the user. Automatically incremented.
        name (str): The username. Must be unique and no longer than 30 characters.

    Methods:
        __repr__(): Returns a string representation of the User instance.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"
