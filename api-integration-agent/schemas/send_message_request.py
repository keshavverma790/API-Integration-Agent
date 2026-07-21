from pydantic import BaseModel

class SendMesssageRequest(BaseModel):
    conversation_id: str
    content: str