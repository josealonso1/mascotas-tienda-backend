from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from fastapi import UploadFile
from app.models import ContactStatus

# Artwork schemas
class ArtworkBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: str
    visible: bool = True

class ArtworkCreate(ArtworkBase):
    pass

class ArtworkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    visible: Optional[bool] = None

class Artwork(ArtworkBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Testimonial schemas
class TestimonialBase(BaseModel):
    client_name: str
    content: str
    artwork_id: Optional[int] = None

class TestimonialCreate(TestimonialBase):
    visible: bool = False

class PublicTestimonialCreate(BaseModel):
    client_name: str = Field(min_length=2, max_length=80)
    content: str = Field(min_length=10, max_length=1000)
    artwork_id: Optional[int] = None
    honeypot: str = Field(default="", description="Honeypot field for spam protection")

class TestimonialUpdate(BaseModel):
    client_name: Optional[str] = None
    content: Optional[str] = None
    visible: Optional[bool] = None
    artwork_id: Optional[int] = None

class Testimonial(TestimonialBase):
    id: int
    visible: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Contact request schemas
class ContactRequestBase(BaseModel):
    client_name: str
    pet_name: Optional[str] = None
    email: EmailStr
    whatsapp: str
    country: str
    pet_image_url: Optional[str] = None
    wants_promotions: bool = False
    notes: Optional[str] = None

class ContactRequestCreate(ContactRequestBase):
    whatsapp: str = Field(pattern=r"^\+[1-9]\d{6,14}$")
    country: str = Field(pattern=r"^[A-Z]{2}$")
    honeypot: str = Field(default="", description="Honeypot field for spam protection")

class ContactRequestUpdate(BaseModel):
    client_name: Optional[str] = None
    pet_name: Optional[str] = None
    email: Optional[EmailStr] = None
    whatsapp: Optional[str] = None
    country: Optional[str] = None
    pet_image_url: Optional[str] = None
    wants_promotions: Optional[bool] = None
    status: Optional[ContactStatus] = None
    notes: Optional[str] = None

class ContactRequest(ContactRequestBase):
    id: int
    status: ContactStatus
    created_at: datetime
    
    class Config:
        from_attributes = True

# Admin schemas
class AdminBase(BaseModel):
    username: str

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
