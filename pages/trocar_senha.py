import time
import re
import streamlit as st
import sqlite3
import bcrypt
from sql.usuarios_sql import UPDATE_SENHA
from utils.config import configurar_pagina, proteger_pagina_completa

configurar_pagina(mostrar_sidebar=False)
proteger_pagina_completa()

def senha_forte(senha):
    error = []
    if not senha:
        AttributeError("A senha não pode ser vazia")
        return
    else:
        if len(senha) < 8:
            error.append("A senha deve ter pelo menos 8 caracteres")
        if not re.search(r"[A-Z]", senha):
            error.append("Deve conter pelo menos 1 letra maiúscula")
        if not re.search(r"[a-z]", senha):
            error.append("Deve conter pelo menos 1 letra minúscula")
        if not re.search(r"[0-9]", senha):
            error.append("Deve conter pelo menos 1 número")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
            error.append("Deve conter pelo menos 1 símbolo")
        return error


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
            st.error(f"{e}\n")
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
    st.session_state.clear()
    st.switch_page("app.py")