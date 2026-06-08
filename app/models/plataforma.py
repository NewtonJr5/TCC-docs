from sqlalchemy import Column, String, Integer, BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from ..database.base import Base


class Plataforma(Base):
    __tablename__ = "plataforma"

    id = Column(String, primary_key=True)

    name = Column(Text)
    url = Column(Text)
    
    posts = relationship("Post", back_populates="plataforma")

