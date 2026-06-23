import requests
import streamlit as st
from datetime import date, datetime

API_BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 10


def init_session_state():
    if "page" not in st.session_state:
        st.session_state["page"] = "login"
    if "token" not in st.session_state:
        st.session_state["token"] = None
    if "email" not in st.session_state:
        st.session_state["email"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "selected_task_id" not in st.session_state:
        st.session_state["selected_task_id"] = None
    if "delete_task_id" not in st.session_state:
        st.session_state["delete_task_id"] = None
    if "show_user_details" not in st.session_state:
        st.session_state["show_user_details"] = False
    if "show_about" not in st.session_state:
        st.session_state["show_about"] = False


def get_auth_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": "Bearer " + token}
    return {}


def api_call(method, endpoint, json=None, params=None, require_auth=False):
    url = API_BASE_URL + endpoint
    headers = get_auth_headers() if require_auth else {}

    try:
        response = requests.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
    except requests.exceptions.ConnectionError:
        return False, "Backend server is not running. Start FastAPI first."
    except requests.exceptions.Timeout:
        return False, "Request timed out. Please try again."
    except requests.exceptions.RequestException as exc:
        return False, "Request failed: " + str(exc)

    try:
        data = response.json()
    except ValueError:
        data = {"detail": response.text or "Unknown server response"}

    if response.status_code >= 200 and response.status_code < 300:
        return True, data

    if response.status_code == 401 and require_auth:
        st.session_state["token"] = None
        st.session_state["email"] = None
        st.session_state["username"] = None
        st.session_state["page"] = "login"

    detail = data.get("detail", "Something went wrong.")
    return False, detail


def go_to(page, task_id=None):
    st.session_state["page"] = page
    if task_id is not None:
        st.session_state["selected_task_id"] = task_id
    st.rerun()


def logout():
    st.session_state["token"] = None
    st.session_state["email"] = None
    st.session_state["username"] = None
    st.session_state["selected_task_id"] = None
    st.session_state["delete_task_id"] = None
    st.session_state["page"] = "login"
    st.rerun()


def format_due_date(value):
    if not value:
        return "-"
    try:
        return datetime.fromisoformat(value).date().isoformat()
    except ValueError:
        return value


def parse_due_date_for_input(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value).date()
    except ValueError:
        try:
            return date.fromisoformat(value)
        except ValueError:
            return None


def require_login():
    if not st.session_state.get("token"):
        st.warning("Please login first.")
        st.session_state["page"] = "login"
        return False
    return True


def render_sidebar():
    st.sidebar.title("📋 Task Manager")
    st.sidebar.write("Stay organized, stay on track!")
    st.sidebar.write("---")

    email = st.session_state.get("email")
    username = st.session_state.get("username")
    if email:
        if st.sidebar.button("👤 User"):
            st.session_state["show_user_details"] = not st.session_state.get("show_user_details", False)

        if st.session_state.get("show_user_details"):
            st.sidebar.info("Username: " + (username or "-") + "\n\nEmail: " + email)

        st.sidebar.write("---")

        if st.sidebar.button("Dashboard"):
            go_to("dashboard")

        if st.sidebar.button("Add Task"):
            go_to("add_task")

        if st.sidebar.button("Logout"):
            logout()
    else:
        st.sidebar.write("Please login or register.")

    st.sidebar.write("---")

    if st.sidebar.button("ℹ️ About"):
        st.session_state["show_about"] = not st.session_state.get("show_about", False)

    if st.session_state.get("show_about"):
        st.sidebar.markdown(
            "**About Task Manager**\n\n"
            "This app helps you keep track of your daily tasks. "
            "You can add tasks, set their priority and due date, "
            "update their status as you work on them, and mark them "
            "done once finished. It keeps all your to-dos organized "
            "in one simple dashboard."
        )


def render_login_page():
    st.markdown("## 📋 Task Manager")
    st.caption("Simple. Organized. Yours.")
    st.write("---")
    st.title("Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if email.strip() == "" or password.strip() == "":
            st.error("Email and password are required.")
        else:
            ok, data = api_call(
                "POST",
                "/auth/login",
                json={"email": email.strip(), "password": password},
            )

            if ok:
                st.session_state["token"] = data["access_token"]
                st.session_state["email"] = data["email"]
                st.session_state["username"] = data["email"].split("@")[0]
                st.session_state["page"] = "dashboard"
                st.success("Login successful.")
                st.rerun()
            else:
                st.error(str(data))

    st.write("New user?")
    if st.button("Go to Register"):
        go_to("register")


def render_register_page():
    st.markdown("## 📋 Task Manager")
    st.caption("Simple. Organized. Yours.")
    st.write("---")
    st.title("Register")

    with st.form("register_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if email.strip() == "" or password.strip() == "" or confirm_password.strip() == "":
            st.error("All fields are required.")
        elif password != confirm_password:
            st.error("Passwords do not match.")
        else:
            ok, data = api_call(
                "POST",
                "/auth/register",
                json={"email": email.strip(), "password": password},
            )

            if ok:
                st.success("Registration successful. Please login.")
                st.session_state["page"] = "login"
                st.rerun()
            else:
                st.error(str(data))

    if st.button("Back to Login"):
        go_to("login")


def fetch_summary():
    ok, data = api_call("GET", "/tasks/summary", require_auth=True)
    if ok:
        return data
    st.error(str(data))
    return None


def fetch_tasks(status_filter, priority_filter):
    params = {}

    if status_filter != "All":
        params["status"] = status_filter
    if priority_filter != "All":
        params["priority"] = priority_filter

    ok, data = api_call("GET", "/tasks/", params=params, require_auth=True)
    if ok:
        return data
    st.error(str(data))
    return None


def render_summary_cards(summary):
    st.markdown(
        """
        <style>
        .summary-card {
            border-radius: 12px;
            padding: 18px 20px;
            color: white;
            text-align: left;
        }
        .summary-card .label {
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 4px;
        }
        .summary-card .value {
            font-size: 30px;
            font-weight: 700;
        }
        .card-total { background: linear-gradient(135deg, #4f46e5, #6366f1); }
        .card-pending { background: linear-gradient(135deg, #d97706, #f59e0b); }
        .card-progress { background: linear-gradient(135deg, #0284c7, #38bdf8); }
        .card-done { background: linear-gradient(135deg, #16a34a, #22c55e); }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            '<div class="summary-card card-total"><div class="label">📋 Total Tasks</div>'
            '<div class="value">' + str(summary.get("total", 0)) + '</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="summary-card card-pending"><div class="label">⏳ Pending</div>'
            '<div class="value">' + str(summary.get("pending", 0)) + '</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="summary-card card-progress"><div class="label">🚀 In Progress</div>'
            '<div class="value">' + str(summary.get("in_progress", 0)) + '</div></div>',
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            '<div class="summary-card card-done"><div class="label">✅ Done</div>'
            '<div class="value">' + str(summary.get("done", 0)) + '</div></div>',
            unsafe_allow_html=True,
        )


def render_task_actions(task_list):
    st.subheader("⚙️ Task Actions")

    if not task_list:
        st.info("No tasks available.")
        return

    options = {}
    for task in task_list:
        label = "#" + str(task["id"]) + " | " + task["title"] + " | " + task["status"] + " | " + task["priority"]
        options[label] = task["id"]

    selected_label = st.selectbox("Select Task", list(options.keys()))
    selected_task_id = options[selected_label]

    action = st.selectbox("Select Action", ["View", "Edit", "Mark Done", "Delete"])
    apply_clicked = st.button("Apply")

    if apply_clicked:
        if action == "View":
            go_to("task_detail", task_id=selected_task_id)

        elif action == "Edit":
            go_to("edit_task", task_id=selected_task_id)

        elif action == "Mark Done":
            ok, data = api_call(
                "PATCH",
                "/tasks/" + str(selected_task_id) + "/status",
                json={"status": "done"},
                require_auth=True,
            )
            if ok:
                st.success("Task marked as done.")
                st.rerun()
            else:
                st.error(str(data))

        elif action == "Delete":
            st.session_state["delete_task_id"] = selected_task_id
            st.rerun()

    delete_task_id = st.session_state.get("delete_task_id")
    if delete_task_id == selected_task_id:
        st.warning("Confirm delete?")
        yes_col, no_col = st.columns(2)

        if yes_col.button("Yes, Delete"):
            ok, data = api_call(
                "DELETE",
                "/tasks/" + str(selected_task_id),
                require_auth=True,
            )
            st.session_state["delete_task_id"] = None

            if ok:
                st.success("Task deleted successfully.")
                st.rerun()
            else:
                st.error(str(data))

        if no_col.button("Cancel"):
            st.session_state["delete_task_id"] = None
            st.rerun()


def render_dashboard_page():
    if not require_login():
        return

    username = st.session_state.get("username")
    st.title("Dashboard")
    if username:
        st.markdown(f"#### 👋 Hi, {username}!")
    st.caption("Here's an overview of your tasks.")

    summary = fetch_summary()
    if summary:
        render_summary_cards(summary)

    st.write("")
    st.write("---")

    st.markdown("#### 🔍 Filters")
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "pending", "in-progress", "done"])
    with col2:
        priority_filter = st.selectbox("Filter by Priority", ["All", "low", "medium", "high"])

    task_list = fetch_tasks(status_filter, priority_filter)

    if task_list is None:
        return

    st.write("---")
    st.markdown("#### 📝 Your Tasks")

    if task_list:
        table_rows = []
        count = 1
        for task in task_list:
            row = {
                "S.No": count,
                "Task ID": task["id"],
                "Title": task["title"],
                "Priority": task["priority"],
                "Status": task["status"],
                "Due Date": format_due_date(task.get("due_date")),
            }
            table_rows.append(row)
            count = count + 1

        event = st.dataframe(
            table_rows,
            on_select="rerun",
            selection_mode="single-row",
            hide_index=True,
        )

        selected_rows = event.selection["rows"] if event and event.selection else []
        if selected_rows:
            selected_index = selected_rows[0]
            selected_task_id = task_list[selected_index]["id"]
            go_to("task_detail", task_id=selected_task_id)
    else:
        st.info("No tasks found.")

    st.write("---")
    render_task_actions(task_list)


def render_add_task_page():
    if not require_login():
        return

    st.title("➕ Add Task")

    with st.form("add_task_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["low", "medium", "high"])
        status = st.selectbox("Status", ["pending", "in-progress", "done"])
        due_date = st.date_input("Due Date", value=None)
        submitted = st.form_submit_button("Create Task")

    if submitted:
        if title.strip() == "":
            st.error("Title is required.")
            return

        payload = {
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "status": status,
            "due_date": due_date.isoformat() if due_date else None,
        }

        ok, data = api_call("POST", "/tasks/", json=payload, require_auth=True)

        if ok:
            st.success("Task created successfully.")
            st.session_state["page"] = "dashboard"
            st.rerun()
        else:
            st.error(str(data))

    if st.button("Back to Dashboard"):
        go_to("dashboard")


def fetch_task_detail(task_id):
    ok, data = api_call("GET", "/tasks/" + str(task_id), require_auth=True)
    if ok:
        return data
    st.error(str(data))
    return None


def render_task_detail_page():
    if not require_login():
        return

    task_id = st.session_state.get("selected_task_id")
    if not task_id:
        st.warning("No task selected.")
        if st.button("Back to Dashboard"):
            go_to("dashboard")
        return

    st.title("📝 Task Detail")

    task = fetch_task_detail(task_id)

    if not task:
        return

    st.write("ID: " + str(task["id"]))
    st.write("Title: " + task["title"])
    st.write("Description: " + (task["description"] or "-"))
    st.write("Priority: " + task["priority"])
    st.write("Status: " + task["status"])
    st.write("Due Date: " + format_due_date(task.get("due_date")))
    st.write("Owner: " + task["owner_email"])

    delete_key = "confirm_delete_detail_" + str(task_id)
    if delete_key not in st.session_state:
        st.session_state[delete_key] = False

    col1, col2, col3 = st.columns(3)

    if col1.button("Edit"):
        go_to("edit_task", task_id=task_id)

    if col2.button("Delete"):
        st.session_state[delete_key] = True
        st.rerun()

    if col3.button("Back"):
        go_to("dashboard")

    if st.session_state.get(delete_key):
        st.warning("Are you sure you want to delete this task?")

        yes_col, no_col = st.columns(2)

        if yes_col.button("Yes, Delete"):
            ok, data = api_call("DELETE", "/tasks/" + str(task_id), require_auth=True)

            st.session_state[delete_key] = False

            if ok:
                st.success("Task deleted successfully.")
                st.session_state["selected_task_id"] = None
                go_to("dashboard")
            else:
                st.error(str(data))

        if no_col.button("Cancel"):
            st.session_state[delete_key] = False
            st.rerun()


def render_edit_task_page():
    if not require_login():
        return

    task_id = st.session_state.get("selected_task_id")
    if not task_id:
        st.warning("No task selected.")
        if st.button("Back to Dashboard"):
            go_to("dashboard")
        return

    st.title("✏️ Edit Task")

    task = fetch_task_detail(task_id)
    if not task:
        return

    default_due_date = parse_due_date_for_input(task.get("due_date"))

    with st.form("edit_task_form"):
        title = st.text_input("Title", value=task["title"])
        description = st.text_area("Description", value=task["description"])
        priority = st.selectbox(
            "Priority",
            ["low", "medium", "high"],
            index=["low", "medium", "high"].index(task["priority"]),
        )
        status_value = task["status"]
        if status_value not in ["pending", "in-progress", "done"]:
            status_value = "pending"
        status = st.selectbox(
            "Status",
            ["pending", "in-progress", "done"],
            index=["pending", "in-progress", "done"].index(status_value),
        )
        due_date = st.date_input("Due Date", value=default_due_date)
        submitted = st.form_submit_button("Update Task")

    if submitted:
        if title.strip() == "":
            st.error("Title is required.")
            return

        payload = {
            "title": title.strip(),
            "description": description.strip(),
            "priority": priority,
            "status": status,
            "due_date": due_date.isoformat() if due_date else None,
        }

        ok, data = api_call("PUT", "/tasks/" + str(task_id), json=payload, require_auth=True)

        if ok:
            st.success("Task updated successfully.")
            go_to("dashboard")
        else:
            st.error(str(data))

    if st.button("Cancel"):
        go_to("dashboard")


def main():
    st.set_page_config(page_title="Task Manager", page_icon="📋")

    init_session_state()
    render_sidebar()
    page = st.session_state.get("page", "login")

    if page == "login":
        render_login_page()
    elif page == "register":
        render_register_page()
    elif page == "dashboard":
        render_dashboard_page()
    elif page == "add_task":
        render_add_task_page()
    elif page == "task_detail":
        render_task_detail_page()
    elif page == "edit_task":
        render_edit_task_page()
    else:
        st.session_state["page"] = "login"
        st.rerun()


if __name__ == "__main__":
    main()