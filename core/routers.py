from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from core.db import get_db
from core.models import Autor, Category, Tag, Post, Comment, NoticiaRapida, TrendingTopic
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Pydantic models
class AutorCreate(BaseModel):
    nome: str
    bio: Optional[str] = None
    url_foto: Optional[str] = None

class CategoryCreate(BaseModel):
    nome: str
    slug: Optional[str] = None
    descricao: Optional[str] = None
    cor: Optional[str] = None

class TagCreate(BaseModel):
    nome: str
    slug: Optional[str] = None

class PostCreate(BaseModel):
    titulo: str
    subtitulo: Optional[str] = None
    conteudo: str
    url_imagem_principal: Optional[str] = None
    url_imagem_miniatura: Optional[str] = None
    status: str = "draft"
    is_destaque: bool = False
    is_highlight: bool = False
    id_autor: Optional[int] = None
    category_ids: List[int] = []
    tag_ids: List[int] = []

class CommentCreate(BaseModel):
    post_id: int
    nome_autor: str
    email_autor: Optional[str] = None
    conteudo: str

# Rotas para templates
@router.get("/index")
def index(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.status == 'published').all()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

# CRUD para Autores
@router.post("/autores/")
def create_autor(autor: AutorCreate, db: Session = Depends(get_db)):
    db_autor = Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

@router.get("/autores/")
def read_autores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    autores = db.query(Autor).offset(skip).limit(limit).all()
    return autores

@router.get("/autores/{autor_id}")
def read_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(Autor).filter(Autor.id == autor_id).first()
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor not found")
    return autor

# CRUD para Categorias
@router.post("/categories/")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    if category.slug is None:
        category.slug = category.nome.lower().replace(" ", "-")
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("/categories/")
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = db.query(Category).offset(skip).limit(limit).all()
    return categories

# CRUD para Tags
@router.post("/tags/")
def create_tag(tag: TagCreate, db: Session = Depends(get_db)):
    if tag.slug is None:
        tag.slug = tag.nome.lower().replace(" ", "-")
    db_tag = Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/tags/")
def read_tags(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    tags = db.query(Tag).offset(skip).limit(limit).all()
    return tags

# CRUD para Posts
@router.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # Verificar se autor existe
    if post.id_autor:
        autor = db.query(Autor).filter(Autor.id == post.id_autor).first()
        if not autor:
            raise HTTPException(status_code=404, detail="Autor not found")
    
    # Criar post
    db_post = Post(
        titulo=post.titulo,
        subtitulo=post.subtitulo,
        conteudo=post.conteudo,
        url_imagem_principal=post.url_imagem_principal,
        url_imagem_miniatura=post.url_imagem_miniatura,
        status=post.status,
        is_destaque=post.is_destaque,
        is_highlight=post.is_highlight,
        id_autor=post.id_autor
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # Adicionar categorias e tags
    if post.category_ids:
        categories = db.query(Category).filter(Category.id.in_(post.category_ids)).all()
        db_post.categories.extend(categories)
    
    if post.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
        db_post.tags.extend(tags)
    
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts/")
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@router.get("/posts/{post_id}")
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# CRUD para Comentários
@router.post("/comments/")
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # Verificar se post existe
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = Comment(**comment.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/comments/")
def read_comments(post_id: Optional[int] = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    query = db.query(Comment)
    if post_id:
        query = query.filter(Comment.post_id == post_id)
    comments = query.offset(skip).limit(limit).all()
    return comments

# Adicione mais rotas aqui conforme necessário
