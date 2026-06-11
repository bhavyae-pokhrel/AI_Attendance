import streamlit as st

import segno #! generate QR codes
import io #! when handle binary data, io module provides tools for working with in-memory file-like objects
#! Instead of saving a file to disk, you can store it in memory using BytesIO.


@st.dialog("Share Class Link")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "ai-snapclasses-main.streamlit.app"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header("Scan to Join")

    qr = segno.make(join_url)

    out = io.BytesIO()

    qr.save(out, kind='png', scale=10, border=1)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language="text") #! provide copy option
        st.code(subject_code, language="text")
        st.info('Copy this link to share on Whatsapp or Email')

    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), caption='QRCODE for class joining')

        