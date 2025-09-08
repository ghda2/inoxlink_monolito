-- Script para configuração do banco de dados

-- 1. Apagar tabelas existentes (desativando constraints)
DROP TABLE IF EXISTS post_categories CASCADE;
DROP TABLE IF EXISTS post_tags CASCADE;
DROP TABLE IF EXISTS comments CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS autores CASCADE;
DROP TABLE IF EXISTS noticias_rapidas CASCADE;
DROP TABLE IF EXISTS trending_topics CASCADE;

-- 2. Criar tabelas
CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    bio TEXT,
    url_foto VARCHAR(255)
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    cor VARCHAR(7)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE,
    subtitulo VARCHAR(500),
    conteudo TEXT NOT NULL,
    url_imagem_principal VARCHAR(255),
    url_imagem_miniatura VARCHAR(255),
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'draft',
    is_destaque BOOLEAN NOT NULL DEFAULT FALSE,
    is_highlight BOOLEAN NOT NULL DEFAULT FALSE,
    visualizacoes INT NOT NULL DEFAULT 0,
    id_autor INT REFERENCES autores(id) ON DELETE SET NULL
);

CREATE TABLE post_categories (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, category_id)
);

CREATE TABLE post_tags (
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INT REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (post_id, tag_id)
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
    nome_autor VARCHAR(255) NOT NULL,
    email_autor VARCHAR(255),
    conteudo TEXT NOT NULL,
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) NOT NULL DEFAULT 'pending'
);

CREATE TABLE noticias_rapidas (
    id SERIAL PRIMARY KEY,
    texto VARCHAR(500) NOT NULL,
    horario TIME NOT NULL
);

CREATE TABLE trending_topics (
    id SERIAL PRIMARY KEY,
    hashtag VARCHAR(100) NOT NULL UNIQUE,
    posicao INT NOT NULL,
    data_atualizacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 3. Função para gerar slug
CREATE OR REPLACE FUNCTION generate_slug(input_text TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN TRIM(BOTH '-' FROM 
        REGEXP_REPLACE(
            LOWER(REGEXP_REPLACE(input_text, '[^a-zA-Z0-9\s-]', '', 'g')),
            '\s+',
            '-',
            'g'
        )
    );
END;
$$ LANGUAGE plpgsql;

-- 4. Trigger para posts (slug + atualização)
CREATE OR REPLACE FUNCTION set_post_slug()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.slug IS NULL OR NEW.slug = '' THEN
        NEW.slug := generate_slug(NEW.titulo);
    END IF;
    NEW.data_atualizacao := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_set_post_slug
    BEFORE INSERT OR UPDATE ON posts
    FOR EACH ROW
    EXECUTE FUNCTION set_post_slug();
