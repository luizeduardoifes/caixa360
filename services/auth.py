import streamlit as st

def get_usuario_id():
    return st.session_state.get("usuario_id")