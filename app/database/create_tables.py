import asyncio

from app.database.base import Base
from app.database.connection import engine

# Importar todos os models para registrá-los no metadata
from app.models.post import Post
from app.models.canal import Canal
from app.models.categoria import Categoria
from app.models.plataforma import Plataforma


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())