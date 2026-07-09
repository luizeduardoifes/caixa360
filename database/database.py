import psycopg2

from config import get_db_config


def criar_conexao():
    cfg = get_db_config()

    if not cfg["password"]:
        raise RuntimeError(
            "DB_PASSWORD não configurada. Defina a variável de ambiente DB_PASSWORD "
            "(ou a chave DB_PASSWORD em .streamlit/secrets.toml) antes de rodar o app. "
            "A senha do banco NUNCA deve ficar escrita no código-fonte."
        )

    return psycopg2.connect(
        host=cfg["host"],
        port=cfg["port"],
        database=cfg["database"],
        user=cfg["user"],
        password=cfg["password"],
    )
