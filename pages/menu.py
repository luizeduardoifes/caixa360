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

# inicializa estado
if "mensagem" not in st.session_state:
    st.session_state.mensagem = ""

texto = st.text_input("Mensagem")
botao = st.button("Enviar")

# salva quando clicar
if botao:
    st.session_state.mensagem = texto

# processa usando estado (não perde no reload)
if st.session_state.mensagem:
    with st.spinner("Processando..."):
        interpretar_comando(st.session_state.mensagem)



    