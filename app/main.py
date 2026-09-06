from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Admin, Artwork, Testimonial, ContactRequest
from app.routers import artworks, testimonials, contact_requests, auth_router

app = FastAPI(title="Mascotas Tienda API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(artworks.router, prefix="/api/artworks", tags=["artworks"])
app.include_router(testimonials.router, prefix="/api/testimonials", tags=["testimonials"])
app.include_router(contact_requests.router, prefix="/api/contact", tags=["contact"])

@app.get("/")
def read_root():
    return {"message": "Mascotas Tienda API"}
