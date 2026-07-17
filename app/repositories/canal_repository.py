from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.canal import Canal


class CanalRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        external_id: str,
        nome: str,
    ):
        canal = Canal(
            external_id=external_id,
            name=nome,
        )

        self.session.add(canal)
        await self.session.commit()
        await self.session.refresh(canal)

        return canal

    async def save(self, canal: Canal):
        self.session.add(canal)
        await self.session.commit()
        await self.session.refresh(canal)
        return canal

    async def get_by_id(self, canal_id: int):
        result = await self.session.execute(
            select(Canal).where(Canal.id == canal_id)
        )
        return result.scalar_one_or_none()

    async def get_by_external_id(self, external_id: str):
        result = await self.session.execute(
            select(Canal).where(Canal.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.session.execute(select(Canal))
        return result.scalars().all()