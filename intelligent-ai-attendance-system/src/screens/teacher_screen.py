import streamlit as st
from src.ui.style_base_layout import style_background_dashboard
from src.ui.style_base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Initialize state properly
    if "teacher_login_type" not in st.session_state:
        st.session_state["teacher_login_type"] = "login"

    if st.session_state["teacher_login_type"] == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go Back to Home", type="secondary"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<h3 style='color: black; text-align: center'>Login using username & password</h3>", unsafe_allow_html=True)

    st.space()
    st.space()

    username = st.text_input("Enter Username:", placeholder="enter username")
    password = st.text_input("Enter Password:", type="password", placeholder="enter password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        st.button("Login", icon="🔐", use_container_width=True)

    with btnc2:
        if st.button("Go to Register", type="primary", icon="📝", use_container_width=True):
            st.session_state["teacher_login_type"] = "register"
            st.rerun()

def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go Back to Home", type="secondary"):
            st.session_state["login_type"] = None
            st.rerun()

    st.markdown("<h3 style='color: black; text-align: center'>Register Your Teacher Profile</h3>", unsafe_allow_html=True)

    st.space()
    st.space()

    username = st.text_input("Enter Username:", placeholder="enter username")
    name = st.text_input("Enter Name:", placeholder="enter name")
    password = st.text_input("Enter Password:", type="password", placeholder="enter password")
    confirm_password = st.text_input("Confirm Password:", type="password", placeholder="confirm password")

    st.divider()

    btnc1, btnc2 = st.columns(2)

    with btnc1:
        st.button("Register", icon="📝", use_container_width=True)

    with btnc2:
        if st.button("Back to Login", type="primary", icon="🔐", use_container_width=True):
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    footer_dashboard()

    