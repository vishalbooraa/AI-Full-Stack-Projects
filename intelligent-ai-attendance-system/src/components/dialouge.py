import streamlit as st
from src.database.db import create_subject
import segno
import io
from src.database.config import supabase
import time
from src.database.db import enroll_student_to_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details for the new subject")
    sub_id=st.text_input("Subject Code", placeholder="e.g., MATH101")
    sub_name=st.text_input("Subject Name", placeholder="e.g., Calculus I")
    sub_section=st.text_input("Section", placeholder="e.g., A")

    if st.button("Create Subject", type="primary",width="stretch"):
        if not sub_id or not sub_name or not sub_section:
            st.warning("Please fill in all fields")
            return
        try:
            response = create_subject(teacher_id, sub_id, sub_name, sub_section)
            if response:
                st.toast("Subject created successfully!")
            else:
                st.error("Failed to create subject. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


@st.dialog("share class link")
def share_subject_dialog(subject_name,subject_code):
    app_domain="http://localhost:8501"
    join_url=f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    qr=segno.make(join_url)
    out = io.BytesIO()

    qr.save(out, kind="png",scale=10,border=1)

    col1,col2=st.columns(2)

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this link to share on whatsapp or email")

    with col2:
        st.markdown("### Scan QR Code to join")
        st.image(out.getvalue(),caption="Scan this QR code to join the class")


@st.dialog("Enroll in New Class")
def enroll_new_class_dialog():
    st.write("Enter the subject code to join the class")
    join_code = st.text_input("Subject Code", placeholder="e.g., MATH101")

    if st.button("Enroll now", type="primary", width="stretch"):
        if not join_code:
            st.warning("Please enter a subject code")
            return

        try:
            res = supabase.table("subjects") \
                .select("*") \
                .eq("subject_code", join_code) \
                .single() \
                .execute()

            subject = res.data

            if not subject:
                st.error("Invalid subject code. Please check and try again.")
                return

            student_id = st.session_state["student_data"]["student_id"]

            check = supabase.table("subject_students") \
                .select("*") \
                .eq("subject_id", subject["subject_id"]) \
                .eq("student_id", student_id) \
                .execute()

            if check.data:
                st.warning("You are already enrolled in this class")
                return

    
            enroll_student_to_subject(student_id, subject["subject_id"])

            st.toast(f"Enrolled in {subject['name']} successfully!")
            time.sleep(1)
            st.rerun()

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


@st.dialog("Quick Enroll in Class")
def auto_enroll_dialog(join_code):

    student_id = st.session_state["student_data"]["student_id"]

    print("Auto Enroll Dialog: Student ID:", student_id)  # Debugging line
    print("Auto Enroll Dialog Triggered with join code:", join_code)  # Debugging line'

    res = supabase.table("subjects")\
        .select("*")\
        .eq("subject_code", join_code)\
        .maybe_single()\
        .execute()
    print("Auto Enroll Query Result:", res)  # Debugging line

    if not res or not res.data:
        st.error("Invalid join code. Please check the link and try again.")
        if st.button("Close", type="primary"):
            st.query_params.clear()
            st.rerun()
        return

    subject = res.data  

    check = supabase.table("subject_students")\
        .select("*")\
        .eq("subject_id", subject["subject_id"])\
        .eq("student_id", student_id)\
        .execute()

    if check.data:
        st.warning(f"You are already enrolled in {subject['name']}")
        if st.button("Got it!", type="primary"):
            st.query_params.clear()
            st.rerun()
        return

    st.markdown(f"## Do you want to enroll in **{subject['name']}**?")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("No Thanks", type="secondary", width="stretch"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("Enroll now", type="primary"):
            enroll_student_to_subject(student_id, subject["subject_id"])
            st.toast(f"Enrolled in {subject['name']} successfully!")
            time.sleep(1)
            st.query_params.clear()
            st.rerun()