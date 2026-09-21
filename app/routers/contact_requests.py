import logging
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Union
from app.database import get_db
from app.models import ContactRequest
from app.schemas import ContactRequestCreate, ContactRequestUpdate, ContactRequest as ContactRequestSchema
from app.auth import get_current_admin
from app.services.loops_service import send_new_contact_request_email, subscribe_contact_to_promotions
from app.services.cloudinary_service import upload_image

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/")
async def create_contact_request(contact: ContactRequestCreate, db: Session = Depends(get_db)) -> Union[ContactRequestSchema, dict]:
    """Create a new contact request (public)"""
    # Honeypot validation - silently discard if filled
    if contact.honeypot:
        return JSONResponse(status_code=200, content={"message": "Contact request received"})
    
    # Remove honeypot field before saving to database
    contact_data = contact.model_dump(exclude={"honeypot"})
    
    db_contact = ContactRequest(**contact_data)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    
    # Send notification email to admin
    try:
        await send_new_contact_request_email(
            client_name=db_contact.client_name,
            pet_name=db_contact.pet_name,
            client_email=db_contact.email,
            whatsapp=db_contact.whatsapp,
            country=db_contact.country,
        )
    except Exception:
        logger.exception("Error sending new contact request email")
    
    # Subscribe to promotions if requested
    if db_contact.wants_promotions:
        try:
            await subscribe_contact_to_promotions(
                email=db_contact.email,
                first_name=db_contact.client_name,
            )
        except Exception:
            logger.exception("Error subscribing contact to promotions")
    
    return db_contact

@router.get("/", response_model=list[ContactRequestSchema])
def get_contact_requests(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Get all contact requests (admin only)"""
    contact_requests = db.query(ContactRequest).all()
    return contact_requests

@router.get("/{request_id}", response_model=ContactRequestSchema)
def get_contact_request(request_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Get a single contact request by ID (admin only)"""
    contact_request = db.query(ContactRequest).filter(ContactRequest.id == request_id).first()
    if not contact_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact request not found")
    return contact_request

@router.put("/{request_id}", response_model=ContactRequestSchema)
def update_contact_request(request_id: int, contact: ContactRequestUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Update a contact request (admin only)"""
    db_contact = db.query(ContactRequest).filter(ContactRequest.id == request_id).first()
    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact request not found")
    
    update_data = contact.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contact, key, value)
    
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/{request_id}")
def delete_contact_request(request_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Delete a contact request (admin only)"""
    contact_request = db.query(ContactRequest).filter(ContactRequest.id == request_id).first()
    if not contact_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact request not found")
    
    db.delete(contact_request)
    db.commit()
    return {"message": "Contact request deleted successfully"}

@router.post("/upload-pet-image")
async def upload_pet_image(file: UploadFile):
    """Upload a pet image to Cloudinary (public)"""
    image_url = await upload_image(file)
    return {"url": image_url}
