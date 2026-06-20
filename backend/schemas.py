# schemas.py

# Import BaseModel from pydantic
from pydantic import BaseModel


# ==========================================
# Register schema
# ==========================================
class UserRegister(BaseModel):
    email: str
    password: str


# ==========================================
# Login schema
# ==========================================
class UserLogin(BaseModel):
    email: str
    password: str


# ==========================================
# Create task schema
# ==========================================
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str


# ==========================================
# Update task schema
# ==========================================
class TaskUpdate(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    due_date: str


# ==========================================
# Update only status
# ==========================================
class TaskStatusUpdate(BaseModel):
    status: str