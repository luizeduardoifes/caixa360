from database.database import criar_conexao
from models.caixa360 import Caixa360
from sql.caixa360_sql import *


def criar_tabela_extrato():
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(CREATE_TABLE_EXTRATO)
        conn.commit()
    finally:
        conn.close()


def inserir_extrato(extrato: Caixa360) -> Caixa360:
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(
            INSERT_EXTRATO,
            (
                extrato.usuario_id,
                extrato.data,
                extrato.valor,
                extrato.tipo,
                extrato.categoria,
                extrato.saldo,
            ),
        )
        conn.commit()
    finally:
        conn.close()
    return extrato


def obter_saldo_atual(usuario_id: int) -> float:
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(SELECT_COLUMN_SALDO, (usuario_id,))
        resultado = cursor.fetchone()
    finally:
        conn.close()
    return resultado[0] if resultado else 0.0


def banco_esta_vazio() -> bool:
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(VAZIO_DADOS_EXTRATO)
        resultado = cursor.fetchone()
    finally:
        conn.close()
    return resultado[0] == 0


def listar_extrato(usuario_id: int) -> list:
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(LISTAR_TODOS, (usuario_id,))
        return cursor.fetchall()
    finally:
        conn.close()


# --- Editar / excluir -------------------------------------------------------

def buscar_extrato_por_id(usuario_id: int, extrato_id: int):
    """Sempre filtra por usuario_id também, pra ninguém editar/ver lançamento de outra pessoa."""
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(SELECIONAR_EXTRATO_POR_ID, (extrato_id, usuario_id))
        return cursor.fetchone()
    finally:
        conn.close()


def atualizar_extrato(
    usuario_id: int,
    extrato_id: int,
    novo_valor: float | None = None,
    nova_categoria: str | None = None,
) -> bool:
    """
    Atualiza valor e/ou categoria de um lançamento existente. Depois recalcula
    o saldo de todos os lançamentos do usuário, porque o saldo é acumulado
    (cada linha guarda o saldo total até ali) e mudar um valor no meio da
    cadeia deixa todo o resto desatualizado se não recalcular.
    """
    registro = buscar_extrato_por_id(usuario_id, extrato_id)
    if not registro:
        return False

    _, _, _, valor_atual, _tipo, categoria_atual, _saldo_atual = registro
    valor_final = novo_valor if novo_valor is not None else valor_atual
    categoria_final = nova_categoria if nova_categoria else categoria_atual

    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_EXTRATO_VALOR_CATEGORIA,
            (valor_final, categoria_final, extrato_id, usuario_id),
        )
        conn.commit()
    finally:
        conn.close()

    _recalcular_saldos(usuario_id)
    return True


def excluir_extrato(usuario_id: int, extrato_id: int) -> bool:
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR_EXTRATO, (extrato_id, usuario_id))
        excluiu = cursor.rowcount > 0
        conn.commit()
    finally:
        conn.close()

    if excluiu:
        _recalcular_saldos(usuario_id)
    return excluiu


def _recalcular_saldos(usuario_id: int) -> None:
    """
    Refaz o saldo acumulado de todos os lançamentos do usuário, na ordem certa,
    depois de qualquer edição ou exclusão. Sem isso o saldo de todos os
    lançamentos posteriores ao que mudou fica errado.
    """
    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        cursor.execute(LISTAR_TODOS, (usuario_id,))
        registros = cursor.fetchall()

        saldo = 0.0
        for registro_id, _usuario_id, _data, valor, tipo, _categoria, _saldo in registros:
            saldo += valor if tipo == "entrada" else -valor
            cursor.execute(ATUALIZAR_EXTRATO_SALDO, (saldo, registro_id))

        conn.commit()
    finally:
        conn.close()
