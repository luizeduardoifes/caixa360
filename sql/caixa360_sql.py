CREATE_TABLE_EXTRATO = '''
CREATE TABLE IF NOT EXISTS extrato (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    valor REAL NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL
);
'''

INSERT_EXTRATO = '''
INSERT INTO extrato (data, hora, valor, tipo, descricao)
VALUES (?, ?, ?, ?, ?);
'''