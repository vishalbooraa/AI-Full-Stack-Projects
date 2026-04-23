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
    @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&family=Plus+Jakarta+Sans:ital,wght@0,200..800;1,200..800&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

    /* Hide Streamlit UI */
    #MainMenu, footer, header {
        visibility: hidden;
    }

    .block-container{
        padding-top:1.5rem !important;       
    }

    /* GLOBAL FONT FIX */
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Headings */
    h1, h2 {
        font-family:'Climate Crisis', sans-serif !important;
        font-size:2rem !important;
        line-height:1.1 !important;
        margin-bottom:0rem !important;
    }

    /* Force text inside Streamlit */
    .stMarkdown, .stText, .stHeader, p, span, div {
        font-family: 'Outfit', sans-serif !important;
    }

    /* Buttons */
    button {
        background: #5965F2 !important;
        border-radius:1.5rem !important;
        color:white !important;
        padding: 10px 20px !important;
        border: none !important;
        transition: transform 0.25s ease-in-out !important;
        font-family: 'Outfit', sans-serif !important;
    }

    button[kind="secondary"]{
        background: #EB459E !important;
    }

    button[kind="tertiary"]{
        background: black !important;
    }

    button:hover{
        transform: scale(1.05);
    }
    /* Text Input */
    input {
        background-color: white !important;
        color: black !important;
    }
    /* Labels */
    label {
        color: black !important;
    }
    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #555 !important;
    }
    /* Full input container (VERY IMPORTANT) */
    div[data-baseweb="input"] {
        background-color: white !important;
        color: black !important;
    }

    /* Inner wrapper (this fixes black patch near eye) */
    div[data-baseweb="input"] > div {
        background-color: white !important;
    }

    /* Actual input field */
    div[data-baseweb="input"] input {
        background-color: white !important;
        color: black !important;
    }

    /* Eye icon button */
    div[data-baseweb="input"] button {
        background-color: white !important;
        color: black !important;
    }

    /* Remove weird hover dark effect */
    div[data-baseweb="input"] button:hover {
        background-color: #f5f5f5 !important;
    }

    /* Optional: border styling for clean UI */
    div[data-baseweb="input"] {
        border-radius: 10px !important;
        border: 1px solid #ccc !important;
    }
    

    </style>
    """, unsafe_allow_html=True)