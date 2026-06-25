from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

# Type aliases
PriorityType = Literal["low", "medium", "high"]
StatusType = Literal["pending", "in-progress", "done"]


# Base model
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# User registration request
class UserRegister(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)


# User login request
class UserLogin(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=100)


# User response
class UserResponse(BaseSchema):
    id: int
    email: EmailStr


# Authentication response
class TokenResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    email: EmailStr


# Generic message response
class MessageResponse(BaseSchema):
    message: str


# Create task request
class TaskCreate(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: PriorityType = "low"
    status: StatusType = "pending"
    due_date: date | None = None


# Update task request
class TaskUpdate(BaseSchema):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = ""
    priority: PriorityType = "low"
    status: StatusType = "pending"
    due_date: date | None = None


# Update task status
class TaskStatusUpdate(BaseSchema):
    status: StatusType


# Task response
class TaskResponse(BaseSchema):
    id: int
    title: str
    description: str
    priority: PriorityType
    status: StatusType
    due_date: date | None = None
    owner_email: EmailStr


# Dashboard summary
class TaskSummary(BaseSchema):
    total: int
    pending: int
    in_progress: int
    done: int