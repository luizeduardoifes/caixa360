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

        # 🔴 valor negativo para saída
        df["valor"] = df.apply(
            lambda row: -row["valor"] if row["tipo"] == "saida" else row["valor"],
            axis=1
        )

        # 💰 formatação moeda
        def formatar_moeda(x):
            return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        df["valor_operação"] = df["valor"].apply(formatar_moeda)
        df["saldo_formatado"] = df["saldo"].apply(formatar_moeda)

        # 🎨 estilo corrigido
        def estilo_linha(row):
            estilos = []

            for col in row.index:
                if col == "valor_operação":
                    if row["tipo"] == "entrada":
                        estilos.append("color: green")
                    elif row["tipo"] == "saida":
                        estilos.append("color: red")
                    else:
                        estilos.append("")

                elif col == "saldo_formatado":
                    # 👇 USA saldo original do df (via nome fixo)
                    saldo_original = df.loc[row.name, "saldo"]

                    if saldo_original >= 0:
                        estilos.append("color: green")
                    else:
                        estilos.append("color: red")
                else:
                    estilos.append("")

            return estilos

        st.dataframe(
            df[["id","data", "valor_operação", "tipo", "categoria", "saldo_formatado"]]
            .style.apply(estilo_linha, axis=1),
            use_container_width=True
        )

        # 💰 saldo atual
        saldo_formatado = formatar_moeda(saldo_atual)

        if saldo_atual >= 0:
            st.markdown(f"<h3 style='color:green'>Saldo Atual: {saldo_formatado}</h3>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h3 style='color:red'>Saldo Atual: {saldo_formatado}</h3>", unsafe_allow_html=True)
    else:
        st.info("Nenhum registro encontrado,faça a primeira operação.")


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


def eh_consulta(formatado):
    comandos_consulta = [
    # 💰 saldo
    "saldo",
    "ver saldo",
    "consultar saldo",
    "mostrar saldo",
    "saldo do caixa",
    "quanto tenho",
    "quanto tem no caixa",
    "quanto há",
    "valor em caixa",
    "total em caixa",
    "dinheiro em caixa",
    "quanto dinheiro tem",
    "quanto dinheiro eu tenho",
    "me diga o saldo",
    "informe o saldo",
    "ver valor",
    "consultar valor",

    # 📊 extrato / histórico
    "extrato",
    "ver extrato",
    "consultar extrato",
    "mostrar extrato",
    "extrato do caixa",
    "ver movimentação",
    "consultar movimentação",
    "mostrar movimentação",
    "movimentação do caixa",
    "historico",
    "histórico",
    "ver histórico",
    "consultar histórico",
    "mostrar histórico",
    "historico do caixa",
    "histórico do caixa",

    # 📈 análise
    "analisar",
    "analisa",
    "analise",
    "análise",
    "analisar caixa",
    "analise do caixa",
    "análise do caixa",
    "analisar movimentação",
    "analisar extrato",
    "resumo",
    "resumo do caixa",
    "resumo financeiro",
    "visão geral",
    "relatorio",
    "relatório",
    "relatorio do caixa",
    "relatório do caixa",

    # 🧠 linguagem mais natural
    "como está o caixa",
    "como está meu saldo",
    "como está o saldo",
    "me mostra o caixa",
    "quero ver o caixa",
    "me mostra o extrato",
    "quero ver o extrato",
    "me mostra as movimentações",
    "o que foi registrado",
    "quais foram os lançamentos",
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
            valor_match = re.search(r"\d{1,3}(?:\.\d{3})*(?:,\d+)?", formatado)

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

    comandos_validos = [
        
        "abrir caixa","fechar caixa","saldo","ver saldo","consultar saldo","mostrar saldo","saldo do caixa","quanto tenho",
        "quanto tem no caixa","quanto há","valor em caixa","total em caixa","dinheiro em caixa","quanto dinheiro tem",
        "quanto dinheiro eu tenho","me diga o saldo","informe o saldo","ver valor","consultar valor",
        "extrato","ver extrato","consultar extrato","mostrar extrato","extrato do caixa","ver movimentação","consultar movimentação",
        "mostrar movimentação","movimentação do caixa","historico","histórico","ver histórico","consultar histórico","mostrar histórico","historico do caixa",
        "histórico do caixa","analisar","analisa","analise","análise","analisar caixa","analise do caixa","análise do caixa",
        "analisar movimentação","analisar extrato","resumo","resumo do caixa","resumo financeiro",
        "visão geral","relatorio","relatório","relatorio do caixa","relatório do caixa","como está o caixa",
        "como está meu saldo","como está o saldo","me mostra o caixa","quero ver o caixa","me mostra o extrato","quero ver o extrato",
        "me mostra as movimentações","o que foi registrado","quais foram os lançamentos","ver registros",
        "consultar registros","gastar","gastei","gastou",
        "registrar venda","cancelar venda","recebi","recebeu","receber"
        "inserir","inseri","inserido","inserir dinheiro","inserir valor",
        "adicionar","adicionei","adicionar dinheiro","adicionar valor",
        "retirar","retirei","retirado","retirar dinheiro","retirar valor",
        "descontar","desconto","descontou","aplicar desconto",
        "entrada","entrada de dinheiro","entrada no caixa",
        "saida","saída","saida de dinheiro","saída de dinheiro"
    ]

    if not any(cmd in formatado for cmd in comandos_validos):
        st.warning("Comando não reconhecido para o sistema de caixa.")
        return

    # 👉 1. Verifica se é consulta
    if eh_consulta(formatado):
        consultar_extrato()
        return

    # 👉 2. Caso contrário, trata como movimentação
    processar_movimentacao(formatado)