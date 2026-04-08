CREATE_TABLE_EXTRATO = '''
CREATE TABLE IF NOT EXISTS extrato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    data DATE NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    categoria TEXT NOT NULL,
    saldo REAL NOT NULL
);
'''

INSERT_EXTRATO = '''
INSERT INTO extrato (usuario_id, data, valor, tipo, categoria, saldo)
VALUES (?, ?, ?, ?, ?, ?);
'''

SELECT_COLUMN_SALDO = """
SELECT saldo 
FROM extrato 
WHERE usuario_id = ?
ORDER BY id DESC 
LIMIT 1
"""

VAZIO_DADOS_EXTRATO = '''SELECT COUNT(*) FROM extrato;
'''

LISTAR_TODOS = """
SELECT * FROM extrato WHERE usuario_id = ?;
"""