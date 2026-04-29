import streamlit as st
from src.database.db import create_subject
import segno
import io


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

