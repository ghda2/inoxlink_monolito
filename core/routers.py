from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/index")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Adicione mais rotas aqui conforme necessário
