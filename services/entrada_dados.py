import datetime

import streamlit as st

from services.auth import get_usuario_id
from models.caixa360 import Caixa360
from repo.caixa360_repo import inserir_extrato, obter_saldo_atual
from services.exibir_resultado import mostrar_resultado

# Antes este arquivo fazia "import datetime" (o módulo) mas chamava
# datetime.now() (que só existe na classe datetime.datetime). Isso só não
# quebrava porque "from services.tratamento_comandos import *" era importado
# depois e reexportava o nome "datetime" da classe, sobrescrevendo o módulo
# — um import circular escondido (tratamento_comandos importa get_dados
# daqui, e este arquivo importava tudo de lá). Removido o import circular e
# corrigido para datetime.datetime.now() explicitamente.


def get_dados(operacao: str, valor: float, categoria: str):
    """Registra uma entrada ou saída, sempre a partir do saldo mais atual do usuário."""
    usuario_id = get_usuario_id()
    saldo_anterior = obter_saldo_atual(usuario_id)

    if operacao == "entrada":
        novo_saldo = saldo_anterior + valor
    elif operacao == "saida":
        novo_saldo = saldo_anterior - valor
    else:
        st.error("Operação inválida.")
        return

    dados = Caixa360(
        id=0,
        usuario_id=usuario_id,
        data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        valor=valor,
        tipo=operacao,
        categoria=categoria,
        saldo=novo_saldo,
    )

    inserir_extrato(dados)

    if operacao == "entrada":
        mostrar_resultado(operacao, valor, categoria,saldo_anterior,novo_saldo)
        st.success("Entrada registrada com sucesso!")
    
    if operacao == "saida":
        mostrar_resultado(operacao, valor, categoria,saldo_anterior,novo_saldo)
        st.success("Saída registrada com sucesso!")
