from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

app = FastAPI(title="Image API", description="API para gerenciar imagens")

IMG_DIR = Path("../static/img")  # Ajustado para o caminho relativo de core/

# Garantir que o diretório existe
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Montar arquivos estáticos para servir imagens diretamente
app.mount("/images", StaticFiles(directory=str(IMG_DIR)), name="images")

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    file_path = IMG_DIR / file.filename
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename, "url": f"/images/{file.filename}"}

@app.get("/list")
def list_images():
    images = [f for f in os.listdir(IMG_DIR) if f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return {"images": images}

@app.get("/image/{filename}")
def get_image(filename: str):
    file_path = IMG_DIR / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)

@app.get("/")
def root():
    return {"message": "Image API running", "endpoints": ["/upload", "/list", "/image/{filename}"]}
