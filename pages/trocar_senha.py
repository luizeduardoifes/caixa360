import time
import re

import streamlit as st
import bcrypt

from repo.usuarios_repo import atualizar_senha
from utils.config import configurar_pagina, proteger_troca_senha

configurar_pagina(mostrar_sidebar=False)
proteger_troca_senha()


def senha_forte(senha: str) -> list:
    if not senha:
        return ["A senha não pode ser vazia"]

    erro = []
    if len(senha) < 8:
        erro.append("A senha deve ter pelo menos 8 caracteres")
    if not re.search(r"[A-Z]", senha):
        erro.append("Deve conter pelo menos 1 letra maiúscula")
    if not re.search(r"[a-z]", senha):
        erro.append("Deve conter pelo menos 1 letra minúscula")
    if not re.search(r"[0-9]", senha):
        erro.append("Deve conter pelo menos 1 número")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        erro.append("Deve conter pelo menos 1 símbolo")
    return erro


st.title("Trocar Senha")

nova_senha = st.text_input("Nova senha", type="password")
confirmar_senha = st.text_input("Confirmar senha", type="password")

if st.button("Atualizar senha"):
    if nova_senha != confirmar_senha:
        st.error("As senhas não coincidem")
        st.stop()

    erro = senha_forte(nova_senha)
    if erro:
        st.write("Erro:")
        for e in erro:
            st.error(e)
        st.stop()

    senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()
    atualizar_senha(st.session_state.usuario_id, senha_hash)

    st.success("Senha atualizada com sucesso!")
    time.sleep(2)
    st.session_state.clear()
    st.switch_page("app.py")
