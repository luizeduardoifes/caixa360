import pandas as pd
import streamlit as st
from repo.caixa360_repo import listar_extrato, obter_saldo_atual
from services.auth import get_usuario_id

def consultar_extrato():
    usuario_atual = get_usuario_id()
    dados = listar_extrato(usuario_atual)
    saldo_atual = obter_saldo_atual(usuario_atual)

    if not dados:
        st.info("Nenhum registro encontrado, faça a primeira operação.")
        return

    st.write("EXTRATO:")

    # 🔹 DataFrame
    df = pd.DataFrame(
        dados,
        columns=["id", "usuario_id", "data", "valor", "tipo", "categoria", "saldo"]
    )

    # 🔥 garante tipos numéricos
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["saldo"] = pd.to_numeric(df["saldo"], errors="coerce")

    # remove lixo
    df = df.dropna(subset=["valor", "saldo"])

    # 🔴 saída negativa
    df.loc[df["tipo"] == "saida", "valor"] *= -1

    # 💰 formatação moeda
    def formatar_moeda(x):
        try:
            return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except:
            return "R$ 0,00"

    df["valor_operação"] = df["valor"].apply(formatar_moeda)
    df["saldo_formatado"] = df["saldo"].apply(formatar_moeda)

    # 📊 colunas visíveis
    colunas_exibir = [
        "id",
        "usuario_id",
        "data",
        "valor_operação",
        "tipo",
        "categoria",
        "saldo_formatado"
    ]

    # 🔥 cria DF separado pra exibição
    df_exibir = df[colunas_exibir].copy()

    # 🎨 estilo corrigido (usa df original pra pegar saldo)
    def estilo_linha(row):
        estilos = []
        saldo_original = df.loc[row.name, "saldo"]

        for col in row.index:
            if col == "valor_operação":
                if row["tipo"] == "entrada":
                    estilos.append("color: green")
                elif row["tipo"] == "saida":
                    estilos.append("color: red")
                else:
                    estilos.append("")

            elif col == "saldo_formatado":
                if saldo_original >= 0:
                    estilos.append("color: green")
                else:
                    estilos.append("color: red")
            else:
                estilos.append("")

        return estilos

    # 📊 tabela (CORRETA)
    st.dataframe(
        df_exibir.style.apply(estilo_linha, axis=1),
        use_container_width=True
    )

    # 💰 saldo atual
    saldo_formatado = formatar_moeda(saldo_atual)
    cor = "green" if saldo_atual >= 0 else "red"

    st.markdown(
        f"<h3 style='color:{cor}'>Saldo Atual: {saldo_formatado}</h3>",
        unsafe_allow_html=True
    )
