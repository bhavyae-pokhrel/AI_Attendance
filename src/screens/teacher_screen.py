import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'teacher_login_type' not in st.session_state:
        st.session_state['teacher_login_type'] = 'login'

    if st.session_state.teacher_login_type == 'login':
        teacher_screen_login()
    elif st.session_state.teacher_login_type == 'register':
        teacher_screen_register()


def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='login_backbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password')
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='ananyaroy', key='login_username')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password", key='login_pass')

    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='login_btn')
    with btnc2:
        if st.button('Register Instead', type="primary", icon=':material/passkey:', width='stretch', key='to_register_btn'):
            st.session_state['teacher_login_type'] = 'register'
            st.rerun()

    footer_dashboard()


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='large')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='register_backbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Register your teacher profile')
    st.space()
    st.space()

    teacher_username = st.text_input("Enter username", placeholder='ananyaroy', key='reg_username')
    teacher_name = st.text_input("Enter name", placeholder='Ananya Roy', key='reg_name')
    teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password", key='reg_pass')
    teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password", key='reg_pass_confirm')

    st.divider()

    btnc1, btnc2 = st.columns(2)
    with btnc1:
        st.button('Register now', icon=':material/passkey:', shortcut='control+enter', width='stretch', key='register_btn')
    with btnc2:
        if st.button('Login Instead', type="primary", icon=':material/passkey:', width='stretch', key='to_login_btn'):
            st.session_state['teacher_login_type'] = 'login'
            st.rerun()

    footer_dashboard()
