# auth.py

# Import uuid to generate tokens
import uuid

# Import bcrypt for password hashing
import bcrypt

# FastAPI imports
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader


# ==========================================
# Sessions dictionary
# token -> email
# ==========================================
sessions = {}


# ==========================================
# API header
# ==========================================
api_key_header = APIKeyHeader(name="Authorization")


# ==========================================
# Hash password
# ==========================================
def hash_password(password):

    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    return hashed.decode()


# ==========================================
# Verify password
# ==========================================
def verify_password(password, hashed_password):

    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


# ==========================================
# Create token
# ==========================================
def create_token():

    return str(uuid.uuid4())


# ==========================================
# Get current user from token
# ==========================================
def get_current_user(
        authorization: str = Depends(api_key_header)
):

    if authorization not in sessions:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    return sessions[authorization]