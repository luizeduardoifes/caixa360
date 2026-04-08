import time
import re
import streamlit as st
import sqlite3
import bcrypt
from sql.usuarios_sql import UPDATE_SENHA
from utils.config import configurar_pagina

configurar_pagina(mostrar_sidebar=False)

def senha_forte(senha):
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres"
    if not re.search(r"[A-Z]", senha):
        return "Deve conter pelo menos 1 letra maiúscula"
    if not re.search(r"[a-z]", senha):
        return "Deve conter pelo menos 1 letra minúscula"
    if not re.search(r"[0-9]", senha):
        return "Deve conter pelo menos 1 número"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return "Deve conter pelo menos 1 símbolo"
    return None

# 🖥️ interface
st.title("Trocar Senha")

nova_senha = st.text_input("Nova senha", type="password")
confirmar_senha = st.text_input("Confirmar senha", type="password")

if st.button("Atualizar senha"):

    if nova_senha != confirmar_senha:
        st.error("As senhas não coincidem")
        st.stop()

    erro = senha_forte(nova_senha)
    if erro:
        st.error(erro)
        st.stop()

    # 🔐 gerar hash
    senha_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

    conn = sqlite3.connect("extrato.db")
    cursor = conn.cursor()

    cursor.execute(
        UPDATE_SENHA,
        (senha_hash, st.session_state.usuario_id)
    )

    conn.commit()
    conn.close()

    st.success("Senha atualizada com sucesso!")
    time.sleep(2)

    st.switch_page("pages/menu.py")