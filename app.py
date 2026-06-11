import streamlit as st
from src.screens.student_screen import student_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.home_screen import home_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog
def main():

    st.set_page_config(
        page_title='SnapClass - Making Attendance faster using AI',
        page_icon= "https://i.ibb.co/YTYGn5qV/logo.png"
    )

    if 'login_type' not in st.session_state:  #! use the if/else instead
        st.session_state['login_type'] = None
    
    match st.session_state['login_type']:
        case 'teacher':
            teacher_screen()
        case 'student':
            student_screen()
        case None:
            home_screen()
    
    join_code = st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type != 'student':
            st.session_state.login_type = 'student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role') == 'student':
            auto_enroll_dialog(join_code)

if __name__ == "__main__":
    main()


# def main():
#     st.header("Title Here")
#     name = st.text_input("Enter the name")

#     col1,col2 = st.columns(2,gap="small")

#     with col1: #! Put all the UI elements written inside this block into col1.
#         if st.button('Hi',type= "primary",key="btn1",width=300): #!if means clicked
#             print('hi',name)  #! width="stretch" -> cover max-width && width="content" cover min-width as per content
        
#     with col2:
#         if st.button('Bye',type= "secondary",key="btn2", width="stretch"):
#             print('hi',name) 
#     # st.button("Submit") st.button("Submit") -> st.button("Submit", key="btn1") st.button("Submit", key="btn2") #! key="btn2"/"btn1" used when label && text is same

#     st.markdown("""
#         <div>
#             <p>This is paragraph text</p>
#         </div>
#     """,unsafe_allow_html=True) #! unsafe_allow_html=True trat as p tag otherwise it will treat as text only

# main()