import streamlit as st
from services.tratamento_comandos import *
from utils.config import configurar_pagina

configurar_pagina(mostrar_sidebar=False)

st.title("Caixa360")

with st.form("form_comando"):
    texto = st.text_input("Mensagem")
    enviado = st.form_submit_button("Enviar")

if enviado:
    with st.spinner("Processando..."):
        interpretar_comando(texto)

    