import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "change_this_to_a_long_random_secret_key"
)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///app.db"
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "60"
    )
)

DEBUG = os.getenv(
    "DEBUG",
    "False"
).lower() == "true"

PROJECT_NAME = os.getenv(
    "PROJECT_NAME",
    "Task Manager API"
)

VERSION = "1.0.0"