from models.message import Message
from models.conversation import Conversation
from models.conversation_document import ConversationDocument
from schemas.create_conversation_request import CreateConversationRequest
from sqlalchemy.orm import Session
import uuid

class ConversationService:
    def create_conversation(self, request: CreateConversationRequest, db: Session) -> Conversation:
        """Create a conversation and link each requested document to it."""
        # Generate the UUID in the service so it is available before persistence.
        primary_key = uuid.uuid4()    
        conversation = Conversation(id=primary_key)
        db.add(conversation)
        
        # The association table supports many documents per conversation and reuse per document.
        for document_id in request.document_ids:
            mapping = ConversationDocument(
                conversation_id=conversation.id,
                document_id=document_id
            )

            db.add(mapping)
    
        db.commit()
        db.refresh(conversation)
        return conversation
        
    def send_message(self, conversation_id: str, content: str, db: Session):
        """Store a user message for the requested conversation."""
        primary_key = uuid.uuid4()
        message = Message(id=primary_key, role="user", content=content, conversation_id=conversation_id)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def get_messages(self, conversation_id: str, db: Session):
        """Return all messages currently stored for a conversation."""
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
        return messages
