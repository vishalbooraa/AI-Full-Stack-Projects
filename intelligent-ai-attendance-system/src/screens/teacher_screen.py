import streamlit as st
from src.ui.style_base_layout import style_background_dashboard
from src.ui.style_base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher
from src.database.db import teacher_login


def register_teacher(username,name,password,confirm_password):
    if not username or not name or not password or not confirm_password:
        return False,"All Fields are required"
    if check_teacher_exists(username):
        return False,"Username already exists"
    if password != confirm_password:
        return False,"Passwords do not match"
    try:
        create_teacher(username,password,name)
        return True,"Teacher registered successfully! Please login now."
    except Exception as e:
        return False,f"An error occurred: {str(e)}"

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Initialize state properly
    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return
    if "teacher_login_type" not in st.session_state:
        st.session_state["teacher_login_type"] = "login"

    if st.session_state["teacher_login_type"] == "login":
        teacher_screen_login()
    else:
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    st.markdown(f"<h1 style='color: black; text-align: center'>Welcome, {teacher_data['name']}!</h1>", unsafe_allow_html=True)

def login_teacher(username, password):
    if not username or not password:
        st.error("Please enter both username and password")
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state["teacher_data"] = teacher
        st.session_state.is_logged_in = True
        return True
    return False

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
        if st.button("Login", icon="🔐", use_container_width=True):
            if login_teacher(username, password):
                st.toast("Login successful!")
                import time
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password")
                

    with btnc2:
        if st.button("Go to Register", type="primary", icon="📝", use_container_width=True):
            st.session_state["teacher_login_type"] = "register"
            st.rerun()
    footer_dashboard()

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
        if st.button("Register", icon="📝", use_container_width=True):
            success,message=register_teacher(username,name,password,confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state["teacher_login_type"] = "login"
                st.rerun()
            else:
                st.error(message)

    with btnc2:
        if st.button("Back to Login", type="primary", icon="🔐", use_container_width=True):
            st.session_state["teacher_login_type"] = "login"
            st.rerun()

    footer_dashboard()

    