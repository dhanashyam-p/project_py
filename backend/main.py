# main.py

# Import FastAPI
from fastapi import FastAPI

# Import database initialization
from database import init_db

# Import routers
from routers import users, tasks


# ==========================================
# Create FastAPI app
# ==========================================
app = FastAPI(
    title="Personal Task Manager",
    version="1.0.0"
)


# ==========================================
# Create tables when server starts
# ==========================================
init_db()


# ==========================================
# Include routers
# ==========================================
app.include_router(users.router)

app.include_router(tasks.router)


# ==========================================
# Home endpoint
# ==========================================
@app.get("/")
def home():

    return {
        "message": "Personal Task Manager API is running"
    }