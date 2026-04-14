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
            /* Esconde sidebar */
            [data-testid="stSidebar"] {display: none !important;}
            [data-testid="collapsedControl"] {display: none !important;}

            /* Esconde elementos padrão */
            #MainMenu {visibility: hidden !important;}
            footer {visibility: hidden !important;}
            header {visibility: hidden !important;}

            /* Tenta esconder links do GitHub */
            a[href*="github"] {
                display: none !important;
                width: 0px !important;
                height: 0px !important;
                overflow: hidden !important;
            }

            /* Caso o botão ainda apareça (fallback) */
            div[data-testid="stToolbar"] {
                position: fixed !important;
                right: -100px !important; /* joga pra fora da tela */
                top: 0px !important;
                opacity: 0 !important; /* invisível */
                pointer-events: none !important;
            }

            /* Reduz qualquer botão no topo */
            button[kind="header"] {
                transform: scale(0.5) !important;
                opacity: 0 !important;
            }

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