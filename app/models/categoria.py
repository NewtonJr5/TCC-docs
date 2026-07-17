from sqlalchemy import Column, String, Integer, BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from ..database.base import Base


class Categoria(Base):
    __tablename__ = "categoria"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(Text)
    
    posts = relationship("Post", back_populates="categoria")