from app.models.post import Post
from app.repositories.post_repository import PostRepository
from app.repositories.canal_repository import CanalRepository
from app.repositories.plataforma_repository import PlataformaRepository
from app.repositories.categoria_repository import CategoriaRepository


class PostService:

    def __init__(
        self,
        post_repository: PostRepository,
        canal_repository: CanalRepository,
        plataforma_repository: PlataformaRepository,
        categoria_repository: CategoriaRepository,
    ):
        """
        Inicializa o serviço de posts com os repositórios necessários
        para acesso e persistência dos dados.
        """
        self.post_repository = post_repository
        self.canal_repository = canal_repository
        self.plataforma_repository = plataforma_repository
        self.categoria_repository = categoria_repository

    async def exists(
        self,
        external_id: str
    ) -> bool:

        return await self.post_repository.exists(
            external_id
        )

    async def get_by_id(self, post_id: str):
        """
        Recupera um post pelo seu identificador.

        Args:
            post_id: Identificador do post.

        Returns:
            Instância de Post ou None caso não seja encontrada.
        """
        return await self.post_repository.get_by_id(post_id)

    async def create(
        self,
        post_data: dict,
        canal_id: str,
        plataforma_id: str,
        categoria_id: str | None = None
    ):

        return Post(
            external_id=post_data["external_id"],
            canal_id=canal_id,
            plataforma_id=plataforma_id,
            categoria_id=categoria_id,
            parent_post_id=post_data.get("parent_post_id"),
            text=post_data["text"],
            url=post_data["url"],
            images=post_data.get("images", []),
            videos=post_data.get("videos", []),
            E_text=post_data.get("E_text"),
            E_images=post_data.get("E_images"),
            E_videos=post_data.get("E_videos"),
            data_post=post_data["data_post"],
            user=post_data["user"],
            type=post_data["type"],
            created_utc=post_data["created_utc"]
        )

    async def save(
        self,
        post_data,
        canal_id,
        plataforma_id,
        categoria_id=None
    ):

        if await self.exists(
            post_data["external_id"]
        ):
            return None

        parent_external_id = post_data.get(
            "parent_external_id"
        )

        if parent_external_id:

            parent = await self.post_repository.get_by_external_id(
                parent_external_id
            )

            if parent is None:
                raise ValueError(
                    f"Post pai {parent_external_id} não encontrado."
                )

        post = await self.create(
            post_data,
            canal_id,
            plataforma_id,
            categoria_id
        )

        await self.post_repository.save(post)

        return post

    async def update_embeddings(
        self,
        post_id: str,
        text_embedding=None,
        image_embedding=None,
        video_embedding=None
    ):
        """
        Atualiza os embeddings associados a um post.

        Permite atualizar separadamente os embeddings de texto,
        imagem e vídeo.

        Args:
            post_id: Identificador do post.
            text_embedding: Embedding textual.
            image_embedding: Embedding de imagem.
            video_embedding: Embedding de vídeo.

        Returns:
            Post atualizado ou None caso não exista.
        """

        post = await self.post_repository.get_by_id(post_id)

        if not post:
            return None

        if text_embedding is not None:
            post.E_text = text_embedding

        if image_embedding is not None:
            post.E_images = image_embedding

        if video_embedding is not None:
            post.E_videos = video_embedding

        await self.post_repository.save(post)

        return post

    async def get_posts_without_embeddings(self):
        """
        Recupera posts que ainda não possuem embeddings gerados.

        Returns:
            Lista de posts pendentes de processamento.
        """
        return await self.post_repository.get_posts_without_embeddings()

    async def get_children(self, parent_post_id: str):
        """
        Recupera todos os posts filhos de um post pai.

        Args:
            parent_post_id: Identificador do post pai.

        Returns:
            Lista de posts filhos.
        """
        return await self.post_repository.get_children(parent_post_id)

    async def get_latest_posts(self, limit: int = 10):
        """
        Recupera os posts mais recentes.

        Args:
            limit: Quantidade máxima de posts retornados.

        Returns:
            Lista de posts ordenados do mais recente para o mais antigo.
        """

        return await self.post_repository.get_latest_posts(limit)
    
    