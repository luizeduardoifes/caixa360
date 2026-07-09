import streamlit as st
from services.tratamento_comandos import interpretar_comando
from services.editar_excluir import confirmar_exclusao_pendente, cancelar_exclusao_pendente
from utils.config import configurar_pagina, proteger_pagina
from utils.saudacao import saudacao_usuario

configurar_pagina(mostrar_sidebar=False)
proteger_pagina()
saudacao_usuario()

st.title("Caixa360")

with st.form("form_comando"):
    texto = st.text_input("Mensagem")
    enviado = st.form_submit_button("Enviar")

if enviado:
    with st.spinner("Processando..."):
        interpretar_comando(texto)

# --- Confirmação de exclusão pendente --------------------------------------
# interpretar_comando() não exclui na hora: se o comando for de exclusão,
# ele só guarda o pedido em session_state. A exclusão de fato só acontece
# se o usuário confirmar aqui, pra evitar apagar um lançamento por engano
# de interpretação do texto.
if st.session_state.get("exclusao_pendente_id") is not None:
    registro = st.session_state["exclusao_pendente_registro"]
    _id, _usuario_id, data, valor, tipo, categoria, _saldo = registro

    st.warning(
        f"Confirma excluir o registro **{_id}** — {tipo} de R$ {valor:.2f} "
        f"em \"{categoria}\" ({data})?"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Sim, excluir", type="primary"):
            confirmar_exclusao_pendente()
            st.rerun()
    with col2:
        if st.button("Cancelar"):
            cancelar_exclusao_pendente()
            st.rerun()
