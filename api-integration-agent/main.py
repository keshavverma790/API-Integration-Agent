from fastapi import FastAPI
from api.health import router as health_router
from api.conversation_controller import router as conversation_router

app = FastAPI()

# Register lightweight operational endpoints before the conversation API.
app.include_router(health_router)
# Group all conversation endpoints under a shared URL prefix.
app.include_router(conversation_router, prefix="/conversation", tags=["Conversation"])