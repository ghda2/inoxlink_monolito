-- Estrutura do Banco de Dados

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL
);

-- Adicione mais tabelas conforme necessário
