from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.database import engine, Base
from app.api import students, clubs, achievements, applications, notifications, staff

# Import all models so Alembic/SQLAlchemy sees them
import app.models  # noqa: F401


scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────────────────
    # Create tables (for dev without Alembic; in prod, use `alembic upgrade head`)
    if settings.APP_ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Schedule daily reminder processing at 08:00
    from app.services.reminders import process_due_reminders
    scheduler.add_job(
        process_due_reminders,
        CronTrigger(hour=8, minute=0),
        id="daily_reminders",
        replace_existing=True,
    )
    scheduler.start()

    yield  # App is running

    # ── Shutdown ──────────────────────────────────────────────────────────
    scheduler.shutdown()


app = FastAPI(
    title="TKS Colours API",
    description=(
        "Backend API for the TKS Colours co-curricular achievement tracker. "
        "Manages students, clubs, criteria, achievements, award applications, "
        "and automated reminders."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow the Vite dev server and the production frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(students.router, prefix="/api/v1")
app.include_router(clubs.router, prefix="/api/v1")
app.include_router(achievements.router, prefix="/api/v1")
app.include_router(applications.router, prefix="/api/v1")
app.include_router(notifications.router, prefix="/api/v1")
app.include_router(staff.router, prefix="/api/v1")


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok", "version": "0.1.0"}
