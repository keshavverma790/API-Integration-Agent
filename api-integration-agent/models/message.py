import uuid
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func, ForeignKey, UUID
from datetime import datetime

class Message(Base):
    """Persist one role-labelled message belonging to a conversation."""
    __tablename__ = "messages"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
        )
    
    # The role identifies the author type, such as "user" or a future assistant.
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False
        )
    
    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
        )
    
    # Each message must belong to an existing conversation.
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False
    )
    
    # Timestamps are generated in the database and updated on model changes.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
