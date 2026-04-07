import sqlite3

import bcrypt


# def verificar_login(nome, senha_digitada):
#     conn = sqlite3.connect("extrato.db")
#     cursor = conn.cursor()

#     cursor.execute(
#         "SELECT id, senha, trocar_senha FROM usuarios WHERE usuario = ?",
#         (nome,)
#     )
#     usuario = cursor.fetchone()

#     conn.close()

#     if usuario:
#         user_id, senha_hash, trocar_senha = usuario

#         if isinstance(senha_hash, str):
#             senha_hash = senha_hash.encode()

#         try:
#             if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
#                 return user_id, trocar_senha
#         except ValueError:
#             return None

#     return None

def verificar_login(nome, senha_digitada):
    conn = sqlite3.connect("extrato.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, senha, trocar_senha FROM usuarios WHERE usuario = ?",
        (nome,)
    )
    usuario = cursor.fetchone()

    conn.close()

    print("Usuario encontrado:", usuario)

    if usuario:
        user_id, senha_hash, trocar_senha = usuario

        print("Hash do banco:", senha_hash)
        print("Senha digitada:", senha_digitada)

        if isinstance(senha_hash, str):
            senha_hash = senha_hash.encode()

        try:
            resultado = bcrypt.checkpw(senha_digitada.encode(), senha_hash)
            print("Resultado bcrypt:", resultado)

            if resultado:
                return user_id, trocar_senha
        except Exception as e:
            print("Erro bcrypt:", e)

    return None