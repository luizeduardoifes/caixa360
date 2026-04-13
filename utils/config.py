import streamlit as st

def configurar_pagina(mostrar_sidebar=False):
    # ⚙️ config base
    st.set_page_config(
        layout="wide" if mostrar_sidebar else "centered",
        initial_sidebar_state="expanded" if mostrar_sidebar else "collapsed"
    )

    # 🔐 controle de login
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        esconder_sidebar()

    # 🎨 sidebar
    if not mostrar_sidebar:
        esconder_sidebar()


def esconder_sidebar():
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {display: none;}
            [data-testid="collapsedControl"] {display: none;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)


def proteger_pagina():
    if not st.session_state.get("logado"):
        st.warning("Faça login primeiro")
        if st.button("Voltar para login"):
            st.switch_page("app.py")
        st.stop()

def proteger_troca_senha():
    if not st.session_state.get("trocar_senha"):
        st.error("Acesso inválido")
        if st.button("Voltar para login"):
            st.switch_page("app.py")
        st.stop()