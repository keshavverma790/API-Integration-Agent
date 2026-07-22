from datetime import datetime
from sqlalchemy import DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from db.database import Base

class Conversation(Base):
    """Persist a conversation and the timestamps that describe its lifecycle."""
    __tablename__ = "conversations"
    
    # UUIDs let clients create and reference conversations without sequential IDs.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
        
    # Database-generated timestamps keep audit times consistent across clients.
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
    
    # Association records provide the conversation-to-document many-to-many link.
    documents = relationship(
        "ConversationDocument",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
