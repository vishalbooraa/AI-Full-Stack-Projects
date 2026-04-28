import streamlit as st
from src.database.db import create_subject



@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details for the new subject")
    sub_id=st.text_input("Subject ID", placeholder="e.g., MATH101")
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
                st.close_dialog()
            else:
                st.error("Failed to create subject. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")