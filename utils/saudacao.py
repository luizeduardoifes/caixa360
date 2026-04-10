from datetime import datetime
import streamlit as st

def saudacao_usuario():
    nome = st.session_state.get("usuario")

    if not nome:
        return

    hora = datetime.now().hour

    if hora < 12:
        saudacao = "Bom dia"
    elif hora < 18:
        saudacao = "Boa tarde"
    else:
        saudacao = "Boa noite"

    st.markdown(f"""
        <style>
        .saudacao-box {{
            margin-top: -30px;
            margin-bottom: 5px;
            margin-left: -10px;
            font-size: 16px;
            font-weight: 500;
            color: white;
        }}
        </style>

        <div class="saudacao-box">
            👋 {saudacao}, <strong>{nome}</strong>
        </div>
    """, unsafe_allow_html=True)