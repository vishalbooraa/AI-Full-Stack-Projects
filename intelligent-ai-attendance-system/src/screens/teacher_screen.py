import streamlit as st
from src.ui.style_base_layout import style_background_dashboard
from src.ui.style_base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists, create_teacher,get_teacher_subjects
from src.database.db import teacher_login
from src.components.dialouge import create_subject_dialog,share_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialouge import add_image_dialog
from src.pipelines.face_pipeline import predict_attendance
import numpy as np
from src.database.config import supabase
from datetime import datetime
import pandas as pd
from src.components.dialouge import attendance_result_dialog
from datetime import date

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
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Log Out", type="secondary"):
            st.session_state.is_logged_in = False
            del st.session_state["teacher_data"]
            st.session_state.user_role = None
            st.session_state["teacher_login_type"] = "login"
            st.toast("Logged out successfully!")
            import time            
            time.sleep(1)
            st.rerun()
    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"
    tab1,tab2,tab3=st.columns(3)
    with tab1:
        type1="primary" if st.session_state.current_teacher_tab=="take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, icon="📸", width="stretch"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()
            
    with tab2:
        type2="primary" if st.session_state.current_teacher_tab=="manage_subjects" else "tertiary"
        if st.button("Manage Subjects", type=type2, icon="📚", width="stretch"):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()
            
    with tab3:
        type3="primary" if st.session_state.current_teacher_tab=="view_attendance" else "tertiary"
        if st.button("View Attendance Records", type=type3, icon="📊", width="stretch"):
            st.session_state.current_teacher_tab = "view_attendance"
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_subjects":
        teacher_manage_subjects()
    elif st.session_state.current_teacher_tab == "view_attendance":
        teacher_view_attendance()
    
    footer_dashboard()


def teacher_take_attendance():
    teacher_id=st.session_state["teacher_data"]["teacher_id"]
    st.header("Take Attendance")

    if "attendance_image" not in st.session_state:
       st.session_state["attendance_image"] = []
    subjects=get_teacher_subjects(teacher_id)

    if not subjects:
       st.warning("No subjects found. Please add a subject to get started.")
       return
    subject_options = {
    f"{s['name']}-{s['subject_code']}": s['subject_id']
    for s in subjects
}
   

    col1,col2=st.columns([3,1])
    with col1:
       selected_subject= st.selectbox("Select Subject", options=list(subject_options.keys()), key="selected_subject")

    with col2:
        if st.button("Add Images", type="primary", icon="📤", use_container_width=True):
            add_image_dialog(subject_options[selected_subject])
    
    st.divider()
    st.header("Captured Images")
    if st.session_state["attendance_image"]:
        st.write("Preview:")
        cols = st.columns(4)
        for idx, img in enumerate(st.session_state["attendance_image"]):
            with cols[idx % 4]:
                st.image(img, use_container_width=True)

        c1,c2,c3=st.columns(3)
        with c1:
            if st.button("clear images", type="secondary", width="stretch", icon="🗑️"):
                st.session_state["attendance_image"] = []
                st.rerun()
        with c2:
            has_photos = len(st.session_state["attendance_image"]) > 0
            if st.button("Run Face Analysis", type="primary", width="stretch", icon="🤖", disabled=not has_photos):
                with st.spinner("Running face analysis..."):
                    all_detected_faces={}
                    for idx, img in enumerate(st.session_state["attendance_image"]):
                        img_np = np.array(img.convert("RGB"))
                        detected,_,_=predict_attendance(img_np)
                        if detected:
                            for sid in detected.keys():
                                student_id=int(sid)
                                all_detected_faces.setdefault(student_id, []).append({"Photo Index": idx+1})
                    
                    enrolled_res=supabase.table("subject_students").select("*,students(*)").eq("subject_id", subject_options[selected_subject]).execute()
                    enrolled_students=enrolled_res.data
                    if not enrolled_students:
                        st.warning("No students enrolled in this subject. Detected faces cannot be matched to any student.")
                        return
                    else:
                        results,attendance_log=[],[]

                        current_timestamp=datetime.now().isoformat()

                        for enrollment in enrolled_students:
                            student=enrollment["students"]
                            sources=all_detected_faces.get(int(student["student_id"]), [])
                            is_present = len(sources) > 0

                            results.append({
                                "Student ID": student["student_id"],
                                "Name": student["name"],
                    
                                "Detected In": ", ".join([f"Img {s['Photo Index']}" for s in sources]) if is_present else "Not Detected",
                                "Attendance Status": "Present" if is_present else "Absent"
                            })

                            attendance_log.append({
                                "student_id": student["student_id"],
                                "subject_id": subject_options[selected_subject],
                                "timestamp": current_timestamp,
                                "date":date.today().isoformat(),
                                "is_present": is_present
                            })
                    attendance_result_dialog(pd.DataFrame(results), attendance_log)
        with c3:
            if st.button("Use Voice Attendance", type="secondary", width="stretch", icon="🎤"):
                voice_attendance_dialog()

def teacher_manage_subjects():
    teacher_id=st.session_state["teacher_data"]["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h2 style='color: black; text-align: center;'>Manage Subject</h2>", unsafe_allow_html=True)
    with col2:
       if st.button("Add New Subject", type="secondary", icon="➕", width="content", use_container_width=True):
           create_subject_dialog(teacher_id)
    
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats=[
                ("🧑‍🎓", "Students", sub["total_students"]),
                ("📅", "Classes", sub["total_classes"])
            ]
            def share_button(sub=sub):
                if st.button("Share Subject", type="secondary", icon="🔗", width="content", key=f"share_{sub['subject_code']}"):
                    share_subject_dialog(sub["name"],sub["subject_code"])
                st.space()
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                stats=stats,
                section=sub["section"],
                footer_callback=share_button
            )
    else:
        st.warning("No subjects found. Please add a subject to get started.")


def teacher_view_attendance():
    st.markdown("<h2 style='color: black; text-align: center'>View Attendance Records</h2>", unsafe_allow_html=True)
    st.info("This feature is under development. Please check back later.")
    # Future implementation: Display attendance records with filtering options.
            

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

    