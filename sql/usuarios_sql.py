CREATE_TABLE_USUARIOS = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    trocar_senha INTEGER NOT NULL DEFAULT 1
);
'''

INSERT_USUARIO = '''
INSERT INTO usuarios (usuario, senha, trocar_senha) 
VALUES (?, ?, ?)
'''

UPDATE_SENHA = '''
"UPDATE usuarios SET senha = ?, trocar_senha = 0 WHERE id = ?"
'''