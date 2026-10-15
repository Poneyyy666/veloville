"""Routeur auth.

À compléter : POST /auth/login.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import User
from api.schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from api.securite import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentification"])

@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    """Vérifie les identifiants puis retourne un JWT."""

    user = db.scalar(
        select(User).where(User.username == data.username)
    )

    # Même message dans les deux cas pour ne pas révéler les comptes existants.
    if user is None or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiants invalides",
        )

    token = create_access_token(
        username=user.username,
        role=user.role,
    )

    return TokenResponse(
        access_token=token,
        role=user.role,
    )