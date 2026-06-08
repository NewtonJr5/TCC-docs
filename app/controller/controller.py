from fastapi import APIRouter, BackgroundTasks


from app.repositories.post_repository import PostRepository
from app.repositories.canal_repository import CanalRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.plataforma_repository import PlataformaRepository

from app.services.post_service import PostService

from app.database.connection import AsyncSessionLocal

from app.pipelines.reddit_pipeline import run_pipeline

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


@router.get("/", tags=["Posts"])
async def listar_posts(limit: int = 20):
    return await post_service.get_latest_posts(limit)


@router.get("/{post_id}", tags=["Posts"])
async def buscar_post(post_id: str):
    return await post_service.get_by_id(post_id)


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