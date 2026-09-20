from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Testimonial
from app.schemas import TestimonialCreate, TestimonialUpdate, Testimonial as TestimonialSchema
from app.auth import get_current_admin, get_current_admin_optional

router = APIRouter()

@router.get("/", response_model=list[TestimonialSchema])
def get_testimonials(db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin_optional)):
    """Get all testimonials (admin) or only visible ones (public)"""
    query = db.query(Testimonial)
    if current_admin is None:
        query = query.filter(Testimonial.visible == True)
    testimonials = query.all()
    return testimonials

@router.get("/{testimonial_id}", response_model=TestimonialSchema)
def get_testimonial(testimonial_id: int, db: Session = Depends(get_db)):
    """Get a single testimonial by ID"""
    testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    return testimonial

@router.post("/", response_model=TestimonialSchema)
def create_testimonial(testimonial: TestimonialCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Create a new testimonial (admin only)"""
    db_testimonial = Testimonial(**testimonial.model_dump())
    db.add(db_testimonial)
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial

@router.put("/{testimonial_id}", response_model=TestimonialSchema)
def update_testimonial(testimonial_id: int, testimonial: TestimonialUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Update a testimonial (admin only)"""
    db_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    
    update_data = testimonial.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_testimonial, key, value)
    
    db.commit()
    db.refresh(db_testimonial)
    return db_testimonial

@router.delete("/{testimonial_id}")
def delete_testimonial(testimonial_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Delete a testimonial (admin only)"""
    db_testimonial = db.query(Testimonial).filter(Testimonial.id == testimonial_id).first()
    if not db_testimonial:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Testimonial not found")
    
    db.delete(db_testimonial)
    db.commit()
    return {"message": "Testimonial deleted successfully"}
