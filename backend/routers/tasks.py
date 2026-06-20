# tasks.py

# Import FastAPI tools
from fastapi import APIRouter, HTTPException, Depends

# Import schema
from schemas import TaskCreate

# Import database functions
from database import (
    create_task,
    get_tasks_by_owner,
    get_task_by_id,
    delete_task,
    get_summary
)

# Import authentication
from auth import get_current_user

# Create router
router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


# ==========================================
# ADD TASK
# ==========================================
@router.post("/")
def add_task(
        task: TaskCreate,
        current_user: str = Depends(get_current_user)
):

    create_task(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date,
        owner_email=current_user
    )

    return {
        "message": "Task created successfully"
    }


# ==========================================
# GET ALL TASKS
# ==========================================
@router.get("/")
def get_tasks(
        current_user: str = Depends(get_current_user)
):

    tasks = get_tasks_by_owner(current_user)

    return tasks


# ==========================================
# SUMMARY
# IMPORTANT:
# This MUST come before /{task_id}
# ==========================================
@router.get("/summary")
def summary(
        current_user: str = Depends(get_current_user)
):

    return get_summary(current_user)


# ==========================================
# GET ONE TASK
# ==========================================
@router.get("/{task_id}")
def get_one_task(
        task_id: int,
        current_user: str = Depends(get_current_user)
):

    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return task


# ==========================================
# DELETE TASK
# ==========================================
@router.delete("/{task_id}")
def remove_task(
        task_id: int,
        current_user: str = Depends(get_current_user)
):

    task = get_task_by_id(task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["owner_email"] != current_user:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    delete_task(task_id)

    return {
        "message": "Task deleted successfully"
    }