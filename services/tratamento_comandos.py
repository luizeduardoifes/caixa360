import unicodedata
import re

import streamlit as st

from repo.caixa360_repo import banco_esta_vazio
from services.consultar_extrato import consultar_extrato, grafico_entrada_saida, grafico_pizza
from services.entrada_dados import get_dados
from services.editar_excluir import (
    eh_edicao,
    eh_exclusao,
    processar_edicao,
    processar_exclusao,
)

COMANDOS_GRAFICO = [
    "grafico", "grafico do caixa", "grafico de entradas e saidas", "grafico de movimentacao",
    "grafico de extrato", "mostrar grafico", "ver grafico", "consultar grafico",
    "analise grafica", "analisa grafica", "relatorio grafico"
]

COMANDOS_CONSULTA = [
    "saldo", "ver saldo", "consultar saldo", "mostrar saldo", "saldo do caixa",
    "quanto tenho", "quanto tem no caixa", "quanto ha", "valor em caixa",
    "total em caixa", "dinheiro em caixa", "quanto dinheiro tem",
    "quanto dinheiro eu tenho", "me diga o saldo", "informe o saldo",
    "ver valor", "consultar valor",
    "extrato", "ver extrato", "consultar extrato", "mostrar extrato",
    "extrato do caixa", "ver movimentacao", "consultar movimentacao",
    "mostrar movimentacao", "movimentacao do caixa", "historico", "ver historico",
    "consultar historico", "mostrar historico", "historico do caixa",
    "analisar", "analisa", "analise", "analisar caixa", "analise do caixa",
    "analisar movimentacao", "analisar extrato", "resumo", "resumo do caixa",
    "resumo financeiro", "visao geral", "relatorio", "relatorio do caixa",
    "como esta o caixa", "como esta meu saldo", "como esta o saldo",
    "me mostra o caixa", "quero ver o caixa", "me mostra o extrato",
    "quero ver o extrato", "me mostra as movimentacoes", "o que foi registrado",
    "quais foram os lancamentos", "ver registros", "consultar registros",
]

COMANDOS_VALIDOS = COMANDOS_CONSULTA + COMANDOS_GRAFICO + [
    "abrir caixa", "fechar caixa", "gastar", "gastei", "gastou",
    "registrar venda", "cancelar venda", "recebi", "recebeu", "receber",
    "inserir", "inseri", "inserido", "inserir dinheiro", "inserir valor",
    "adicionar", "adicionei", "adicionar dinheiro", "adicionar valor",
    "retirar", "retirei", "retirado", "retirar dinheiro", "retirar valor",
    "descontar", "desconto", "descontou", "aplicar desconto",
    "entrada", "entrada de dinheiro", "entrada no caixa",
    "saida", "saida de dinheiro",
    # Editar / excluir
    "excluir", "deletar", "apagar", "remover",
    "editar", "alterar", "corrigir", "atualizar",
]


def eh_consulta_grafico(formatado):
    return any(p in formatado for p in COMANDOS_GRAFICO)


def eh_consulta(formatado):
    return any(p in formatado for p in COMANDOS_CONSULTA)


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


def eh_movimentacao_rapida(texto):
    palavras = texto.split()

    if len(palavras) != 2:
        return False

    tem_numero = any(re.match(r'^\d+[,.]?\d*$', p) for p in palavras)
    tem_texto = any(not re.match(r'^\d+[,.]?\d*$', p) for p in palavras)

    return tem_numero and tem_texto


def processar_movimentacao(formatado):
    valor = None

    match_mil = re.search(r"(\d+)\s*mil", formatado)
    if match_mil:
        valor = int(match_mil.group(1)) * 1000
    else:
        numeros_formatado = {
            "um": 1, "uma": 1, "dois": 2, "duas": 2, "tres": 3, "três": 3,
            "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8, "nove": 9,
            "dez": 10
        }

        palavras = formatado.split()
        for i, palavra in enumerate(palavras):
            if palavra in numeros_formatado:
                if i + 1 < len(palavras) and palavras[i + 1] == "mil":
                    valor = numeros_formatado[palavra] * 1000
                    break

        if valor is None:
            valor_match = re.search(r"\d+(?:\.\d{3})*(?:,\d+)?", formatado)
            if valor_match:
                valor_str = valor_match.group().replace(".", "").replace(",", ".")
                valor = float(valor_str)

    entrada_palavras = ["adicionei", "inseri", "inserir", "adicionar", "depositar", "colocar", "coloquei", "recebi", "entrada"]
    saida_palavras = ["gastou", "gastar", "retirei", "gastei", "retirar", "pagar", "paguei", "saída", "tirei", "saida"]

    operacao = None
    if any(p in formatado for p in entrada_palavras):
        operacao = "entrada"
    elif any(p in formatado for p in saida_palavras):
        operacao = "saida"

    palavras = formatado.split()
    categoria = None
    for chave in ["de", "com", "no", "na", "para", "em", "do", "da", "sobre", "sobre o", "sobre a", "sobre os", "sobre as","ao", "ao", "aos", "às", "à", "ào", "àos","para o", "para a", "para os", "para as"]:
        if chave in palavras:
            idx = palavras.index(chave)
            if idx + 1 < len(palavras):
                categoria = palavras[idx + 1]

    if categoria is None:
        categoria = "geral"

    if not validacao(operacao, valor, categoria):
        return

    get_dados(operacao, valor, categoria)


def processar_movimentacao_rapida(texto):
    palavras_ignoradas = ["reais", "real", "r$"]

    categoria = []
    valor = None

    for palavra in texto.split():
        palavra = palavra.lower()

        if palavra in palavras_ignoradas:
            continue

        if re.match(r'^\d+[,.]?\d*$', palavra):
            valor = float(palavra.replace(",", "."))
        else:
            categoria.append(palavra)

    if not valor:
        st.warning("Valor não encontrado")
        return

    categoria_final = " ".join(categoria)
    operacao = "entrada"

    get_dados(operacao, valor, categoria_final)


def interpretar_comando(formatado):
    def normalizar(texto):
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        return texto.encode("ascii", "ignore").decode("utf-8")

    if not formatado:
        st.warning("Digite um comando antes de enviar.")
        return

    formatado = normalizar(formatado)

    # Exclusão/edição são checadas ANTES do atalho de "movimentação rápida":
    # um comando de 2 palavras como "excluir 5" tem número + texto e seria
    # confundido com um depósito de R$5 se checado depois.
    if eh_exclusao(formatado):
        processar_exclusao(formatado)
        return

    if eh_edicao(formatado):
        processar_edicao(formatado)
        return

    if eh_consulta(formatado):
        consultar_extrato()
        return

    if eh_consulta_grafico(formatado):
        st.write("Dashboard")
        grafico_entrada_saida()
        grafico_pizza()
        return

    if eh_movimentacao_rapida(formatado):
        processar_movimentacao_rapida(formatado)
        return

    if not any(cmd in formatado for cmd in COMANDOS_VALIDOS):
        st.warning("Comando não reconhecido")
        return

    processar_movimentacao(formatado)
