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
        </style>
    """, unsafe_allow_html=True)


def proteger_pagina():
    if not st.session_state.get("logado"):
        st.warning("Faça login para acessar")
        st.stop()