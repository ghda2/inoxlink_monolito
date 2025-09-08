from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter()

@router.get("/sitemap.xml")
def sitemap():
    # Lógica para gerar sitemap dinâmico
    sitemap_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>http://localhost:8000/</loc>
        <lastmod>2023-01-01</lastmod>
        <changefreq>monthly</changefreq>
        <priority>1.0</priority>
    </url>
    <!-- Adicione mais URLs aqui -->
</urlset>"""
    return Response(content=sitemap_content, media_type="application/xml")
