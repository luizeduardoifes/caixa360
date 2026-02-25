from datetime import *
import streamlit as st
from models.caixa360 import Caixa360
from repo.caixa360_repo import *

def get_dados(tipo_operacao, valor_operacao, descricao_operacao):
    if tipo_operacao == "Entrada":
        saldo = obter_saldo_atual() + valor_operacao
        data = datetime.now()
        dados = Caixa360(id=0,data=data, valor=valor_operacao, tipo=tipo_operacao, descricao=descricao_operacao, saldo=saldo)
        inserir_extrato(dados)
        st.success("Operação tipo entrada gravada com sucesso!")
    
    elif tipo_operacao == "Saída":
        saldo = obter_saldo_atual() - valor_operacao
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados = Caixa360(id=0,data=data, valor=valor_operacao, tipo=tipo_operacao, descricao=descricao_operacao, saldo=saldo)
        inserir_extrato(dados)
        st.success("Operação tipo saída gravada com sucesso!")


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

