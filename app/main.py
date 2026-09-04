from fastapi import FastAPI
from app.database import engine, Base
from app.models import Admin, Artwork, Testimonial, ContactRequest
from app.routers import artworks, testimonials, contact_requests, auth_router

app = FastAPI(title="Mascotas Tienda API", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(artworks.router, prefix="/api/artworks", tags=["artworks"])
app.include_router(testimonials.router, prefix="/api/testimonials", tags=["testimonials"])
app.include_router(contact_requests.router, prefix="/api/contact", tags=["contact"])

@app.get("/")
def read_root():
    return {"message": "Mascotas Tienda API"}
