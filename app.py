import streamlit as st
from repo.caixa360_repo import criar_tabela_extrato
from repo.usuarios_repo import criar_tabela_usuarios
from services.seguranca_senha import autenticar_usuario
from utils.config import configurar_pagina

configurar_pagina(mostrar_sidebar=False)
criar_tabela_extrato()
criar_tabela_usuarios()

st.title("Login")

usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if st.button("Entrar"):

    resultado = autenticar_usuario(usuario, senha)

    if resultado:
        if resultado[1]:
            st.session_state.usuario_id = resultado[0]
            st.session_state.trocar_senha = True
            st.switch_page("pages/trocar_senha.py")
        
        else:
            nome_usuario = resultado[1]
            st.session_state.usuario_id = resultado[0]
            st.session_state.usuario = usuario
            st.session_state.logado = True
            st.switch_page("pages/menu.py")
  


    else:
        st.error("Usuário ou senha inválidos")
    
