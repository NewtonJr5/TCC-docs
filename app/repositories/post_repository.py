from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post


class PostRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, post: Post):
        self.session.add(post)
        await self.session.commit()
        await self.session.refresh(post)
        return post

    async def get_by_id(self, post_id: str):
        stmt = select(Post).where(Post.id == post_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, external_id: str) -> bool:
        stmt = select(Post.external_id).where(
            Post.external_id == external_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None

    async def delete(self, post_id: str):
        post = await self.get_by_id(post_id)

        if post:
            await self.session.delete(post)
            await self.session.commit()

    async def get_latest_posts(self, limit: int):
        """
        Retorna os posts mais recentes ordenados pela data de criação.
        """

        result = await self.session.execute(
            select(Post)
            .order_by(desc(Post.data_post))
            .limit(limit)
        )

        return result.scalars().all()
    
    async def get_by_external_id(self, external_id: str):
        stmt = select(Post).where(
            Post.external_id == external_id
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()