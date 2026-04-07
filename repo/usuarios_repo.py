from database.database import criar_conexao
from sql.usuarios_sql import *


def criar_tabela_usuarios():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_USUARIOS)
    conn.commit()
    conn.close()