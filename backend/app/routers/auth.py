from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db  # Correct import
from app.core.security import create_access_token  # JWT helper

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ---------------- PASSWORD CONFIG ----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_PASSWORD_LENGTH = 72  # bcrypt hard limit

# ---------------- REGISTER ----------------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user safely."""

    # 1️⃣ Validate password length
    if len(user.password.encode("utf-8")) > MAX_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Password too long. Max {MAX_PASSWORD_LENGTH} characters.",
        )

    # 2️⃣ Normalize email
    email_normalized = user.email.lower()

    # 3️⃣ Check if user already exists
    existing_user = db.query(User).filter(User.email == email_normalized).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # 4️⃣ Hash password safely
    hashed_pw = pwd_context.hash(user.password)

    # 5️⃣ Create user
    db_user = User(
        email=email_normalized,
        hashed_password=hashed_pw
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )

    return db_user

# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""

    email_normalized = user.email.lower()
    db_user = db.query(User).filter(User.email == email_normalized).first()

    # Invalid credentials
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate JWT token
    token = create_access_token(db_user.id)

    return {"access_token": token, "token_type": "bearer"}
