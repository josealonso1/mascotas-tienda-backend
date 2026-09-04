from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Artwork
from app.schemas import ArtworkCreate, ArtworkUpdate, Artwork as ArtworkSchema
from app.auth import get_current_admin
from app.services.cloudinary_service import upload_image

router = APIRouter()

@router.get("/", response_model=list[ArtworkSchema])
def get_artworks(db: Session = Depends(get_db)):
    """Get all artworks"""
    artworks = db.query(Artwork).all()
    return artworks

@router.get("/{artwork_id}", response_model=ArtworkSchema)
def get_artwork(artwork_id: int, db: Session = Depends(get_db)):
    """Get a single artwork by ID"""
    artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if not artwork:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artwork not found")
    return artwork

@router.post("/", response_model=ArtworkSchema)
def create_artwork(artwork: ArtworkCreate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Create a new artwork (admin only)"""
    db_artwork = Artwork(**artwork.model_dump())
    db.add(db_artwork)
    db.commit()
    db.refresh(db_artwork)
    return db_artwork

@router.put("/{artwork_id}", response_model=ArtworkSchema)
def update_artwork(artwork_id: int, artwork: ArtworkUpdate, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Update an artwork (admin only)"""
    db_artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if not db_artwork:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artwork not found")
    
    update_data = artwork.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_artwork, key, value)
    
    db.commit()
    db.refresh(db_artwork)
    return db_artwork

@router.delete("/{artwork_id}")
def delete_artwork(artwork_id: int, db: Session = Depends(get_db), current_admin: dict = Depends(get_current_admin)):
    """Delete an artwork (admin only)"""
    db_artwork = db.query(Artwork).filter(Artwork.id == artwork_id).first()
    if not db_artwork:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Artwork not found")
    
    db.delete(db_artwork)
    db.commit()
    return {"message": "Artwork deleted successfully"}

@router.post("/upload-image")
async def upload_artwork_image(file: UploadFile, current_admin: dict = Depends(get_current_admin)):
    """Upload an artwork image to Cloudinary (admin only)"""
    image_url = await upload_image(file)
    return {"url": image_url}
