import secrets
import hashlib
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.config import settings
import uuid

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

# DB operations
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, full_name: str, email: str, password: str, role, institution=None, department=None) -> User:
    user = User(
        full_name=full_name,
        email=email,
        hashed_password=hash_password(password),
        role=role,
        institution=institution,
        department=department,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def generate_reset_token() -> tuple[str, str]:
    """Generate a raw token (sent to user) and its hash (stored in DB)."""
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    return raw_token, token_hash


def set_reset_token(db: Session, user: User) -> str:
    """Generate and store a reset token for a user. Returns the raw token."""
    raw_token, token_hash = generate_reset_token()
    user.reset_token_hash = token_hash
    user.reset_token_expires = datetime.utcnow() + timedelta(minutes=15)
    db.commit()
    return raw_token


def verify_reset_token(db: Session, email: str, raw_token: str) -> User | None:
    """Check a reset token is valid, not expired, and matches the user."""
    user = get_user_by_email(db, email)
    if not user or not user.reset_token_hash or not user.reset_token_expires:
        return None
    if user.reset_token_expires < datetime.utcnow():
        return None
    token_hash = hashlib.sha256(raw_token.encode()).hexdigest()
    if token_hash != user.reset_token_hash:
        return None
    return user


def reset_password(db: Session, user: User, new_password: str) -> None:
    """Set a new password and invalidate the reset token."""
    user.hashed_password = hash_password(new_password)
    user.reset_token_hash = None
    user.reset_token_expires = None
    db.commit()