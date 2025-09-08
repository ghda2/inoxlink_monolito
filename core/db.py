import sqlite3
from pathlib import Path

DATABASE_PATH = Path("database.db")

def init_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    # Criar tabelas conforme bd.sql
    with open("bd.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn
