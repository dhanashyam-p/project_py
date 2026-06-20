# users.py

# Import FastAPI tools
from fastapi import APIRouter, HTTPException, Depends

# Import schemas
from schemas import UserRegister, UserLogin

# Import database functions
from database import (
    create_user,
    get_user_by_email
)

# Import authentication functions
from auth import (
    hash_password,
    verify_password,
    create_token,
    sessions,
    get_current_user
)

# Create router
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ==========================================
# REGISTER
# ==========================================
@router.post("/register")
def register(user: UserRegister):

    # Check if email already exists
    existing_user = get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Hash password
    hashed_password = hash_password(user.password)

    # Save user in database
    create_user(
        user.email,
        hashed_password
    )

    return {
        "message": "User registered successfully"
    }


# ==========================================
# LOGIN
# ==========================================
@router.post("/login")
def login(user: UserLogin):

    # Find user
    db_user = get_user_by_email(user.email)

    # Email not found
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Wrong password
    if not verify_password(
            user.password,
            db_user["hashed_password"]):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Generate token
    token = create_token()

    # Store token -> email
    sessions[token] = db_user["email"]

    return {
        "token": token
    }


# ==========================================
# CURRENT USER
# ==========================================
@router.get("/me")
def get_me(
        current_user: str = Depends(get_current_user)
):

    user = get_user_by_email(current_user)

    return {
        "id": user["id"],
        "email": user["email"]
    }