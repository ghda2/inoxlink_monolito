from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from core.routers import router
from core.db import init_db
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
def read_root():
    return {"message": "Sistema FastAPI rodando"}
