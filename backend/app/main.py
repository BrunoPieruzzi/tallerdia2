from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

ACCESS_TOKEN_EXPIRE_SECONDS = 300
REFRESH_TOKEN_EXPIRE_SECONDS = 3600
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
VALID_USERNAME = "admin"
VALID_PASSWORD = "admin123"


class TokenRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


app = FastAPI(title="JWT FastAPI Example")


def _create_token(subject: str, token_type: str, expires_in_seconds: int) -> str:
    now = datetime.now(tz=timezone.utc)
    payload = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in_seconds),
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


@app.post("/token")
def create_token(credentials: TokenRequest):
    if credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = _create_token(VALID_USERNAME, "access", ACCESS_TOKEN_EXPIRE_SECONDS)
    refresh_token = _create_token(VALID_USERNAME, "refresh", REFRESH_TOKEN_EXPIRE_SECONDS)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }


@app.post("/token/refresh")
def refresh_token(payload: RefreshRequest):
    try:
        decoded = jwt.decode(payload.refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid refresh token") from exc

    if decoded.get("type") != "refresh" or decoded.get("sub") != VALID_USERNAME:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = _create_token(VALID_USERNAME, "access", ACCESS_TOKEN_EXPIRE_SECONDS)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_SECONDS,
    }
