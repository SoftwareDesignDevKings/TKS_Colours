"""
Seed script — populates the database with:
- 3 clubs (Media, Programming, Robotics)
- 2 Programming sub-clubs (Cyber, AI)
- Sample criteria for each club
- 3 sample staff members
Run: python -m scripts.seed
"""
import asyncio
import uuid
from app.database import AsyncSessionLocal, engine, Base
from app.models import Club, Criterion, Staff
import app.models  # ensure all models are registered


CLUBS = [
    {
        "id": "c1000000-0000-0000-0000-000000000001",
        "name": "Media",
        "slug": "media",
        "description": "Photography, videography, journalism and digital media creation.",
        "colour": "#f59e0b",
    },
    {
        "id": "c1000000-0000-0000-0000-000000000002",
        "name": "Programming",
        "slug": "programming",
        "description": "Computer programming, software development and computational thinking.",
        "colour": "#6366f1",
    },
    {
        "id": "c1000000-0000-0000-0000-000000000003",
        "name": "Robotics",
        "slug": "robotics",
        "description": "Robotics design, engineering and competition.",
        "colour": "#10b981",
    },
    # Sub-clubs of Programming
    {
        "id": "c1000000-0000-0000-0000-000000000004",
        "name": "Cyber Security",
        "slug": "cyber",
        "description": "Network security, ethical hacking and digital forensics.",
        "colour": "#ef4444",
        "parent_club_id": "c1000000-0000-0000-0000-000000000002",
    },
    {
        "id": "c1000000-0000-0000-0000-000000000005",
        "name": "Artificial Intelligence",
        "slug": "ai",
        "description": "Machine learning, data science and AI ethics.",
        "colour": "#8b5cf6",
        "parent_club_id": "c1000000-0000-0000-0000-000000000002",
    },
]

CRITERIA = [
    # Media criteria
    {"club_id": "c1000000-0000-0000-0000-000000000001", "title": "Published a school article or news piece", "required_count": 1, "sort_order": 1},
    {"club_id": "c1000000-0000-0000-0000-000000000001", "title": "Produced a video or podcast episode", "required_count": 1, "sort_order": 2},
    {"club_id": "c1000000-0000-0000-0000-000000000001", "title": "Photographed a school event", "required_count": 2, "sort_order": 3},
    {"club_id": "c1000000-0000-0000-0000-000000000001", "title": "Participated in club for at least one semester", "required_count": 1, "sort_order": 4},
    # Programming criteria
    {"club_id": "c1000000-0000-0000-0000-000000000002", "title": "Completed a programming project", "required_count": 1, "sort_order": 1},
    {"club_id": "c1000000-0000-0000-0000-000000000002", "title": "Contributed to a collaborative codebase", "required_count": 1, "sort_order": 2},
    {"club_id": "c1000000-0000-0000-0000-000000000002", "title": "Participated in club for at least one semester", "required_count": 1, "sort_order": 3},
    # Robotics criteria
    {"club_id": "c1000000-0000-0000-0000-000000000003", "title": "Designed and built a robot component", "required_count": 1, "sort_order": 1},
    {"club_id": "c1000000-0000-0000-0000-000000000003", "title": "Participated in an internal or external competition", "required_count": 1, "sort_order": 2},
    {"club_id": "c1000000-0000-0000-0000-000000000003", "title": "Documented a build process or engineering log", "required_count": 1, "sort_order": 3},
    {"club_id": "c1000000-0000-0000-0000-000000000003", "title": "Participated in club for at least one semester", "required_count": 1, "sort_order": 4},
    # Cyber criteria
    {"club_id": "c1000000-0000-0000-0000-000000000004", "title": "Completed a CTF challenge or cyber competition", "required_count": 1, "sort_order": 1},
    {"club_id": "c1000000-0000-0000-0000-000000000004", "title": "Demonstrated knowledge of a security concept", "required_count": 2, "sort_order": 2},
    {"club_id": "c1000000-0000-0000-0000-000000000004", "title": "Participated in club for at least one semester", "required_count": 1, "sort_order": 3},
    # AI criteria
    {"club_id": "c1000000-0000-0000-0000-000000000005", "title": "Trained or fine-tuned an AI model", "required_count": 1, "sort_order": 1},
    {"club_id": "c1000000-0000-0000-0000-000000000005", "title": "Presented an AI project to peers", "required_count": 1, "sort_order": 2},
    {"club_id": "c1000000-0000-0000-0000-000000000005", "title": "Participated in club for at least one semester", "required_count": 1, "sort_order": 3},
]

STAFF = [
    {"name": "Admin Staff", "email": "admin@school.edu", "role": "admin"},
    {"name": "Club Coordinator", "email": "coordinator@school.edu", "role": "coordinator"},
    {"name": "Teacher", "email": "teacher@school.edu", "role": "teacher"},
]


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Clubs
        for club_data in CLUBS:
            existing = await db.get(Club, club_data["id"])
            if not existing:
                db.add(Club(**club_data))
        await db.flush()

        # Criteria
        for crit_data in CRITERIA:
            db.add(Criterion(id=str(uuid.uuid4()), **crit_data))

        # Staff
        for staff_data in STAFF:
            db.add(Staff(id=str(uuid.uuid4()), **staff_data))

        await db.commit()
        print("✅  Seed complete — clubs, criteria and staff loaded.")


if __name__ == "__main__":
    asyncio.run(seed())
