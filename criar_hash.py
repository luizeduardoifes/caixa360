import bcrypt
import sqlite3

def criar_usuario(nome, senha):
    conn = sqlite3.connect("extrato.db")
    cursor = conn.cursor()

    senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

    cursor.execute(
        "INSERT INTO usuarios (usuario, senha, trocar_senha) VALUES (?, ?, ?)",
        (nome, senha_hash, 1)
    )

    conn.commit()
    conn.close()

criar_usuario("dudu", "Le07122005@")