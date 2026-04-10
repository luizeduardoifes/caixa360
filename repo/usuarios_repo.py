from database.database import criar_conexao
from sql.usuarios_sql import *

def criar_tabela_usuarios():
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_USUARIOS)
        conn.commit()
    finally:
        conn.close()

def verificar_login(usuario):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(SELECIONAR_USUARIO_POR_ID,(usuario.strip(),)
        )
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def atualizar_senha(user_id, nova_senha_hash):
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(UPDATE_SENHA, (nova_senha_hash, user_id))
    conn.commit()
    conn.close()