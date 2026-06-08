from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categoria import Categoria


class CategoriaRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, categoria: Categoria):
        self.session.add(categoria)
        await self.session.commit()
        await self.session.refresh(categoria)
        return categoria

    async def get_by_id(self, categoria_id: int):
        result = await self.session.execute(
            select(Categoria).where(Categoria.id == categoria_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(Categoria))
        return result.scalars().all()