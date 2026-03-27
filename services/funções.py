import re
from datetime import *
import streamlit as st
from models.caixa360 import Caixa360
from repo.caixa360_repo import *
import pandas as pd

def consultar_extrato():
    dados = listar_extrato()
    saldo_atual = obter_saldo_atual()
    if dados:
        st.write("EXTRATO:")
        df = pd.DataFrame(dados, columns=["id","data", "valor", "tipo", "categoria", "saldo"])
        st.dataframe(df, use_container_width=True)
        st.write(f"Saldo Atual: {saldo_atual}")
    else:
        st.info("Nenhum registro encontrado.")


def get_dados(operacao, valor, categoria):

    if operacao == "entrada":
        saldo = obter_saldo_atual() + valor
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        dados = Caixa360(
            id=0,
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
            data=data,
            valor=valor,
            tipo=operacao,
            categoria=categoria,
            saldo=saldo
        )

        inserir_extrato(dados)
        st.success("Saída registrada com sucesso!")


def validacao(tipo_operacao, valor_operacao, categoria_operacao):
    erro = []

    if tipo_operacao not in ["entrada", "saida"]:
        erro.append("Tipo de operação inválido.")

    if valor_operacao is None or valor_operacao <= 0:
        erro.append("O valor deve ser maior que zero.")

    if not categoria_operacao or not categoria_operacao.strip():
        erro.append("A categoria não pode estar vazia.")

    if banco_esta_vazio() and tipo_operacao == "saida":
        erro.append("Não é possível registrar saída sem saldo inicial.")

    if erro:
        for msg in erro:
            st.error(msg)
        return False

    return True


def eh_consulta(texto):
    consulta_palavras = [
        "saldo",
        "extrato",
        "consulta",
        "consultar",
        "analisa",
        "analisar",
        "analise",
        "análise",
        "extrato"
    ]

    return any(p in texto for p in consulta_palavras)

import re

def processar_movimentacao(texto):
    # 🔍 valor
    valor_match = re.search(r"\d+\.?\d*", texto)
    valor = float(valor_match.group()) if valor_match else None

    # 🔍 operação
    entrada_palavras = ["adicionei","inseri","inserir","adicionar","depositar","colocar","coloquei","recebi","entrada"]
    saida_palavras = ["retirei","gastei","retirar","pagar","paguei","saída","tirei","saida"]

    operacao = None

    if any(p in texto for p in entrada_palavras):
        operacao = "entrada"
    elif any(p in texto for p in saida_palavras):
        operacao = "saida"

    # 🔍 categoria
    palavras = texto.split()
    categoria = None

    for chave in ["de", "com", "no"]:
        if chave in palavras:
            idx = palavras.index(chave)
            if idx + 1 < len(palavras):
                categoria = palavras[idx + 1]

    if categoria is None:
        categoria = "geral"

    # 🧪 debug
    st.write(f"Valor: {valor}")
    st.write(f"Operação: {operacao}")
    st.write(f"Categoria: {categoria}")

    # ✅ validação
    if not validacao(operacao, valor, categoria):
        return

    # 💾 salvar no banco
    get_dados(operacao, valor, categoria)


def interpretar_comando(texto):
    texto = texto.lower()

    comandos_validos = [
        
        "abrir caixa","fechar caixa","ver saldo","consultar saldo","saldo do caixa",
        "registrar venda","cancelar venda",
        "inserir","inseri","inserido","inserir dinheiro","inserir valor",
        "adicionar","adicionei","adicionar dinheiro","adicionar valor",
        "retirar","retirei","retirado","retirar dinheiro","retirar valor",
        "descontar","desconto","descontou","aplicar desconto",
        "entrada","entrada de dinheiro","entrada no caixa",
        "saida","saída","saida de dinheiro","saída de dinheiro"
    ]

    if not any(cmd in texto for cmd in comandos_validos):
        st.warning("Comando não reconhecido para o sistema de caixa.")
        return

    # 👉 1. Verifica se é consulta
    if eh_consulta(texto):
        consultar_extrato()
        return

    # 👉 2. Caso contrário, trata como movimentação
    processar_movimentacao(texto)