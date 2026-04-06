import streamlit as st
from services.tratamento_comandos import *

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

with st.form("form_comando"):
    texto = st.text_input("Mensagem")
    enviado = st.form_submit_button("Enviar")

st.write("Texto recebido:", texto)

# if enviado:
#     with st.spinner("Processando..."):
#         interpretar_comando(texto)

    