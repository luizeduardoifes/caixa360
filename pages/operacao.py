import streamlit as st

from services.funções import *

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

st.title("Operação")

tipo_operacao = st.selectbox("Tipo de Operação", ["Selecione uma operação", "Entrada", "Saída"])
valor_operacao = st.number_input("Valor da Operação")
descricao_operacao = st.text_input("Descrição da Operação")

if st.button("Gravar Operação", use_container_width=True):
    if validacao(tipo_operacao, valor_operacao, descricao_operacao):
        get_dados(tipo_operacao, valor_operacao, descricao_operacao)

if st.button("Voltar ao Menu Principal", use_container_width=True):
    st.switch_page("pages/menu.py")
        
