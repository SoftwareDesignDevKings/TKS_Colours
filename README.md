# TKS Colours — Co-Curricular Achievement Tracker

A Progressive Web App for tracking student records of achievement in co-curricular clubs.
Staff use this app to log achievements, monitor criteria completion, manage award applications,
and receive automated reminders for pending decisions.

---

## Clubs Supported

| Club | Sub-clubs |
|---|---|
| Media | — |
| Programming | Cyber Security, Artificial Intelligence |
| Robotics | — |

---

## Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Node.js 20+ (for local frontend development)
- Python 3.11+ (for local backend development)

### 1. Start the full stack

```bash
# Copy env template
cp backend/.env.example backend/.env

# Start all services (PostgreSQL + FastAPI + Vite dev server)
docker compose up
```

Then open:
- **Frontend:** http://localhost:5173
- **API Docs (Swagger):** http://localhost:8000/docs

### 2. Seed the database

```bash
# With Docker running:
docker compose exec backend python -m scripts.seed

# Or locally:
cd backend && python -m scripts.seed
```

---

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Start a local PostgreSQL instance or use Docker for just the DB:
docker compose up db -d

cp .env.example .env
# Edit .env to point DATABASE_URL at your local Postgres

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## Project Structure

```
TKS_Colours/
├── backend/
│   ├── app/
│   │   ├── api/           # FastAPI route handlers
│   │   ├── models/        # SQLAlchemy ORM models
│   │   ├── schemas/       # Pydantic request/response schemas
│   │   ├── services/      # Criteria engine + reminder scheduler
│   │   └── main.py        # App entry point
│   ├── scripts/
│   │   └── seed.py        # Seed clubs, criteria, staff
│   ├── .env.example
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/           # Typed Axios client
│   │   ├── components/    # AppShell layout
│   │   ├── pages/         # All 8 pages
│   │   └── types.ts       # Shared TypeScript types
│   ├── vite.config.ts     # PWA + dev proxy config
│   └── tailwind.config.js
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

See `backend/.env.example` for all options.

| Variable | Description |
|---|---|
| `DATABASE_URL` | asyncpg connection string |
| `CORS_ORIGINS` | Allowed frontend origins (JSON array) |
| `MAIL_*` | SMTP credentials for reminder emails (optional) |

---

## Deployment

For production, build the frontend and serve with nginx:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

*(docker-compose.prod.yml to be created in Stage 5)*

---

## Roadmap

- **Stage 1** ✅ — Architecture, DB schema, API skeleton, React shell
- **Stage 2** — Student CRUD, Achievement logging, Criteria seed data
- **Stage 3** — Criteria engine, Applications workflow, In-app notifications
- **Stage 4** — Reminder emails, Notification feed, Staff decision UI
- **Stage 5** — Reporting, PWA install prompt, Offline support
- **Future** — OAuth2 (Google Workspace), Student self-service, Push notifications
