import io
import logging
import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.config import settings

logger = logging.getLogger(__name__)

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_CONTENT_TYPES = ["image/jpeg", "image/png", "image/webp"]


def _has_valid_signature(content_type: str, data: bytes) -> bool:
    """Validate file signature based on content type"""
    if content_type == "image/jpeg":
        return data.startswith(b"\xff\xd8\xff")
    elif content_type == "image/png":
        return data.startswith(b"\x89PNG\r\n\x1a\n")
    elif content_type == "image/webp":
        return len(data) >= 12 and data[0:4] == b"RIFF" and data[8:12] == b"WEBP"
    return False

async def upload_image(file: UploadFile) -> str:
    """Upload an image to Cloudinary and return the secure URL"""
    # Validate content type
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    # Read file content by chunks to validate size and signature
    file_content = b''
    chunk_size = 1024 * 1024  # 1MB
    
    while True:
        chunk = await file.read(chunk_size)
        if not chunk:
            break
        file_content += chunk
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
    
    # Validate file signature
    if not _has_valid_signature(file.content_type, file_content):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed types: {', '.join(ALLOWED_CONTENT_TYPES)}"
        )
    
    # Upload to Cloudinary using BytesIO
    try:
        result = cloudinary.uploader.upload(
            io.BytesIO(file_content),
            folder="mascotas_tienda"
        )
        return result["secure_url"]
    except Exception:
        logger.exception("Error uploading image to Cloudinary")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading image"
        )
