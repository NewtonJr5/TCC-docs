from sqlalchemy import (
    Column, String, Integer, BigInteger,
    Text, TIMESTAMP, ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from ..database.base import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)

    text = Column(Text)
    url = Column(Text)

    images = Column(JSONB)
    videos = Column(JSONB)

    E_text = Column(JSONB)
    E_images = Column(JSONB)
    E_videos = Column(JSONB)

    data_post = Column(BigInteger)
    user = Column(String)
    type = Column(String)

    external_id = Column(String)

    created_utc = Column(BigInteger)
    inserted_at = Column(TIMESTAMP, server_default=func.now())

    parent_post = relationship(
        "Post",
        remote_side=[id],
        back_populates="children"
    )

    parent_post_id = Column(
        Integer,
        ForeignKey("post.id"),
        nullable=True
    )

    children = relationship(
        "Post",
        back_populates="parent_post"
    )

    plataforma = relationship(
        "Plataforma",
        back_populates="posts"
    )

    plataforma_id = Column(
        Integer,
        ForeignKey("plataforma.id"),
        nullable=False
    )

    canal = relationship(
        "Canal",
        back_populates="posts"
    )

    canal_id = Column(
        Integer,
        ForeignKey("canal.id"),
        nullable=False
    )

    categoria = relationship(
        "Categoria",
        back_populates="posts"
    )

    categoria_id = Column(
        Integer,
        ForeignKey("categoria.id"),
        nullable=True
    )