from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plataforma import Plataforma


class PlataformaRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, plataforma: Plataforma):
        self.session.add(plataforma)
        await self.session.commit()
        await self.session.refresh(plataforma)
        return plataforma

    async def get_by_id(self, plataforma_id: int):
        result = await self.session.execute(
            select(Plataforma).where(Plataforma.id == plataforma_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(Plataforma))
        return result.scalars().all()
    
    async def get_or_create(self, nome: str):

        plataforma = await self.get_by_nome(nome)

        if plataforma:
            return plataforma

        plataforma = Plataforma(name=nome)

        self.session.add(plataforma)
        await self.session.commit()
        await self.session.refresh(plataforma)

        return plataforma
    
    async def get_by_nome(self, nome: str):

        result = await self.session.execute(
            select(Plataforma).where(
                Plataforma.name == nome
            )
        )

        return result.scalar_one_or_none()