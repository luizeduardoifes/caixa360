"""
Comandos de editar/excluir um lançamento, na mesma linguagem natural que o
resto do app já usa. Ex.:
    "excluir registro 12"
    "deletar lançamento 7"
    "editar registro 12 valor 300"
    "alterar registro 12 categoria salario"

Exclusão nunca acontece direto: fica pendente em st.session_state até o
usuário confirmar clicando num botão (ver pages/menu.py), pra evitar apagar
um lançamento por engano de interpretação do texto.
"""
import re

import streamlit as st

from repo.caixa360_repo import atualizar_extrato, buscar_extrato_por_id, excluir_extrato
from services.auth import get_usuario_id

PALAVRAS_EXCLUSAO = ["excluir", "deletar", "apagar", "remover"]
PALAVRAS_EDICAO = ["editar", "alterar", "corrigir", "atualizar"]


def eh_exclusao(formatado: str) -> bool:
    return any(p in formatado for p in PALAVRAS_EXCLUSAO)


def eh_edicao(formatado: str) -> bool:
    return any(p in formatado for p in PALAVRAS_EDICAO)


def _extrair_id_registro(formatado: str):
    # Prioriza um número logo depois de uma palavra-chave, tipo "registro 12".
    match = re.search(r"(?:registro|lancamento|lançamento|id|numero)\s*(\d+)", formatado)
    if match:
        return int(match.group(1))

    # Sem palavra-chave, usa o primeiro número encontrado no texto.
    match = re.search(r"\d+", formatado)
    return int(match.group()) if match else None


def _extrair_novo_valor(formatado: str):
    match = re.search(r"valor\D{0,10}?(\d+(?:[.,]\d+)?)", formatado)
    if not match:
        return None
    return float(match.group(1).replace(",", "."))


def _extrair_nova_categoria(formatado: str):
    match = re.search(r"categoria\s+(?:de|para|pra)?\s*([a-z0-9çãáàâéêíóôõú_]+)", formatado)
    return match.group(1).strip() if match else None


def processar_exclusao(formatado: str):
    usuario_id = get_usuario_id()
    extrato_id = _extrair_id_registro(formatado)

    if extrato_id is None:
        st.warning("Não entendi qual registro excluir. Diga o número, ex: 'excluir registro 12'.")
        return

    registro = buscar_extrato_por_id(usuario_id, extrato_id)
    if not registro:
        st.warning(f"Não encontrei o registro {extrato_id} na sua conta.")
        return

    # Guarda o pedido pendente; a exclusão de fato só roda quando o usuário
    # confirmar no botão (pages/menu.py lê essas chaves de session_state).
    st.session_state["exclusao_pendente_id"] = extrato_id
    st.session_state["exclusao_pendente_registro"] = registro


def processar_edicao(formatado: str):
    usuario_id = get_usuario_id()
    extrato_id = _extrair_id_registro(formatado)

    if extrato_id is None:
        st.warning("Não entendi qual registro editar. Diga o número, ex: 'editar registro 12 valor 300'.")
        return

    registro = buscar_extrato_por_id(usuario_id, extrato_id)
    if not registro:
        st.warning(f"Não encontrei o registro {extrato_id} na sua conta.")
        return

    novo_valor = _extrair_novo_valor(formatado)
    nova_categoria = _extrair_nova_categoria(formatado)

    if novo_valor is None and nova_categoria is None:
        st.warning(
            "Diga o que quer mudar. Ex: 'editar registro 12 valor 300' "
            "ou 'editar registro 12 categoria salario'."
        )
        return

    sucesso = atualizar_extrato(
        usuario_id, extrato_id, novo_valor=novo_valor, nova_categoria=nova_categoria
    )

    if sucesso:
        st.success(f"Registro {extrato_id} atualizado com sucesso.")
    else:
        st.error("Não foi possível atualizar o registro.")


def confirmar_exclusao_pendente():
    """Chamada pelo botão de confirmação em pages/menu.py."""
    extrato_id = st.session_state.get("exclusao_pendente_id")
    if extrato_id is None:
        return

    usuario_id = get_usuario_id()
    if excluir_extrato(usuario_id, extrato_id):
        st.success(f"Registro {extrato_id} excluído com sucesso.")
    else:
        st.error("Não foi possível excluir o registro.")

    st.session_state.pop("exclusao_pendente_id", None)
    st.session_state.pop("exclusao_pendente_registro", None)


def cancelar_exclusao_pendente():
    st.session_state.pop("exclusao_pendente_id", None)
    st.session_state.pop("exclusao_pendente_registro", None)
