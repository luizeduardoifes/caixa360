import bcrypt
from database.database import criar_conexao

def criar_usuario(nome, senha):
    conn = criar_conexao()
    cursor = conn.cursor()

    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO usuarios (usuario, senha, trocar_senha) VALUES (%s, %s, %s)",
        (nome, senha_hash, True)
    )

    conn.commit()
    conn.close()

criar_usuario("Luiz Eduardo", "12345")