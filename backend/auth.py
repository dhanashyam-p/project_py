#random uid
from uuid import uuid4

#depends,show errors,status
from fastapi import Depends, HTTPException, status

#store info token and used for bearer token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

#compare,encrypt
from passlib.context import CryptContext #pass encryption tool

#store pass settings,encryptionmanager...,handle older algo automatically
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#security object created and read tokens
security = HTTPBearer()

#which token belongs to which user
sessions: dict[str, str] = {}

# Hash a user's password before storing it
def hash_password(password: str) -> str:
    try:
        return pwd_context.hash(password)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
# Verify a plain password against its hashed version
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False
# Create a unique token and store the user session
def create_token(email: str) -> str:
    token = str(uuid4())
    sessions[token] = email
    return token
# Retrieve the currently authenticated user from the token
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    email = sessions.get(token)

    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return email