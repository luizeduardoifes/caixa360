import sqlite3
import bcrypt

def verificar_login(nome, senha_digitada):
    conn = sqlite3.connect("extrato.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, senha, trocar_senha FROM usuarios WHERE usuario = ?",
        (nome.strip(),)
    )
    usuario = cursor.fetchone()

    conn.close()

    # ❌ usuário não existe
    if not usuario:
        return None

    user_id, senha_hash, trocar_senha = usuario

    # 🔐 garantir bytes
    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode()

    try:
        # 🔑 valida senha
        if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
            return {
                "id": user_id,
                "trocar_senha": trocar_senha
            }
    except Exception:
        return None

    return None