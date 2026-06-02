"""
seed_data.py
------------
Seeds the database with the initial clubs, sub-clubs, and placeholder criteria.

Run from the backend/ directory:
    source .venv/bin/activate
    set -a && source .env && set +a
    python seed_data.py

Safe to re-run — uses INSERT ... ON CONFLICT DO NOTHING via upsert logic.
"""
import asyncio
import uuid
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# ── Seed data definition ──────────────────────────────────────────────────────

CLUBS = [
    {
        "slug": "media",
        "name": "Media",
        "description": "Students explore digital media creation including photography, video production, podcasting, and graphic design.",
        "colour": "#f59e0b",  # amber
        "sub_clubs": [
            {
                "slug": "media-half-colours",
                "name": "Media - Half Colours",
                "description": "Award level for initial outstanding contribution to Media club.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding contribution (2+ years)",
                        "description": "Outstanding contribution to the Club for 2 or more years. Applications considered from Year 9 and above.",
                        "required_count": 1,
                        "sort_order": 0,
                    }
                ],
            },
            {
                "slug": "media-full-colours",
                "name": "Media - Full Colours",
                "description": "Award level for extended outstanding contribution and competition placement.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding contribution (4+ years)",
                        "description": "Outstanding contribution to the club for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Competition placement",
                        "description": "Placement in recognised state, national and international competitions eg Screen It, Tropfest Jr, My Rode Reel.",
                        "required_count": 1,
                        "sort_order": 1,
                    }
                ],
            },
            {
                "slug": "media-honour-colours",
                "name": "Media - Honour Colours",
                "description": "Highest award level for outstanding media students with top competition placements.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding media student (4+ years)",
                        "description": "Outstanding media student for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "First place in competition",
                        "description": "First place in recognised state, national and international competitions eg Screen It, Tropfest Jr, My Rode Reel.",
                        "required_count": 1,
                        "sort_order": 1,
                    }
                ],
            },
        ],
        "criteria": [],
    },
    {
        "slug": "programming",
        "name": "Programming",
        "description": "Students develop software skills through coding projects, competitions, and collaborative development. Includes Cyber Security and AI sub-clubs.",
        "colour": "#6366f1",  # indigo
        "sub_clubs": [
            {
                "slug": "programming-cyber",
                "name": "Cyber",
                "description": "Focused on cyber security concepts, ethical hacking challenges (CTF), and digital safety.",
                "colour": "#ef4444",  # red
            },
            {
                "slug": "programming-ai",
                "name": "AI",
                "description": "Explores artificial intelligence, machine learning concepts, and practical AI tool usage.",
                "colour": "#8b5cf6",  # violet
            },
            {
                "slug": "programming-half-colours",
                "name": "Programming - Half Colours",
                "description": "Award level for initial outstanding contribution to Programming club.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding contribution (2+ years)",
                        "description": "Outstanding contribution to the Club for 2 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Elimination round qualification",
                        "description": "Qualify for elimination round in recognised state, national and international competitions eg UNSW Prog Comp, GROK Challenge, CyberTaipan",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                    {
                        "title": "High Distinction / Gold Placement",
                        "description": "High Distinction/Gold Placement in recognised state and national competitions eg AIO, Cambridge",
                        "required_count": 1,
                        "sort_order": 2,
                    }
                ],
            },
            {
                "slug": "programming-full-colours",
                "name": "Programming - Full Colours",
                "description": "Award level for extended outstanding contribution and competition placement.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding contribution (3+ years)",
                        "description": "Outstanding contribution to the Club for 3 or more years",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Competition placement",
                        "description": "Placement in recognised state, national and international competitions eg UNSW Prog Comp, GROK Challenge, CyberTaipan",
                        "required_count": 1,
                        "sort_order": 1,
                    }
                ],
            },
            {
                "slug": "programming-honour-colours",
                "name": "Programming - Honour Colours",
                "description": "Highest award level for outstanding programming students with top competition wins.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding programming student (4+ years)",
                        "description": "Outstanding Programming student for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "First in competition",
                        "description": "First in recognised state, national and international competitions eg UNSW Prog Comp, CyberTaipan",
                        "required_count": 1,
                        "sort_order": 1,
                    }
                ],
            },
        ],
        "criteria": [],
    },
    {
        "slug": "robotics",
        "name": "Robotics",
        "description": "Students build, program, and compete with robots using platforms such as LEGO Mindstorms, VEX, or Arduino.",
        "colour": "#10b981",  # emerald
        "sub_clubs": [
            {
                "slug": "robotics-half-colours",
                "name": "Robotics - Half Colours",
                "description": "Award level for initial outstanding contribution to Robotics club.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Build and program a robot",
                        "description": "Construct and program a robot that can complete at least one defined task or challenge.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Attend club sessions",
                        "description": "Attend at least 8 Robotics club sessions across the academic year.",
                        "required_count": 8,
                        "sort_order": 1,
                    }
                ],
            },
            {
                "slug": "robotics-full-colours",
                "name": "Robotics - Full Colours",
                "description": "Award level for extended outstanding contribution and competition placement.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Participate in a robotics challenge",
                        "description": "Take part in an in-school or inter-school robotics competition or demonstration event.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Document a build process",
                        "description": "Keep an engineering journal or write-up documenting the design decisions and iteration of a build.",
                        "required_count": 1,
                        "sort_order": 1,
                    }
                ],
            },
            {
                "slug": "robotics-honour-colours",
                "name": "Robotics - Honour Colours",
                "description": "Highest award level for outstanding robotics students.",
                "colour": "#10b981",
                "criteria": [],
            }
        ],
        "criteria": [],
    },
]

STAFF = [
    {"name": "Admin Staff", "email": "admin@school.edu", "role": "admin"},
]


# ── Helpers ───────────────────────────────────────────────────────────────────

async def upsert_club(session: AsyncSession, data: dict, parent_id: str | None = None) -> str:
    """Insert a club if its slug doesn't already exist. Returns the club's id."""
    result = await session.execute(
        text("SELECT id FROM clubs WHERE slug = :slug"),
        {"slug": data["slug"]},
    )
    row = result.fetchone()
    if row:
        print(f"  [skip]   Club '{data['name']}' already exists")
        return row[0]

    club_id = str(uuid.uuid4())
    await session.execute(
        text("""
            INSERT INTO clubs (id, name, slug, description, colour, parent_club_id, is_active, created_at)
            VALUES (:id, :name, :slug, :description, :colour, :parent_id, true, now())
        """),
        {
            "id": club_id,
            "name": data["name"],
            "slug": data["slug"],
            "description": data.get("description", ""),
            "colour": data.get("colour", "#6366f1"),
            "parent_id": parent_id,
        },
    )
    print(f"  [create] Club '{data['name']}' (id={club_id})")
    return club_id


async def upsert_criterion(session: AsyncSession, club_id: str, data: dict) -> None:
    """Insert a criterion if the (club_id, title) pair doesn't already exist."""
    result = await session.execute(
        text("SELECT id FROM criteria WHERE club_id = :club_id AND title = :title"),
        {"club_id": club_id, "title": data["title"]},
    )
    if result.fetchone():
        print(f"    [skip]   Criterion '{data['title']}' already exists")
        return

    criterion_id = str(uuid.uuid4())
    await session.execute(
        text("""
            INSERT INTO criteria (id, club_id, title, description, required_count, sort_order, is_active, created_at)
            VALUES (:id, :club_id, :title, :description, :required_count, :sort_order, true, now())
        """),
        {
            "id": criterion_id,
            "club_id": club_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "required_count": data.get("required_count", 1),
            "sort_order": data.get("sort_order", 0),
        },
    )
    print(f"    [create] Criterion '{data['title']}'")


async def upsert_staff(session: AsyncSession, data: dict) -> None:
    result = await session.execute(
        text("SELECT id FROM staff WHERE email = :email"),
        {"email": data["email"]},
    )
    if result.fetchone():
        print(f"  [skip]   Staff '{data['name']}' already exists")
        return

    staff_id = str(uuid.uuid4())
    await session.execute(
        text("""
            INSERT INTO staff (id, name, email, role, is_active, created_at)
            VALUES (:id, :name, :email, :role, true, now())
        """),
        {"id": staff_id, "name": data["name"], "email": data["email"], "role": data["role"]},
    )
    print(f"  [create] Staff '{data['name']}' (id={staff_id})")


# ── Main ──────────────────────────────────────────────────────────────────────

async def seed():
    print("=== TKS Colours — Database Seed ===\n")
    async with AsyncSessionLocal() as session:
        async with session.begin():
            print("── Cleaning up old database tables ──")
            await session.execute(text("DELETE FROM notifications"))
            await session.execute(text("DELETE FROM reminders"))
            await session.execute(text("DELETE FROM applications"))
            await session.execute(text("DELETE FROM achievements"))
            await session.execute(text("DELETE FROM criteria"))
            await session.execute(text("DELETE FROM clubs"))

            print("── Clubs & Criteria ──")
            for club_data in CLUBS:
                # Insert top-level club
                club_id = await upsert_club(session, club_data)

                # Insert sub-clubs
                for sub_data in club_data.get("sub_clubs", []):
                    sub_club_id = await upsert_club(session, sub_data, parent_id=club_id)
                    # Seed criteria for sub-club if present
                    for criterion_data in sub_data.get("criteria", []):
                        await upsert_criterion(session, sub_club_id, criterion_data)

                # Insert criteria on the top-level club
                for criterion_data in club_data.get("criteria", []):
                    await upsert_criterion(session, club_id, criterion_data)

            print("\n── Staff ──")
            for staff_data in STAFF:
                await upsert_staff(session, staff_data)

    print("\n✅ Seed complete.")


if __name__ == "__main__":
    asyncio.run(seed())
