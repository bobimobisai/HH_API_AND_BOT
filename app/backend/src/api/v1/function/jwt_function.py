from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import HTTPException
from backend.src.settings import settings
from fastapi import FastAPI, Depends, HTTPException, status

SECRET_KEY = settings.JWT_CONFIG["secret_key"]
ALGORITHM = settings.JWT_CONFIG["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = settings.JWT_CONFIG["ACCESS_TOKEN_EXPIRE_MINUTES"]


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def decrypt_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
