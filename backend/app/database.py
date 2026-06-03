from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
from app.config import settings

# Supabase (and most hosts) hand out a sync-style URL like
# "postgresql://..." or "postgres://...". The async engine needs the asyncpg
# driver, so normalize the scheme regardless of what the env var provides.
# We also append `prepared_statement_cache_size=0`: this is a SQLAlchemy asyncpg
# *dialect* option read from the URL query string (it is neither a create_engine
# kwarg nor an asyncpg.connect arg). It disables SQLAlchemy's prepared-statement
# cache, which pgBouncer in transaction mode can't reuse.
def _to_async_url(url: str) -> str:
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+asyncpg://", 1)

    if "prepared_statement_cache_size" not in url:
        url += ("&" if "?" in url else "?") + "prepared_statement_cache_size=0"
    return url


engine = create_async_engine(
    _to_async_url(settings.DATABASE_URL),
    echo=settings.APP_ENV == "development",
    # Serverless functions are short-lived and Supabase's pooler (pgBouncer)
    # manages pooling on its side, so don't pool connections in-process.
    poolclass=NullPool,
    # `statement_cache_size` is passed straight through to asyncpg.connect();
    # disabling it avoids "prepared statement does not exist" errors behind pgBouncer.
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
