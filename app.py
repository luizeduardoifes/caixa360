import streamlit as st
from repo.caixa360_repo import criar_tabela_extrato
from repo.usuarios_repo import criar_tabela_usuarios
from services.seguranca_senha import verificar_login

criar_tabela_extrato()
criar_tabela_usuarios()

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

    resultado = verificar_login(usuario, senha)

    if resultado:
        user_id, trocar_senha = resultado

        st.session_state.logado = True
        st.session_state.usuario_id = user_id

        # 🔥 AQUI É O PULO DO GATO
        if trocar_senha == 1:
            st.switch_page("pages/trocar_senha.py")
        else:
            st.switch_page("pages/menu.py")

    else:
        st.error("Usuário ou senha inválidos")