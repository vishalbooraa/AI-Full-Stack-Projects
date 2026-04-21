import streamlit as st


def header_home():
    logo_url = "https://cdn-icons-png.flaticon.com/512/3135/3135755.png"
    
    st.markdown(f"""
            <div style='display:flex; flex-direction:column; align-items:center; justify-content:center; margin-bottom:30px; margin-top:10px'>
            <img src='{logo_url}' style='height:100px'>
            <h1 style='text-align:center; color:#E0E3FF; font-family: "Climate Crisis", sans-serif;'>AttendFusion AI</h1>
            </div>
    """,unsafe_allow_html=True)