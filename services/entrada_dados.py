import datetime
import streamlit as st
from services.auth import get_usuario_id
from services.tratamento_comandos import *
from models.caixa360 import Caixa360
from repo.caixa360_repo import inserir_extrato, obter_saldo_atual


def get_dados(operacao, valor, categoria):

    if operacao == "entrada":
        saldo = obter_saldo_atual() + valor
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados = Caixa360(
            id=0,
            usuario_id = get_usuario_id(),
            data=data,
            valor=valor,
            tipo=operacao,
            categoria=categoria,
            saldo=saldo
        )

        inserir_extrato(dados)
        st.success("Entrada registrada com sucesso!")

    elif operacao == "saida":
        saldo = obter_saldo_atual() - valor
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados = Caixa360(
            id=0,
            usuario_id = get_usuario_id(),
            data=data,
            valor=valor,
            tipo=operacao,
            categoria=categoria,
            saldo=saldo
        )

        inserir_extrato(dados)
        st.success("Saída registrada com sucesso!")