import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.components.dialouge import auto_enroll_dialog

# ✅ ALWAYS initialize FIRST
if "login_type" not in st.session_state:
    st.session_state["login_type"] = None

# (Optional but recommended)
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "user_role" not in st.session_state:
    st.session_state["user_role"] = None


# ✅ Handle join लिंक AFTER initialization
params = st.query_params
join_code = params.get("join-code")

if join_code:
    join_code = join_code

    if st.session_state.get("login_type") != "student":
        st.session_state["login_type"] = "student"
        st.rerun()

    if (
        st.session_state.get("is_logged_in") and 
        st.session_state.get("user_role") == "student"
    ):
        auto_enroll_dialog(join_code)


def main():
    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()
        case "student":
            student_screen()
        case None:
            home_screen()


main()