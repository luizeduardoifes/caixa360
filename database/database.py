import psycopg2

def criar_conexao():
    conn = psycopg2.connect(
        host = "aws-1-us-east-2.pooler.supabase.com",
        port = 5432,
        database = "postgres",
        user = "postgres.ghdasibpuzyvhbfsboke",
        password = "Cxa!9vT#2026@Db"
)
    return conn