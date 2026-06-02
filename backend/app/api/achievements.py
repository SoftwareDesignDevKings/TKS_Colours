from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional
from datetime import datetime
from app.database import get_db
from app.models import Achievement, Criterion, Student
from app.schemas import AchievementCreate, AchievementRead, AchievementWithCriterion, CriteriaStatus
from app.services import criteria_engine

router = APIRouter(prefix="/achievements", tags=["Achievements"])


@router.get("", response_model=list[AchievementWithCriterion])
async def list_achievements(
    student_id: Optional[str] = Query(None),
    club_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from app.models import Club
    q = (
        select(Achievement)
        .options(selectinload(Achievement.criterion))
        .order_by(Achievement.achieved_at.desc())
    )
    if student_id:
        q = q.where(Achievement.student_id == student_id)
    if club_id:
        # Include achievements from sub-clubs as well
        sub_ids_result = await db.execute(
            select(Club.id).where(Club.parent_club_id == club_id)
        )
        sub_ids = sub_ids_result.scalars().all()
        all_club_ids = [club_id] + list(sub_ids)
        q = q.join(Criterion).where(Criterion.club_id.in_(all_club_ids))
    result = await db.execute(q)
    return result.scalars().all()



@router.post("", response_model=AchievementRead, status_code=201)
async def log_achievement(payload: AchievementCreate, db: AsyncSession = Depends(get_db)):
    # Validate student exists
    student = await db.get(Student, payload.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    # Validate criterion exists and get its club
    criterion = await db.get(Criterion, payload.criterion_id)
    if not criterion:
        raise HTTPException(status_code=404, detail="Criterion not found.")

    achievement = Achievement(
        student_id=payload.student_id,
        criterion_id=payload.criterion_id,
        logged_by_staff_id=payload.logged_by_staff_id,
        evidence_note=payload.evidence_note,
        evidence_url=payload.evidence_url,
        achieved_at=payload.achieved_at or datetime.utcnow(),
    )
    db.add(achievement)
    await db.commit()
    await db.refresh(achievement)

    # Run criteria engine — check if student now qualifies for an award
    await criteria_engine.check_and_trigger(db, payload.student_id, criterion.club_id)

    return achievement


@router.delete("/{achievement_id}", status_code=204)
async def delete_achievement(achievement_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement).where(Achievement.id == achievement_id))
    achievement = result.scalars().first()
    if not achievement:
        raise HTTPException(status_code=404, detail="Achievement not found.")
    await db.delete(achievement)
    await db.commit()


@router.get("/criteria-status", response_model=CriteriaStatus)
async def get_criteria_status(
    student_id: str = Query(...),
    club_id: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    """Check a student's progress against all criteria for a given club."""
    status = await criteria_engine.get_criteria_status(db, student_id, club_id)
    club = await db.get(__import__("app.models", fromlist=["Club"]).Club, club_id)
    status["club_name"] = club.name if club else "Unknown"
    return status
