import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from backend.config import PROJECT_NAME, VERSION
from backend.database import init_db
from backend.logger import logger
from backend.routers.tasks import router as tasks_router
from backend.routers.users import router as users_router

# Create FastAPI application
app = FastAPI(
    title=PROJECT_NAME,
    version=VERSION,
    description="Backend API for the Task Manager application.",
)


# Initialize database when the application starts
@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logger.info("Database initialized successfully")
    logger.info(f"{PROJECT_NAME} started successfully")


# Middleware to measure request processing time
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{duration:.4f}"

    logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} "
        f"{duration:.4f}s"
    )

    return response


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Change this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register API Routers
app.include_router(users_router)
app.include_router(tasks_router)


# Root endpoint
@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "message": f"{PROJECT_NAME} is running",
        "version": VERSION,
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "application": PROJECT_NAME,
        "version": VERSION,
    }