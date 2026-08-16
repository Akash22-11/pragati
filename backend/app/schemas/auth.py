from pydantic import BaseModel, EmailStr
from uuid import UUID
from app.models.user import UserRole

class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.student
    institution: str | None = None
    department: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: str
    role: UserRole
    institution: str | None
    department: str | None

    class Config:
        from_attributes = True