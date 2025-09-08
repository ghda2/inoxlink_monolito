from sqlalchemy import Column, Integer, String, Text, DateTime, Time, Boolean, ForeignKey, Table
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from core.db import Base

# Tabela de associação para post_categories
post_categories = Table('post_categories', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# Tabela de associação para post_tags
post_tags = Table('post_tags', Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    bio = Column(Text)
    url_foto = Column(String(255))

    # Relacionamento com posts
    posts = relationship("Post", back_populates="autor")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    descricao = Column(Text)
    cor = Column(String(7))

    # Relacionamento com posts
    posts = relationship("Post", secondary=post_categories, back_populates="categories")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)

    # Relacionamento com posts
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True)
    subtitulo = Column(String(500))
    conteudo = Column(Text, nullable=False)
    url_imagem_principal = Column(String(255))
    url_imagem_miniatura = Column(String(255))
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    status = Column(String(50), nullable=False, default='draft')
    is_destaque = Column(Boolean, nullable=False, default=False)
    is_highlight = Column(Boolean, nullable=False, default=False)
    visualizacoes = Column(Integer, nullable=False, default=0)
    id_autor = Column(Integer, ForeignKey("autores.id"), nullable=True)

    # Relacionamentos
    autor = relationship("Autor", back_populates="posts")
    categories = relationship("Category", secondary=post_categories, back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="tags")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    nome_autor = Column(String(255), nullable=False)
    email_autor = Column(String(255))
    conteudo = Column(Text, nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False, default='pending')

    # Relacionamento com post
    post = relationship("Post", back_populates="comments")

class NoticiaRapida(Base):
    __tablename__ = "noticias_rapidas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String(500), nullable=False)
    horario = Column(Time, nullable=False)

class TrendingTopic(Base):
    __tablename__ = "trending_topics"

    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String(100), unique=True, nullable=False)
    posicao = Column(Integer, nullable=False)
    data_atualizacao = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
