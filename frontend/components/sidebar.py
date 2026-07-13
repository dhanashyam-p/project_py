import streamlit as st


def show_sidebar():
    st.sidebar.title("📋 Task Manager")

    # Logout at the top
    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.session_state["page"] = "login"
        st.rerun()

    st.sidebar.write("---")

    page_map = {
        "Dashboard": "dashboard",
        "Tasks": "tasks",
        "Analytics": "analytics",
        "Profile": "profile",
        "Settings": "settings",
    }

    reverse_map = {v: k for k, v in page_map.items()}

    current_page = st.session_state.get("page", "dashboard")

    if current_page in reverse_map:
        index = list(page_map.keys()).index(reverse_map[current_page])
    else:
        index = 0

    selected = st.sidebar.radio(
        "Navigation",
        list(page_map.keys()),
        index=index,
        key="navigation",
    )

    if page_map[selected] != current_page:
        st.session_state["page"] = page_map[selected]
        st.rerun()

    st.sidebar.write("---")
    st.sidebar.info("Version 1.0")