from fastapi import APIRouter, UploadFile
import os
import pathlib
from models.models import FileUpload
from services.dbconnection import SessionLocal

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Server is running!"}

@router.post("/upload")
async def upload_file(file: UploadFile):
    filename = pathlib.Path(file.filename).name

    # Create uploads folder
    os.makedirs("uploads", exist_ok=True)
    file_location = f"uploads/{filename}"

    # Save file in chunks
    with open(file_location, "wb") as f:
        while chunk := await file.read(1024*1024):
            f.write(chunk)

    # breakpoint()
    # Save metadata to DB
    db = SessionLocal()
    try:
        new_file = FileUpload(
            filename=filename,
            content_type=file.content_type,
            file_path=file_location,
            is_synced=False
        )
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
    finally:
        db.close()

    return {
        "filename": new_file.filename,
        "content_type": new_file.content_type,
        "file_path": new_file.file_path,
        "is_synced": new_file.is_synced
    }
