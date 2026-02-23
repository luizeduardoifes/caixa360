import streamlit as st

st.set_page_config(layout="centered")


if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none;
            }
        </style>
    """, unsafe_allow_html=True)

st.title("Caixa360")
st.markdown("Menu")

col1, col2, col3 = st.columns(3)

if st.button("Operação", use_container_width=True):
    st.switch_page("pages/operacao.py")

if st.button("sair do sistema", use_container_width=True):
    st.switch_page("app.py")
