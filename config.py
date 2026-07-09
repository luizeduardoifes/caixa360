import os


def _get(chave: str, padrao: str | None = None) -> str | None:
    """
    Busca a configuração primeiro em st.secrets (Streamlit Cloud / secrets.toml)
    e, se não encontrar, numa variável de ambiente. Evita ter que hardcodar
    credenciais dentro do código-fonte.
    """
    try:
        import streamlit as st
        if chave in st.secrets:
            return st.secrets[chave]
    except Exception:
        pass
    return os.getenv(chave, padrao)


def get_db_config() -> dict:
    return {
        "host": _get("DB_HOST", "aws-1-us-east-2.pooler.supabase.com"),
        "port": int(_get("DB_PORT", "5432")),
        "database": _get("DB_NAME", "postgres"),
        "user": _get("DB_USER", "postgres.ghdasibpuzyvhbfsboke"),
        "password": _get("DB_PASSWORD", "Cxa!9vT#2026@Db")
    }
