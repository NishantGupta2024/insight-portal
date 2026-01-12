from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import database, schemas, models, auth
from ..utils.email import send_email_async
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/reports", tags=["Reports"])

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

@router.post("/", response_model=schemas.ReportResponse)
async def create_report(
    title: str,
    client_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_admin),
    db: Session = Depends(database.get_db)
):
    # Upload to Supabase
    file_content = await file.read()
    filename = f"reports/{client_id}/{file.filename}"
    
    public_url = ""
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            supabase.storage.from_("reports").upload(filename, file_content)
            public_url = f"{SUPABASE_URL}/storage/v1/object/public/reports/{filename}"
        except Exception as e:
            print(f"Supabase upload failed: {e}")
            public_url = f"mock_url/{filename}"
    else:
        public_url = f"mock_url/{filename}"

    new_report = models.Report(
        admin_id=current_user.id,
        client_id=client_id,
        title=title,
        report_url=public_url
    )
    db.add(new_report)
    db.flush() 



    # Create Notification (DB)
    notification = models.Notification(
        user_id=client_id,
        message=f"New report '{title}' is available."
    )
    db.add(notification)
    
    # Send Email Notification
    client_user = db.query(models.User).filter(models.User.id == client_id).first()
    print(f"DEBUG: Found user {client_user.email if client_user else 'None'} for ID {client_id}")
    if client_user and client_user.email:
        email_body = f"""
        <h1>New Report Available</h1>
        <p>Hello {client_user.full_name},</p>
        <p>A new report titled <b>{title}</b> has been uploaded to your dashboard.</p>
        <p>Please login to view and download it.</p>
        <br>
        <p>Best regards,<br>InsightData Team</p>
        """
        await send_email_async(f"New Report: {title}", [client_user.email], email_body)

    db.commit()
    db.refresh(new_report)
    return new_report

@router.get("/", response_model=List[schemas.ReportResponse])
def read_reports(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(database.get_db)
):
    if current_user.role == models.UserRole.ADMIN:
        reports = db.query(models.Report).offset(skip).limit(limit).all()
    else:
        reports = db.query(models.Report).filter(models.Report.client_id == current_user.id).offset(skip).limit(limit).all()
    return reports
