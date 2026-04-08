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
    cursor.execute(INSERT_EXTRATO, (extrato.usuario_id, extrato.data, extrato.valor, extrato.tipo, extrato.categoria, extrato.saldo))
    conn.commit()
    conn.close()

def obter_saldo_atual(usuario_id: int) -> float:
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(SELECT_COLUMN_SALDO,(usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0.0

def banco_esta_vazio():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(VAZIO_DADOS_EXTRATO)
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] == 0

def listar_extrato(usuario_id: Caixa360) -> list[Caixa360]:
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute(LISTAR_TODOS,(usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados