import sqlite3

def criar_conexao():
    conexao = sqlite3.connect('extrato.db')
    return conexao