# database.py

# Import sqlite3 to work with SQLite database
import sqlite3

# Database file name
DATABASE_NAME = "app.db"


# ==========================================
# Create connection
# ==========================================
def get_connection():

    conn = sqlite3.connect(DATABASE_NAME)

    # Allows accessing columns by name
    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# Create tables
# ==========================================
def init_db():

    conn = get_connection()

    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        hashed_password TEXT NOT NULL
    )
    """)

    # Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority TEXT,
        status TEXT,
        due_date TEXT,
        owner_email TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# Create user
# ==========================================
def create_user(email, hashed_password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO users(email, hashed_password)
        VALUES (?, ?)
        """,
        (email, hashed_password)
    )

    conn.commit()

    conn.close()


# ==========================================
# Get user by email
# ==========================================
def get_user_by_email(email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ==========================================
# Create task
# ==========================================
def create_task(
        title,
        description,
        priority,
        status,
        due_date,
        owner_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(
            title,
            description,
            priority,
            status,
            due_date,
            owner_email
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            priority,
            status,
            due_date,
            owner_email
        )
    )

    conn.commit()

    task_id = cursor.lastrowid

    conn.close()

    return task_id


# ==========================================
# Get tasks of one user
# ==========================================
def get_tasks_by_owner(owner_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE owner_email = ?
        """,
        (owner_email,)
    )

    tasks = cursor.fetchall()

    conn.close()

    return tasks


# ==========================================
# Get one task
# ==========================================
def get_task_by_id(task_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    task = cursor.fetchone()

    conn.close()

    return task


# ==========================================
# Delete task
# ==========================================
def delete_task(task_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM tasks
        WHERE id = ?
        """,
        (task_id,)
    )

    conn.commit()

    conn.close()


# ==========================================
# Task summary
# ==========================================
def get_summary(owner_email):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email = ?
        """,
        (owner_email,)
    )

    total = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email = ?
        AND status='pending'
        """,
        (owner_email,)
    )

    pending = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE owner_email = ?
        AND status='done'
        """,
        (owner_email,)
    )

    done = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "pending": pending,
        "done": done
    }