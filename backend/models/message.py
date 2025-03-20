import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from models.base import Base


class Message(Base):
    """
    Represents a message in a threaded conversation.

    Attributes:
        id (int): The primary key of the message.
        thread_id (int): Foreign key linking the message to a specific thread.
        content (str): The text content of the message.
        sender_type (str): Indicates whether the sender is a 'User' or 'System'.
        created_at (datetime): Timestamp of when the message was created.

    Relationships:
        thread (Thread): Establishes a relationship with the `Thread` model,
                         allowing access to the thread's messages.

    Example:
        ```python
        message = Message(thread_id=1, content="Hello!", sender_type="User")
        print(message)  # Output: <Message id=1 thread_id=1 sender_type=User>
        ```
    """

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    thread_id = Column(Integer, ForeignKey("threads.id"), nullable=False)
    content = Column(String, nullable=False)
    sender_type = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # Relationships
    thread = relationship("Thread", back_populates="messages")

    def __repr__(self):
        """Returns a string representation of the Message object."""
        return (
            f"<Message id={self.id} thread_id={self.thread_id} "
            f"sender_type={self.sender_type}>"
        )
