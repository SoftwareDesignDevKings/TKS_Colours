from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Staff
from app.schemas import StaffRead

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.get("", response_model=list[StaffRead])
async def list_staff(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Staff).where(Staff.is_active == True).order_by(Staff.name)
    )
    return result.scalars().all()
