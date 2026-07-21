from fastapi import APIRouter, Depends
from services.conversation_service import ConversationService

from db.database import get_db
from sqlalchemy.orm import Session

from schemas.send_message_request import SendMesssageRequest

router = APIRouter()

# Keep HTTP handlers thin by delegating persistence work to the service layer.
conversation_service = ConversationService()

@router.post("/create")
def create_conversation(db: Session = Depends(get_db)):
    """Create a conversation using the request-scoped database session."""
    conversation = conversation_service.create_conversation(db)
    return {"message": "Conversation created successfully.", "status_code": 201, "conversation": conversation.id}

@router.post("/message")
def send_message(request: SendMesssageRequest, db: Session = Depends(get_db)):
    """Validate and persist an incoming user message."""
    message = conversation_service.send_message(request.conversation_id, request.content, db)
    return {"message": "Message sent successfully.", "status_code": 201, "message_id": message.id}

@router.get("/{conversation_id}/messages")
def get_messages(conversation_id: str, db: Session = Depends(get_db)):
    """Retrieve every stored message for the supplied conversation ID."""
    messages = conversation_service.get_messages(conversation_id, db)
    return {"message": "Messages retrieved successfully.", "status_code": 200, "messages": messages}
