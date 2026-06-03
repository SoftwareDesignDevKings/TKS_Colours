from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings

# Supabase (and most hosts) hand out a sync-style URL like
# "postgresql://..." or "postgres://...". The async engine needs the asyncpg
# driver, so normalize the scheme regardless of what the env var provides.
def _to_async_url(url: str) -> str:
    if url.startswith("postgresql+asyncpg://"):
        return url
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgres://"):
        return url.replace("postgres://", "postgresql+asyncpg://", 1)
    return url


engine = create_async_engine(
    _to_async_url(settings.DATABASE_URL),
    echo=settings.APP_ENV == "development",
    # Serverless functions are short-lived and Supabase's pooler (pgBouncer)
    # manages pooling on its side, so don't pool connections in-process.
    poolclass=NullPool,
    # pgBouncer in transaction mode can't reuse asyncpg's prepared statements,
    # which otherwise causes "prepared statement does not exist" errors.
    # This is a SQLAlchemy-level asyncpg dialect arg (not an asyncpg.connect arg).
    # Required for Supabase's transaction pooler; harmless on a direct connection.
    prepared_statement_cache_size=0,
    connect_args={
        "statement_cache_size": 0,
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
