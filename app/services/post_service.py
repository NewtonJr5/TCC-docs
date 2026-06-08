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

    async def exists(self, post_id: str) -> bool:
        """
        Verifica se um post já existe na base de dados.

        Args:
            post_id: Identificador único do post.

        Returns:
            True se o post existir, False caso contrário.
        """
        return await self.post_repository.exists(post_id)

    async def get_by_id(self, post_id: str):
        """
        Recupera um post pelo seu identificador.

        Args:
            post_id: Identificador do post.

        Returns:
            Instância de Post ou None caso não seja encontrada.
        """
        return await self.post_repository.get_by_id(post_id)

    async def create_from_reddit(
        self,
        reddit_post: dict,
        canal_id: int,
        plataforma_id: int,
        categoria_id: int | None = None
    ) -> Post:
        """
        Constrói uma entidade Post a partir dos dados retornados pela API do Reddit.

        Não persiste o objeto no banco, apenas realiza o mapeamento
        dos dados externos para o modelo interno.

        Args:
            reddit_post: Dicionário contendo os dados do post do Reddit.
            canal_id: Identificador do canal associado.
            plataforma_id: Identificador da plataforma.
            categoria_id: Identificador da categoria (opcional).

        Returns:
            Objeto Post preenchido.
        """

        return Post(
            id=reddit_post["id"],
            canal_id=canal_id,
            plataforma_id=plataforma_id,
            categoria_id=categoria_id,
            text=reddit_post.get("selftext"),
            url=reddit_post.get("url"),
            images=[],
            videos=[],
            E_text=None,
            E_images=None,
            E_videos=None,
            data_post=reddit_post.get("created_utc"),
            user=reddit_post.get("author"),
            type="reddit_post",
            created_utc=reddit_post.get("created_utc")
        )

    async def save_reddit_post(
        self,
        reddit_post: dict,
        canal_id: int,
        plataforma_id: int,
        categoria_id: int | None = None
    ) -> Post | None:
        """
        Salva um post do Reddit caso ele ainda não exista na base.

        Args:
            reddit_post: Dados do post retornados pelo Reddit.
            canal_id: Canal associado.
            plataforma_id: Plataforma associada.
            categoria_id: Categoria associada (opcional).

        Returns:
            Post salvo ou None caso o post já exista.
        """

        if await self.exists(reddit_post["id"]):
            return None

        post = await self.create_from_reddit(
            reddit_post=reddit_post,
            canal_id=canal_id,
            plataforma_id=plataforma_id,
            categoria_id=categoria_id
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

    async def create_child_post(
        self,
        parent_post_id: str,
        reddit_post: dict,
        canal_id: int,
        plataforma_id: int,
        categoria_id: int | None = None
    ):
        """
        Cria e persiste um post filho vinculado a um post pai.

        Utilizado principalmente para comentários e respostas.

        Args:
            parent_post_id: Identificador do post pai.
            reddit_post: Dados do comentário/post.
            canal_id: Canal associado.
            plataforma_id: Plataforma associada.
            categoria_id: Categoria associada (opcional).

        Returns:
            Post filho criado.

        Raises:
            ValueError: Caso o post pai não exista.
        """

        parent = await self.post_repository.get_by_id(
            parent_post_id
        )

        if not parent:
            raise ValueError(
                f"Post pai {parent_post_id} não encontrado"
            )

        child = await self.create_from_reddit(
            reddit_post=reddit_post,
            canal_id=canal_id,
            plataforma_id=plataforma_id,
            categoria_id=categoria_id
        )

        child.parent_post_id = parent.id

        await self.post_repository.save(child)

        return child

    async def process_comments(
        self,
        comments,
        post_map,
        canal_id,
        plataforma_id,
        categoria_id=None
    ):
        """
        Processa recursivamente a árvore de comentários do Reddit.

        Para cada comentário:
        - identifica o post pai;
        - cria um post filho correspondente;
        - atualiza o mapa de relacionamentos;
        - processa recursivamente as respostas.

        Args:
            comments: Lista de comentários retornada pela API.
            post_map: Mapa que relaciona IDs do Reddit aos IDs internos.
            canal_id: Canal associado.
            plataforma_id: Plataforma associada.
            categoria_id: Categoria associada (opcional).
        """

        for item in comments:

            if item["kind"] != "t1":
                continue

            comment = item["data"]

            parent_id = comment["parent_id"]

            parent_post_id = post_map.get(parent_id)

            if parent_post_id is None:
                continue

            saved_comment = await self.post_service.create_child_post(
                parent_post_id=parent_post_id,
                reddit_post={
                    "id": comment["id"],
                    "author": comment.get("author"),
                    "selftext": comment.get("body"),
                    "url": None,
                    "created_utc": comment.get("created_utc")
                },
                canal_id=canal_id,
                plataforma_id=plataforma_id,
                categoria_id=categoria_id
            )

            post_map[f"t1_{saved_comment.id}"] = saved_comment.id

            replies = comment.get("replies")

            if (
                replies
                and isinstance(replies, dict)
                and "data" in replies
            ):
                await self.process_comments(
                    comments=replies["data"]["children"],
                    post_map=post_map,
                    canal_id=canal_id,
                    plataforma_id=plataforma_id,
                    categoria_id=categoria_id
                )
    
    async def get_latest_posts(self, limit: int = 10):
        """
        Recupera os posts mais recentes.

        Args:
            limit: Quantidade máxima de posts retornados.

        Returns:
            Lista de posts ordenados do mais recente para o mais antigo.
        """

        return await self.post_repository.get_latest_posts(limit)