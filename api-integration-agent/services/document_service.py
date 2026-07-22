from sqlalchemy.orm import Session
import uuid
from fastapi import UploadFile, HTTPException
from models.document import Document
from pathlib import Path
import shutil

# Local directory used to hold the uploaded file contents; the database stores metadata.
UPLOAD_ROOT = Path("uploads")

class DocumentService:
    def upload_document(self, file: UploadFile, db: Session) -> Document:
        """Validate a supported upload, store it locally, and persist its metadata."""
        
        # Validate file extension
        extension = Path(file.filename).suffix.lower()

        if extension != ".pdf" and extension != ".json":
            raise HTTPException(
                status_code=400,
                detail="Only PDF and JSON files are supported."
            )

        # Validate MIME type
        if file.content_type != "application/pdf" and file.content_type != "application/json":
            raise HTTPException(
                status_code=400,
                detail="Invalid content type. Only PDF and JSON files are supported."
            )

        # Generate the document ID first so the disk filename is collision-resistant.
        document_id = uuid.uuid4()

        # Preserve the original extension for easier file-type handling later.
        extension = Path(file.filename).suffix

        # Keep user-provided filenames out of the storage path while retaining them as metadata.
        stored_filename = f"{document_id}{extension}"

        # Ensure upload directory exists
        UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)

        # Full destination path
        stored_path = UPLOAD_ROOT / stored_filename

        # Save the file to disk
        with stored_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Persist only file metadata; the content itself remains on the local filesystem.
        document = Document(
            id=document_id,
            original_filename=file.filename,
            stored_filename=stored_filename,
            stored_path=str(stored_path),
            file_type=file.content_type,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document
    
