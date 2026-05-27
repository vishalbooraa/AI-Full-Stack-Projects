import streamlit as st

def style_background_home():
    st.markdown("""
    <style>
        .stApp{
              background: #5865F2 !important
            }
        .stApp div[data-testid="stColumn"]{
                background-color:#E0E3FF !important;
                padding:2.5rem !important;
                border-radius: 5rem !important;
                color:black !important;
        }
    </style>

""",unsafe_allow_html=True)
    

def style_background_dashboard():
    st.markdown("""
    <style>
        .stApp{
              background: #E0E3FF !important
            }
    </style>

""",unsafe_allow_html=True)
    
def style_base_layout():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&family=Outfit:wght@100..900&display=swap');

    /* ---------------- GLOBAL FONT ---------------- */
    html, body {
        font-family: 'Outfit', sans-serif !important;
    }

    /* ---------------- HEADINGS ONLY ---------------- */
    h1, h2, h3,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3 {
        font-family: 'Climate Crisis', sans-serif !important;
        letter-spacing: 1px;
    }

    /* ---------------- BUTTONS ---------------- */
    button {
        background: #5965F2 !important;
        border-radius: 1.5rem !important;
        color: white !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: transform 0.2s ease-in-out !important;
    }

    button[kind="secondary"] {
        background: #EB459E !important;
        color: white !important;
    }

    button[kind="tertiary"] {
        background: #f2f4f8 !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
    }

    button:hover {
        transform: scale(1.05);
    }

    /* ---------------- INPUT FIELDS ---------------- */
    div[data-baseweb="input"] {
        background-color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ccc !important;
    }

    div[data-baseweb="input"] input {
        color: black !important;
    }

    div[data-baseweb="input"] button {
        background-color: white !important;
        color: black !important;
    }

    div[data-baseweb="input"] button:hover {
        background-color: #f5f5f5 !important;
    }

    /* ---------------- LABELS ---------------- */
    label {
        color: black !important;
    }

    input::placeholder, textarea::placeholder {
        color: #555 !important;
    }
    
    /* ---------------- INPUT FIX (SAFE) ---------------- */

    /* Main input container */
    div[data-baseweb="input"] {
        background-color: white !important;
        border-radius: 10px !important;
        border: 1px solid #ccc !important;
    }

    /* Inner wrapper */
    div[data-baseweb="input"] > div {
        background-color: white !important;
    }

    /* Actual text input */
    div[data-baseweb="input"] input {
        background-color: white !important;
        color: black !important;
    }

    /* Password eye icon */
    div[data-baseweb="input"] button {
        background-color: white !important;
        color: black !important;
    }

    /* Hover fix */
    div[data-baseweb="input"] button:hover {
        background-color: #f5f5f5 !important;
    }

    /* Placeholder */
    div[data-baseweb="input"] input::placeholder {
        color: #777 !important;
    }
    /* ---------------- THEMED DIALOG ---------------- */

    /* Dialog background */
    div[role="dialog"] {
        background-color: #E0E3FF !important;
        border-radius: 1.5rem !important;
    }

    /* Labels */
    div[role="dialog"] label {
        color: #1a1a1a !important;
        font-weight: 500;
    }

    /* Input container */
    div[role="dialog"] div[data-baseweb="input"] {
        background-color: white !important;
        border: 2px solid transparent !important;
        border-radius: 0.8rem !important;
        transition: all 0.2s ease-in-out !important;
    }

    /* Input text */
    div[role="dialog"] input {
        color: black !important;
    }

    /* Placeholder */
    div[role="dialog"] input::placeholder {
        color: #888 !important;
    }

    /* Focus effect (🔥 matches theme) */
    div[role="dialog"] div[data-baseweb="input"]:focus-within {
        border: 2px solid #5965F2 !important;
        box-shadow: 0 0 0 2px rgba(89, 101, 242, 0.2) !important;
    }

    /* Button override inside dialog */
    div[role="dialog"] button[kind="primary"] {
        background: #5965F2 !important;
        color: white !important;
    }

    div[role="dialog"] button[kind="secondary"] {
        background: #EB459E !important;
        color: white !important;
    }

    div[role="dialog"] button[kind="tertiary"] {
        background: #f2f4f8 !important;
        color: #1a1a1a !important;
        border: 1px solid #ccc !important;
    }

    div[role="dialog"] h1,
    div[role="dialog"] h2 {
        text-shadow: 0 2px 8px rgba(89, 101, 242, 0.2);
    }
    /* ---------------- FIX DIALOG TEXT COLORS ---------------- */

    /* Dialog title (e.g. "Quick Enroll in Class") */
    div[role="dialog"] [data-testid="stDialogTitle"] {
        color: #1a1a1a !important;
    }

    /* All normal text inside dialog (st.write, markdown, etc.) */
    div[role="dialog"] p,
    div[role="dialog"] span,
    div[role="dialog"] div {
        color: #1a1a1a !important;
    }

    /* Markdown container text */
    div[role="dialog"] [data-testid="stMarkdownContainer"] {
        color: #1a1a1a !important;
    }
    /* ---------------- CODE BLOCK FIX (DIALOG) ---------------- */

    /* Code block container */
    div[role="dialog"] pre {
        background-color: white !important;
        color: black !important;
        border-radius: 0.8rem !important;
        padding: 12px !important;
        border: 1px solid #ccc !important;
    }

    /* Inner code text */
    div[role="dialog"] code {
        color: #333 !important;
        font-family: 'Outfit', monospace !important;
    }
    </style>
    """, unsafe_allow_html=True)