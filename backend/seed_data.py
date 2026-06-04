"""
seed_data.py
------------
Seeds the database with the initial clubs, sub-clubs, and placeholder criteria.

Run from the backend/ directory:
    source .venv/bin/activate
    set -a && source .env && set +a
    python seed_data.py

Safe to re-run — uses INSERT ... ON CONFLICT DO NOTHING via upsert logic.

─────────────────────────────────────────────────────────────────────────────
CRITERIA LOGIC NOTES
─────────────────────────────────────────────────────────────────────────────
Colour tiers are awarded when a student meets ANY ONE of the OR paths defined
as sub-clubs under the parent club. Within a single sub-club (path), ALL
criteria listed must be satisfied (AND logic).

Robotics Half Colours — 4 paths (any one qualifies):
  Path A: Outstanding contribution 2+ years
  Path B: Elimination round finals at Regional/State level AND ≥1 yr mentoring
  Path C: Award recipient at Regional/State level AND ≥1 yr mentoring
  Path D: National Level qualification AND ≥1 yr mentoring

Robotics Full Colours — 3 paths:
  Path A: Outstanding contribution 4+ years
  Path B: Elimination round finals at National level AND ≥1 yr mentoring
  Path C: Award recipient at National level AND ≥1 yr mentoring

Robotics Honour Colours — 1 sub-club with 2 OR criteria (either qualifies):
  OR: National finalist
  OR: International qualification

Media Half Colours: Outstanding contribution 2+ yrs (Year 9+)
Media Full Colours: Outstanding contribution 4+ yrs OR Competition placement
Media Honour Colours: Outstanding student 4+ yrs OR First place in competition

Programming Half Colours: Any one of —
  Outstanding contribution 2+ yrs
  OR Elimination round qualification (state/national/international)
  OR High Distinction / Gold placement (state/national)

Programming Full Colours: Any one of —
  Outstanding contribution 3+ yrs
  OR Competition placement (state/national/international)

Programming Honour Colours: Any one of —
  Outstanding programming student 4+ yrs
  OR First place (state/national/international)
─────────────────────────────────────────────────────────────────────────────
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
    # ── ROBOTICS ──────────────────────────────────────────────────────────────
    {
        "slug": "robotics",
        "name": "Robotics",
        "description": "Students build, program, and compete with robots using platforms such as LEGO Mindstorms, VEX, or Arduino.",
        "colour": "#10b981",  # emerald
        "sub_clubs": [
            # ── Half Colours — Path A ──────────────────────────────────────
            {
                "slug": "robotics-half-colours-a",
                "name": "Robotics — Half Colours (Path A: Contribution)",
                "description": "Awarded via outstanding contribution path. Meets all criteria in this path.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 2 or more years",
                        "description": "Outstanding contribution to the Robotics Club for 2 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Half Colours — Path B ──────────────────────────────────────
            {
                "slug": "robotics-half-colours-b",
                "name": "Robotics — Half Colours (Path B: Regional/State Finals + Mentoring)",
                "description": "Awarded via regional/state elimination finals AND junior mentoring.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Qualify for elimination round finals — Regional/State",
                        "description": "Qualify for elimination round finals in a recognised Regional or State Level tournament (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "At least 1 year mentoring Junior Robotics team",
                        "description": "At least ONE year of mentoring of a Junior Robotics team.",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
            # ── Half Colours — Path C ──────────────────────────────────────
            {
                "slug": "robotics-half-colours-c",
                "name": "Robotics — Half Colours (Path C: Regional/State Award + Mentoring)",
                "description": "Awarded via award at regional/state level AND junior mentoring.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Award recipient — Regional/State Level",
                        "description": "Award recipient (Excellence, Design, Amaze, Build, etc) at a recognised Regional or State Level tournament (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "At least 1 year mentoring Junior Robotics team",
                        "description": "At least ONE year of mentoring of a Junior Robotics team.",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
            # ── Half Colours — Path D ──────────────────────────────────────
            {
                "slug": "robotics-half-colours-d",
                "name": "Robotics — Half Colours (Path D: National Qualification + Mentoring)",
                "description": "Awarded via national level championship qualification AND junior mentoring.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Qualification for National Level Championship",
                        "description": "Qualification for a National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "At least 1 year mentoring Junior Robotics team",
                        "description": "At least ONE year of mentoring of a Junior Robotics team.",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
            # ── Full Colours — Path A ──────────────────────────────────────
            {
                "slug": "robotics-full-colours-a",
                "name": "Robotics — Full Colours (Path A: Contribution)",
                "description": "Awarded via outstanding contribution path.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 4 or more years",
                        "description": "Outstanding contribution to the Robotics Club for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Full Colours — Path B ──────────────────────────────────────
            {
                "slug": "robotics-full-colours-b",
                "name": "Robotics — Full Colours (Path B: National Finals + Mentoring)",
                "description": "Awarded via national elimination finals AND junior mentoring.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Qualify for elimination round finals — National Level",
                        "description": "Qualify for elimination round finals in a recognised National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "At least 1 year mentoring Junior Robotics team",
                        "description": "At least ONE year of mentoring of a Junior Robotics team.",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
            # ── Full Colours — Path C ──────────────────────────────────────
            {
                "slug": "robotics-full-colours-c",
                "name": "Robotics — Full Colours (Path C: National Award + Mentoring)",
                "description": "Awarded via award at national level AND junior mentoring.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Award recipient — National Level Championship",
                        "description": "Award recipient (Excellence, Design, Amaze, Build, etc) at a recognised National Level Championship (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "At least 1 year mentoring Junior Robotics team",
                        "description": "At least ONE year of mentoring of a Junior Robotics team.",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
            # ── Honour Colours ────────────────────────────────────────────
            {
                "slug": "robotics-honour-colours",
                "name": "Robotics — Honour Colours",
                "description": "Highest award level. Meet either criterion.",
                "colour": "#10b981",
                "criteria": [
                    {
                        "title": "Finalist — National Level competition",
                        "description": "Finalist in a recognised National Level competition (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                    {
                        "title": "Qualification for International Level Championships",
                        "description": "Qualification for International Level Championships (eg FLL, RoboCup, VRC, FTC, FRC).",
                        "required_count": 1,
                        "sort_order": 1,
                    },
                ],
            },
        ],
        "criteria": [
            {"title": "Member for 2 or more years", "description": "Member of the club for 2 or more years.", "required_count": 1, "sort_order": 0},
            {"title": "Member for 3 or more years", "description": "Member of the club for 3 or more years.", "required_count": 1, "sort_order": 1},
            {"title": "Member for 4 or more years", "description": "Member of the club for 4 or more years.", "required_count": 1, "sort_order": 2},
            {"title": "Mentor for 1 year", "description": "Served as a mentor for 1 year.", "required_count": 1, "sort_order": 3},
            {"title": "Mentor for 2 years", "description": "Served as a mentor for 2 years.", "required_count": 1, "sort_order": 4},
            {"title": "Mentor for 3 years", "description": "Served as a mentor for 3 years.", "required_count": 1, "sort_order": 5},
            {"title": "Club Captain", "description": "Served as Club Captain.", "required_count": 1, "sort_order": 6},
        ],
    },

    # ── MEDIA ─────────────────────────────────────────────────────────────────
    {
        "slug": "media",
        "name": "Media",
        "description": "Students explore digital media creation including photography, video production, podcasting, and graphic design.",
        "colour": "#f59e0b",  # amber
        "sub_clubs": [
            # ── Half Colours ─────────────────────────────────────────────
            {
                "slug": "media-half-colours",
                "name": "Media — Half Colours",
                "description": "Initial award level for outstanding contribution. Applications from Year 9 and above.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 2 or more years",
                        "description": "Outstanding contribution to the Media Club for 2 or more years. Applications considered from Year 9 and above.",
                        "required_count": 1,
                        "year_group_applicable": 9,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Full Colours — Path A ──────────────────────────────────────
            {
                "slug": "media-full-colours-a",
                "name": "Media — Full Colours (Path A: Contribution)",
                "description": "Awarded via outstanding contribution.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 4 or more years",
                        "description": "Outstanding contribution to the Media Club for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Full Colours — Path B ──────────────────────────────────────
            {
                "slug": "media-full-colours-b",
                "name": "Media — Full Colours (Path B: Competition Placement)",
                "description": "Awarded via placement in a recognised competition.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Placement in recognised competition",
                        "description": "Placement in recognised state, national and international competitions (eg Screen It, Tropfest Jr, My Rode Reel).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Honour Colours — Path A ───────────────────────────────────
            {
                "slug": "media-honour-colours-a",
                "name": "Media — Honour Colours (Path A: Outstanding Student)",
                "description": "Awarded to outstanding media students over 4+ years.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "Outstanding media student for 4 or more years",
                        "description": "Recognised as an outstanding media student for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Honour Colours — Path B ───────────────────────────────────
            {
                "slug": "media-honour-colours-b",
                "name": "Media — Honour Colours (Path B: First Place)",
                "description": "Awarded via first place in a recognised competition.",
                "colour": "#f59e0b",
                "criteria": [
                    {
                        "title": "First place in recognised competition",
                        "description": "First place in recognised state, national and international competitions (eg Screen It, Tropfest Jr, My Rode Reel).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
        ],
        "criteria": [
            {"title": "Member for 2 or more years", "description": "Member of the club for 2 or more years.", "required_count": 1, "sort_order": 0},
            {"title": "Member for 3 or more years", "description": "Member of the club for 3 or more years.", "required_count": 1, "sort_order": 1},
            {"title": "Member for 4 or more years", "description": "Member of the club for 4 or more years.", "required_count": 1, "sort_order": 2},
            {"title": "Mentor for 1 year", "description": "Served as a mentor for 1 year.", "required_count": 1, "sort_order": 3},
            {"title": "Mentor for 2 years", "description": "Served as a mentor for 2 years.", "required_count": 1, "sort_order": 4},
            {"title": "Mentor for 3 years", "description": "Served as a mentor for 3 years.", "required_count": 1, "sort_order": 5},
            {"title": "Club Captain", "description": "Served as Club Captain.", "required_count": 1, "sort_order": 6},
        ],
    },

    # ── PROGRAMMING ───────────────────────────────────────────────────────────
    {
        "slug": "programming",
        "name": "Programming",
        "description": "Students develop software skills through coding projects, competitions, and collaborative development. Includes Cyber Security and AI sub-clubs.",
        "colour": "#6366f1",  # indigo
        "sub_clubs": [
            # ── Cyber & AI (non-colour, informational) ───────────────────
            {
                "slug": "programming-cyber",
                "name": "Cyber",
                "description": "Focused on cyber security concepts, ethical hacking challenges (CTF), and digital safety. Cyber students apply under Programming colours criteria.",
                "colour": "#ef4444",  # red
            },
            {
                "slug": "programming-ai",
                "name": "AI",
                "description": "Explores artificial intelligence, machine learning concepts, and practical AI tool usage. AI students apply under Programming colours criteria.",
                "colour": "#8b5cf6",  # violet
            },
            # ── Half Colours — Path A ──────────────────────────────────────
            {
                "slug": "programming-half-colours-a",
                "name": "Programming — Half Colours (Path A: Contribution)",
                "description": "Awarded via outstanding contribution.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 2 or more years",
                        "description": "Outstanding contribution to the Programming Club for 2 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Half Colours — Path B ──────────────────────────────────────
            {
                "slug": "programming-half-colours-b",
                "name": "Programming — Half Colours (Path B: Elimination Round Qualification)",
                "description": "Awarded via qualification for an elimination round in a recognised competition.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Qualify for elimination round — state/national/international",
                        "description": "Qualify for elimination round in recognised state, national and international competitions (eg UNSW Programming Competition, GROK Challenge, CyberTaipan).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Half Colours — Path C ──────────────────────────────────────
            {
                "slug": "programming-half-colours-c",
                "name": "Programming — Half Colours (Path C: High Distinction / Gold)",
                "description": "Awarded via High Distinction or Gold placement in a recognised competition.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "High Distinction / Gold Placement",
                        "description": "High Distinction or Gold Placement in recognised state and national competitions (eg AIO, Cambridge).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Full Colours — Path A ──────────────────────────────────────
            {
                "slug": "programming-full-colours-a",
                "name": "Programming — Full Colours (Path A: Contribution)",
                "description": "Awarded via outstanding contribution.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding contribution for 3 or more years",
                        "description": "Outstanding contribution to the Programming Club for 3 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Full Colours — Path B ──────────────────────────────────────
            {
                "slug": "programming-full-colours-b",
                "name": "Programming — Full Colours (Path B: Competition Placement)",
                "description": "Awarded via placement in a recognised competition.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Placement in recognised competition",
                        "description": "Placement in recognised state, national and international competitions (eg UNSW Programming Competition, GROK Challenge, CyberTaipan).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Honour Colours — Path A ───────────────────────────────────
            {
                "slug": "programming-honour-colours-a",
                "name": "Programming — Honour Colours (Path A: Outstanding Student)",
                "description": "Awarded to outstanding programming students over 4+ years.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "Outstanding Programming student for 4 or more years",
                        "description": "Recognised as an outstanding Programming student for 4 or more years.",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
            # ── Honour Colours — Path B ───────────────────────────────────
            {
                "slug": "programming-honour-colours-b",
                "name": "Programming — Honour Colours (Path B: First Place)",
                "description": "Awarded via first place in a recognised competition.",
                "colour": "#6366f1",
                "criteria": [
                    {
                        "title": "First place in recognised competition",
                        "description": "First place in recognised state, national and international competitions (eg UNSW Programming Competition, CyberTaipan).",
                        "required_count": 1,
                        "sort_order": 0,
                    },
                ],
            },
        ],
        "criteria": [
            {"title": "Member for 2 or more years", "description": "Member of the club for 2 or more years.", "required_count": 1, "sort_order": 0},
            {"title": "Member for 3 or more years", "description": "Member of the club for 3 or more years.", "required_count": 1, "sort_order": 1},
            {"title": "Member for 4 or more years", "description": "Member of the club for 4 or more years.", "required_count": 1, "sort_order": 2},
            {"title": "Mentor for 1 year", "description": "Served as a mentor for 1 year.", "required_count": 1, "sort_order": 3},
            {"title": "Mentor for 2 years", "description": "Served as a mentor for 2 years.", "required_count": 1, "sort_order": 4},
            {"title": "Mentor for 3 years", "description": "Served as a mentor for 3 years.", "required_count": 1, "sort_order": 5},
            {"title": "Club Captain", "description": "Served as Club Captain.", "required_count": 1, "sort_order": 6},
        ],
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
            INSERT INTO criteria (id, club_id, title, description, required_count, year_group_applicable, sort_order, is_active, created_at)
            VALUES (:id, :club_id, :title, :description, :required_count, :year_group_applicable, :sort_order, true, now())
        """),
        {
            "id": criterion_id,
            "club_id": club_id,
            "title": data["title"],
            "description": data.get("description", ""),
            "required_count": data.get("required_count", 1),
            "year_group_applicable": data.get("year_group_applicable"),
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
    from app.database import Base
    import app.models  # ensure all models are registered
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
