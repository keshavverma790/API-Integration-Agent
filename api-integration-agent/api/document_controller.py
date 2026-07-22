from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from db.database import get_db
from services.document_service import DocumentService

router = APIRouter()

# The controller delegates validation, disk storage, and persistence to this service.
document_service = DocumentService()

@router.post("/upload")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Accept a document upload and return its generated database ID."""
    document = document_service.upload_document(file, db)
    return {
        "message": "Document uploaded successfully.",
        "status_code": 201,
        "document_id": str(document.id),
    }
