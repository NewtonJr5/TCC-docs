import asyncio
import logging
from datetime import datetime, timezone

from app.database.connection import AsyncSessionLocal

from app.scrapper.reddit.posts import fetch_subreddit
from app.scrapper.reddit.comments import fetch_comments

from app.repositories.post_repository import PostRepository
from app.services.post_service import PostService

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Intervalo entre ciclos de coleta contínua (segundos)
# ---------------------------------------------------------------------------
COLLECTION_INTERVAL = 300  # 5 minutos


async def run_pipeline(
    subreddit: str,
    canal_id: str | None = None,
    plataforma_id: str | None = None,
    categoria_id: str | None = None,
    pages: int = 2,
    after: str | None = None,       # cursor externo (coleta incremental)
) -> str | None:
    """
    Executa uma rodada de coleta para um subreddit.

    Retorna o último cursor ``after`` coletado para ser reutilizado
    na próxima chamada (coleta incremental).
    """
    logger.info("[%s] Iniciando pipeline – pages=%d after=%s", subreddit, pages, after)

    async with AsyncSessionLocal() as session:
        post_repository = PostRepository(session)
        post_service = PostService(
            post_repository=post_repository,
            canal_repository=None,
            plataforma_repository=None,
            categoria_repository=None,
        )

        current_after = after

        for page in range(1, pages + 1):
            logger.info("[%s] Página %d/%d (after=%s)", subreddit, page, pages, current_after)

            try:
                data = await fetch_subreddit(subreddit=subreddit, after=current_after)
            except Exception:
                logger.exception("[%s] Falha ao buscar página %d – abortando pipeline", subreddit, page)
                break

            posts = data["data"]["children"]
            next_after = data["data"].get("after")

            for item in posts:
                reddit_post = item["data"]

                try:
                    root_post = await post_service.save_reddit_post(
                        reddit_post=reddit_post,
                        canal_id=canal_id,
                        plataforma_id=plataforma_id,
                        categoria_id=categoria_id,
                    )
                except Exception:
                    logger.exception("[%s] Erro ao salvar post %s", subreddit, reddit_post.get("id"))
                    continue

                if root_post is None:
                    continue

                try:
                    comments_json = await fetch_comments(subreddit, reddit_post["id"])
                    comments = comments_json[1]["data"]["children"]

                    post_map = {f"t3_{root_post.id}": root_post.id}

                    await post_service.process_comments(
                        comments=comments,
                        post_service=post_service,
                        post_map=post_map,
                        canal_id=canal_id,
                        plataforma_id=plataforma_id,
                        categoria_id=categoria_id,
                    )
                except Exception:
                    logger.exception("[%s] Erro ao processar comentários do post %s", subreddit, reddit_post.get("id"))

            # Persiste cursor antes do commit para não perder progresso
            current_after = next_after

            if not current_after:
                logger.info("[%s] Sem mais páginas disponíveis.", subreddit)
                break

        await session.commit()

    logger.info("[%s] Pipeline concluído. Último cursor: %s", subreddit, current_after)
    return current_after


async def run_continuous(
    subreddit: str,
    canal_id: str | None = None,
    plataforma_id: str | None = None,
    categoria_id: str | None = None,
    pages: int = 2,
    initial_after: str | None = None,
    interval: int = COLLECTION_INTERVAL,
) -> None:
    """
    Executa coleta contínua e incremental de forma indefinida.

    O cursor ``after`` é preservado entre ciclos: cada rodada começa
    exatamente onde a anterior parou.

    Parâmetros
    ----------
    interval : int
        Tempo de espera (segundos) entre o fim de um ciclo e o início do próximo.
    """
    after = initial_after

    while True:
        cycle_start = datetime.now(timezone.utc)
        logger.info("[%s] Iniciando ciclo contínuo em %s", subreddit, cycle_start.isoformat())

        try:
            after = await run_pipeline(
                subreddit=subreddit,
                canal_id=canal_id,
                plataforma_id=plataforma_id,
                categoria_id=categoria_id,
                pages=pages,
                after=after,
            )
        except Exception:
            logger.exception("[%s] Erro crítico no ciclo – retentando no próximo intervalo", subreddit)

        logger.info("[%s] Aguardando %ds até o próximo ciclo…", subreddit, interval)
        await asyncio.sleep(interval)