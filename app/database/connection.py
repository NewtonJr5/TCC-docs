from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

DATABASE_URL = (
    "postgresql+asyncpg://reddit:reddit@localhost:5433/reddit_pipeline"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)