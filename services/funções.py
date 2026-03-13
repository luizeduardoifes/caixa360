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


import re

def interpretar_comando(texto):
    comandos_validos = [
    "abrir caixa",
    "fechar caixa",
    "ver saldo",
    "consultar saldo",
    "saldo do caixa",

    "registrar venda",
    "cancelar venda",

    "inserir",
    "inseri",
    "inserido",
    "inserir dinheiro",
    "inserir valor",

    "adicionar",
    "adicionei",
    "adicionar dinheiro",
    "adicionar valor",

    "retirar",
    "retirei",
    "retirado",
    "retirar dinheiro",
    "retirar valor",

    "descontar",
    "desconto",
    "descontou",
    "aplicar desconto",

    "entrada",
    "entrada de dinheiro",
    "entrada no caixa",

    "saida",
    "saída",
    "saida de dinheiro",
    "saída de dinheiro",

    "movimentação",
    "ver movimentação",
    "consultar movimentação",

    "historico",
    "histórico",
    "historico do caixa",
    "histórico do caixa"
]
    comando_encontrado = None
    for comando in comandos_validos:
        if comando in texto:
            comando_encontrado = comando
            break


    if comando_encontrado:
        texto = texto.lower()

        # detectar valor
        valor_match = re.search(r"\d+\.?\d*", texto)
        valor = float(valor_match.group()) if valor_match else None

        # detectar operação
        entrada_palavras = ["adicionei","inseri","inserir", "adicionar", "depositar", "colocar","coloquei" ,"recebi"]
        saida_palavras = ["retirei","gastei", "retirar", "pagar","paguei", "saída", "tirei"]

        operacao = None

        for palavra in entrada_palavras:
            if palavra in texto:
                operacao = "entrada"

        for palavra in saida_palavras:
            if palavra in texto:
                operacao = "saida"

        # detectar categoria
        palavras = texto.split()

        categoria = None
        if "de" in palavras:
            index = palavras.index("de")
            if index + 1 < len(palavras):
                categoria = palavras[index + 1]
        if "com" in palavras:
            index = palavras.index("com")
            if index + 1 < len(palavras):
                categoria = palavras[index + 1]
        if "no" in palavras:
            index = palavras.index("no")
            if index + 1 < len(palavras):
                categoria = palavras[index + 1]
        if "com a" in palavras:
            index = palavras.index("com a")
            if index + 1 < len(palavras):
                categoria = palavras[index + 1]

        if valor == None and operacao == None and categoria == None:
            st.warning("Este sistema aceita apenas comandos relacionados ao caixa. Não é um sistema de conversa.")

        else:
            st.write(f"Valor: {valor}")
            st.write(f"Operação: {operacao}")
            st.write(f"Categoria: {categoria}")

    else:
        st.warning("Este sistema aceita apenas comandos relacionados ao caixa. Não é um sistema de conversa.")
       
