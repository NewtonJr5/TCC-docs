from fastapi import APIRouter, BackgroundTasks

from app.repositories.post_repository import PostRepository
from app.repositories.canal_repository import CanalRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.plataforma_repository import PlataformaRepository

from app.services.post_service import PostService

from app.database.connection import AsyncSessionLocal

from app.pipelines.reddit_pipeline import run_pipeline

from app.services.youtube_service import YoutubeService
from app.scrapper.youtube.extrator_youtube import YouTubeExtractor

session = AsyncSessionLocal()
post_repository = PostRepository(session)
canal_repository = CanalRepository(session)
categoria_repository = CategoriaRepository(session)
plataforma_repository = PlataformaRepository(session)

router = APIRouter()

post_service = PostService(
    canal_repository=canal_repository,
    post_repository=post_repository,
    categoria_repository=categoria_repository,
    plataforma_repository=plataforma_repository
)

youtube_service = YoutubeService(
    extractor=YouTubeExtractor(),
    post_service=post_service,
    canal_repository=canal_repository,
    plataforma_repository=plataforma_repository
)

@router.post("/youtube/hot", tags=["Youtube"])
async def youtube_hot(
    max_videos: int = 5
):

    posts = await youtube_service.extrair_hot(
        max_videos=max_videos
    )

    return {
        "message": "Extração concluída.",
        "posts_salvos": len(posts)
    }


@router.post("/youtube/new", tags=["Youtube"])
async def youtube_new(
    query: str,
    published_after: str,
    published_before: str,
    max_videos: int = 5
):

    posts = await youtube_service.extrair_new(
        query=query,
        published_after=published_after,
        published_before=published_before,
        max_videos=max_videos
    )

    return {
        "message": "Extração concluída.",
        "posts_salvos": len(posts)
    }

@router.post("/youtube/channel", tags=["Youtube"])
async def youtube_channel(
    nome_canal: str,
    max_videos: int = 5
):

    posts = await youtube_service.extrair_canal(
        channel_id=nome_canal,
        max_videos=max_videos
    )

    return {
        "message": "Extração concluída.",
        "posts_salvos": len(posts)
    }

'''
@router.post("/pipeline/reddit/run", tags=["Pipeline"])
async def run_pipeline_reddit(
    subreddit: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(
        run_pipeline,
        subreddit
    )

    return {
        "message": "Pipeline iniciado"
    }
'''