import streamlit as st

def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; justify-content:center; align-items:center;margin-top:30px; margin-bottom:30px;">
            <img src='{logo_url}' style='height:100px;'/> 
            <h1 style="text-align:center;color:#E0E3FF">SNAP CLASS</h1> 
        </div>
        
    """,unsafe_allow_html=True)
    #st.header("Snap Class") #! Bydefault used h2 && Streamlit automatically creates an anchor link for title/header