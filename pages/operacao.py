import streamlit as st

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