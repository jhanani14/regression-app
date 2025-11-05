from datetime import datetime, timedelta
import os
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_EXPIRE_MIN = int(os.getenv("JWT_EXPIRE_MIN", 30))
JWT_ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRE_MIN)
    payload = {"sub": str(user_id), "exp": expire}
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
