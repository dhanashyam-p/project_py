import streamlit as st


def dashboard_page():

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Tasks", "0")

    with col2:
        st.metric("Pending", "0")

    with col3:
        st.metric("Completed", "0")

    st.info("Dashboard connected successfully.")
    