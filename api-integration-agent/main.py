from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.health import router as health_router
from api.conversation_controller import router as conversation_router
from api.document_controller import router as document_router

app = FastAPI()

# Register lightweight operational endpoints before the conversation API.
app.include_router(health_router)

# Group all conversation endpoints under a shared URL prefix.
app.include_router(conversation_router, prefix="/conversation", tags=["Conversation"])

# Expose document-upload operations under their own API namespace.
app.include_router(document_router, prefix="/document", tags=["Document"])

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """Return FastAPI HTTP errors in the application's common response shape."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
        },
    )
