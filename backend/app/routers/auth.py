from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.db.session import get_db     # ✅ Correct import for your project
from app.core.security import create_access_token  # ✅ JWT helper

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- REGISTER ----------------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    hashed_pw = pwd_context.hash(user.password)

    # Create user
    db_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    """Authenticate user and return JWT token."""
    db_user = db.query(User).filter(User.email == user.email).first()

    # Invalid credentials
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    # Generate token
    token = create_access_token(db_user.id)
    return {"access_token": token, "token_type": "bearer"}
