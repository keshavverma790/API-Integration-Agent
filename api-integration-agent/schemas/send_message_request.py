from pydantic import BaseModel

class SendMesssageRequest(BaseModel):
    """Validate the payload accepted by the send-message endpoint."""
    conversation_id: str
    content: str
