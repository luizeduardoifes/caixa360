import pandas as pd
import streamlit as st
from services.tratamento_comandos import *
from repo.caixa360_repo import listar_extrato, obter_saldo_atual


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