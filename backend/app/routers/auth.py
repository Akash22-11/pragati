from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from app.services.auth import create_user, get_user_by_email, verify_password, create_access_token
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    existing = get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(
        db=db,
        full_name=payload.full_name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        institution=payload.institution,
        department=payload.department,
    )
    return user

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}