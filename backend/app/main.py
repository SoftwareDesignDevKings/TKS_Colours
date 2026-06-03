import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.api import students, clubs, achievements, applications, notifications, staff

# Import all models so Alembic/SQLAlchemy sees them
import app.models  # noqa: F401

IS_VERCEL = os.environ.get("VERCEL") == "1"

# Only import APScheduler when NOT running on Vercel (serverless has no persistent process)
scheduler = None
if not IS_VERCEL:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from apscheduler.triggers.cron import CronTrigger
    scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────────────────
    # Create tables (for dev without Alembic; in prod, use `alembic upgrade head`)
    if settings.APP_ENV == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Schedule daily reminder processing at 08:00 (only when running as a server, not serverless)
    if scheduler is not None:
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
    if scheduler is not None:
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


# ── Vercel Cron Endpoint ─────────────────────────────────────────────────────
# Vercel Cron Jobs call this endpoint on a schedule (configured in vercel.json).
# Replaces APScheduler's in-process cron when running in serverless mode.
@app.get("/api/v1/cron/reminders", tags=["Cron"], include_in_schema=False)
async def cron_reminders(request: Request):
    """Process due reminders — called by Vercel Cron Jobs."""
    # Verify the request comes from Vercel Cron (not external callers)
    auth_header = request.headers.get("authorization")
    cron_secret = os.environ.get("CRON_SECRET")
    if cron_secret and auth_header != f"Bearer {cron_secret}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    from app.services.reminders import process_due_reminders
    processed = await process_due_reminders()
    return {"status": "ok", "reminders_processed": processed}
