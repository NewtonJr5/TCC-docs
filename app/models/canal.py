from sqlalchemy import Column, String, Integer, BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from ..database.base import Base


class Canal(Base):
    __tablename__ = "canal"


    id = Column(String, primary_key=True)

    name = Column(Text)
    url = Column(Text)
    followers = Column(Integer)
    Country = Column(String)
    
    posts = relationship("Post", back_populates="canal")