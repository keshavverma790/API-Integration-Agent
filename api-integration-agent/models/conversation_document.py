import uuid
from sqlalchemy import ForeignKey, DateTime, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.database import Base


class ConversationDocument(Base):
    """Join table that associates documents with conversations."""
    __tablename__ = "conversation_documents"

    # The two foreign keys form a composite key, preventing duplicate links.
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        primary_key=True,
    )

    document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        primary_key=True,
    )
    
    # Database-generated timestamps keep audit times consistent across clients.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # ORM relationships make the association navigable from either parent model.
    conversation = relationship("Conversation", back_populates="documents")
    document = relationship("Document", back_populates="conversations")
