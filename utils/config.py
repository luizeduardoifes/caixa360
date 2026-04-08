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


def proteger_pagina_completa():
    if not st.session_state.get("logado"):
        st.warning("Faça login primeiro")
        if st.button("voltar para login", key="voltar_login"):
            st.switch_page("app.py")
        st.stop()

    if not st.session_state.get("usuario_id"):
        st.error("Sessão inválida. Faça login novamente.")
        if st.button("voltar para login", key="voltar_para_login"):
            st.switch_page("app.py")
        st.stop()