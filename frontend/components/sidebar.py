import streamlit as st


def show_sidebar():

    st.sidebar.title("📋 Task Manager")

    st.sidebar.write("---")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Tasks",
            "Analytics",
            "Profile",
            "Settings",
        ],
    )

    # Update session state based on selection
    page_map = {
        "Dashboard": "dashboard",
        "Tasks": "tasks",
        "Analytics": "analytics",
        "Profile": "profile",
        "Settings": "settings",
    }

    st.session_state["page"] = page_map[page]

    st.sidebar.write("---")

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state["token"] = None
        st.session_state["email"] = None
        st.session_state["username"] = None
        st.session_state["selected_task_id"] = None
        st.session_state["delete_task_id"] = None
        st.session_state["page"] = "login"
        st.rerun()

    st.sidebar.write("---")
    st.sidebar.info("Version 1.0")