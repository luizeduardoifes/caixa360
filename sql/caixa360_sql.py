CREATE_TABLE_EXTRATO = '''
CREATE TABLE IF NOT EXISTS extrato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    saldo REAL NOT NULL
);
'''

INSERT_EXTRATO = '''
INSERT INTO extrato (data, valor, tipo, descricao, saldo)
VALUES (?, ?, ?, ?, ?);
'''

SELECT_COLUMN_SALDO = '''
SELECT saldo FROM extrato WHERE id = (SELECT MAX(id) FROM extrato);
'''

VAZIO_DADOS_EXTRATO = '''SELECT COUNT(*) FROM extrato;
'''