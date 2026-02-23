from datetime import *
import streamlit as st
from models.caixa360 import Caixa360
from repo.caixa360_repo import *
saldo = 0
def entrada(tipo_operacao, valor_operacao, descricao_operacao):
    global saldo
    saldo += valor_operacao
    hora = datetime.now().strftime("%H:%M:%S")
    data = date.now().strftime("%Y-%m-%d")
    dados = Caixa360(id=0,data=data, hora=hora, valor=saldo, tipo=tipo_operacao, descricao=descricao_operacao)
    inserir_extrato(dados)
    st.success("Operação de entrada gravada com sucesso!")


def validacao(tipo_operacao, valor_operacao, descricao_operacao):
    erro = []
    if tipo_operacao == "Selecione uma operação":
        erro.append("Selecione um tipo de operação.")

    if valor_operacao <= 0:
        erro.append("O valor da operação deve ser maior que zero.")

    if not descricao_operacao.strip():
        erro.append("A descrição da operação não pode estar vazia.")

    if erro:
        for msg in erro:
            st.error(msg)
    
    else:
        entrada(tipo_operacao, valor_operacao, descricao_operacao)
