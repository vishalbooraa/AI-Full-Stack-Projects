import streamlit as st
from src.ui.style_base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np
import time

from src.pipelines.face_pipeline import (
    predict_attendance,
    get_face_embeddings,
    train_classifier
)
from src.database.db import get_all_students, create_student
from src.pipelines.voice_pipeline import get_voice_embedding


# ---------------- DASHBOARD ---------------- #
def student_dashboard():
    student_data = st.session_state["student_data"]

    st.markdown(
        f"<h1 style='color: black; text-align: center'>Welcome, {student_data['name']}!</h1>",
        unsafe_allow_html=True
    )


# ---------------- MAIN SCREEN ---------------- #
def student_screen():
    style_background_dashboard()
    style_base_layout()

    # If already logged in → go dashboard
    if "student_data" in st.session_state:
        student_dashboard()
        return

    # Session state for registration toggle
    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    # HEADER
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Go Back to Home", type="secondary"):
            st.session_state["login_type"] = None
            st.rerun()

    st.space()
    st.space()

    st.markdown(
        "<h1 style='text-align: center; color: black;'>Log in using FaceID</h1>",
        unsafe_allow_html=True
    )

    # CAMERA INPUT
    photo = st.camera_input("Position your face in the center of the camera")

    if photo:
        img = np.array(Image.open(photo))

        with st.spinner("AI is Scanning..."):
            detected, all_ids, num_faces = predict_attendance(img)
            print(f"Detected: {detected}, All IDs: {all_ids}, Num Faces: {num_faces}")

        # -------- FACE VALIDATION -------- #
        if num_faces == 0:
            st.warning("No faces detected. Please try again.")

        elif num_faces > 1:
            st.warning("Multiple faces detected. Please ensure only your face is visible.")

        else:
            if detected:
                student_id = list(detected.keys())[0]

                all_students = get_all_students()

                student = next(
                    (s for s in all_students if s["student_id"] == student_id),
                    None
                )

                if student:
                    st.toast(f"Welcome, {student['name']}!")

                    st.session_state["student_data"] = student
                    st.session_state["user_role"] = "student"
                    st.session_state["is_logged_in"] = True

                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Student record not found.")

            else:
                st.error("Face not recognized. Please register first.")
                st.session_state.show_registration = True

    # ---------------- REGISTRATION ---------------- #
    if st.session_state.show_registration:
        with st.container(border=True):
            st.header("Face not recognized. Please register.")

            new_name = st.text_input("Enter your name:", placeholder="Enter your name")

            st.subheader("Optional: Voice Enrollment")
            st.info("This helps improve accuracy but is optional.")

            audio_data = None

            try:
                audio_data = st.audio_input(
                    "Record: 'I am present, my name is ...'"
                )
            except Exception:
                st.warning("Audio input not supported in this browser.")

            if st.button("Register", type="primary"):

                if not new_name:
                    st.error("Please enter your name.")
                    return

                with st.spinner("Registering your face and voice..."):

                    img = np.array(Image.open(photo))
                    encodings = get_face_embeddings(img)

                    if not encodings:
                        st.error("Face not detected clearly. Try again.")
                        return

                    # Face embedding
                    face_embedding = encodings[0].tolist()

                    # Voice embedding (optional)
                    voice_embedding = None
                    if audio_data is not None:
                        try:
                            voice_embedding_raw = get_voice_embedding(audio_data)
                            if voice_embedding_raw is not None:
                                voice_embedding = voice_embedding_raw.tolist()
                        except Exception as e:
                            st.warning(f"Voice processing failed: {e}")

                    # Store in DB
                    response_data = create_student(
                        new_name,
                        face_embedding,
                        voice_embedding
                    )

                    if response_data:
                        train_classifier()  # retrain model

                        st.toast(f"Profile Created, {new_name}!")

                        st.session_state["student_data"] = response_data[0]
                        st.session_state["user_role"] = "student"
                        st.session_state["is_logged_in"] = True

                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Registration failed. Try again.")

    footer_dashboard()