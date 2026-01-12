from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, auth
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/uploads", tags=["Uploads"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@router.post("/", response_model=schemas.UploadResponse)
async def create_upload(
    description: str = "",
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    # Upload to Supabase
    file_content = await file.read()
    filename = f"{current_user.id}/{file.filename}"
    
    public_url = ""
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            # Ensure bucket exists or handle error (assuming 'uploads' bucket exists)
            # supabase.storage.create_bucket("uploads") 
            supabase.storage.from_("uploads").upload(filename, file_content)
            # Construct public URL (assuming public bucket)
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/uploads/{filename}"
        except Exception as e:
            print(f"Supabase upload failed: {e}")
            public_url = f"mock_url/{filename}"
    else:
        public_url = f"mock_url/{filename}"

    new_upload = models.Upload(
        client_id=current_user.id,
        filename=file.filename,
        file_url=public_url,
        description=description
    )
    db.add(new_upload)
    db.commit()
    db.refresh(new_upload)
    return new_upload

@router.get("/", response_model=List[schemas.UploadResponse])
def read_uploads(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    if current_user.role == models.UserRole.ADMIN:
        uploads = db.query(models.Upload).offset(skip).limit(limit).all()
    else:
        uploads = db.query(models.Upload).filter(models.Upload.client_id == current_user.id).offset(skip).limit(limit).all()
    return uploads
