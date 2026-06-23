from datetime import date
from typing import Literal
from pydantic import BaseModel, EmailStr, Field

PriorityType = Literal["low", "medium", "high"]
StatusType = Literal["pending", "in-progress", "done"]

# Schema for user registration request
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)

# Schema for user login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)

# Schema for user response data
class UserResponse(BaseModel):
    id: int
    email: EmailStr

# Schema for authentication token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    email: EmailStr

#  message response schema
#task created sucssfully 
class MessageResponse(BaseModel):
    message: str

# Schema for creating a task
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: PriorityType = "low"
    status: StatusType = "pending"
    due_date: date | None = None

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: PriorityType = "low"
    status: StatusType = "pending"
    due_date: date | None = None

# Schema for updating task status only
class TaskStatusUpdate(BaseModel):
    status: StatusType

# Schema for task response data
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: PriorityType
    status: StatusType
    due_date: date | None = None
    owner_email: EmailStr

# Schema for task summary 
class TaskSummary(BaseModel):
    total: int
    pending: int
    in_progress: int
    done: int