from app.scrapper.youtube.extrator_youtube import YouTubeExtractor
from app.services.post_service import PostService

from app.repositories.canal_repository import CanalRepository
from app.repositories.plataforma_repository import PlataformaRepository


class YoutubeService:

    def __init__(
        self,
        extractor: YouTubeExtractor,
        post_service: PostService,
        canal_repository: CanalRepository,
        plataforma_repository: PlataformaRepository
    ):
        self.extractor = extractor
        self.post_service = post_service
        self.canal_repository = canal_repository
        self.plataforma_repository = plataforma_repository

    async def _get_plataforma(self):

        plataforma = await self.plataforma_repository.get_or_create(
            "Youtube"
        )

        if not plataforma:
            raise ValueError("Plataforma Youtube não cadastrada.")

        return plataforma

    async def _get_canal(
        self,
        external_id: str,
        nome: str,
        plataforma_id: str
    ):

        canal = await self.canal_repository.get_by_external_id(
            external_id
        )

        if canal:
            return canal

        return await self.canal_repository.create(
            external_id=external_id,
            nome=nome,
        )

    async def _save_posts(
        self,
        posts
    ):

        plataforma = await self._get_plataforma()

        saved_posts = []

        for post in posts:

            canal = await self._get_canal(
                external_id=post["channel_id"],
                nome=post["channel_name"],
                plataforma_id=plataforma.id
            )

            saved = await self.post_service.save(
                post_data=post,
                canal_id=canal.id,
                plataforma_id=plataforma.id
            )

            if saved:
                saved_posts.append(saved)

        return saved_posts

    async def extrair_hot(
        self,
        max_videos: int = 5
    ):

        posts = self.extractor.extrair_hot(
            max_videos=max_videos
        )

        return await self._save_posts(posts)

    async def extrair_new(
        self,
        query: str,
        published_after: str,
        published_before: str,
        max_videos: int = 5
    ):

        posts = self.extractor.extrair_new(
            query=query,
            published_after=published_after,
            published_before=published_before,
            max_videos=max_videos
        )

        return await self._save_posts(posts)

    async def extrair_canal(
        self,
        nome_canal: str,
        max_videos: int = 5
    ):

        posts = self.extractor.extrair_canal(
            channel_id=nome_canal,
            max_videos=max_videos
        )

        return await self._save_posts(posts)