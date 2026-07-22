import uuid
from datetime import datetime
from sqlalchemy import DateTime, String, UUID, func
from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Document(Base):
    """Persist a document and the timestamps that describe its lifecycle."""
    __tablename__ = "documents"
    
    # UUIDs let clients create and reference documents without sequential IDs.
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    
    # Retain the client filename for display while using a generated name on disk.
    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # This generated filename is the filesystem-safe reference to the upload.
    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    # The relative local path points to the file contents stored outside the database.
    stored_path: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    file_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
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
    
    # Join records connect this document to one or more conversations.
    conversations = relationship(
        "ConversationDocument",
        back_populates="document",
        cascade="all, delete-orphan"
    )
