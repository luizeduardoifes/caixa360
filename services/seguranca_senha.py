from repo.usuarios_repo import verificar_login
import bcrypt


def autenticar_usuario(usuario, senha_digitada):
    resultado = verificar_login(usuario)

    if not resultado:
        return None
    
    user_id, senha_hash, trocar_senha = resultado

    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode()

    if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
        return (user_id, trocar_senha)
    
    return None