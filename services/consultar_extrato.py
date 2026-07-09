import altair as alt
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

    df = pd.DataFrame(
        dados,
        columns=["id", "usuario_id", "data", "valor", "tipo", "categoria", "saldo"]
    )

    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["saldo"] = pd.to_numeric(df["saldo"], errors="coerce")
    df = df.dropna(subset=["valor", "saldo"])

    df.loc[df["tipo"] == "saida", "valor"] *= -1

    def formatar_moeda(x):
        try:
            return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception:
            return "R$ 0,00"

    df["valor_operação"] = df["valor"].apply(formatar_moeda)
    df["saldo_formatado"] = df["saldo"].apply(formatar_moeda)

    colunas_exibir = [
        "id", "usuario_id", "data", "valor_operação", "tipo", "categoria", "saldo_formatado"
    ]
    df_exibir = df[colunas_exibir].copy()

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
                estilos.append("color: green" if saldo_original >= 0 else "color: red")
            else:
                estilos.append("")

        return estilos

    st.dataframe(
        df_exibir.style.apply(estilo_linha, axis=1),
        use_container_width=True
    )

    saldo_formatado = formatar_moeda(saldo_atual)
    cor = "green" if saldo_atual >= 0 else "red"

    st.markdown(
        f"<h3 style='color:{cor}'>Saldo Atual: {saldo_formatado}</h3>",
        unsafe_allow_html=True
    )


def _carregar_df_base(usuario_atual):
    """Reaproveitada pelos dois gráficos, evita duplicar a checagem de dados vazios."""
    dados = listar_extrato(usuario_atual)
    if not dados:
        return None

    df = pd.DataFrame(
        dados, columns=["id", "usuario_id", "data", "valor", "tipo", "categoria", "saldo"]
    )
    df["valor"] = pd.to_numeric(df["valor"])
    df["tipo"] = df["tipo"].str.lower()
    return df


# Paleta e tema compartilhados pelos dois gráficos, pra manter a mesma
# identidade visual em qualquer gráfico novo que for adicionado depois.
PALETA_TIPO = {"entrada": "#10b981", "saida": "#f43f5e"}
FONTE = "Helvetica Neue, Arial, sans-serif"


def _estilo_grafico(chart):
    return (
        chart
        .configure_view(strokeWidth=0)
        .configure_axis(
            grid=True,
            gridColor="#e5e7eb",
            gridDash=[3, 3],
            domain=False,
            tickColor="#9ca3af",
            labelColor="#4b5563",
            titleColor="#374151",
            labelFontSize=12,
            titleFontSize=13,
            labelFont=FONTE,
            titleFont=FONTE,
        )
        .configure_legend(
            labelFontSize=12,
            titleFontSize=13,
            labelColor="#4b5563",
            titleColor="#374151",
            symbolType="circle",
            orient="top",
        )
        .configure_title(fontSize=16, font=FONTE, color="#111827", anchor="start")
    )


def _formatar_moeda_compacta(valor: float) -> str:
    return f"R$ {valor:,.0f}".replace(",", ".")


def grafico_entrada_saida():
    usuario_atual = get_usuario_id()
    df = _carregar_df_base(usuario_atual)

    if df is None:
        st.info("Nenhum registro encontrado ainda para gerar o gráfico.")
        return

    df["data"] = pd.to_datetime(df["data"]).dt.strftime("%d/%m")

    df_group = (
        df.groupby(["data", "tipo"])["valor"]
        .sum()
        .reset_index()
    )
    df_group["valor_fmt"] = df_group["valor"].apply(_formatar_moeda_compacta)

    barras = (
        alt.Chart(df_group)
        .mark_bar(size=28, cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("data:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("valor:Q", title="Total (R$)"),
            xOffset=alt.XOffset("tipo:N", sort=["entrada", "saida"]),
            color=alt.Color(
                "tipo:N",
                title=None,
                scale=alt.Scale(
                    domain=["entrada", "saida"],
                    range=[PALETA_TIPO["entrada"], PALETA_TIPO["saida"]],
                ),
                legend=alt.Legend(orient="top"),
            ),
            tooltip=[
                alt.Tooltip("data:N", title="Dia"),
                alt.Tooltip("tipo:N", title="Tipo"),
                alt.Tooltip("valor:Q", title="Total", format=",.2f"),
            ],
        )
    )

    # rótulo com o valor em cima de cada barra — dá um ar mais "dashboard pago"
    rotulos = (
        alt.Chart(df_group)
        .mark_text(dy=-8, fontSize=11, fontWeight="bold", color="#374151")
        .encode(
            x=alt.X("data:N"),
            y=alt.Y("valor:Q"),
            xOffset=alt.XOffset("tipo:N", sort=["entrada", "saida"]),
            text="valor_fmt:N",
        )
    )

    chart = (barras + rotulos).properties(height=380)

    st.subheader("📊 Entradas vs Saídas")
    st.altair_chart(_estilo_grafico(chart), use_container_width=True)


def grafico_pizza():
    usuario_atual = get_usuario_id()
    df = _carregar_df_base(usuario_atual)

    if df is None:
        st.info("Nenhum registro encontrado ainda para gerar o gráfico.")
        return

    df_group = df.groupby("tipo")["valor"].sum().reset_index()
    total = df_group["valor"].sum()

    if total == 0:
        st.info("Sem movimentação suficiente para montar o gráfico.")
        return

    df_group["percentual"] = (df_group["valor"] / total) * 100
    df_group["label"] = df_group["percentual"].map(lambda x: f"{x:.0f}%")

    cores = alt.Scale(
        domain=["entrada", "saida"],
        range=[PALETA_TIPO["entrada"], PALETA_TIPO["saida"]],
    )

    # donut com espaçamento entre as fatias e cantos arredondados
    pizza = (
        alt.Chart(df_group)
        .mark_arc(innerRadius=85, outerRadius=140, cornerRadius=4, padAngle=0.02)
        .encode(
            theta=alt.Theta("valor:Q"),
            color=alt.Color("tipo:N", scale=cores, title=None, legend=alt.Legend(orient="bottom")),
            order=alt.Order("valor:Q", sort="descending"),
            tooltip=[
                alt.Tooltip("tipo:N", title="Tipo"),
                alt.Tooltip("valor:Q", title="Valor", format=",.2f"),
                alt.Tooltip("percentual:Q", title="%", format=".1f"),
            ],
        )
    )

    # rótulos de % do lado de fora da rosca, em vez de espremidos dentro da fatia
    texto_fatias = (
        alt.Chart(df_group)
        .mark_text(radius=165, size=14, fontWeight="bold", color="#374151")
        .encode(theta=alt.Theta("valor:Q"), text="label:N", order=alt.Order("valor:Q", sort="descending"))
    )

    # valor total no centro do donut
    texto_central = (
        alt.Chart(pd.DataFrame({"texto": [_formatar_moeda_compacta(total)]}))
        .mark_text(size=20, fontWeight="bold", color="#111827", dy=-6)
        .encode(text="texto:N")
    )
    subtexto_central = (
        alt.Chart(pd.DataFrame({"sub": ["total movimentado"]}))
        .mark_text(size=11, color="#6b7280", dy=14)
        .encode(text="sub:N")
    )

    chart = (pizza + texto_fatias + texto_central + subtexto_central).properties(height=380, width=380)

    st.subheader("🍩 Distribuição Financeira")
    st.altair_chart(_estilo_grafico(chart), use_container_width=True)
