from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(
    os.getenv("DATABASE_URL"),
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)