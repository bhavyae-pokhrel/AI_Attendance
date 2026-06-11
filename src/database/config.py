from supabase import create_client, Client
import streamlit as st

supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# supabase = create_client(
#     st.secrets["SUPABASE_URL"],
#     st.secrets["SUPABASE_KEY"]
# )