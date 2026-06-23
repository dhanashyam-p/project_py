# Task Manager

A simple Task Manager application built using FastAPI, Streamlit, and SQLite.

## Features

- User Registration and Login
- Create Tasks
- View Tasks
- Update Tasks
- Delete Tasks
- Filter Tasks by Status and Priority
- Task Summary Dashboard

## Technologies Used

### Backend
- FastAPI
- SQLite
- Pydantic

### Frontend
- Streamlit
- Requests

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/task-manager.git
cd task-manager
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

## Run Frontend

```bash
streamlit run frontend/app.py
```

Open:

```
http://localhost:8501
```

## Project Structure

```
task-manager/
├── backend/
├── frontend/
├── requirements.txt
├── README.md
└── .gitignore
```

## Author

dhanashyam

## License

This project is for learning and educational purposes.