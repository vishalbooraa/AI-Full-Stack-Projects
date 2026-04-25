import streamlit as st
from src.ui.style_base_layout import style_background_dashboard
from src.ui.style_base_layout import style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from PIL import Image
import numpy as np

def student_screen():
    style_background_dashboard()
    style_base_layout()
    
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
    "<h1 style='text-align: center; color: black;'>Log in using faceID</h1>",
    unsafe_allow_html=True
    )
    
    photo=st.camera_input("Position your face in the center of the camera")

    if photo:
        np.array(Image.open(photo))
    footer_dashboard()
