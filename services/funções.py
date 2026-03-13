import re
from datetime import *
import streamlit as st
from models.caixa360 import Caixa360
from repo.caixa360_repo import *


def get_dados(tipo_operacao, valor_operacao, categoria_operacao):
    if tipo_operacao == "Entrada":
        saldo = obter_saldo_atual() + valor_operacao
        data = datetime.now()
        dados = Caixa360(id=0,data=data, valor=valor_operacao, tipo=tipo_operacao, categoria=categoria_operacao, saldo=saldo)
        inserir_extrato(dados)
        st.success("Operação tipo entrada gravada com sucesso!")
    
    elif tipo_operacao == "Saída":
        saldo = obter_saldo_atual() - valor_operacao
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dados = Caixa360(id=0,data=data, valor=valor_operacao, tipo=tipo_operacao, categoria=categoria_operacao, saldo=saldo)
        inserir_extrato(dados)
        st.success("Operação tipo saída gravada com sucesso!")


def validacao(tipo_operacao, valor_operacao, categoria_operacao):
    erro = []
    
    if tipo_operacao == "Selecione uma operação":
        erro.append("Selecione um tipo de operação.")

    if valor_operacao <= 0:
        erro.append("O valor da operação deve ser maior que zero.")

    if not categoria_operacao.strip():
        erro.append("A descrição da operação não pode estar vazia.")

    if banco_esta_vazio() and tipo_operacao == "Saída":
        erro.append("Não é possível registrar uma saída sem um saldo inicial. Por favor, registre uma entrada primeiro.")

    if erro:
        for msg in erro:
            st.error(msg)
        return False

    else:
        return True



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
        "saida","saída","saida de dinheiro","saída de dinheiro",
        "movimentação","ver movimentação","consultar movimentação",
        "historico","histórico","historico do caixa","histórico do caixa"
    ]

    comando_encontrado = any(cmd in texto for cmd in comandos_validos)

    if not comando_encontrado:
        st.warning("Este sistema aceita apenas comandos relacionados ao caixa. Não é um sistema de conversa.")
        return

    # detectar valor
    valor_match = re.search(r"\d+\.?\d*", texto)
    valor = float(valor_match.group()) if valor_match else None

    # detectar operação
    entrada_palavras = ["adicionei","inseri","inserir","adicionar","depositar","colocar","coloquei","recebi"]
    saida_palavras = ["retirei","gastei","retirar","pagar","paguei","saída","tirei"]

    operacao = None

    if any(p in texto for p in entrada_palavras):
        operacao = "entrada"

    elif any(p in texto for p in saida_palavras):
        operacao = "saida"

    # detectar categoria
    palavras = texto.split()
    categoria = None

    for chave in ["de","com","no"]:
        if chave in palavras:
            idx = palavras.index(chave)
            if idx + 1 < len(palavras):
                categoria = palavras[idx + 1]

    st.write(f"Valor: {valor}")
    st.write(f"Operação: {operacao}")
    st.write(f"Categoria: {categoria}")