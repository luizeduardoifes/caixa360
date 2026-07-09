import bcrypt

from repo.usuarios_repo import verificar_login


def autenticar_usuario(usuario: str, senha_digitada: str):
    """
    repo.verificar_login só busca o usuário pelo login; a checagem de senha
    (a parte sensível) fica isolada aqui.
    Retorna (usuario_id, trocar_senha) se a senha bater, ou None.
    """
    resultado = verificar_login(usuario)

    if not resultado:
        return None

    user_id, senha_hash, trocar_senha = resultado

    if isinstance(senha_hash, str):
        senha_hash = senha_hash.encode()

    if bcrypt.checkpw(senha_digitada.encode(), senha_hash):
        return (user_id, trocar_senha)

    return None
