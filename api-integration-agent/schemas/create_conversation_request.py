from pydantic import BaseModel
import uuid

class CreateConversationRequest(BaseModel):
    """Validate the document IDs to associate with a new conversation."""
    document_ids: list[uuid.UUID]
