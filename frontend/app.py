import streamlit as st
import requests
import pandas as pd

# ----------------------------------
# Page settings
# ----------------------------------
st.set_page_config(
    page_title="TaskFlow Pro",
    page_icon="🚀",
    layout="wide"
)

# ----------------------------------
# Custom CSS
# ----------------------------------
st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

h1 {
    color: #2563eb;
}

div[data-testid="stMetric"] {
    background-color: black;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 8px lightgray;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    background-color: #2563eb;
    color: white;
    height: 45px;
    border: none;
}

.stButton > button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# Backend URL
# ----------------------------------
BASE_URL = "http://127.0.0.1:8000"

# ----------------------------------
# Session variables
# ----------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "token" not in st.session_state:
    st.session_state.token = ""

# ----------------------------------
# Title
# ----------------------------------
st.title("🚀 TaskFlow Pro")
st.caption("Simple and Beautiful Task Manager")

# =====================================================
# LOGIN / REGISTER
# =====================================================
if not st.session_state.logged_in:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"]
    )

    # ---------------- REGISTER ----------------
    if menu == "Register":

        st.subheader("Create Account")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Register"):

            response = requests.post(
                f"{BASE_URL}/auth/register",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:
                st.success("Registration successful")

            else:
                st.error(response.json()["detail"])

    # ---------------- LOGIN ----------------
    if menu == "Login":

        st.subheader("Login")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            response = requests.post(
                f"{BASE_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                st.session_state.token = response.json()["token"]
                st.session_state.logged_in = True

                st.rerun()

            else:
                st.error("Invalid credentials")

# =====================================================
# DASHBOARD
# =====================================================
else:

    headers = {
        "Authorization": st.session_state.token
    }

    st.sidebar.success("Logged In")

    page = st.sidebar.radio(
        "Dashboard",
        [
            "🏠 Home",
            "➕ Add Task",
            "📋 View Tasks",
            "📊 Summary"
        ]
    )

    # Logout
    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.token = ""

        st.rerun()

    # ======================================
    # HOME
    # ======================================
    if page == "🏠 Home":

        st.header("Welcome 👋")

        st.info(
            "Manage your tasks efficiently using TaskFlow Pro."
        )

    # ======================================
    # ADD TASK
    # ======================================
    elif page == "➕ Add Task":

        st.header("Add New Task")

        title = st.text_input("Title")

        description = st.text_area("Description")

        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"]
        )

        status = st.selectbox(
            "Status",
            ["pending", "done"]
        )

        due_date = st.date_input("Due Date")

        if st.button("Save Task"):

            response = requests.post(
                f"{BASE_URL}/tasks/",
                headers=headers,
                json={
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "status": status,
                    "due_date": str(due_date)
                }
            )

            if response.status_code == 200:
                st.success("Task created successfully")

            else:
                st.error("Error")

    # ======================================
    # VIEW TASKS
    # ======================================
    elif page == "📋 View Tasks":

        st.header("My Tasks")

        response = requests.get(
            f"{BASE_URL}/tasks/",
            headers=headers
        )

        tasks = response.json()

        if len(tasks) > 0:

            df = pd.DataFrame(tasks)

            st.dataframe(
                df,
                use_container_width=True
            )

        else:
            st.warning("No tasks found")

    # ======================================
    # SUMMARY
    # ======================================
    elif page == "📊 Summary":

        st.header("Task Summary")

        response = requests.get(
            f"{BASE_URL}/tasks/summary",
            headers=headers
        )

        summary = response.json()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "📋 Total",
                summary["total"]
            )

        with col2:
            st.metric(
                "⏳ Pending",
                summary["pending"]
            )

        with col3:
            st.metric(
                "✅ Done",
                summary["done"]
            )