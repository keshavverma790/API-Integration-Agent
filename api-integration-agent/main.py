from fastapi import FastAPI
from api.health import router as health_router
from api.conversation_controller import router as conversation_router

app = FastAPI()

app.include_router(health_router)
app.include_router(conversation_router, prefix="/conversation", tags=["Conversation"])