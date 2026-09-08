from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum
from app.database import Base

class ContactStatus(str, Enum):
    pending = "pending"
    contacted = "contacted"
    in_progress = "in_progress"
    shipped = "shipped"
    delivered = "delivered"

class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Artwork(Base):
    __tablename__ = "artworks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship to testimonials
    testimonials = relationship("Testimonial", back_populates="artwork")

class Testimonial(Base):
    __tablename__ = "testimonials"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    visible = Column(Boolean, default=False)
    artwork_id = Column(Integer, ForeignKey("artworks.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship to artwork
    artwork = relationship("Artwork", back_populates="testimonials")

class ContactRequest(Base):
    __tablename__ = "contact_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    pet_name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    whatsapp = Column(String, nullable=False)
    country = Column(String, nullable=False)
    pet_image_url = Column(String, nullable=True)
    wants_promotions = Column(Boolean, default=False)
    status = Column(SQLEnum(ContactStatus), default=ContactStatus.pending)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
