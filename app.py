from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from sqlalchemy.orm import Session
from core.routers import router
from core.db import init_db, get_db
from core.models import Post
from core.sitemap import router as sitemap_router

app = FastAPI()

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Incluir routers
app.include_router(router)
app.include_router(sitemap_router)

# Inicializar banco de dados
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    posts = db.query(Post).filter(Post.status == 'published').all()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})
