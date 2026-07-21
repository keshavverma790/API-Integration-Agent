from models.message import Message
from models.conversation import Conversation
from sqlalchemy.orm import Session
import uuid

class ConversationService:
    def create_conversation(self, db: Session) -> Conversation:
        primary_key = uuid.uuid4()    
        conversation = Conversation(id=primary_key)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
        
    def send_message(self, conversation_id: str, content: str, db: Session):
        primary_key = uuid.uuid4()
        message = Message(id=primary_key, role="user", content=content, conversation_id=conversation_id)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def get_messages(self, conversation_id: str, db: Session):
        messages = db.query(Message).filter(Message.conversation_id == conversation_id).all()
        return messages