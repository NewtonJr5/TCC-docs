import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.controller.controller import router as post_router

app = FastAPI(
    title="API Web para extratores de postagens de redes sociais",
    version="1.0.0",
    description=(
        "API para coleta, armazenamento e consulta de dados de conteúdo digital. "
        "Permite extrair dados de vídeos, comentários e informações de canais, além de consultar "
        "registros salvos no banco por filtros."
    ),
    openapi_tags=[
        {
            "name": "Youtube",
            "description": "Endpoints para extração de dados de vídeos, de comentários e de canais do YouTube."
        },
        {
            "name": "Posts",
            "description": "Endpoints para consulta de posts salvos no banco conforme filtros específicos."
        },
    ],
)

print(app.title)

app.include_router(
    post_router,
    prefix="/posts"
)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Erro interno do servidor: {exc}"
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )