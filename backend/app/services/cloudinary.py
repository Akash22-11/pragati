import cloudinary
import cloudinary.uploader
from app.config import settings

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

def upload_file(file_bytes: bytes, filename: str, folder: str = "pragati") -> str:
    """Upload a file to Cloudinary and return the secure URL."""
    result = cloudinary.uploader.upload(
        file_bytes,
        folder=folder,
        public_id=filename,
        resource_type="auto",  # handles PDF, images, docs
        overwrite=True,
    )
    return result["secure_url"]

def delete_file(public_id: str) -> None:
    """Delete a file from Cloudinary by public_id."""
    cloudinary.uploader.destroy(public_id)