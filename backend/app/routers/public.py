from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import database, schemas, models

router = APIRouter(tags=["Public"])

@router.post("/contact")
def submit_inquiry(inquiry: schemas.InquiryCreate, db: Session = Depends(database.get_db)):
    db_inquiry = models.Inquiry(**inquiry.dict())
    db.add(db_inquiry)
    db.commit()
    return {"message": "Inquiry received"}
