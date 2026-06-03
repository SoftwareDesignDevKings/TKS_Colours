from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.APP_ENV == "development",
    # Serverless functions are short-lived and Supabase's pooler (pgBouncer)
    # manages pooling on its side, so don't pool connections in-process.
    poolclass=NullPool,
    # pgBouncer in transaction mode can't reuse asyncpg's prepared statements,
    # which otherwise causes "prepared statement does not exist" errors.
    # Required for Supabase's transaction pooler; harmless on a direct connection.
    connect_args={
        "statement_cache_size": 0,
        "prepared_statement_cache_size": 0,
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
