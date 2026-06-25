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

    st.sidebar.write("---")

    st.sidebar.info("Version 1.0")

    return page