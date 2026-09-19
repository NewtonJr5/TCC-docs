import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI

from app.controller.controller import router as post_router

# async def main():
#     await run_continuous(
#         subreddit="python",
#         pages=3,
#         interval=5
#     )


# if __name__ == "__main__":
#     asyncio.run(main())

app = FastAPI(
    title="Data Pipeline API",
    version="1.0.0",
    description=(
        "API para coleta, armazenamento e consulta de dados de conteúdo digital. "
        "Permite extrair comentários e informações de canais, além de consultar "
        "registros salvos no banco por filtros."
    ),
    openapi_tags=[
        {
            "name": "Youtube",
            "description": "Endpoints para extração de vídeos, comentários e dados de canais do YouTube."
        },
        {
            "name": "Posts",
            "description": "Endpoints para consulta de posts salvos no banco conforme filtros específicos."
        },
    ],
)

app.include_router(
    post_router,
    prefix="/posts"
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )