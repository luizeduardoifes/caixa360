from database.database import criar_conexao
from models.caixa360 import Caixa360
from sql.caixa360_sql import *

def criar_tabela_extrato():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_EXTRATO)
    conn.commit()
    conn.close()

def inserir_extrato(extrato: Caixa360) -> Caixa360:
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(INSERT_EXTRATO, (extrato.data, extrato.valor, extrato.tipo, extrato.descricao, extrato.saldo))
    conn.commit()
    conn.close()

def obter_saldo_atual() -> float:
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(SELECT_COLUMN_SALDO)
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0.0