import streamlit as st



def mostrar_resultado(operacao, valor, categoria,saldo_anterior,novo_saldo):

    st.write(f"Operação: {operacao.capitalize()}")
    st.write(f"Valor: R$ {valor:.2f}")
    st.write(f"Categoria: {categoria}\n")
    st.write(f"Saldo anterior: R$ {saldo_anterior:.2f}")
    st.write(f"Novo saldo: R$ {novo_saldo:.2f}\n")
