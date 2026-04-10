CREATE_TABLE_USUARIOS = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id SERIAL PRIMARY KEY,
    usuario TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    trocar_senha BOOLEAN NOT NULL DEFAULT TRUE
);
'''

INSERT_USUARIO = '''
INSERT INTO usuarios (usuario, senha, trocar_senha) 
VALUES (%s, %s, %s)
'''

UPDATE_SENHA = '''
UPDATE usuarios 
SET senha = %s, trocar_senha = FALSE 
WHERE id = %s
'''

SELECIONAR_USUARIO_POR_ID = '''
SELECT id, senha, trocar_senha FROM usuarios WHERE usuario = %s
'''