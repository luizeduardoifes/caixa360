import unicodedata
import re
from datetime import *
import streamlit as st
from repo.caixa360_repo import *
from services.consultar_extrato import consultar_extrato
from services.entrada_dados import get_dados


def eh_consulta(formatado):
    comandos_consulta = [
        "saldo",
        "ver saldo",
        "consultar saldo",
        "mostrar saldo",
        "saldo do caixa",
        "quanto tenho",
        "quanto tem no caixa",
        "quanto ha",
        "valor em caixa",
        "total em caixa",
        "dinheiro em caixa",
        "quanto dinheiro tem",
        "quanto dinheiro eu tenho",
        "me diga o saldo",
        "informe o saldo",
        "ver valor",
        "consultar valor",

        "extrato",
        "ver extrato",
        "consultar extrato",
        "mostrar extrato",
        "extrato do caixa",
        "ver movimentacao",
        "consultar movimentacao",
        "mostrar movimentacao",
        "movimentacao do caixa",
        "historico",
        "ver historico",
        "consultar historico",
        "mostrar historico",
        "historico do caixa",

        "analisar",
        "analisa",
        "analise",
        "analisar caixa",
        "analise do caixa",
        "analisar movimentacao",
        "analisar extrato",
        "resumo",
        "resumo do caixa",
        "resumo financeiro",
        "visao geral",
        "relatorio",
        "relatorio do caixa",

        "como esta o caixa",
        "como esta meu saldo",
        "como esta o saldo",
        "me mostra o caixa",
        "quero ver o caixa",
        "me mostra o extrato",
        "quero ver o extrato",
        "me mostra as movimentacoes",
        "o que foi registrado",
        "quais foram os lancamentos",
        "ver registros",
        "consultar registros",
    ]

    return any(p in formatado for p in comandos_consulta)


def processar_movimentacao(formatado):
    # 🔍 valor (suporte completo: 2.500, 3 mil, tres mil)

    valor = None

    # 1. pega "3 mil", "10 mil"
    match_mil = re.search(r"(\d+)\s*mil", formatado)

    if match_mil:
        valor = int(match_mil.group(1)) * 1000

    else:
        # 2. pega "tres mil"
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

        # 3. fallback para número normal (2.500,50 etc)
        if valor is None:
            valor_match = re.search(r"\d+(?:\.\d{3})*(?:,\d+)?", formatado)

            if valor_match:
                valor_str = valor_match.group()
                valor_str = valor_str.replace(".", "").replace(",", ".")
                valor = float(valor_str)

    # 🔍 operação
    entrada_palavras = ["adicionei","inseri","inserir","adicionar","depositar","colocar","coloquei","recebi","entrada"]
    saida_palavras = ["gastou","gastar","retirei","gastei","retirar","pagar","paguei","saída","tirei","saida"]

    operacao = None

    if any(p in formatado for p in entrada_palavras):
        operacao = "entrada"
    elif any(p in formatado for p in saida_palavras):
        operacao = "saida"

    # 🔍 categoria
    palavras = formatado.split()
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

def interpretar_comando(formatado):


    # 🔥 normaliza (resolve problema de mobile, acento, etc)
    def normalizar(texto):
        texto = texto.lower().strip()
        texto = unicodedata.normalize("NFD", texto)
        texto = texto.encode("ascii", "ignore").decode("utf-8")
        return texto

    if not formatado:
        st.warning("Digite um comando antes de enviar.")
        return

    formatado = normalizar(formatado)

    comandos_validos = [
        "abrir caixa","fechar caixa","saldo","ver saldo","consultar saldo","mostrar saldo","saldo do caixa","quanto tenho",
        "quanto tem no caixa","quanto ha","valor em caixa","total em caixa","dinheiro em caixa","quanto dinheiro tem",
        "quanto dinheiro eu tenho","me diga o saldo","informe o saldo","ver valor","consultar valor",
        "extrato","ver extrato","consultar extrato","mostrar extrato","extrato do caixa","ver movimentacao","consultar movimentacao",
        "mostrar movimentacao","movimentacao do caixa","historico","ver historico","consultar historico","mostrar historico","historico do caixa",
        "analisar","analisa","analise","analisar caixa","analise do caixa",
        "analisar movimentacao","analisar extrato","resumo","resumo do caixa","resumo financeiro",
        "visao geral","relatorio","relatorio do caixa","como esta o caixa",
        "como esta meu saldo","como esta o saldo","me mostra o caixa","quero ver o caixa","me mostra o extrato","quero ver o extrato",
        "me mostra as movimentacoes","o que foi registrado","quais foram os lancamentos","ver registros",
        "consultar registros","gastar","gastei","gastou",
        "registrar venda","cancelar venda","recebi","recebeu","receber",  # ✅ corrigido aqui
        "inserir","inseri","inserido","inserir dinheiro","inserir valor",
        "adicionar","adicionei","adicionar dinheiro","adicionar valor",
        "retirar","retirei","retirado","retirar dinheiro","retirar valor",
        "descontar","desconto","descontou","aplicar desconto",
        "entrada","entrada de dinheiro","entrada no caixa",
        "saida","saida de dinheiro"
    ]

    # 🔍 debug (te ajuda a ver no mobile)
    # st.write("Recebido:", formatado)

    if not any(cmd in formatado for cmd in comandos_validos):
        st.warning(f"Comando não reconhecido")
        return

    # 👉 1. Verifica se é consulta
    if eh_consulta(formatado):
        consultar_extrato()
        return

    # 👉 2. Caso contrário, trata como movimentação
    processar_movimentacao(formatado)


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