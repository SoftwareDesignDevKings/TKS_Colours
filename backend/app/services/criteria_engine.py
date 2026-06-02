"""
Criteria Engine
---------------
After a new achievement is logged, this service checks whether a student has
now met *all* active criteria for a club. If so, it auto-creates a pending
Application and a Notification.

Sub-club inheritance rule
~~~~~~~~~~~~~~~~~~~~~~~~~
Criteria are only ever attached to **top-level clubs** (e.g. Programming).
When an achievement is logged under a sub-club (e.g. Cyber, AI), the engine
resolves upward to the parent club before running criteria checks. This means
achievements from Cyber *and* AI both count toward Programming's criteria.
"""
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models import Achievement, Criterion, Application, Notification, Club, Student
from app.models.application import ApplicationStatus
from app.models.notification import NotificationType

REMINDER_DAYS_DEFAULT = 60  # days before first reminder fires (2 months)


async def _resolve_criteria_club(db: AsyncSession, club_id: str) -> Club | None:
    """
    Resolve to the club that actually defines the criteria.
    If the club has criteria, return it.
    Otherwise, if it has a parent, try resolving to the parent.
    Failsafe: return the club itself.
    """
    club = await db.get(Club, club_id)
    if club is None:
        return None
    
    # Check if this club has active criteria
    criteria_count = await db.scalar(
        select(func.count(Criterion.id)).where(
            Criterion.club_id == club.id,
            Criterion.is_active == True,
        )
    )
    if criteria_count > 0:
        return club
        
    if club.parent_club_id:
        parent = await db.get(Club, club.parent_club_id)
        if parent:
            return parent
            
    return club


async def _get_member_club_ids(db: AsyncSession, criteria_club_id: str) -> list[str]:
    """
    Return the criteria club id PLUS all its sub-club ids.
    Achievements logged against any of these count toward the criteria.
    """
    sub_result = await db.execute(
        select(Club.id).where(Club.parent_club_id == criteria_club_id)
    )
    sub_ids = sub_result.scalars().all()
    return [criteria_club_id] + list(sub_ids)


async def check_and_trigger(
    db: AsyncSession, student_id: str, club_id: str
) -> Application | None:
    """
    Check if the student has met all criteria for the resolved criteria club.
    If yes and no pending/approved application already exists, create one.
    Returns the Application if newly created, else None.
    """
    # 1. Resolve to criteria club
    criteria_club = await _resolve_criteria_club(db, club_id)
    if criteria_club is None:
        return None

    # 2. Get all active criteria for the resolved club
    criteria_result = await db.execute(
        select(Criterion).where(
            Criterion.club_id == criteria_club.id,
            Criterion.is_active == True,
        )
    )
    criteria = criteria_result.scalars().all()

    if not criteria:
        return None

    # 3. Collect all club IDs whose achievements count (parent + sub-clubs)
    member_ids = await _get_member_club_ids(db, criteria_club.id)

    # We need the student's year group to verify any year group applicability constraints
    student = await db.get(Student, student_id)
    if not student:
        return None

    # 4. Check how many achievements exist per criterion for this student,
    #    counting across all member clubs
    for criterion in criteria:
        # Check if student meets the minimum year group requirements for this criterion
        if criterion.year_group_applicable and student.year_group < criterion.year_group_applicable:
            return None

        count_result = await db.execute(
            select(func.count(Achievement.id))
            .join(Criterion, Achievement.criterion_id == Criterion.id)
            .where(
                Achievement.student_id == student_id,
                Achievement.criterion_id == criterion.id,
                Criterion.club_id.in_(member_ids),
            )
        )
        count = count_result.scalar_one()
        if count < criterion.required_count:
            return None  # Not all criteria met yet

    # 5. All criteria met — check if an application already exists
    existing = await db.execute(
        select(Application).where(
            Application.student_id == student_id,
            Application.club_id == criteria_club.id,
            Application.status.in_([ApplicationStatus.PENDING, ApplicationStatus.APPROVED]),
        )
    )
    if existing.scalars().first():
        return None  # Already has a pending or approved application

    # 6. Create the application (against the criteria club)
    application = Application(
        student_id=student_id,
        club_id=criteria_club.id,
        status=ApplicationStatus.PENDING,
        auto_triggered=True,
    )
    db.add(application)
    await db.flush()  # get the ID

    # 7. Create a notification
    notification = Notification(
        type=NotificationType.CRITERIA_MET,
        title=f"Criteria met — {criteria_club.name}",
        body=(
            f"A student has met all criteria for {criteria_club.name} "
            f"and is ready for an award application."
        ),
        student_id=student_id,
        application_id=application.id,
        club_id=criteria_club.id,
    )
    db.add(notification)

    # 8. Create the first reminder (due in REMINDER_DAYS_DEFAULT days)
    from app.models.reminder import Reminder
    reminder = Reminder(
        application_id=application.id,
        due_at=datetime.utcnow() + timedelta(days=REMINDER_DAYS_DEFAULT),
    )
    db.add(reminder)

    await db.commit()
    await db.refresh(application)

    return application


async def get_criteria_status(
    db: AsyncSession, student_id: str, club_id: str
) -> dict:
    """
    Returns detailed status of a student's progress against a club's criteria.
    """
    # Resolve to criteria club
    criteria_club = await _resolve_criteria_club(db, club_id)
    if criteria_club is None:
        return {
            "club_id": club_id,
            "total_criteria": 0,
            "met_criteria": 0,
            "is_complete": False,
            "criteria_detail": [],
        }

    criteria_result = await db.execute(
        select(Criterion).where(
            Criterion.club_id == criteria_club.id,
            Criterion.is_active == True,
        ).order_by(Criterion.sort_order)
    )
    criteria = criteria_result.scalars().all()

    student = await db.get(Student, student_id)
    if not student:
        return {
            "club_id": criteria_club.id,
            "total_criteria": 0,
            "met_criteria": 0,
            "is_complete": False,
            "criteria_detail": [],
        }

    member_ids = await _get_member_club_ids(db, criteria_club.id)

    detail = []
    met = 0

    for criterion in criteria:
        # Check year group restriction
        year_group_ok = True
        if criterion.year_group_applicable and student.year_group < criterion.year_group_applicable:
            year_group_ok = False

        count_result = await db.execute(
            select(func.count(Achievement.id))
            .join(Criterion, Achievement.criterion_id == Criterion.id)
            .where(
                Achievement.student_id == student_id,
                Achievement.criterion_id == criterion.id,
                Criterion.club_id.in_(member_ids),
            )
        )
        count = count_result.scalar_one()
        is_met = count >= criterion.required_count and year_group_ok
        if is_met:
            met += 1
        detail.append({
            "criterion_id": criterion.id,
            "title": criterion.title,
            "required_count": criterion.required_count,
            "current_count": count,
            "is_met": is_met,
        })

    return {
        "club_id": criteria_club.id,
        "total_criteria": len(criteria),
        "met_criteria": met,
        "is_complete": met == len(criteria) and len(criteria) > 0,
        "criteria_detail": detail,
    }
