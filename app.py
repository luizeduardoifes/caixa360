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



st.title("Login")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):
    if usuario == "admin" and senha == "123":
        st.switch_page("pages/operacao.py")
    else:
        st.error("Usuário ou senha inválidos")