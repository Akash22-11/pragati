import qrcode
import io
import uuid
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.services.cloudinary import upload_file

def generate_qr_code(data: str) -> bytes:
    """Generate a QR code image and return as bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()

def generate_student_qr(db: Session, student_id: uuid.UUID, base_url: str = "http://localhost:5500") -> Profile:
    """Generate QR code for a student and save to their profile."""
    # Get or create profile
    profile = db.query(Profile).filter(Profile.student_id == student_id).first()
    if not profile:
        profile = Profile(student_id=student_id)
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # Generate unique token
    qr_token = str(uuid.uuid4())
    profile.qr_token = qr_token

    # Generate QR code pointing to public verifier page
    verify_url = f"{base_url}/pages/verify.html?token={qr_token}"
    qr_bytes = generate_qr_code(verify_url)

    # Upload QR image to Cloudinary
    filename = f"qr_{student_id}"
    qr_url = upload_file(qr_bytes, filename, folder="pragati/qrcodes")
    profile.qr_code_url = qr_url

    db.commit()
    db.refresh(profile)
    return profile