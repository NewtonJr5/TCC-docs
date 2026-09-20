from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel, Field

from app.repositories.post_repository import PostRepository
from app.repositories.canal_repository import CanalRepository
from app.repositories.categoria_repository import CategoriaRepository
from app.repositories.plataforma_repository import PlataformaRepository

from app.services.post_service import PostService

from app.database.connection import AsyncSessionLocal

from app.services.youtube_service import YoutubeService
from app.scrapper.youtube.extrator_youtube import YouTubeExtractor

session = AsyncSessionLocal()
post_repository = PostRepository(session)
canal_repository = CanalRepository(session)
categoria_repository = CategoriaRepository(session)
plataforma_repository = PlataformaRepository(session)

router = APIRouter()


def _serialize_posts(posts: list[Any]) -> list[dict[str, Any]]:
    serialized: list[dict[str, Any]] = []

    for post in posts:
        if isinstance(post, dict):
            serialized.append(post)
            continue

        item = post.__dict__.copy()
        item.pop("_sa_instance_state", None)
        serialized.append(item)

    return serialized


class YoutubeExtractionResponse(BaseModel):
    message: str = Field(
        ..., description="Mensagem resumindo o resultado da extração."
    )
    posts_salvos: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Lista dos posts extraídos e persistidos no banco."
    )


class PostFilterResponse(BaseModel):
    message: str = Field(
        ..., description="Mensagem resumindo a consulta dos posts."
    )
    total: int = Field(
        ..., ge=0, description="Número total de registros retornados."
    )
    data: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Lista de posts encontrados conforme os filtros informados."
    )


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

@router.post(
    "/youtube/hot",
    tags=["Youtube"],
    summary="Extrair dados de vídeos em alta do YouTube",
    description=(
        "Busca os vídeos mais populares do YouTube e salva os dados no banco. "
        "Útil para monitorar tendências e coletar conteúdos em destaque."
    ),
    response_model=YoutubeExtractionResponse,
    responses={
        200: {"description": "Extração concluída com sucesso."},
        500: {"description": "Erro interno durante a extração ou salvamento dos vídeos."},
    },
)
async def youtube_hot(
    max_videos: int = Query(
        default=5,
        ge=1,
        le=50,
        description="Número máximo de vídeos a serem extraídos.",
        examples={"padrao": {"summary": "Padrão", "value": 5}},
    ),
    max_comments: int = Query(
        default=5,
        ge=0,
        le=50,
        description="Número máximo de comentários a buscar por vídeo.",
        examples={"padrao": {"summary": "Padrão", "value": 5}},
    ),
):

    try:
        posts = await youtube_service.extrair_hot(
            max_videos=max_videos,
            max_comments=max_comments,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao extrair vídeos em alta do YouTube: {exc}",
        ) from exc

    return {
        "message": "Extração concluída.",
        "posts_salvos": _serialize_posts(posts),
    }


@router.post(
    "/youtube/new",
    tags=["Youtube"],
    summary="Extrair dados de vídeos recentes do YouTube",
    description=(
        "Busca vídeos recentes conforme uma consulta e intervalo de data informado. "
        "Pode ser usado para coletar conteúdo novo em um período específico."
    ),
    response_model=YoutubeExtractionResponse,
    responses={
        200: {"description": "Extração concluída com sucesso."},
        400: {"description": "Parâmetros inválidos ou consulta incompleta."},
        500: {"description": "Erro durante a extração ou persistência dos dados."},
    },
)
async def youtube_new(
    query: str = Query(
        ..., description="Termo de busca usado para localizar vídeos no YouTube.", examples={"python": {"summary": "Exemplo de busca", "value": "python"}},
    ),
    published_after: str = Query(
        ..., description="Data inicial no formato ISO 8601 para filtrar os vídeos.", examples={"exemplo": {"summary": "Últimos 7 dias", "value": "2025-01-01T00:00:00Z"}},
    ),
    published_before: str = Query(
        ..., description="Data final no formato ISO 8601 para filtrar os vídeos.", examples={"exemplo": {"summary": "Até hoje", "value": "2025-01-10T00:00:00Z"}},
    ),
    max_videos: int = Query(
        default=5,
        ge=1,
        le=50,
        description="Número máximo de vídeos a serem recuperados.",
    ),
    max_comments: int = Query(
        default=5,
        ge=0,
        le=50,
        description="Número máximo de comentários por vídeo.",
    ),
):

    try:
        posts = await youtube_service.extrair_new(
            query=query,
            published_after=published_after,
            published_before=published_before,
            max_videos=max_videos,
            max_comments=max_comments,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao extrair vídeos recentes do YouTube: {exc}",
        ) from exc

    return {
        "message": "Extração concluída.",
        "posts_salvos": _serialize_posts(posts),
    }


@router.post(
    "/youtube/channel",
    tags=["Youtube"],
    summary="Extrair dados de vídeos de um canal do YouTube",
    description=(
        "Busca os vídeos de um canal específico e salva os conteúdos coletados no banco. "
        "Útil para monitorar canais favoritos ou competidores."
    ),
    response_model=YoutubeExtractionResponse,
    responses={
        200: {"description": "Extração concluída com sucesso."},
        500: {"description": "Erro ao consultar o canal ou persistir os dados."},
    },
)
async def youtube_channel(
    nome_canal: str = Query(
        ..., description="Nome do canal do YouTube a ser consultado.", examples={"python": {"summary": "Canal de exemplo", "value": "Microsoft Developer"}},
    ),
    max_videos: int = Query(
        default=5,
        ge=1,
        le=50,
        description="Número máximo de vídeos a recuperar do canal.",
    ),
    max_comments: int = Query(
        default=5,
        ge=0,
        le=50,
        description="Número máximo de comentários por vídeo.",
    ),
):

    try:
        posts = await youtube_service.extrair_canal(
            nome_canal=nome_canal,
            max_videos=max_videos,
            max_comments=max_comments,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao extrair vídeos do canal do YouTube: {exc}",
        ) from exc

    return {
        "message": "Extração concluída.",
        "posts_salvos": _serialize_posts(posts),
    }


@router.get(
    "/filter",
    tags=["Posts"],
    summary="Buscar posts por filtros",
    description=(
        "Consulta posts armazenados no banco utilizando filtros enviados pela query string. "
        "É possível combinar múltiplos filtros para refinar a busca."
    ),
    response_model=PostFilterResponse,
    responses={
        200: {"description": "Lista de posts encontrada com sucesso."},
        400: {"description": "Nenhum filtro informado ou filtro inválido."},
    },
)
async def get_posts_by_columns(
    request: Request,
    external_id: str | None = Query(
        default=None,
        description="Identificador externo do post.",
    ),
    user: str | None = Query(
        default=None,
        description="Usuário autor do post.",
    ),
    type: str | None = Query(
        default=None,
        description="Tipo do post, por exemplo: youtube_video ou youtube_comment.",
    ),
    plataforma_id: str | None = Query(
        default=None,
        description="Identificador da plataforma relacionada ao post.",
    ),
    canal_id: str | None = Query(
        default=None,
        description="Identificador do canal relacionado ao post.",
    ),
    categoria_id: str | None = Query(
        default=None,
        description="Identificador da categoria relacionada ao post.",
    ),
):
    """
    Busca posts por filtros enviados via query string.

    Exemplos:
    /posts/filter?external_id=abc123
    /posts/filter?type=youtube_video&user=meu_usuario
    /posts/filter?plataforma_id=1&plataforma_id=2
    """
    query_params = request.query_params.multi_items()
    filters: dict[str, Any] = {}

    explicit_filters = {
        "external_id": external_id,
        "user": user,
        "type": type,
        "plataforma_id": plataforma_id,
        "canal_id": canal_id,
        "categoria_id": categoria_id,
    }

    for key, value in explicit_filters.items():
        if value is not None:
            filters[key] = value

    for key, value in query_params:
        if key in {"external_id", "user", "type", "plataforma_id", "canal_id", "categoria_id"}:
            continue
        if key in filters:
            if isinstance(filters[key], list):
                filters[key].append(value)
            else:
                filters[key] = [filters[key], value]
        else:
            filters[key] = value

    if not filters:
        raise HTTPException(
            status_code=400,
            detail="Informe ao menos um filtro na query string."
        )

    try:
        posts = await post_service.get_by_columns(**filters)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Posts encontrados.",
        "total": len(posts),
        "data": _serialize_posts(posts),
    }