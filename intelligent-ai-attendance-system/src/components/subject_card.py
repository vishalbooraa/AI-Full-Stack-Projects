import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    # Apply custom CSS for the card styling (only once)
    st.markdown("""
        <style>
        .custom-subject-card {
            background: white;
            border-left: 8px solid #5865F2;
            padding: 25px;
            border-radius: 20px;
            border: 1px solid #e2e8f0;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        }
        .subject-title {
            margin: 0;
            color: #1e293b !important;
            font-size: 1.5rem;
            font-family: sans-serif;
        }
        .subject-code {
            color: #64748b;
            margin: 10px 0;
            font-family: sans-serif;
        }
        .code-badge {
            background: #E0E3FF;
            color: #5865F2;
            padding: 2px 8px;
            border-radius: 5px;
            font-weight: 600;
        }
        .stats-container {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 15px;
        }
        .stat-badge {
            background: #fdf2f8;
            color: #be185d;
            padding: 6px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-family: sans-serif;
            border: 1px solid #fbcfe8;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Build complete HTML string in one go to avoid empty divs
    html = f"""
    <div class="custom-subject-card">
        <h3 class="subject-title">{name}</h3>
        <p class="subject-code">Code: <span class="code-badge">{code}</span> | Section: <b>{section}</b></p>
    """
    
    if stats:
        html += '<div class="stats-container">'
        for icon, label, value in stats:
            html += f'<div class="stat-badge">{icon} <span style="margin-left: 4px;"><b>{value}</b> {label}</span></div>'
        html += '</div>'
    
    html += '</div>'
    
    # Render everything at once
    st.markdown(html, unsafe_allow_html=True)
    
    # Footer callback button
    if footer_callback:
        footer_callback()