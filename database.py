import sqlite3

def conectar():
    conn = sqlite3.connect("epi.db")
    return conn


def criar_tabela():

    conn = conectar()
    cursor = conn.cursor()

    # TABELA FUNCIONÁRIOS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cargo TEXT,
        setor TEXT
    )
    """)

    # TABELA EPIs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS epis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        ca TEXT,
        validade_dias INTEGER,
        fabricante TEXT
    )
    """)

    # TABELA ENTREGAS
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entregas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario TEXT,
        epi TEXT,
        data TEXT,
        vencimento TEXT
    )
    """)

    conn.commit()
    conn.close()