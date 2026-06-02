from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models import Club, Criterion
from app.schemas import ClubWithSubClubs, CriterionRead

router = APIRouter(prefix="/clubs", tags=["Clubs"])


@router.get("", response_model=list[ClubWithSubClubs])
async def list_clubs(db: AsyncSession = Depends(get_db)):
    """Return top-level clubs with their sub-clubs nested."""
    result = await db.execute(
        select(Club)
        .where(Club.parent_club_id.is_(None), Club.is_active == True)
        .options(selectinload(Club.sub_clubs))
        .order_by(Club.name)
    )
    return result.scalars().all()


@router.get("/{club_id}", response_model=ClubWithSubClubs)
async def get_club(club_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Club)
        .where(Club.id == club_id)
        .options(selectinload(Club.sub_clubs))
    )
    club = result.scalars().first()
    if not club:
        raise HTTPException(status_code=404, detail="Club not found.")
    return club


@router.get("/{club_id}/criteria", response_model=list[CriterionRead])
async def list_criteria(club_id: str, db: AsyncSession = Depends(get_db)):
    """Return all active criteria for a club.
    If club_id is a sub-club, transparently returns the parent club's criteria
    (since sub-clubs share criteria with their parent).
    """
    club = await db.get(Club, club_id)
    if not club:
        raise HTTPException(status_code=404, detail="Club not found.")
    # Resolve to parent only if this is a sub-club and the sub-club itself has no criteria
    from sqlalchemy import func
    criteria_count = await db.scalar(
        select(func.count(Criterion.id)).where(
            Criterion.club_id == club.id,
            Criterion.is_active == True,
        )
    )
    resolved_id = club.id
    if criteria_count == 0 and club.parent_club_id:
        resolved_id = club.parent_club_id

    result = await db.execute(
        select(Criterion)
        .where(Criterion.club_id == resolved_id, Criterion.is_active == True)
        .order_by(Criterion.sort_order)
    )
    return result.scalars().all()

