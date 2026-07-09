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


def verificar_login(usuario: str):
    """
    Busca o usuário pelo login e retorna (id, senha_hash, trocar_senha).
    Não confere a senha aqui — quem faz isso é services/seguranca_senha.py,
    de propósito (repo só fala com o banco, a regra de autenticação fica no service).
    """
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(SELECIONAR_USUARIO_POR_ID, (usuario.strip(),))
        return cursor.fetchone()
    finally:
        conn.close()


def atualizar_senha(user_id: int, nova_senha_hash: str):
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(UPDATE_SENHA, (nova_senha_hash, user_id))
        conn.commit()
    finally:
        conn.close()
