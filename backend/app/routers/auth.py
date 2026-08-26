from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse, ForgotPasswordRequest, ResetPasswordRequest
from app.services.auth import create_user, get_user_by_email, verify_password, create_access_token, set_reset_token, verify_reset_token, reset_password
from app.services.email import send_password_reset_email
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



@router.post("/forgot-password")
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, payload.email)
    if user:
        raw_token = set_reset_token(db, user)
        send_password_reset_email(
            to_email=user.email,
            student_name=user.full_name,
            raw_token=raw_token,
        )
    # Always return the same message, whether or not the email exists.
    # This prevents attackers from using this endpoint to discover which emails are registered.
    return {"message": "If that email is registered, a reset link has been sent."}


@router.post("/reset-password")
def reset_password_endpoint(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = verify_reset_token(db, payload.email, payload.token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    reset_password(db, user, payload.new_password)
    return {"message": "Password reset successfully"}