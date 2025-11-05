# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime

# -------------------------
# Request schema: creating a new user
# -------------------------
class UserCreate(BaseModel):
    email: EmailStr       # validates proper email format
    password: str         # plain password; will be hashed before saving

# -------------------------
# Response schema: returning user info
# -------------------------
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True   # Pydantic v2 replacement for orm_mode
