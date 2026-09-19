import asyncio
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.database.base import Base
from app.database.connection import engine

# Importar os models
from app.models.post import Post
from app.models.canal import Canal
from app.models.categoria import Categoria
from app.models.plataforma import Plataforma

async def recreate_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(recreate_tables())