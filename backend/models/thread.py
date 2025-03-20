from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base


class Thread(Base):
    """
    Represents a thread in a messaging system, linking messages to a specific user.

    Attributes:
        id (int): The primary key of the thread.
        user_id (int): Foreign key linking the thread to a specific user.
        messages (List[Message]): A list of messages associated with the thread.

    Relationships:
        messages (Message): Establishes a relationship with the `Message` model,
                             allowing access to all messages within the thread.

    Example:
        ```python
        thread = Thread(user_id=1)
        print(thread)  # Output: <Thread id=1 user_id=1>
        ```
    """

    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    messages = relationship("Message", back_populates="thread")

    def __repr__(self):
        """Returns a string representation of the Thread object."""
        return f"<Thread id={self.id} user_id={self.user_id}>"
